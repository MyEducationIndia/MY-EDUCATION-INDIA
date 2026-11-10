import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    actor_user_id: uuid.UUID | None
    actor_username: str | None = None
    actor_role: str | None = None
    institute_id: uuid.UUID | None
    module_key: str
    action: str
    event_category: str = "CRUD_OPERATION"
    severity: str = "INFO"
    resource_type: str
    resource_id: str | None
    http_method: str
    endpoint_path: str
    status_code: int
    duration_ms: int = 0
    ip_address: str
    ip_location: str = "Indore, MP, India"
    user_agent: str
    request_id: str
    changes_payload: Dict[str, Any]
    payload_checksum: str | None = None
    created_at: datetime


class AuditLogSummaryResponse(BaseModel):
    total_events: int
    category_breakdown: Dict[str, int]
    severity_breakdown: Dict[str, int]
    security_alerts_count: int
    active_audited_modules_count: int
