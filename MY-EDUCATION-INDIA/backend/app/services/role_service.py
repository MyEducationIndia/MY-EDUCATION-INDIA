import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    ResourceNotFoundException,
)
from app.models.permission import Permission
from app.models.rbac_extended import PermissionGroup, RoleTemplate
from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.schemas.role import (
    PermissionGroupResponse,
    PermissionResponse,
    RoleCreateRequest,
    RoleResponse,
    RoleTemplateResponse,
    RoleUpdatePermissionsRequest,
)
from app.services.audit_service import AuditService


class RoleService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.role_repo = RoleRepository(session)
        self.audit_service = AuditService(session)

    async def list_roles(self, institute_id: uuid.UUID | None) -> List[RoleResponse]:
        roles = await self.role_repo.list_roles(institute_id)
        return [RoleResponse.model_validate(r) for r in roles]

    async def list_permissions(self, module_key: str | None = None) -> List[PermissionResponse]:
        perms = await self.role_repo.list_permissions(module_key)
        return [PermissionResponse.model_validate(p) for p in perms]

    async def list_permission_groups(self) -> List[PermissionGroupResponse]:
        await self._ensure_seed_permission_groups()
        groups = await self.role_repo.list_permission_groups()
        return [PermissionGroupResponse.model_validate(g) for g in groups]

    async def list_role_templates(self) -> List[RoleTemplateResponse]:
        await self._ensure_seed_role_templates()
        templates = await self.role_repo.list_role_templates()
        return [RoleTemplateResponse.model_validate(t) for t in templates]

    async def create_role(
        self,
        payload: RoleCreateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> RoleResponse:
        existing = await self.role_repo.get_by_code(payload.code, payload.institute_id)
        if existing:
            raise ConflictException(f"Role with code '{payload.code}' already exists.")

        permissions = await self.role_repo.get_permissions_by_codes(payload.permission_codes)
        role = Role(
            code=payload.code.upper(),
            name=payload.name,
            description=payload.description,
            portal_subdomain=payload.portal_subdomain,
            is_system_role=False,
            is_custom_role=payload.is_custom_role or True,
            department_name=payload.department_name,
            data_scope=payload.data_scope,
            field_permissions_json=payload.field_permissions_json,
            menu_permissions_json=payload.menu_permissions_json,
            institute_id=payload.institute_id or actor.institute_id,
            permissions=permissions,
        )
        await self.role_repo.create(role)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=actor.institute_id,
            module_key="role_management",
            action="ROLE_CREATED",
            resource_type="role",
            resource_id=str(role.id),
            http_method="POST",
            endpoint_path="/api/v1/roles",
            status_code=201,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={
                "code": role.code,
                "name": role.name,
                "is_custom_role": role.is_custom_role,
                "department_name": role.department_name,
                "data_scope": role.data_scope,
                "permissions": payload.permission_codes,
            },
        )
        await self.session.commit()
        await self.session.refresh(role)
        return RoleResponse.model_validate(role)

    async def create_role_from_template(
        self,
        template_key: str,
        role_code: str,
        role_name: str,
        department_name: Optional[str],
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> RoleResponse:
        await self._ensure_seed_role_templates()
        template = await self.role_repo.get_role_template_by_key(template_key)
        if not template:
            raise ResourceNotFoundException("RoleTemplate", template_key)

        req = RoleCreateRequest(
            code=role_code.upper(),
            name=role_name or template.name,
            description=template.description,
            portal_subdomain=template.default_subdomain,
            institute_id=actor.institute_id,
            is_custom_role=True,
            department_name=department_name or template.department,
            data_scope=template.default_data_scope,
            permission_codes=template.default_permissions,
        )
        return await self.create_role(req, actor, ip_address, user_agent, request_id)

    async def update_role_permissions(
        self,
        role_id: uuid.UUID,
        payload: RoleUpdatePermissionsRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> RoleResponse:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise ResourceNotFoundException("Role", role_id)
        if role.is_system_role and not actor.is_super_admin:
            raise ForbiddenException("System roles can only be modified by the Super Administrator.")

        if payload.name is not None:
            role.name = payload.name
        if payload.description is not None:
            role.description = payload.description
        if payload.department_name is not None:
            role.department_name = payload.department_name
        if payload.data_scope is not None:
            role.data_scope = payload.data_scope
        if payload.field_permissions_json is not None:
            role.field_permissions_json = payload.field_permissions_json
        if payload.menu_permissions_json is not None:
            role.menu_permissions_json = payload.menu_permissions_json

        if payload.permission_codes is not None:
            new_permissions = await self.role_repo.get_permissions_by_codes(payload.permission_codes)
            role.permissions = new_permissions

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=actor.institute_id,
            module_key="role_management",
            action="ROLE_UPDATED",
            resource_type="role",
            resource_id=str(role.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/roles/{role_id}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={
                "code": role.code,
                "name": role.name,
                "data_scope": role.data_scope,
                "department_name": role.department_name,
                "field_permissions": role.field_permissions_json,
                "menu_permissions": role.menu_permissions_json,
                "permission_count": len(role.permissions),
            },
        )
        await self.session.commit()
        await self.session.refresh(role)
        return RoleResponse.model_validate(role)

    async def delete_role(
        self,
        role_id: uuid.UUID,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> dict:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise ResourceNotFoundException("Role", role_id)
        if role.is_system_role:
            raise ForbiddenException("Core system roles cannot be deleted. You may only modify their permissions.")

        role_code = role.code
        await self.role_repo.delete(role)
        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=actor.institute_id,
            module_key="role_management",
            action="ROLE_DELETED",
            resource_type="role",
            resource_id=str(role_id),
            http_method="DELETE",
            endpoint_path=f"/api/v1/roles/{role_id}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"deleted_code": role_code},
        )
        await self.session.commit()
        return {"status": "success", "message": f"Role '{role_code}' has been permanently removed."}

    async def _ensure_seed_permission_groups(self) -> None:
        groups = await self.role_repo.list_permission_groups()
        if len(groups) >= 8:
            return

        defaults = [
            ("AUTH_IDENTITY", "Authentication & Identity", "SECURITY", "Sign-in, MFA, Session management and credential policies", 1),
            ("RBAC_GOVERNANCE", "RBAC & Permissions", "SECURITY", "Role definition, permission matrices, scopes and field masks", 2),
            ("ACADEMICS_LMS", "Academics & Curricula", "EDUCATION", "Course offerings, syllabi, class schedules and LMS materials", 3),
            ("ADMISSIONS_CRM", "Admissions & Inquiries", "OPERATIONS", "Application pipeline, entrance validation and CRM leads", 4),
            ("EXAM_CBT", "Examinations & CBT", "EVALUATION", "Question banks, test proctoring, evaluation and grade cards", 5),
            ("FINANCE_ACCOUNTS", "Finance & Accounts", "FINANCE", "Fee collection, scholarship payouts, reconciliation and payroll", 6),
            ("FACULTY_HR", "Faculty & Staff HR", "HR", "Faculty designations, workload, leaves and performance appraisals", 7),
            ("CAMPUS_OPS", "Campus Infrastructure", "OPERATIONS", "Hostel allotments, library inventory, laboratories and fleet", 8),
            ("PLATFORM_DEVOPS", "DevOps & Integrations", "TECHNOLOGY", "API gateways, webhooks, audit telemetry and system backups", 9),
        ]
        for key, name, cat, desc, order in defaults:
            exists = any(g.group_key == key for g in groups)
            if not exists:
                self.session.add(
                    PermissionGroup(
                        group_key=key,
                        group_name=name,
                        category=cat,
                        description=desc,
                        display_order=order,
                    )
                )
        await self.session.flush()

    async def _ensure_seed_role_templates(self) -> None:
        templates = await self.role_repo.list_role_templates()
        if len(templates) >= 6:
            return

        defaults = [
            (
                "JUNIOR_LECTURER",
                "Junior Assistant Professor",
                "Academic Faculty",
                "Entry-level faculty role with classroom teaching, attendance and grade submission rights.",
                ["courses:read", "courses:write", "attendance:write", "lms:write"],
                "OWN_DEPARTMENT",
                "faculty",
            ),
            (
                "FEE_ACCOUNTANT",
                "Fee & Accounts Executive",
                "Finance Office",
                "Cashier and fee reconciliation desk with payment posting and ledger tracking permissions.",
                ["finance:read", "finance:write", "fees:read", "fees:write", "reports:read"],
                "ALL_INSTITUTE",
                "admin",
            ),
            (
                "CBT_PROCTOR",
                "CBT Examination Proctor",
                "Examination Cell",
                "Invigilator role for computer-based testing, session monitoring and biometric attendance.",
                ["exams:read", "cbt:proctor", "attendance:read"],
                "ALL_INSTITUTE",
                "exam",
            ),
            (
                "ADMISSIONS_COUNSELOR",
                "Admissions Counselor",
                "Admissions & CRM",
                "Inquiry desk and counselor role handling candidate queries, campus tours and applications.",
                ["admissions:read", "admissions:write", "crm:read", "crm:write"],
                "ALL_INSTITUTE",
                "admin",
            ),
            (
                "DEPT_HOD",
                "Head of Department (HOD)",
                "Academic Faculty",
                "Departmental head overseeing academic schedules, faculty workloads and grade sign-offs.",
                ["courses:read", "courses:write", "faculty:read", "approvals:write", "reports:read"],
                "OWN_DEPARTMENT",
                "faculty",
            ),
            (
                "STUDENT_COUNCIL",
                "Student Council Member",
                "Student Welfare",
                "Student representative role with noticeboard publishing and event coordination rights.",
                ["student:read", "events:read", "events:write", "notices:read"],
                "OWN_RECORDS",
                "student",
            ),
        ]
        for key, name, dept, desc, perms, scope, sub in defaults:
            exists = any(t.template_key == key for t in templates)
            if not exists:
                self.session.add(
                    RoleTemplate(
                        template_key=key,
                        name=name,
                        department=dept,
                        description=desc,
                        default_permissions=perms,
                        default_data_scope=scope,
                        default_subdomain=sub,
                    )
                )
        await self.session.flush()
