import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# -----------------------------------------------------------------------------
# 1. Course Category Schemas
# -----------------------------------------------------------------------------
class CmsCourseCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    name: str
    slug: str
    description: Optional[str] = None
    icon_name: Optional[str] = "BookOpen"
    display_order: int
    is_active: bool
    created_at: datetime


class CmsCourseCategoryCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    slug: str = Field(..., min_length=2, max_length=128)
    description: Optional[str] = None
    icon_name: Optional[str] = Field(default="BookOpen", max_length=64)
    display_order: int = 0
    is_active: bool = True


class CmsCourseCategoryUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=128)
    slug: Optional[str] = Field(default=None, min_length=2, max_length=128)
    description: Optional[str] = None
    icon_name: Optional[str] = Field(default=None, max_length=64)
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# -----------------------------------------------------------------------------
# 2. Curriculum & Faculty Schemas
# -----------------------------------------------------------------------------
class CmsCourseCurriculumResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    course_id: uuid.UUID
    semester_number: int
    semester_title: str
    credits: int
    subjects: List[Dict[str, Any]] = []
    display_order: int
    created_at: datetime


class CmsCourseCurriculumCreateRequest(BaseModel):
    semester_number: int = Field(..., ge=1, le=12)
    semester_title: str = Field(..., min_length=2, max_length=128)
    credits: int = Field(default=24, ge=1, le=40)
    subjects: List[Dict[str, Any]] = Field(default_factory=list)
    display_order: int = 0


class CmsCourseFacultyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    course_id: uuid.UUID
    faculty_name: str
    designation: str
    qualifications: str
    specialization: str
    avatar_url: Optional[str] = None
    display_order: int
    created_at: datetime


class CmsCourseFacultyCreateRequest(BaseModel):
    faculty_name: str = Field(..., min_length=2, max_length=128)
    designation: str = Field(..., min_length=2, max_length=128)
    qualifications: str = Field(..., min_length=2, max_length=255)
    specialization: str = Field(..., min_length=2, max_length=255)
    avatar_url: Optional[str] = None
    display_order: int = 0


# -----------------------------------------------------------------------------
# 3. Course Summary & Detail Schemas
# -----------------------------------------------------------------------------
class CmsCourseSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    category_id: uuid.UUID
    code: str
    slug: str
    title: str
    short_name: str
    degree_level: str
    duration: str
    study_mode: str
    annual_fee: str
    total_fee: Optional[str] = None
    seats_intake: int
    eligibility_summary: str
    summary: str
    image_url: Optional[str] = None
    is_admissions_open: bool
    is_featured: bool
    display_order: int
    is_active: bool
    created_at: datetime


class CmsCourseDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    category_id: uuid.UUID
    category: Optional[CmsCourseCategoryResponse] = None
    code: str
    slug: str
    title: str
    short_name: str
    degree_level: str
    duration: str
    study_mode: str
    annual_fee: str
    total_fee: Optional[str] = None
    seats_intake: int
    eligibility_summary: str
    admission_process: str
    career_prospects: str
    summary: str
    overview: str
    image_url: Optional[str] = None
    brochure_pdf_url: Optional[str] = None
    syllabus_pdf_url: Optional[str] = None
    is_admissions_open: bool
    is_featured: bool
    display_order: int
    is_active: bool
    created_at: datetime
    curricula: List[CmsCourseCurriculumResponse] = []
    faculty_members: List[CmsCourseFacultyResponse] = []


class CmsCourseCreateRequest(BaseModel):
    category_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    slug: str = Field(..., min_length=2, max_length=128)
    title: str = Field(..., min_length=2, max_length=255)
    short_name: str = Field(..., min_length=2, max_length=64)
    degree_level: str = Field(..., min_length=2, max_length=64)
    duration: str = Field(..., min_length=2, max_length=64)
    study_mode: str = Field(default="Full-Time On-Campus", max_length=64)
    annual_fee: str = Field(..., min_length=2, max_length=64)
    total_fee: Optional[str] = Field(default=None, max_length=64)
    seats_intake: int = Field(default=60, ge=1)
    eligibility_summary: str = Field(..., min_length=5)
    admission_process: str = Field(..., min_length=5)
    career_prospects: str = Field(..., min_length=5)
    summary: str = Field(..., min_length=5)
    overview: str = Field(..., min_length=10)
    image_url: Optional[str] = None
    brochure_pdf_url: Optional[str] = None
    syllabus_pdf_url: Optional[str] = None
    is_admissions_open: bool = True
    is_featured: bool = False
    display_order: int = 0
    is_active: bool = True


class CmsCourseUpdateRequest(BaseModel):
    category_id: Optional[uuid.UUID] = None
    code: Optional[str] = Field(default=None, min_length=2, max_length=32)
    slug: Optional[str] = Field(default=None, min_length=2, max_length=128)
    title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    short_name: Optional[str] = Field(default=None, min_length=2, max_length=64)
    degree_level: Optional[str] = Field(default=None, min_length=2, max_length=64)
    duration: Optional[str] = Field(default=None, min_length=2, max_length=64)
    study_mode: Optional[str] = Field(default=None, max_length=64)
    annual_fee: Optional[str] = Field(default=None, min_length=2, max_length=64)
    total_fee: Optional[str] = Field(default=None, max_length=64)
    seats_intake: Optional[int] = Field(default=None, ge=1)
    eligibility_summary: Optional[str] = None
    admission_process: Optional[str] = None
    career_prospects: Optional[str] = None
    summary: Optional[str] = None
    overview: Optional[str] = None
    image_url: Optional[str] = None
    brochure_pdf_url: Optional[str] = None
    syllabus_pdf_url: Optional[str] = None
    is_admissions_open: Optional[bool] = None
    is_featured: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# -----------------------------------------------------------------------------
# 4. Public Courses Master Bundle Schema
# -----------------------------------------------------------------------------
class PublicCoursesBundle(BaseModel):
    categories: List[CmsCourseCategoryResponse]
    courses: List[CmsCourseSummaryResponse]
    featured_courses: List[CmsCourseSummaryResponse]
    total_courses: int
