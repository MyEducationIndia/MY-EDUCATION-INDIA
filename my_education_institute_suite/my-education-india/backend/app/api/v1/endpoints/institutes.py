import uuid
from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    require_permissions,
)
from app.schemas.institute import (
    InstituteBrandingUpdateRequest,
    InstituteCreateRequest,
    InstituteResponse,
    ModuleConfigResponse,
    ModuleToggleRequest,
)
from app.services.institute_service import InstituteService

router = APIRouter(prefix="/institutes", tags=["Institute & Module Governance"])


@router.get("", response_model=List[InstituteResponse])
async def list_institutes(
    current_user: User = Depends(
        require_permissions("institutes:read", module_key="institute_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> List[InstituteResponse]:
    return await InstituteService(db).list_institutes()


@router.get("/{institute_id}", response_model=InstituteResponse)
async def get_institute(
    institute_id: uuid.UUID,
    current_user: User = Depends(
        require_permissions("institutes:read", module_key="institute_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> InstituteResponse:
    return await InstituteService(db).get_institute(institute_id)


@router.post(
    "",
    response_model=InstituteResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def create_institute(
    payload: InstituteCreateRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("institutes:write", module_key="institute_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> InstituteResponse:
    return await InstituteService(db).create_institute(
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.patch(
    "/{institute_id}/branding",
    response_model=InstituteResponse,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def update_institute_branding(
    institute_id: uuid.UUID,
    payload: InstituteBrandingUpdateRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("institutes:write", module_key="institute_management")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> InstituteResponse:
    return await InstituteService(db).update_branding_and_settings(
        institute_id=institute_id,
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )


@router.patch(
    "/{institute_id}/modules/{module_key}",
    response_model=ModuleConfigResponse,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def toggle_institute_module(
    institute_id: uuid.UUID,
    module_key: str,
    payload: ModuleToggleRequest,
    request: Request,
    current_user: User = Depends(
        require_permissions("modules:toggle", module_key="settings")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> ModuleConfigResponse:
    return await InstituteService(db).toggle_module_state(
        institute_id=institute_id,
        module_key=module_key,
        payload=payload,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
