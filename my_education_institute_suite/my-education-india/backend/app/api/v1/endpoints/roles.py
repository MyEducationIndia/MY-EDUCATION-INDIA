import uuid
from typing import List
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    require_permissions,
)
from app.schemas.role import (
    PermissionResponse,
    RoleCreateRequest,
    RoleResponse,
    RoleUpdatePermissionsRequest,
)
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["Role & Permission Management"])


@router.get("", response_model=List[RoleResponse])
async def list_roles(
    institute_id: uuid.UUID | None = Query(default=None),
    current_user: User = Depends(
        require_permissions("roles:read", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> List[RoleResponse]:
    effective_inst = institute_id if current_user.is_super_admin else current_user.institute_id
    return await RoleService(db).list_roles(effective_inst)


@router.get("/permissions", response_model=List[PermissionResponse])
async def list_permissions(
    module_key: str | None = Query(default=None),
    current_user: User = Depends(
        require_permissions("roles:read", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> List[PermissionResponse]:
    return await RoleService(db).list_permissions(module_key)


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def create_role(
    payload: RoleCreateRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("roles:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> RoleResponse:
    return await RoleService(db).create_role(
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.put(
    "/{role_id}/permissions",
    response_model=RoleResponse,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def update_role_permissions(
    role_id: uuid.UUID,
    payload: RoleUpdatePermissionsRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("roles:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> RoleResponse:
    return await RoleService(db).update_role_permissions(
        role_id=role_id,
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
