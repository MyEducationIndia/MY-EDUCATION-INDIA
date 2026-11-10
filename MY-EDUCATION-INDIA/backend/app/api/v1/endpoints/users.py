import uuid
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    require_permissions,
)
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
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["User Administration"])


@router.get("", response_model=PaginatedResponse[UserSummaryResponse])
async def list_users(
    institute_id: uuid.UUID | None = Query(default=None),
    search: str | None = Query(default=None, max_length=120),
    user_category: str | None = Query(default=None, max_length=32),
    is_archived: bool | None = Query(default=None),
    department: str | None = Query(default=None, max_length=100),
    verification_status: str | None = Query(default=None, max_length=32),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(
        require_permissions("users:read", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[UserSummaryResponse]:
    effective_inst = institute_id if current_user.is_super_admin else current_user.institute_id
    return await UserService(db).list_users(
        institute_id=effective_inst,
        search=search,
        user_category=user_category,
        is_archived=is_archived,
        department=department,
        verification_status=verification_status,
        page=page,
        page_size=page_size,
    )


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user_detail(
    user_id: uuid.UUID,
    current_user: User = Depends(
        require_permissions("users:read", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> UserDetailResponse:
    return await UserService(db).get_user_detail(user_id)


@router.post(
    "",
    response_model=UserDetailResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def create_user(
    payload: UserCreateRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> UserDetailResponse:
    return await UserService(db).create_user(
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.patch(
    "/{user_id}",
    response_model=UserDetailResponse,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def update_user(
    user_id: uuid.UUID,
    payload: UserUpdateRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> UserDetailResponse:
    return await UserService(db).update_user(
        user_id=user_id,
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.post(
    "/{user_id}/archive",
    dependencies=[Depends(enforce_csrf_protection)],
)
async def archive_user(
    user_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    return await UserService(db).archive_user(
        user_id=user_id,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.post(
    "/{user_id}/restore",
    dependencies=[Depends(enforce_csrf_protection)],
)
async def restore_user(
    user_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    return await UserService(db).restore_user(
        user_id=user_id,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.post(
    "/bulk-action",
    dependencies=[Depends(enforce_csrf_protection)],
)
async def execute_bulk_action(
    payload: UserBulkActionRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    return await UserService(db).execute_bulk_action(
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.post(
    "/import",
    dependencies=[Depends(enforce_csrf_protection)],
)
async def bulk_import_users(
    payload: UserBulkImportRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    return await UserService(db).bulk_import(
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.post(
    "/{user_id}/documents",
    response_model=UserDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def add_user_document(
    user_id: uuid.UUID,
    payload: UserDocumentCreateRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> UserDocumentResponse:
    return await UserService(db).add_document(
        user_id=user_id,
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.patch(
    "/{user_id}/documents/{document_id}/verify",
    response_model=UserDocumentResponse,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def verify_user_document(
    user_id: uuid.UUID,
    document_id: uuid.UUID,
    payload: UserDocumentVerifyRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> UserDocumentResponse:
    return await UserService(db).verify_document(
        user_id=user_id,
        document_id=document_id,
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.delete(
    "/{user_id}/documents/{document_id}",
    dependencies=[Depends(enforce_csrf_protection)],
)
async def delete_user_document(
    user_id: uuid.UUID,
    document_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    return await UserService(db).delete_document(
        user_id=user_id,
        document_id=document_id,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
