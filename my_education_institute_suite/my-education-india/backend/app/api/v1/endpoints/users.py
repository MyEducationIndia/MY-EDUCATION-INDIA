import uuid
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
    UserCreateRequest,
    UserSummaryResponse,
    UserUpdateStatusRequest,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["User Administration"])


@router.get("", response_model=PaginatedResponse[UserSummaryResponse])
async def list_users(
    institute_id: uuid.UUID | None = Query(default=None),
    search: str | None = Query(default=None, max_length=120),
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
        page=page,
        page_size=page_size,
    )


@router.post(
    "",
    response_model=UserSummaryResponse,
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
) -> UserSummaryResponse:
    return await UserService(db).create_user(
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.patch(
    "/{user_id}",
    response_model=UserSummaryResponse,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def update_user_status(
    user_id: uuid.UUID,
    payload: UserUpdateStatusRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("users:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> UserSummaryResponse:
    return await UserService(db).update_user_status(
        user_id=user_id,
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
