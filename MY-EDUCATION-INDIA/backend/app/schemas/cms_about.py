import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ----------------------------------------------------
# 1. Milestone Timeline Schemas
# ----------------------------------------------------
class CmsMilestoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    year: str
    title: str
    description: str
    image_url: Optional[str] = None
    icon_name: Optional[str] = None
    display_order: int
    is_active: bool
    created_at: datetime


class CmsMilestoneCreateRequest(BaseModel):
    year: str = Field(..., min_length=2, max_length=16)
    title: str = Field(..., min_length=2, max_length=255)
    description: str = Field(..., min_length=5)
    image_url: Optional[str] = None
    icon_name: Optional[str] = Field(default=None, max_length=64)
    display_order: int = 0
    is_active: bool = True


class CmsMilestoneUpdateRequest(BaseModel):
    year: Optional[str] = Field(default=None, min_length=2, max_length=16)
    title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = None
    icon_name: Optional[str] = Field(default=None, max_length=64)
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 2. Leadership Messages Schemas
# ----------------------------------------------------
class CmsLeadershipMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    leader_name: str
    leader_designation: str
    role_category: str
    salutation_title: str
    message_body: str
    portrait_image_url: Optional[str] = None
    signature_image_url: Optional[str] = None
    video_address_url: Optional[str] = None
    display_order: int
    is_active: bool
    created_at: datetime


class CmsLeadershipMessageCreateRequest(BaseModel):
    leader_name: str = Field(..., min_length=2, max_length=128)
    leader_designation: str = Field(..., min_length=2, max_length=128)
    role_category: str = Field(..., min_length=2, max_length=64) # CHAIRMAN, DIRECTOR, PRINCIPAL, DEAN
    salutation_title: str = Field(..., min_length=2, max_length=255)
    message_body: str = Field(..., min_length=10)
    portrait_image_url: Optional[str] = None
    signature_image_url: Optional[str] = None
    video_address_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class CmsLeadershipMessageUpdateRequest(BaseModel):
    leader_name: Optional[str] = Field(default=None, min_length=2, max_length=128)
    leader_designation: Optional[str] = Field(default=None, min_length=2, max_length=128)
    role_category: Optional[str] = Field(default=None, min_length=2, max_length=64)
    salutation_title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    message_body: Optional[str] = None
    portrait_image_url: Optional[str] = None
    signature_image_url: Optional[str] = None
    video_address_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 3. Accreditations Schemas
# ----------------------------------------------------
class CmsAccreditationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    accrediting_body: str
    title: str
    approval_reference_number: str
    valid_from: Optional[str] = None
    valid_upto: Optional[str] = None
    certificate_pdf_url: Optional[str] = None
    logo_badge_url: Optional[str] = None
    display_order: int
    is_active: bool
    created_at: datetime


class CmsAccreditationCreateRequest(BaseModel):
    accrediting_body: str = Field(..., min_length=2, max_length=128)
    title: str = Field(..., min_length=2, max_length=255)
    approval_reference_number: str = Field(..., min_length=2, max_length=128)
    valid_from: Optional[str] = Field(default=None, max_length=32)
    valid_upto: Optional[str] = Field(default=None, max_length=32)
    certificate_pdf_url: Optional[str] = None
    logo_badge_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class CmsAccreditationUpdateRequest(BaseModel):
    accrediting_body: Optional[str] = Field(default=None, min_length=2, max_length=128)
    title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    approval_reference_number: Optional[str] = Field(default=None, min_length=2, max_length=128)
    valid_from: Optional[str] = Field(default=None, max_length=32)
    valid_upto: Optional[str] = Field(default=None, max_length=32)
    certificate_pdf_url: Optional[str] = None
    logo_badge_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 4. Campus Infrastructure Schemas
# ----------------------------------------------------
class CmsCampusInfrastructureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    facility_name: str
    category: str
    capacity_metric: str
    description: str
    image_url: Optional[str] = None
    floor_or_location: Optional[str] = None
    display_order: int
    is_active: bool
    created_at: datetime


class CmsCampusInfrastructureCreateRequest(BaseModel):
    facility_name: str = Field(..., min_length=2, max_length=128)
    category: str = Field(..., min_length=2, max_length=64)
    capacity_metric: str = Field(..., min_length=1, max_length=64)
    description: str = Field(..., min_length=5)
    image_url: Optional[str] = None
    floor_or_location: Optional[str] = Field(default=None, max_length=128)
    display_order: int = 0
    is_active: bool = True


class CmsCampusInfrastructureUpdateRequest(BaseModel):
    facility_name: Optional[str] = Field(default=None, min_length=2, max_length=128)
    category: Optional[str] = Field(default=None, min_length=2, max_length=64)
    capacity_metric: Optional[str] = Field(default=None, min_length=1, max_length=64)
    description: Optional[str] = None
    image_url: Optional[str] = None
    floor_or_location: Optional[str] = Field(default=None, max_length=128)
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# ----------------------------------------------------
# 5. Public Master About Bundle Schema
# ----------------------------------------------------
class PublicAboutInstituteBundle(BaseModel):
    milestones: List[CmsMilestoneResponse]
    leadership_messages: List[CmsLeadershipMessageResponse]
    accreditations: List[CmsAccreditationResponse]
    infrastructure: List[CmsCampusInfrastructureResponse]
