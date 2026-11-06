import uuid
from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    actor_user_id: uuid.UUID | None
    institute_id: uuid.UUID | None
    module_key: str
    action: str
    resource_type: str
    resource_id: str | None
    http_method: str
    endpoint_path: str
    status_code: int
    ip_address: str
    user_agent: str
    request_id: str
    changes_payload: Dict[str, Any]
    created_at: datetime
