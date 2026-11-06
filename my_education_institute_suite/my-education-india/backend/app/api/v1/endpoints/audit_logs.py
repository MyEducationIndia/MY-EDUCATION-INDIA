import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import require_permissions
from app.schemas.audit_log import AuditLogResponse
from app.schemas.common import PaginatedResponse
from app.services.audit_service import AuditService

router = APIRouter(prefix="/audit-logs", tags=["Compliance & Audit Logs"])


@router.get("", response_model=PaginatedResponse[AuditLogResponse])
async def list_audit_logs(
    institute_id: uuid.UUID | None = Query(default=None),
    module_key: str | None = Query(default=None, max_length=64),
    action: str | None = Query(default=None, max_length=120),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    current_user: User = Depends(
        require_permissions("audit:read", module_key="audit_logs")
    ),
    db: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[AuditLogResponse]:
    effective_inst = institute_id if current_user.is_super_admin else current_user.institute_id
    return await AuditService(db).get_paginated_logs(
        institute_id=effective_inst,
        module_key=module_key,
        action=action,
        page=page,
        page_size=page_size,
    )
