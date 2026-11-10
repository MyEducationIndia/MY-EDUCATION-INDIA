import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    require_permissions,
)
from app.schemas.role import (
    PermissionGroupResponse,
    PermissionResponse,
    RoleCreateRequest,
    RoleResponse,
    RoleTemplateResponse,
    RoleUpdatePermissionsRequest,
)
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["Role & Permission Management"])


class InstantiateTemplateRequest(BaseModel):
    role_code: str = Field(..., min_length=2, max_length=64, pattern=r"^[A-Z0-9_]+$")
    role_name: str = Field(..., min_length=2, max_length=120)
    department_name: Optional[str] = Field(default=None, max_length=100)


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


@router.get("/groups", response_model=List[PermissionGroupResponse])
async def list_permission_groups(
    current_user: User = Depends(
        require_permissions("roles:read", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> List[PermissionGroupResponse]:
    return await RoleService(db).list_permission_groups()


@router.get("/templates", response_model=List[RoleTemplateResponse])
async def list_role_templates(
    current_user: User = Depends(
        require_permissions("roles:read", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> List[RoleTemplateResponse]:
    return await RoleService(db).list_role_templates()


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


@router.post(
    "/templates/{template_key}/instantiate",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def instantiate_role_template(
    template_key: str,
    payload: InstantiateTemplateRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("roles:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> RoleResponse:
    return await RoleService(db).create_role_from_template(
        template_key=template_key,
        role_code=payload.role_code,
        role_name=payload.role_name,
        department_name=payload.department_name,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.patch(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def update_role(
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


@router.delete(
    "/{role_id}",
    dependencies=[Depends(enforce_csrf_protection)],
)
async def delete_role(
    role_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(
        require_permissions("roles:write", module_key="role_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    return await RoleService(db).delete_role(
        role_id=role_id,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
