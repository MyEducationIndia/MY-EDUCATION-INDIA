import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
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


class AcademicSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    session_code: str
    session_name: str
    start_date: date
    end_date: date
    is_current: bool
    is_admission_open: bool
    term_structure: str
    terms_count: int
    status: str
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class AcademicSessionCreateRequest(BaseModel):
    session_code: str = Field(..., min_length=2, max_length=32, pattern=r"^[A-Z0-9_-]+$")
    session_name: str = Field(..., min_length=3, max_length=100)
    start_date: date
    end_date: date
    is_current: bool = False
    is_admission_open: bool = True
    term_structure: str = Field(default="SEMESTER", max_length=32)
    terms_count: int = Field(default=2, ge=1, le=12)
    status: str = Field(default="ACTIVE", max_length=32)
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class AcademicSessionUpdateRequest(BaseModel):
    session_name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    is_admission_open: Optional[bool] = None
    term_structure: Optional[str] = Field(default=None, max_length=32)
    terms_count: Optional[int] = Field(default=None, ge=1, le=12)
    status: Optional[str] = Field(default=None, max_length=32)
    metadata_json: Optional[Dict[str, Any]] = None


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


class InstituteProfileUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=255)
    tagline: Optional[str] = Field(default=None, max_length=500)
    affiliation_number: Optional[str] = Field(default=None, max_length=128)
    official_email: Optional[EmailStr] = None
    official_phone: Optional[str] = Field(default=None, min_length=10, max_length=24)
    website_domain: Optional[str] = Field(default=None, max_length=255)
    address_line1: Optional[str] = Field(default=None, min_length=3, max_length=255)
    address_line2: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, min_length=2, max_length=100)
    state: Optional[str] = Field(default=None, min_length=2, max_length=100)
    postal_code: Optional[str] = Field(default=None, min_length=4, max_length=20)
    country: Optional[str] = Field(default=None, max_length=100)
    time_zone: Optional[str] = Field(default=None, max_length=64)
    default_language: Optional[str] = Field(default=None, max_length=16)
    currency_code: Optional[str] = Field(default=None, max_length=10)
    currency_symbol: Optional[str] = Field(default=None, max_length=10)
    current_academic_year: Optional[str] = Field(default=None, max_length=64)
    custom_domain: Optional[str] = Field(default=None, max_length=255)
    custom_domain_status: Optional[str] = Field(default=None, max_length=32)
    google_maps_embed_url: Optional[str] = None
    google_maps_latitude: Optional[float] = None
    google_maps_longitude: Optional[float] = None


class InstituteIntegrationsUpdateRequest(BaseModel):
    smtp_config: Optional[Dict[str, Any]] = None
    sms_gateway_config: Optional[Dict[str, Any]] = None
    whatsapp_gateway_config: Optional[Dict[str, Any]] = None
    payment_gateway_config: Optional[Dict[str, Any]] = None
    social_media_links: Optional[Dict[str, Any]] = None
    theme_config: Optional[Dict[str, Any]] = None


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
    time_zone: str = "Asia/Kolkata"
    default_language: str = "en-IN"
    currency_code: str = "INR"
    currency_symbol: str = "₹"
    current_academic_year: str = "2026-2027"
    custom_domain: str | None = None
    custom_domain_status: str = "ACTIVE"
    google_maps_embed_url: str | None = None
    google_maps_latitude: float | None = None
    google_maps_longitude: float | None = None
    social_media_links: Dict[str, Any] = Field(default_factory=dict)
    smtp_config: Dict[str, Any] = Field(default_factory=dict)
    sms_gateway_config: Dict[str, Any] = Field(default_factory=dict)
    whatsapp_gateway_config: Dict[str, Any] = Field(default_factory=dict)
    payment_gateway_config: Dict[str, Any] = Field(default_factory=dict)
    theme_config: Dict[str, Any] = Field(default_factory=dict)
    seo_metadata: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool
    module_configs: List[ModuleConfigResponse] = Field(default_factory=list)
    academic_sessions: List[AcademicSessionResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class InstituteSetupBundleResponse(BaseModel):
    institute: InstituteResponse
    current_session: Optional[AcademicSessionResponse] = None
    all_sessions: List[AcademicSessionResponse] = Field(default_factory=list)
    module_configs: List[ModuleConfigResponse] = Field(default_factory=list)
    system_status: Dict[str, Any] = Field(default_factory=dict)
