import uuid
from datetime import date
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    ResourceNotFoundException,
)
from app.models.academic_session import AcademicSession
from app.models.institute import Institute
from app.models.module_config import SystemModuleConfig
from app.models.user import User
from app.permissions.module_catalog import ENTERPRISE_MODULES_CATALOG
from app.repositories.institute_repository import InstituteRepository
from app.schemas.institute import (
    AcademicSessionCreateRequest,
    AcademicSessionResponse,
    AcademicSessionUpdateRequest,
    InstituteBrandingUpdateRequest,
    InstituteCreateRequest,
    InstituteIntegrationsUpdateRequest,
    InstituteProfileUpdateRequest,
    InstituteResponse,
    InstituteSetupBundleResponse,
    ModuleConfigResponse,
    ModuleToggleRequest,
)
from app.services.audit_service import AuditService


class InstituteService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = InstituteRepository(session)
        self.audit_service = AuditService(session)

    async def list_institutes(self) -> List[InstituteResponse]:
        institutes = await self.repo.list_all()
        return [InstituteResponse.model_validate(inst) for inst in institutes]

    async def get_institute(self, institute_id: uuid.UUID) -> InstituteResponse:
        inst = await self.repo.get_by_id(institute_id)
        if not inst:
            raise ResourceNotFoundException("Institute", institute_id)
        await self._ensure_default_sessions(inst)
        return InstituteResponse.model_validate(inst)

    async def get_setup_bundle(self, institute_id: uuid.UUID) -> InstituteSetupBundleResponse:
        inst = await self.repo.get_by_id(institute_id)
        if not inst:
            raise ResourceNotFoundException("Institute", institute_id)
        await self._ensure_default_sessions(inst)

        sessions = await self.repo.list_academic_sessions(institute_id)
        current_sess = next((s for s in sessions if s.is_current), sessions[0] if sessions else None)

        system_status = {
            "is_active": inst.is_active,
            "custom_domain_configured": bool(inst.custom_domain),
            "custom_domain_status": inst.custom_domain_status,
            "smtp_configured": bool(inst.smtp_config.get("host")),
            "sms_configured": bool(inst.sms_gateway_config.get("api_key")),
            "whatsapp_configured": bool(inst.whatsapp_gateway_config.get("phone_number_id")),
            "payment_gateway_configured": bool(inst.payment_gateway_config.get("key_id")),
            "google_maps_configured": bool(inst.google_maps_embed_url),
            "academic_sessions_count": len(sessions),
        }

        return InstituteSetupBundleResponse(
            institute=InstituteResponse.model_validate(inst),
            current_session=AcademicSessionResponse.model_validate(current_sess) if current_sess else None,
            all_sessions=[AcademicSessionResponse.model_validate(s) for s in sessions],
            module_configs=[ModuleConfigResponse.model_validate(m) for m in inst.module_configs],
            system_status=system_status,
        )

    async def create_institute(
        self,
        payload: InstituteCreateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> InstituteResponse:
        existing = await self.repo.get_by_code(payload.code)
        if existing:
            raise ConflictException(f"Institute with code '{payload.code}' already exists.")

        institute = Institute(
            code=payload.code.upper(),
            name=payload.name,
            tagline=payload.tagline,
            affiliation_number=payload.affiliation_number,
            official_email=payload.official_email,
            official_phone=payload.official_phone,
            website_domain=payload.website_domain,
            address_line1=payload.address_line1,
            address_line2=payload.address_line2,
            city=payload.city,
            state=payload.state,
            postal_code=payload.postal_code,
            country=payload.country,
            logo_url=payload.logo_url,
            favicon_url=payload.favicon_url,
            primary_color_hex=payload.primary_color_hex,
            secondary_color_hex=payload.secondary_color_hex,
            seo_metadata=payload.seo_metadata,
            is_active=True,
        )
        await self.repo.create(institute)

        # Provision all 37 enterprise modules for the newly created institute
        for mod_def in ENTERPRISE_MODULES_CATALOG:
            cfg = SystemModuleConfig(
                institute_id=institute.id,
                module_key=mod_def["module_key"],
                display_name=mod_def["display_name"],
                category=mod_def["category"],
                subdomain=mod_def["subdomain"],
                description=mod_def["description"],
                is_enabled=True,
                is_core_locked=mod_def["is_core_locked"],
                configuration={},
            )
            self.session.add(cfg)

        await self._ensure_default_sessions(institute)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=institute.id,
            module_key="institute_management",
            action="INSTITUTE_CREATED",
            resource_type="institute",
            resource_id=str(institute.id),
            http_method="POST",
            endpoint_path="/api/v1/institutes",
            status_code=201,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"code": institute.code, "name": institute.name},
        )
        await self.session.commit()
        reloaded = await self.repo.get_by_id(institute.id)
        return InstituteResponse.model_validate(reloaded)

    async def update_profile(
        self,
        institute_id: uuid.UUID,
        payload: InstituteProfileUpdateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> InstituteResponse:
        inst = await self.repo.get_by_id(institute_id)
        if not inst:
            raise ResourceNotFoundException("Institute", institute_id)

        update_data = payload.model_dump(exclude_unset=True)
        for field_name, val in update_data.items():
            setattr(inst, field_name, val)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=inst.id,
            module_key="institute_management",
            action="INSTITUTE_PROFILE_UPDATED",
            resource_type="institute",
            resource_id=str(inst.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/institutes/{inst.id}/profile",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload=update_data,
        )
        await self.session.commit()
        reloaded = await self.repo.get_by_id(inst.id)
        return InstituteResponse.model_validate(reloaded)

    async def update_branding_and_settings(
        self,
        institute_id: uuid.UUID,
        payload: InstituteBrandingUpdateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> InstituteResponse:
        inst = await self.repo.get_by_id(institute_id)
        if not inst:
            raise ResourceNotFoundException("Institute", institute_id)

        update_data = payload.model_dump(exclude_unset=True)
        for field_name, val in update_data.items():
            setattr(inst, field_name, val)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=inst.id,
            module_key="institute_management",
            action="INSTITUTE_BRANDING_UPDATED",
            resource_type="institute",
            resource_id=str(inst.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/institutes/{inst.id}/branding",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload=update_data,
        )
        await self.session.commit()
        reloaded = await self.repo.get_by_id(inst.id)
        return InstituteResponse.model_validate(reloaded)

    async def update_integrations(
        self,
        institute_id: uuid.UUID,
        payload: InstituteIntegrationsUpdateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> InstituteResponse:
        inst = await self.repo.get_by_id(institute_id)
        if not inst:
            raise ResourceNotFoundException("Institute", institute_id)

        update_data = payload.model_dump(exclude_unset=True)
        for field_name, val in update_data.items():
            setattr(inst, field_name, val)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=inst.id,
            module_key="institute_management",
            action="INSTITUTE_INTEGRATIONS_UPDATED",
            resource_type="institute",
            resource_id=str(inst.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/institutes/{inst.id}/integrations",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={k: "[CONFIGURED]" for k in update_data.keys()},
        )
        await self.session.commit()
        reloaded = await self.repo.get_by_id(inst.id)
        return InstituteResponse.model_validate(reloaded)

    async def list_academic_sessions(self, institute_id: uuid.UUID) -> List[AcademicSessionResponse]:
        sessions = await self.repo.list_academic_sessions(institute_id)
        return [AcademicSessionResponse.model_validate(s) for s in sessions]

    async def create_academic_session(
        self,
        institute_id: uuid.UUID,
        payload: AcademicSessionCreateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> AcademicSessionResponse:
        existing = await self.repo.get_academic_session_by_code(institute_id, payload.session_code)
        if existing:
            raise ConflictException(f"Session '{payload.session_code}' already exists for this institute.")

        if payload.is_current:
            existing_sessions = await self.repo.list_academic_sessions(institute_id)
            for s in existing_sessions:
                if s.is_current:
                    s.is_current = False

        sess = AcademicSession(
            institute_id=institute_id,
            session_code=payload.session_code.upper(),
            session_name=payload.session_name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            is_current=payload.is_current,
            is_admission_open=payload.is_admission_open,
            term_structure=payload.term_structure,
            terms_count=payload.terms_count,
            status=payload.status,
            metadata_json=payload.metadata_json,
        )
        await self.repo.create_academic_session(sess)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=institute_id,
            module_key="institute_management",
            action="ACADEMIC_SESSION_CREATED",
            resource_type="academic_session",
            resource_id=str(sess.id),
            http_method="POST",
            endpoint_path=f"/api/v1/institutes/{institute_id}/academic-sessions",
            status_code=201,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"session_code": sess.session_code, "name": sess.session_name},
        )
        await self.session.commit()
        await self.session.refresh(sess)
        return AcademicSessionResponse.model_validate(sess)

    async def update_academic_session(
        self,
        institute_id: uuid.UUID,
        session_id: uuid.UUID,
        payload: AcademicSessionUpdateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> AcademicSessionResponse:
        sess = await self.repo.get_academic_session_by_id(session_id)
        if not sess or sess.institute_id != institute_id:
            raise ResourceNotFoundException("AcademicSession", session_id)

        update_data = payload.model_dump(exclude_unset=True)

        if update_data.get("is_current") is True:
            all_sessions = await self.repo.list_academic_sessions(institute_id)
            for s in all_sessions:
                if s.id != sess.id and s.is_current:
                    s.is_current = False

        for field_name, val in update_data.items():
            setattr(sess, field_name, val)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=institute_id,
            module_key="institute_management",
            action="ACADEMIC_SESSION_UPDATED",
            resource_type="academic_session",
            resource_id=str(sess.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/institutes/{institute_id}/academic-sessions/{session_id}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload=update_data,
        )
        await self.session.commit()
        await self.session.refresh(sess)
        return AcademicSessionResponse.model_validate(sess)

    async def delete_academic_session(
        self,
        institute_id: uuid.UUID,
        session_id: uuid.UUID,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Dict[str, Any]:
        sess = await self.repo.get_academic_session_by_id(session_id)
        if not sess or sess.institute_id != institute_id:
            raise ResourceNotFoundException("AcademicSession", session_id)

        if sess.is_current:
            raise ForbiddenException("Active current academic session cannot be deleted. Promote another session first.")

        session_code = sess.session_code
        await self.repo.delete_academic_session(sess)
        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=institute_id,
            module_key="institute_management",
            action="ACADEMIC_SESSION_DELETED",
            resource_type="academic_session",
            resource_id=str(session_id),
            http_method="DELETE",
            endpoint_path=f"/api/v1/institutes/{institute_id}/academic-sessions/{session_id}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"deleted_code": session_code},
        )
        await self.session.commit()
        return {"status": "success", "message": f"Academic session '{session_code}' has been removed."}

    async def toggle_module_state(
        self,
        institute_id: uuid.UUID,
        module_key: str,
        payload: ModuleToggleRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> ModuleConfigResponse:
        mod_cfg = await self.repo.get_module_config(institute_id, module_key)
        if not mod_cfg:
            raise ResourceNotFoundException("SystemModuleConfig", f"{institute_id}:{module_key}")

        if mod_cfg.is_core_locked and not payload.is_enabled:
            raise ForbiddenException(
                f"Module '{mod_cfg.display_name}' is locked as an immutable core component of MY EDUCATION INDIA ERP."
            )

        mod_cfg.is_enabled = payload.is_enabled
        if payload.configuration is not None:
            mod_cfg.configuration = payload.configuration

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=institute_id,
            module_key="settings",
            action="MODULE_TOGGLED",
            resource_type="system_module_config",
            resource_id=str(mod_cfg.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/institutes/{institute_id}/modules/{module_key}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={
                "module_key": module_key,
                "is_enabled": payload.is_enabled,
            },
        )
        await self.session.commit()
        await self.session.refresh(mod_cfg)
        return ModuleConfigResponse.model_validate(mod_cfg)

    async def _ensure_default_sessions(self, institute: Institute) -> None:
        sessions = await self.repo.list_academic_sessions(institute.id)
        if sessions:
            return

        defaults = [
            (
                "AY-2026-27",
                "Academic Year 2026 - 2027",
                date(2026, 7, 1),
                date(2027, 6, 30),
                True,
                True,
                "SEMESTER",
                2,
                "ACTIVE",
            ),
            (
                "AY-2025-26",
                "Academic Year 2025 - 2026",
                date(2025, 7, 1),
                date(2026, 6, 30),
                False,
                False,
                "SEMESTER",
                2,
                "COMPLETED",
            ),
        ]
        for code, name, start, end, is_curr, is_adm, term, count, stat in defaults:
            s = AcademicSession(
                institute_id=institute.id,
                session_code=code,
                session_name=name,
                start_date=start,
                end_date=end,
                is_current=is_curr,
                is_admission_open=is_adm,
                term_structure=term,
                terms_count=count,
                status=stat,
                metadata_json={},
            )
            self.session.add(s)
        await self.session.flush()
