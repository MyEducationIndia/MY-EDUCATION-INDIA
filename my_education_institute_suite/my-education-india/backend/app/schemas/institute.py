import uuid
from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ModuleConfigResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    module_key: str
    display_name: str
    category: str
    subdomain: str
    description: str
    is_enabled: bool
    is_core_locked: bool
    configuration: Dict[str, Any]
    updated_at: datetime


class ModuleToggleRequest(BaseModel):
    is_enabled: bool
    configuration: Dict[str, Any] | None = None


class InstituteCreateRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=32, pattern=r"^[A-Z0-9_-]+$")
    name: str = Field(..., min_length=3, max_length=255)
    tagline: str | None = Field(default=None, max_length=500)
    affiliation_number: str | None = Field(default=None, max_length=128)
    official_email: EmailStr
    official_phone: str = Field(..., min_length=10, max_length=24)
    website_domain: str | None = Field(default=None, max_length=255)
    address_line1: str = Field(..., min_length=3, max_length=255)
    address_line2: str | None = Field(default=None, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=4, max_length=20)
    country: str = Field(default="India", max_length=100)
    logo_url: str | None = None
    favicon_url: str | None = None
    primary_color_hex: str = Field(default="#1E40AF", pattern=r"^#[0-9A-Fa-f]{6}$")
    secondary_color_hex: str = Field(default="#0D9488", pattern=r"^#[0-9A-Fa-f]{6}$")
    seo_metadata: Dict[str, Any] = Field(default_factory=dict)


class InstituteBrandingUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=255)
    tagline: str | None = Field(default=None, max_length=500)
    official_email: EmailStr | None = None
    official_phone: str | None = Field(default=None, min_length=10, max_length=24)
    logo_url: str | None = None
    favicon_url: str | None = None
    primary_color_hex: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    secondary_color_hex: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    seo_metadata: Dict[str, Any] | None = None
    communication_settings: Dict[str, Any] | None = None


class InstituteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    tagline: str | None
    affiliation_number: str | None
    official_email: EmailStr
    official_phone: str
    website_domain: str | None
    address_line1: str
    address_line2: str | None
    city: str
    state: str
    postal_code: str
    country: str
    logo_url: str | None
    favicon_url: str | None
    primary_color_hex: str
    secondary_color_hex: str
    seo_metadata: Dict[str, Any]
    is_active: bool
    module_configs: List[ModuleConfigResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
