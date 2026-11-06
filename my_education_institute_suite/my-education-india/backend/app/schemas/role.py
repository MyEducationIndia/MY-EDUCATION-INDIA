import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    module_key: str
    description: str | None


class RoleCreateRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=64, pattern=r"^[A-Z0-9_]+$")
    name: str = Field(..., min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    portal_subdomain: str = Field(default="admin", max_length=32)
    institute_id: uuid.UUID | None = None
    permission_codes: List[str] = Field(default_factory=list)


class RoleUpdatePermissionsRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    permission_codes: List[str] = Field(..., min_length=0)


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    description: str | None
    portal_subdomain: str
    is_system_role: bool
    institute_id: uuid.UUID | None
    permissions: List[PermissionResponse]
    created_at: datetime
    updated_at: datetime
