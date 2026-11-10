import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ----------------------------------------------------
# 1. Hero Slide Schemas
# ----------------------------------------------------
class CmsHeroSlideResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    badge_text: Optional[str] = None
    title: str
    subtitle: str
    background_image_url: Optional[str] = None
    video_url: Optional[str] = None
    primary_cta_text: str
    primary_cta_link: str
    secondary_cta_text: Optional[str] = None
    secondary_cta_link: Optional[str] = None
    display_order: int
    is_active: bool
    created_at: datetime


class CmsHeroSlideCreateRequest(BaseModel):
    badge_text: Optional[str] = Field(default=None, max_length=128)
    title: str = Field(..., min_length=2, max_length=255)
    subtitle: str = Field(..., min_length=2)
    background_image_url: Optional[str] = None
    video_url: Optional[str] = None
    primary_cta_text: str = Field(default="Apply Now", max_length=64)
    primary_cta_link: str = Field(default="/admissions/apply", max_length=255)
    secondary_cta_text: Optional[str] = Field(default=None, max_length=64)
    secondary_cta_link: Optional[str] = Field(default=None, max_length=255)
    display_order: int = 0
    is_active: bool = True


class CmsHeroSlideUpdateRequest(BaseModel):
    badge_text: Optional[str] = Field(default=None, max_length=128)
    title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    subtitle: Optional[str] = None
    background_image_url: Optional[str] = None
    video_url: Optional[str] = None
    primary_cta_text: Optional[str] = Field(default=None, max_length=64)
    primary_cta_link: Optional[str] = Field(default=None, max_length=255)
    secondary_cta_text: Optional[str] = Field(default=None, max_length=64)
    secondary_cta_link: Optional[str] = Field(default=None, max_length=255)
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 2. Stat Counter Schemas
# ----------------------------------------------------
class CmsStatCounterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    metric_value: str
    numeric_target: Optional[int] = None
    label: str
    subtext: Optional[str] = None
    icon_name: Optional[str] = None
    display_order: int
    is_active: bool


class CmsStatCounterCreateRequest(BaseModel):
    metric_value: str = Field(..., min_length=1, max_length=64)
    numeric_target: Optional[int] = None
    label: str = Field(..., min_length=2, max_length=128)
    subtext: Optional[str] = Field(default=None, max_length=255)
    icon_name: Optional[str] = Field(default=None, max_length=64)
    display_order: int = 0
    is_active: bool = True


class CmsStatCounterUpdateRequest(BaseModel):
    metric_value: Optional[str] = Field(default=None, min_length=1, max_length=64)
    numeric_target: Optional[int] = None
    label: Optional[str] = Field(default=None, min_length=2, max_length=128)
    subtext: Optional[str] = Field(default=None, max_length=255)
    icon_name: Optional[str] = Field(default=None, max_length=64)
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 3. Quick Link Schemas
# ----------------------------------------------------
class CmsQuickLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    title: str
    description: Optional[str] = None
    path: str
    icon_name: Optional[str] = None
    badge_label: Optional[str] = None
    is_external: bool
    display_order: int
    is_active: bool


class CmsQuickLinkCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=128)
    description: Optional[str] = Field(default=None, max_length=255)
    path: str = Field(..., min_length=1, max_length=255)
    icon_name: Optional[str] = Field(default=None, max_length=64)
    badge_label: Optional[str] = Field(default=None, max_length=32)
    is_external: bool = False
    display_order: int = 0
    is_active: bool = True


class CmsQuickLinkUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=128)
    description: Optional[str] = Field(default=None, max_length=255)
    path: Optional[str] = Field(default=None, min_length=1, max_length=255)
    icon_name: Optional[str] = Field(default=None, max_length=64)
    badge_label: Optional[str] = Field(default=None, max_length=32)
    is_external: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 4. Featured Program Schemas
# ----------------------------------------------------
class CmsFeaturedProgramResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    title: str
    code: str
    category: str
    degree_level: str
    duration: str
    annual_fee: Optional[str] = None
    eligibility_summary: str
    summary: str
    image_url: Optional[str] = None
    syllabus_url: Optional[str] = None
    is_admissions_open: bool
    display_order: int
    is_active: bool


class CmsFeaturedProgramCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    code: str = Field(..., min_length=2, max_length=32)
    category: str = Field(..., min_length=2, max_length=64)
    degree_level: str = Field(default="Undergraduate", max_length=32)
    duration: str = Field(default="4 Years (8 Semesters)", max_length=64)
    annual_fee: Optional[str] = Field(default=None, max_length=64)
    eligibility_summary: str = Field(default="10+2 with PCM >= 60%", max_length=255)
    summary: str = Field(..., min_length=5)
    image_url: Optional[str] = None
    syllabus_url: Optional[str] = None
    is_admissions_open: bool = True
    display_order: int = 0
    is_active: bool = True


class CmsFeaturedProgramUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    code: Optional[str] = Field(default=None, min_length=2, max_length=32)
    category: Optional[str] = Field(default=None, min_length=2, max_length=64)
    degree_level: Optional[str] = Field(default=None, max_length=32)
    duration: Optional[str] = Field(default=None, max_length=64)
    annual_fee: Optional[str] = Field(default=None, max_length=64)
    eligibility_summary: Optional[str] = Field(default=None, max_length=255)
    summary: Optional[str] = None
    image_url: Optional[str] = None
    syllabus_url: Optional[str] = None
    is_admissions_open: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 5. Corporate Recruiter Schemas
# ----------------------------------------------------
class CmsRecruiterLogoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    company_name: str
    tier: str
    highest_package_lpa: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    display_order: int
    is_active: bool


class CmsRecruiterLogoCreateRequest(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=128)
    tier: str = Field(default="Tier 1", max_length=32)
    highest_package_lpa: Optional[str] = Field(default=None, max_length=32)
    logo_url: Optional[str] = None
    website_url: Optional[str] = Field(default=None, max_length=500)
    display_order: int = 0
    is_active: bool = True


class CmsRecruiterLogoUpdateRequest(BaseModel):
    company_name: Optional[str] = Field(default=None, min_length=2, max_length=128)
    tier: Optional[str] = Field(default=None, max_length=32)
    highest_package_lpa: Optional[str] = Field(default=None, max_length=32)
    logo_url: Optional[str] = None
    website_url: Optional[str] = Field(default=None, max_length=500)
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 6. Testimonial Schemas
# ----------------------------------------------------
class CmsTestimonialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    author_name: str
    author_role: str
    author_category: str
    rating_stars: int
    quote: str
    avatar_url: Optional[str] = None
    video_url: Optional[str] = None
    display_order: int
    is_active: bool


class CmsTestimonialCreateRequest(BaseModel):
    author_name: str = Field(..., min_length=2, max_length=128)
    author_role: str = Field(..., min_length=2, max_length=128)
    author_category: str = Field(default="Student", max_length=32)
    rating_stars: int = Field(default=5, ge=1, le=5)
    quote: str = Field(..., min_length=5)
    avatar_url: Optional[str] = None
    video_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class CmsTestimonialUpdateRequest(BaseModel):
    author_name: Optional[str] = Field(default=None, min_length=2, max_length=128)
    author_role: Optional[str] = Field(default=None, min_length=2, max_length=128)
    author_category: Optional[str] = Field(default=None, max_length=32)
    rating_stars: Optional[int] = Field(default=None, ge=1, le=5)
    quote: Optional[str] = None
    avatar_url: Optional[str] = None
    video_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 7. Newsletter Subscription Schemas
# ----------------------------------------------------
class CmsNewsletterSubscribeRequest(BaseModel):
    email: EmailStr


class CmsNewsletterResponse(BaseModel):
    success: bool
    message: str


# ----------------------------------------------------
# 8. Public Home Page Master Bundle
# ----------------------------------------------------
class PublicHomePageBundle(BaseModel):
    hero_slides: List[CmsHeroSlideResponse]
    stat_counters: List[CmsStatCounterResponse]
    quick_links: List[CmsQuickLinkResponse]
    featured_programs: List[CmsFeaturedProgramResponse]
    recruiters: List[CmsRecruiterLogoResponse]
    testimonials: List[CmsTestimonialResponse]
