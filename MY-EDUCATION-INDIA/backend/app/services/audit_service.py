import hashlib
import json
import math
import uuid
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
from app.repositories.audit_repository import AuditLogRepository
from app.schemas.audit_log import AuditLogResponse, AuditLogSummaryResponse
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
        event_category: Optional[str] = None,
        severity: str = "INFO",
        actor_username: Optional[str] = None,
        actor_role: Optional[str] = None,
        duration_ms: int = 0,
        ip_location: str = "Indore, MP, India",
    ) -> AuditLog:
        # Determine event category if omitted
        if not event_category:
            act_up = action.upper()
            if "LOGIN" in act_up:
                event_category = "AUTH_LOGIN"
            elif "LOGOUT" in act_up:
                event_category = "AUTH_LOGOUT"
            elif any(w in act_up for w in ["PERMISSION", "ROLE", "POLICY"]):
                event_category = "PERMISSION_CHANGE"
            elif any(w in act_up for w in ["SECURITY", "BLOCKED", "LOCKOUT", "MFA"]):
                event_category = "SECURITY_EVENT"
            elif any(w in act_up for w in ["SETTING", "BRANDING", "MODULE_TOGGLE"]):
                event_category = "SETTINGS_CHANGE"
            elif any(w in act_up for w in ["FILE", "MEDIA", "DOCUMENT_UPLOAD"]):
                event_category = "FILE_UPLOAD"
            elif "API" in act_up or http_method in ("GET", "HEAD"):
                event_category = "API_CALL"
            else:
                event_category = "CRUD_OPERATION"

        # Tamper-evident checksum
        payload_data = changes_payload or {}
        raw_json = json.dumps(payload_data, sort_keys=True, default=str)
        checksum = hashlib.sha256(raw_json.encode("utf-8")).hexdigest()

        log_entry = AuditLog(
            actor_user_id=actor_user_id,
            actor_username=actor_username,
            actor_role=actor_role,
            institute_id=institute_id,
            module_key=module_key,
            action=action,
            event_category=event_category.upper(),
            severity=severity.upper(),
            resource_type=resource_type,
            resource_id=resource_id,
            http_method=http_method,
            endpoint_path=endpoint_path,
            status_code=status_code,
            duration_ms=duration_ms,
            ip_address=ip_address,
            ip_location=ip_location,
            user_agent=user_agent[:512],
            request_id=request_id,
            changes_payload=payload_data,
            payload_checksum=checksum,
        )
        return await self.repo.create(log_entry)

    async def get_summary_stats(
        self, institute_id: uuid.UUID | None
    ) -> AuditLogSummaryResponse:
        data = await self.repo.get_summary_stats(institute_id)
        return AuditLogSummaryResponse(
            total_events=data["total_events"],
            category_breakdown=data["category_breakdown"],
            severity_breakdown=data["severity_breakdown"],
            security_alerts_count=data["security_alerts_count"],
            active_audited_modules_count=data["active_audited_modules_count"],
        )

    async def get_paginated_logs(
        self,
        institute_id: uuid.UUID | None,
        event_category: Optional[str] = None,
        severity: Optional[str] = None,
        module_key: Optional[str] = None,
        actor_username: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedResponse[AuditLogResponse]:
        items, total = await self.repo.list_paginated(
            institute_id=institute_id,
            event_category=event_category,
            severity=severity,
            module_key=module_key,
            actor_username=actor_username,
            search=search,
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
