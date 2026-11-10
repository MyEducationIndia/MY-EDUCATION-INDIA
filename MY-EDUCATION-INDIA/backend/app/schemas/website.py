import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ----------------------------------------------------
# 1. Website Settings Schemas
# ----------------------------------------------------
class WebsiteSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    site_title: str
    tagline: str
    header_logo_url: Optional[str] = None
    footer_logo_url: Optional[str] = None
    favicon_url: Optional[str] = None

    header_is_sticky: bool
    header_show_search: bool
    header_show_login: bool
    header_login_button_text: str
    header_login_route: str

    contact_phone: str
    contact_email: str
    contact_address: str

    meta_description: str
    meta_keywords: str
    og_image_url: Optional[str] = None
    google_analytics_id: Optional[str] = None

    is_maintenance_mode: bool
    maintenance_message: Optional[str] = None
    custom_css: Optional[str] = None
    custom_head_scripts: Optional[str] = None
    updated_at: datetime


class WebsiteSettingsUpdateRequest(BaseModel):
    site_title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    tagline: Optional[str] = Field(default=None, max_length=500)
    header_logo_url: Optional[str] = None
    footer_logo_url: Optional[str] = None
    favicon_url: Optional[str] = None

    header_is_sticky: Optional[bool] = None
    header_show_search: Optional[bool] = None
    header_show_login: Optional[bool] = None
    header_login_button_text: Optional[str] = Field(default=None, max_length=64)
    header_login_route: Optional[str] = Field(default=None, max_length=128)

    contact_phone: Optional[str] = Field(default=None, max_length=64)
    contact_email: Optional[str] = Field(default=None, max_length=255)
    contact_address: Optional[str] = Field(default=None, max_length=500)

    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_image_url: Optional[str] = None
    google_analytics_id: Optional[str] = None

    is_maintenance_mode: Optional[bool] = None
    maintenance_message: Optional[str] = None
    custom_css: Optional[str] = None
    custom_head_scripts: Optional[str] = None


# ----------------------------------------------------
# 2. Website Theme Schemas
# ----------------------------------------------------
class WebsiteThemeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    primary_color: str
    secondary_color: str
    accent_color: str
    background_color: str
    surface_color: str
    text_primary_color: str
    text_secondary_color: str

    font_family: str
    heading_font_family: str
    border_radius: str
    button_style: str
    shadow_style: str
    animation_enabled: bool
    updated_at: datetime


class WebsiteThemeUpdateRequest(BaseModel):
    primary_color: Optional[str] = Field(default=None, max_length=32)
    secondary_color: Optional[str] = Field(default=None, max_length=32)
    accent_color: Optional[str] = Field(default=None, max_length=32)
    background_color: Optional[str] = Field(default=None, max_length=32)
    surface_color: Optional[str] = Field(default=None, max_length=32)
    text_primary_color: Optional[str] = Field(default=None, max_length=32)
    text_secondary_color: Optional[str] = Field(default=None, max_length=32)

    font_family: Optional[str] = Field(default=None, max_length=64)
    heading_font_family: Optional[str] = Field(default=None, max_length=64)
    border_radius: Optional[str] = Field(default=None, max_length=32)
    button_style: Optional[str] = Field(default=None, max_length=32)
    shadow_style: Optional[str] = Field(default=None, max_length=32)
    animation_enabled: Optional[bool] = None


# ----------------------------------------------------
# 3. Live Update Ticker Schemas
# ----------------------------------------------------
class WebsiteTickerItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    title: str
    category: str
    link_url: Optional[str] = None
    is_external: bool
    open_new_tab: bool
    is_emergency: bool
    priority_level: int
    publish_at: datetime
    expire_at: Optional[datetime] = None
    is_active: bool
    display_order: int
    created_at: datetime


class WebsiteTickerItemCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=500)
    category: str = Field(default="Important Notice", max_length=64)
    link_url: Optional[str] = Field(default=None, max_length=500)
    is_external: bool = False
    open_new_tab: bool = False
    is_emergency: bool = False
    priority_level: int = Field(default=1, ge=1, le=5)
    publish_at: Optional[datetime] = None
    expire_at: Optional[datetime] = None
    display_order: int = 0
    is_active: bool = True


class WebsiteTickerItemUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=500)
    category: Optional[str] = Field(default=None, max_length=64)
    link_url: Optional[str] = Field(default=None, max_length=500)
    is_external: Optional[bool] = None
    open_new_tab: Optional[bool] = None
    is_emergency: Optional[bool] = None
    priority_level: Optional[int] = Field(default=None, ge=1, le=5)
    publish_at: Optional[datetime] = None
    expire_at: Optional[datetime] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 4. Navigation Menu Schemas
# ----------------------------------------------------
class NavigationMenuItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    menu_location: str
    title: str
    path: str
    icon_name: Optional[str] = None
    badge_text: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None
    is_external: bool
    open_new_tab: bool
    is_mega_menu: bool
    display_order: int
    is_active: bool
    children: List["NavigationMenuItemResponse"] = []


class NavigationMenuCreateRequest(BaseModel):
    menu_location: str = Field(default="HEADER_MAIN", max_length=64)
    title: str = Field(..., min_length=1, max_length=128)
    path: str = Field(..., max_length=255)
    icon_name: Optional[str] = Field(default=None, max_length=64)
    badge_text: Optional[str] = Field(default=None, max_length=32)
    description: Optional[str] = Field(default=None, max_length=255)
    category: Optional[str] = Field(default=None, max_length=64)
    parent_id: Optional[uuid.UUID] = None
    is_external: bool = False
    open_new_tab: bool = False
    is_mega_menu: bool = False
    display_order: int = 0
    is_active: bool = True


class NavigationMenuUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=128)
    path: Optional[str] = Field(default=None, max_length=255)
    icon_name: Optional[str] = Field(default=None, max_length=64)
    badge_text: Optional[str] = Field(default=None, max_length=32)
    description: Optional[str] = Field(default=None, max_length=255)
    category: Optional[str] = Field(default=None, max_length=64)
    parent_id: Optional[uuid.UUID] = None
    is_external: Optional[bool] = None
    open_new_tab: Optional[bool] = None
    is_mega_menu: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None



# ----------------------------------------------------
# 4B. Quick Link Schemas
# ----------------------------------------------------
class WebsiteQuickLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    title: str
    path: str
    icon_name: Optional[str] = None
    badge_text: Optional[str] = None
    target_type: str
    is_highlighted: bool
    display_order: int
    is_active: bool


class WebsiteQuickLinkCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    path: str = Field(..., max_length=255)
    icon_name: Optional[str] = Field(default=None, max_length=64)
    badge_text: Optional[str] = Field(default=None, max_length=32)
    target_type: str = Field(default="INTERNAL", max_length=32)
    is_highlighted: bool = False
    display_order: int = 0
    is_active: bool = True


class WebsiteQuickLinkUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=128)
    path: Optional[str] = Field(default=None, max_length=255)
    icon_name: Optional[str] = Field(default=None, max_length=64)
    badge_text: Optional[str] = Field(default=None, max_length=32)
    target_type: Optional[str] = Field(default=None, max_length=32)
    is_highlighted: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

# ----------------------------------------------------
# 5. Social Link Schemas
# ----------------------------------------------------
class WebsiteSocialLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    platform: str
    url: str
    display_order: int
    is_active: bool


class WebsiteSocialLinkCreateRequest(BaseModel):
    platform: str = Field(..., min_length=2, max_length=64)
    url: str = Field(..., min_length=5, max_length=500)
    display_order: int = 0
    is_active: bool = True


# ----------------------------------------------------
# 6. Global Search Schemas
# ----------------------------------------------------
class SearchResultItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    entity_type: str
    category: str = "GENERAL"
    title: str
    summary: str
    target_url: str
    badge_text: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class SearchSuggestionItem(BaseModel):
    title: str
    category: str
    target_url: str
    entity_type: str
    badge_text: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    category_filter: Optional[str] = None
    total_results: int
    results: List[SearchResultItem]
    category_counts: Dict[str, int] = {}


class SitemapItem(BaseModel):
    loc: str
    lastmod: Optional[str] = None
    changefreq: str = "weekly"
    priority: float = 0.7
    title: str
    category: str = "PAGE"


class SitemapResponse(BaseModel):
    generated_at: datetime
    total_urls: int
    urls: List[SitemapItem]


class SearchAnalyticsSummary(BaseModel):
    total_searches: int
    top_queries: List[Dict[str, Any]]
    zero_result_queries: List[Dict[str, Any]]
    category_distribution: Dict[str, int]


# ----------------------------------------------------
# 7. Public Website Master Bundle Schema
# ----------------------------------------------------
class PublicWebsiteFrameworkBundle(BaseModel):
    settings: WebsiteSettingsResponse
    theme: WebsiteThemeResponse
    header_navigation: List[NavigationMenuItemResponse]
    ticker_announcements: List[WebsiteTickerItemResponse]
    social_links: List[WebsiteSocialLinkResponse]
    quick_links: List[WebsiteQuickLinkResponse] = []
