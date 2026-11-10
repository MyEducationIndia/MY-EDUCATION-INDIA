"""
Module 20: Experience Platform Schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class RootOwnerLoginRequest(BaseModel):
    username: str
    passphrase: str

class RootOwnerOverview(BaseModel):
    owner_username: str
    emergency_lockdown_active: bool
    developer_mode_enabled: bool
    license_tier: str
    total_institutes_active: int
    total_modules_licensed: int

class PortalConfigResponse(BaseModel):
    portal_type: str
    display_title: str
    allowed_roles: List[str]
    default_route: str
    is_enabled: bool

class DynamicMenuItemCreate(BaseModel):
    label: str = Field(..., max_length=100)
    route_path: str = Field(..., max_length=200)
    icon_name: str = "Circle"
    order_index: int = 1
    required_permission: Optional[str] = None
    parent_item_id: Optional[str] = None

class DynamicMenuCreate(BaseModel):
    menu_key: str = Field(..., max_length=60)
    menu_name: str = Field(..., max_length=150)
    target_portal: str
    items: Optional[List[DynamicMenuItemCreate]] = None

class FormDefinitionCreate(BaseModel):
    form_key: str = Field(..., max_length=60)
    form_title: str = Field(..., max_length=200)
    target_module: str
    schema_fields_json: List[Dict[str, Any]]
    conditional_rules_json: Optional[List[Dict[str, Any]]] = None

class FormSubmissionRequest(BaseModel):
    form_id: str
    submission_data: Dict[str, Any]

class SupportTicketCreate(BaseModel):
    subject: str = Field(..., max_length=255)
    category: str = "SYSTEM_QUERY"
    priority: str = "MEDIUM"
    message_text: str

class GlobalSearchResult(BaseModel):
    module_name: str
    record_id: str
    title: str
    subtitle: Optional[str] = None
    target_route: str
