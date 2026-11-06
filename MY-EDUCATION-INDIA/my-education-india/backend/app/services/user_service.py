import math
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.security import hash_password
from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.common import PaginatedResponse
from app.schemas.user import (
    UserCreateRequest,
    UserSummaryResponse,
    UserUpdateStatusRequest,
)
from app.services.audit_service import AuditService


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.role_repo = RoleRepository(session)
        self.audit_service = AuditService(session)

    async def list_users(
        self,
        institute_id: uuid.UUID | None,
        search: str | None,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[UserSummaryResponse]:
        items, total = await self.user_repo.list_paginated(
            institute_id=institute_id,
            search=search,
            page=page,
            page_size=page_size,
        )
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        return PaginatedResponse[UserSummaryResponse](
            items=[UserSummaryResponse.model_validate(u) for u in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    async def create_user(
        self,
        payload: UserCreateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserSummaryResponse:
        existing_email = await self.user_repo.get_by_identifier(payload.email)
        if existing_email:
            raise ConflictException(f"Email '{payload.email}' is already registered.")
        existing_username = await self.user_repo.get_by_identifier(payload.username)
        if existing_username:
            raise ConflictException(f"Username '{payload.username}' is already taken.")

        roles = await self.role_repo.get_Roles_by_ids(payload.role_ids)
        new_user = User(
            email=payload.email.lower(),
            username=payload.username,
            phone_number=payload.phone_number,
            first_name=payload.first_name,
            last_name=payload.last_name,
            password_hash=hash_password(payload.password),
            is_active=True,
            is_super_admin=payload.is_super_admin if actor.is_super_admin else False,
            is_verified=True,
            institute_id=payload.institute_id or actor.institute_id,
            roles=roles,
        )
        await self.user_repo.create(new_user)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=new_user.institute_id,
            module_key="role_management",
            action="USER_PROVISIONED",
            resource_type="user",
            resource_id=str(new_user.id),
            http_method="POST",
            endpoint_path="/api/v1/users",
            status_code=201,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={
                "email": new_user.email,
                "username": new_user.username,
                "role_ids": [str(rid) for rid in payload.role_ids],
            },
        )
        await self.session.commit()
        await self.session.refresh(new_user)
        return UserSummaryResponse.model_validate(new_user)

    async def update_user_status(
        self,
        user_id: uuid.UUID,
        payload: UserUpdateStatusRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserSummaryResponse:
        target = await self.user_repo.get_by_id(user_id)
        if not target:
            raise ResourceNotFoundException("User", user_id)

        target.is_active = payload.is_active
        if payload.role_ids is not None:
            target.roles = await self.role_repo.get_Roles_by_ids(payload.role_ids)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=target.institute_id,
            module_key="role_management",
            action="USER_STATUS_UPDATED",
            resource_type="user",
            resource_id=str(target.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/users/{target.id}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"is_active": payload.is_active},
        )
        await self.session.commit()
        await self.session.refresh(target)
        return UserSummaryResponse.model_validate(target)
