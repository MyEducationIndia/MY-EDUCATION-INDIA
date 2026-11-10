import math
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.security import hash_password
from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    ResourceNotFoundException,
)
from app.models.user import User
from app.models.user_document import UserDocument
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.common import PaginatedResponse
from app.schemas.user import (
    UserBulkActionRequest,
    UserBulkImportRequest,
    UserCreateRequest,
    UserDetailResponse,
    UserDocumentCreateRequest,
    UserDocumentResponse,
    UserDocumentVerifyRequest,
    UserSummaryResponse,
    UserUpdateRequest,
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
        user_category: str | None,
        is_archived: bool | None,
        department: str | None,
        verification_status: str | None,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[UserSummaryResponse]:
        items, total = await self.user_repo.list_paginated(
            institute_id=institute_id,
            search=search,
            user_category=user_category,
            is_archived=is_archived,
            department=department,
            verification_status=verification_status,
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

    async def get_user_detail(self, user_id: uuid.UUID) -> UserDetailResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)
        return UserDetailResponse.model_validate(user)

    async def create_user(
        self,
        payload: UserCreateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserDetailResponse:
        existing_email = await self.user_repo.get_by_identifier(payload.email)
        if existing_email:
            raise ConflictException(f"Email '{payload.email}' is already registered.")
        existing_username = await self.user_repo.get_by_identifier(payload.username)
        if existing_username:
            raise ConflictException(f"Username '{payload.username}' is already taken.")

        roles = await self.role_repo.get_roles_by_ids(payload.role_ids)
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
            user_category=payload.user_category.upper(),
            department=payload.department,
            designation=payload.designation,
            admission_or_emp_id=payload.admission_or_emp_id,
            dob=payload.dob,
            gender=payload.gender,
            blood_group=payload.blood_group,
            photo_url=payload.photo_url,
            digital_signature_url=payload.digital_signature_url,
            identity_verification_status="PENDING",
            verification_id_type=payload.verification_id_type,
            verification_id_number=payload.verification_id_number,
            is_archived=False,
            metadata_json={},
            institute_id=payload.institute_id or actor.institute_id,
            roles=roles,
        )
        await self.user_repo.create(new_user)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=new_user.institute_id,
            module_key="user_management",
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
                "category": new_user.user_category,
                "role_ids": [str(rid) for rid in payload.role_ids],
            },
        )
        await self.session.commit()
        await self.session.refresh(new_user)
        return UserDetailResponse.model_validate(new_user)

    async def update_user(
        self,
        user_id: uuid.UUID,
        payload: UserUpdateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserDetailResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)

        update_data = payload.model_dump(exclude_unset=True)

        if "role_ids" in update_data and payload.role_ids is not None:
            new_roles = await self.role_repo.get_roles_by_ids(payload.role_ids)
            user.roles = new_roles
            del update_data["role_ids"]

        for k, v in update_data.items():
            setattr(user, k, v)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=user.institute_id,
            module_key="user_management",
            action="USER_PROFILE_UPDATED",
            resource_type="user",
            resource_id=str(user.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/users/{user.id}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={k: str(v) for k, v in update_data.items()},
        )
        await self.session.commit()
        await self.session.refresh(user)
        return UserDetailResponse.model_validate(user)

    async def archive_user(
        self,
        user_id: uuid.UUID,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Dict[str, Any]:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)
        if user.is_super_admin:
            raise ForbiddenException("Super Administrator account cannot be archived.")

        user.is_archived = True
        user.is_active = False
        user.archived_at = datetime.now(timezone.utc)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=user.institute_id,
            module_key="user_management",
            action="USER_ARCHIVED",
            resource_type="user",
            resource_id=str(user.id),
            http_method="POST",
            endpoint_path=f"/api/v1/users/{user.id}/archive",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"archived": True},
        )
        await self.session.commit()
        return {"status": "success", "message": f"User '{user.username}' has been safely archived."}

    async def restore_user(
        self,
        user_id: uuid.UUID,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Dict[str, Any]:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)

        user.is_archived = False
        user.is_active = True
        user.archived_at = None

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=user.institute_id,
            module_key="user_management",
            action="USER_RESTORED",
            resource_type="user",
            resource_id=str(user.id),
            http_method="POST",
            endpoint_path=f"/api/v1/users/{user.id}/restore",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"restored": True},
        )
        await self.session.commit()
        return {"status": "success", "message": f"User '{user.username}' has been restored to active duty."}

    async def execute_bulk_action(
        self,
        payload: UserBulkActionRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Dict[str, Any]:
        processed_count = 0
        role_to_assign = None
        if payload.action == "ASSIGN_ROLE" and payload.role_id:
            role_to_assign = await self.role_repo.get_by_id(payload.role_id)

        for uid in payload.user_ids:
            u = await self.user_repo.get_by_id(uid)
            if not u:
                continue

            if payload.action == "ACTIVATE":
                u.is_active = True
                u.is_archived = False
            elif payload.action == "DEACTIVATE":
                if not u.is_super_admin:
                    u.is_active = False
            elif payload.action == "ARCHIVE":
                if not u.is_super_admin:
                    u.is_archived = True
                    u.is_active = False
                    u.archived_at = datetime.now(timezone.utc)
            elif payload.action == "RESTORE":
                u.is_archived = False
                u.is_active = True
                u.archived_at = None
            elif payload.action == "ASSIGN_ROLE" and role_to_assign:
                if role_to_assign not in u.roles:
                    u.roles.append(role_to_assign)

            processed_count += 1

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=actor.institute_id,
            module_key="user_management",
            action=f"BULK_{payload.action}",
            resource_type="user",
            resource_id="batch",
            http_method="POST",
            endpoint_path="/api/v1/users/bulk-action",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"action": payload.action, "count": processed_count},
        )
        await self.session.commit()
        return {
            "status": "success",
            "message": f"Successfully performed {payload.action} on {processed_count} user accounts.",
            "processed_count": processed_count,
        }

    async def bulk_import(
        self,
        payload: UserBulkImportRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Dict[str, Any]:
        created_count = 0
        skipped_count = 0
        hashed_pwd = hash_password(payload.default_password)

        for item in payload.users:
            existing = await self.user_repo.get_by_identifier(item.email)
            if existing:
                skipped_count += 1
                continue

            new_user = User(
                email=item.email.lower(),
                username=item.username,
                phone_number=item.phone_number,
                first_name=item.first_name,
                last_name=item.last_name,
                password_hash=hashed_pwd,
                is_active=True,
                is_super_admin=False,
                is_verified=True,
                user_category=item.user_category.upper(),
                department=item.department,
                designation=item.designation,
                admission_or_emp_id=item.admission_or_emp_id,
                gender=item.gender,
                identity_verification_status="PENDING",
                is_archived=False,
                metadata_json={},
                institute_id=actor.institute_id,
            )
            await self.user_repo.create(new_user)
            created_count += 1

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=actor.institute_id,
            module_key="user_management",
            action="BULK_IMPORT_USERS",
            resource_type="user",
            resource_id="import_batch",
            http_method="POST",
            endpoint_path="/api/v1/users/import",
            status_code=201,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"created": created_count, "skipped": skipped_count},
        )
        await self.session.commit()
        return {
            "status": "success",
            "message": f"Import complete: {created_count} users created, {skipped_count} skipped (duplicates).",
            "created_count": created_count,
            "skipped_count": skipped_count,
        }

    async def add_document(
        self,
        user_id: uuid.UUID,
        payload: UserDocumentCreateRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserDocumentResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)

        doc = UserDocument(
            user_id=user_id,
            document_type=payload.document_type.upper(),
            document_title=payload.document_title,
            document_url=payload.document_url,
            file_size_bytes=payload.file_size_bytes,
            mime_type=payload.mime_type,
            verification_status="PENDING",
            remarks=payload.remarks,
        )
        await self.user_repo.add_document(doc)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=user.institute_id,
            module_key="user_management",
            action="USER_DOCUMENT_UPLOADED",
            resource_type="user_document",
            resource_id=str(doc.id),
            http_method="POST",
            endpoint_path=f"/api/v1/users/{user_id}/documents",
            status_code=201,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"document_type": doc.document_type, "title": doc.document_title},
        )
        await self.session.commit()
        await self.session.refresh(doc)
        return UserDocumentResponse.model_validate(doc)

    async def verify_document(
        self,
        user_id: uuid.UUID,
        document_id: uuid.UUID,
        payload: UserDocumentVerifyRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserDocumentResponse:
        doc = await self.user_repo.get_document_by_id(document_id)
        if not doc or doc.user_id != user_id:
            raise ResourceNotFoundException("UserDocument", document_id)

        doc.verification_status = payload.verification_status
        doc.verified_by_user_id = actor.id
        doc.verified_at = datetime.now(timezone.utc)
        if payload.remarks is not None:
            doc.remarks = payload.remarks

        # If document is verified, check overall user verification
        user = await self.user_repo.get_by_id(user_id)
        if user and payload.verification_status == "VERIFIED":
            user.identity_verification_status = "VERIFIED"

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=user.institute_id if user else None,
            module_key="user_management",
            action=f"DOCUMENT_{payload.verification_status}",
            resource_type="user_document",
            resource_id=str(doc.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/users/{user_id}/documents/{document_id}/verify",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"status": payload.verification_status, "remarks": payload.remarks},
        )
        await self.session.commit()
        await self.session.refresh(doc)
        return UserDocumentResponse.model_validate(doc)

    async def delete_document(
        self,
        user_id: uuid.UUID,
        document_id: uuid.UUID,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Dict[str, Any]:
        doc = await self.user_repo.get_document_by_id(document_id)
        if not doc or doc.user_id != user_id:
            raise ResourceNotFoundException("UserDocument", document_id)

        doc_type = doc.document_type
        await self.user_repo.delete_document(doc)

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=actor.institute_id,
            module_key="user_management",
            action="USER_DOCUMENT_DELETED",
            resource_type="user_document",
            resource_id=str(document_id),
            http_method="DELETE",
            endpoint_path=f"/api/v1/users/{user_id}/documents/{document_id}",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"deleted_type": doc_type},
        )
        await self.session.commit()
        return {"status": "success", "message": "Document removed."}

    async def update_user_status(
        self,
        user_id: uuid.UUID,
        payload: UserUpdateStatusRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserSummaryResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)

        user.is_active = payload.is_active
        if payload.role_ids is not None:
            roles = await self.role_repo.get_roles_by_ids(payload.role_ids)
            user.roles = roles

        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=user.institute_id,
            module_key="user_management",
            action="USER_STATUS_UPDATED",
            resource_type="user",
            resource_id=str(user.id),
            http_method="PATCH",
            endpoint_path=f"/api/v1/users/{user_id}/status",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"is_active": user.is_active},
        )
        await self.session.commit()
        await self.session.refresh(user)
        return UserSummaryResponse.model_validate(user)
