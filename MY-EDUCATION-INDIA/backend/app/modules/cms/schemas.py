import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==================== Page Builder Schemas ====================
class PageSectionBase(BaseModel):
    section_key: str = Field(..., min_length=2, max_length=80)
    block_type: str = Field(default="HERO")
    display_order: int = Field(default=0)
    is_visible: bool = True
    container_width: str = "BOXED"
    background_color: Optional[str] = None
    background_image_url: Optional[str] = None
    padding_top: int = 40
    padding_bottom: int = 40
    content_payload: Dict[str, Any] = Field(default_factory=dict)


class PageSectionResponse(PageSectionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    page_id: uuid.UUID


class PageCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    slug: str = Field(..., min_length=2, max_length=200, pattern=r"^[a-z0-9-]+$")
    summary: Optional[str] = None
    featured_image_url: Optional[str] = None
    status: str = "PUBLISHED"
    is_homepage: bool = False
    template_type: str = "DEFAULT"
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    institute_id: uuid.UUID
    sections: List[PageSectionBase] = Field(default_factory=list)


class PageUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    featured_image_url: Optional[str] = None
    status: Optional[str] = None
    is_homepage: Optional[bool] = None
    template_type: Optional[str] = None
    custom_css: Optional[str] = None
    custom_js: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    sections: Optional[List[PageSectionBase]] = None


class PageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    title: str
    slug: str
    summary: Optional[str] = None
    featured_image_url: Optional[str] = None
    status: str
    published_at: Optional[datetime] = None
    is_homepage: bool
    template_type: str
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    view_count: int
    version: int
    sections: List[PageSectionResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


# ==================== Menus Schemas ====================
class MenuItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    url: str = Field(..., min_length=1, max_length=255)
    target: str = "_self"
    icon_name: Optional[str] = None
    badge_label: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    parent_id: Optional[uuid.UUID] = None


class MenuItemResponse(MenuItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    menu_id: uuid.UUID
    children: List["MenuItemResponse"] = Field(default_factory=list)


class MenuResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    code: str
    name: str
    location: str
    is_active: bool
    items: List[MenuItemResponse] = Field(default_factory=list)


# ==================== Media Library ====================
class MediaAssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    folder_path: str
    filename: str
    original_filename: str
    file_type: str
    mime_type: str
    file_size_bytes: int
    url: str
    thumbnail_url: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    created_at: datetime


# ==================== Banners Schemas ====================
class BannerCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    subtitle: Optional[str] = None
    banner_type: str = "DESKTOP"
    image_url: str
    mobile_image_url: Optional[str] = None
    cta_text: Optional[str] = None
    cta_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    institute_id: uuid.UUID


class BannerResponse(BannerCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# ==================== News & Blog Schemas ====================
class NewsCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    slug: str = Field(..., min_length=3, max_length=255, pattern=r"^[a-z0-9-]+$")
    content: str
    excerpt: Optional[str] = None
    author_name: str = "Editorial Team"
    featured_image_url: Optional[str] = None
    is_featured: bool = False
    is_trending: bool = False
    status: str = "PUBLISHED"
    institute_id: uuid.UUID


class NewsResponse(NewsCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    published_at: datetime
    view_count: int


# ==================== Downloads Schemas ====================
class DownloadCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    resource_type: str = "BROCHURE"
    file_url: str
    file_size_formatted: str = "1.5 MB"
    is_active: bool = True
    institute_id: uuid.UUID


class DownloadResponse(DownloadCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    download_count: int
    created_at: datetime


# ==================== Testimonials Schemas ====================
class TestimonialCreate(BaseModel):
    author_name: str = Field(..., min_length=2, max_length=120)
    author_role: str = "Student"
    avatar_url: Optional[str] = None
    content: str
    rating_stars: int = Field(default=5, ge=1, le=5)
    company_or_course: Optional[str] = None
    is_approved: bool = True
    display_order: int = 0
    institute_id: uuid.UUID


class TestimonialResponse(TestimonialCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# ==================== Enquiries Schemas ====================
class EnquiryCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone_number: str = Field(..., min_length=8, max_length=32)
    enquiry_type: str = "ADMISSION"
    course_interested: Optional[str] = None
    message: str = Field(..., min_length=5)
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None


class EnquiryResponse(EnquiryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    created_at: datetime


# ==================== Website Settings ====================
class WebsiteSettingsUpdate(BaseModel):
    website_title: Optional[str] = None
    tagline: Optional[str] = None
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    whatsapp_number: Optional[str] = None
    address_display: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None
    footer_text: Optional[str] = None
    analytics_tracking_code: Optional[str] = None


class WebsiteSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    website_title: str
    tagline: str
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    primary_color: str
    secondary_color: str
    contact_phone: str
    contact_email: str
    whatsapp_number: Optional[str] = None
    address_display: str
    social_links: Dict[str, str]
    footer_text: str
    analytics_tracking_code: Optional[str] = None
