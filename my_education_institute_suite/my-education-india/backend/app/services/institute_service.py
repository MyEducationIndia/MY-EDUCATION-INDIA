import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import (
    ConflictException,
    ForbiddenException,
    ResourceNotFoundException,
)
from app.models.institute import Institute
from app.models.module_config import SystemModuleConfig
from app.models.user import User
from app.permissions.module_catalog import ENTERPRISE_MODULES_CATALOG
from app.repositories.institute_repository import InstituteRepository
from app.schemas.institute import (
    InstituteBrandingUpdateRequest,
    InstituteCreateRequest,
    InstituteResponse,
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
        return InstituteResponse.model_validate(inst)

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
                f"Core security/system module '{mod_cfg.display_name}' cannot be disabled."
            )

        mod_cfg.is_enabled = payload.is_enabled
        if payload.configuration is not None:
            mod_cfg.configuration = payload.configuration

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=institute_id,
            module_key="settings",
            action="MODULE_STATE_TOGGLED",
            resource_type="system_module_config",
            resource_id=str(mod_cfg.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/institutes/{institute_id}/modules/{module_key}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"module_key": module_key, "is_enabled": payload.is_enabled},
        )
        await self.session.commit()
        await self.session.refresh(mod_cfg)
        return ModuleConfigResponse.model_validate(mod_cfg)
