import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import (
    ConflictException,
    ForbiddenException,
    ResourceNotFoundException,
)
from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.schemas.role import (
    PermissionResponse,
    RoleCreateRequest,
    RoleResponse,
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
                "permissions": payload.permission_codes,
            },
        )
        await self.session.commit()
        await self.session.refresh(role)
        return RoleResponse.model_validate(role)

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

        permissions = await self.role_repo.get_permissions_by_codes(payload.permission_codes)
        role.permissions = permissions

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=actor.institute_id,
            module_key="role_management",
            action="ROLE_PERMISSIONS_UPDATED",
            resource_type="role",
            resource_id=str(role.id),
            http_method="PUT",
            endpoint_path=f"/api/v1/roles/{role.id}/permissions",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"permission_codes": payload.permission_codes},
        )
        await self.session.commit()
        await self.session.refresh(role)
        return RoleResponse.model_validate(role)
