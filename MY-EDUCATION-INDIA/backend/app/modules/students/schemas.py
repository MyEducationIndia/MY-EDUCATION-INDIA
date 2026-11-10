import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==================== Student Core & Profile ====================
class StudentProfileData(BaseModel):
    aadhaar_number: Optional[str] = None
    pan_number: Optional[str] = None
    apaar_id: Optional[str] = None
    abc_account_id: Optional[str] = None
    religion: Optional[str] = None
    caste_category: Optional[str] = "GENERAL"
    nationality: str = "Indian"
    mother_tongue: Optional[str] = "Hindi"
    previous_school: Optional[str] = None
    previous_qualification: Optional[str] = None
    previous_marks_percentage: Optional[float] = None


class StudentAddressData(BaseModel):
    address_type: str = "PERMANENT"
    address_line1: str = Field(..., min_length=3, max_length=255)
    address_line2: Optional[str] = None
    city: str = Field(..., min_length=2, max_length=100)
    district: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=4, max_length=20)
    country: str = "India"
    is_primary: bool = True


class StudentGuardianData(BaseModel):
    relationship_type: str = "FATHER"
    full_name: str = Field(..., min_length=2, max_length=150)
    mobile_number: str = Field(..., min_length=8, max_length=24)
    email: Optional[EmailStr] = None
    occupation: Optional[str] = None
    annual_income: Optional[float] = None
    is_emergency_contact: bool = True


class StudentMedicalData(BaseModel):
    blood_group: Optional[str] = "O+"
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    emergency_doctor_name: Optional[str] = None
    emergency_doctor_phone: Optional[str] = None


class StudentRegisterRequest(BaseModel):
    institute_id: uuid.UUID
    branch_id: uuid.UUID
    first_name: str = Field(..., min_length=2, max_length=100)
    middle_name: Optional[str] = None
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=8, max_length=24)
    date_of_birth: date
    gender: str = Field(..., pattern=r"^(MALE|FEMALE|OTHER)$")
    course_name: str = Field(..., min_length=2, max_length=150)
    batch_name: str = Field(..., min_length=2, max_length=100)
    academic_year_code: str = Field(..., min_length=4, max_length=32)
    admission_date: date = Field(default_factory=date.today)
    semester_or_year: int = 1
    photo_url: Optional[str] = None

    profile: Optional[StudentProfileData] = None
    addresses: List[StudentAddressData] = Field(default_factory=list)
    guardians: List[StudentGuardianData] = Field(default_factory=list)
    medical: Optional[StudentMedicalData] = None
    custom_fields: Dict[str, str] = Field(default_factory=dict)


class StudentUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    course_name: Optional[str] = None
    batch_name: Optional[str] = None
    semester_or_year: Optional[int] = None
    status: Optional[str] = None


class StudentDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    document_type: str
    document_title: str
    file_url: str
    mime_type: str
    file_size_bytes: int
    is_verified: bool
    created_at: datetime


class StudentTimelineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    event_category: str
    event_title: str
    event_description: str
    recorded_by: str
    occurred_at: datetime
    meta_payload: Dict[str, Any]


class StudentSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    registration_number: str
    enrollment_number: Optional[str] = None
    roll_number: Optional[str] = None
    erp_id: Optional[str] = None
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    gender: str
    course_name: str
    batch_name: str
    academic_year_code: str
    status: str
    photo_url: Optional[str] = None
    admission_date: date
    created_at: datetime


class StudentDetailedProfileResponse(StudentSummaryResponse):
    profile: Optional[StudentProfileData] = None
    addresses: List[StudentAddressData] = Field(default_factory=list)
    guardians: List[StudentGuardianData] = Field(default_factory=list)
    medical: Optional[StudentMedicalData] = None
    documents: List[StudentDocumentResponse] = Field(default_factory=list)
    timeline: List[StudentTimelineResponse] = Field(default_factory=list)
    custom_values: Dict[str, str] = Field(default_factory=dict)
    qr_svg: Optional[str] = None


class StudentSearchQuery(BaseModel):
    query: Optional[str] = None
    course_name: Optional[str] = None
    batch_name: Optional[str] = None
    status: Optional[str] = None
    branch_id: Optional[uuid.UUID] = None
    academic_year_code: Optional[str] = None
    page: int = 1
    page_size: int = 20


class StudentStatusChangeRequest(BaseModel):
    new_status: str = Field(..., pattern=r"^(ACTIVE|INACTIVE|PENDING_ADMISSION|TRANSFERRED|SUSPENDED|PASSED|DROPPED|ALUMNI|ARCHIVED)$")
    reason: Optional[str] = None


class StudentPromotionRequest(BaseModel):
    student_ids: List[uuid.UUID]
    target_course_name: Optional[str] = None
    target_batch_name: Optional[str] = None
    target_semester_or_year: int
    target_academic_year_code: str


class StudentBulkDeleteRequest(BaseModel):
    student_ids: List[uuid.UUID]


class StudentCustomFieldCreate(BaseModel):
    field_key: str = Field(..., min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    field_label: str = Field(..., min_length=2, max_length=120)
    field_type: str = "TEXT"
    is_required: bool = False
    display_order: int = 0
    options_list: List[str] = Field(default_factory=list)
    institute_id: uuid.UUID


class StudentCustomFieldResponse(StudentCustomFieldCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
