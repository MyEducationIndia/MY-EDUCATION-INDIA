import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    module_key: str
    group_key: str = "GENERAL"
    action_type: str = "READ"
    description: str | None = None


class PermissionGroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    group_key: str
    group_name: str
    category: str
    description: str | None = None
    display_order: int = 0


class RoleTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    template_key: str
    name: str
    department: str
    description: str | None = None
    default_permissions: List[str] = Field(default_factory=list)
    default_data_scope: str = "OWN_DEPARTMENT"
    default_subdomain: str = "admin"


class RoleCreateRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=64, pattern=r"^[A-Z0-9_]+$")
    name: str = Field(..., min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    portal_subdomain: str = Field(default="admin", max_length=32)
    institute_id: uuid.UUID | None = None
    is_custom_role: bool = Field(default=False)
    department_name: str | None = Field(default=None, max_length=100)
    data_scope: str = Field(default="ALL_INSTITUTE", max_length=50)
    field_permissions_json: Dict[str, Any] | None = None
    menu_permissions_json: List[str] | None = None
    permission_codes: List[str] = Field(default_factory=list)


class RoleUpdatePermissionsRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    department_name: str | None = Field(default=None, max_length=100)
    data_scope: str | None = Field(default=None, max_length=50)
    field_permissions_json: Dict[str, Any] | None = None
    menu_permissions_json: List[str] | None = None
    permission_codes: List[str] | None = None


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    description: str | None
    portal_subdomain: str
    is_system_role: bool
    is_custom_role: bool = False
    department_name: str | None = None
    data_scope: str = "ALL_INSTITUTE"
    field_permissions_json: Dict[str, Any] | None = None
    menu_permissions_json: List[str] | None = None
    institute_id: uuid.UUID | None
    permissions: List[PermissionResponse]
    created_at: datetime
    updated_at: datetime
