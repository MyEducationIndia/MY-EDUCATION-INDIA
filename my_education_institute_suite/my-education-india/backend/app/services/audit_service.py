import math
import uuid
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
from app.repositories.audit_repository import AuditLogRepository
from app.schemas.audit_log import AuditLogResponse
from app.schemas.common import PaginatedResponse


class AuditService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = AuditLogRepository(session)

    async def record_event(
        self,
        *,
        actor_user_id: uuid.UUID | None,
        institute_id: uuid.UUID | None,
        module_key: str,
        action: str,
        resource_type: str,
        resource_id: str | None,
        http_method: str,
        endpoint_path: str,
        status_code: int,
        ip_address: str,
        user_agent: str,
        request_id: str,
        changes_payload: Dict[str, Any] | None = None,
    ) -> AuditLog:
        log_entry = AuditLog(
            actor_user_id=actor_user_id,
            institute_id=institute_id,
            module_key=module_key,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            http_method=http_method,
            endpoint_path=endpoint_path,
            status_code=status_code,
            ip_address=ip_address,
            user_agent=user_agent[:512],
            request_id=request_id,
            changes_payload=changes_payload or {},
        )
        return await self.repo.create(log_entry)

    async def get_paginated_logs(
        self,
        institute_id: uuid.UUID | None,
        module_key: str | None,
        action: str | None,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[AuditLogResponse]:
        items, total = await self.repo.list_paginated(
            institute_id=institute_id,
            module_key=module_key,
            action=action,
            page=page,
            page_size=page_size,
        )
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        return PaginatedResponse[AuditLogResponse](
            items=[AuditLogResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
