import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==================== Lead & CRM ====================
class LeadCreateRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    phone_number: str = Field(..., min_length=8, max_length=24)
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    state: Optional[str] = None
    source_channel: str = "WEBSITE"
    interested_course: Optional[str] = None
    preferred_batch: Optional[str] = None
    priority: str = "HOT"
    assigned_counsellor_id: Optional[uuid.UUID] = None
    estimated_budget: Optional[float] = None
    remarks: Optional[str] = None
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None


class LeadFollowupRequest(BaseModel):
    channel: str = "CALL"
    discussion_notes: str = Field(..., min_length=3)
    outcome: str = "INTERESTED"
    scheduled_next_at: Optional[datetime] = None


class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_number: str
    full_name: str
    phone_number: str
    email: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    source_channel: str
    interested_course: Optional[str] = None
    priority: str
    status: str
    score: int
    assigned_counsellor_id: Optional[uuid.UUID] = None
    next_followup_at: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: datetime


# ==================== Application Schemas ====================
class ApplicationCreateRequest(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    middle_name: Optional[str] = None
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=8, max_length=24)
    date_of_birth: date
    gender: str = "MALE"
    category: str = "GENERAL"
    course_name: str = Field(..., min_length=2, max_length=150)
    batch_preference: str = "2026-Batch-A"
    academic_year_code: str = "2026-2027"
    guardian_name: str = Field(..., min_length=2, max_length=150)
    guardian_phone: str = Field(..., min_length=8, max_length=24)
    guardian_relation: str = "FATHER"
    address_line1: str = Field(..., min_length=3, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=4, max_length=20)
    previous_institution: Optional[str] = None
    previous_marks_percentage: Optional[float] = None
    application_mode: str = "ONLINE"
    custom_form_data: Dict[str, Any] = Field(default_factory=dict)
    institute_id: uuid.UUID
    branch_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None


class DocumentVerifyRequest(BaseModel):
    document_id: uuid.UUID
    verification_status: str = Field(..., pattern=r"^(VERIFIED|REJECTED|CORRECTION_REQUIRED)$")
    remarks: Optional[str] = None


class AdmissionApproveRequest(BaseModel):
    application_id: uuid.UUID
    allocated_batch: str = "2026-Batch-A"
    remarks: Optional[str] = None


class AdmissionRejectRequest(BaseModel):
    application_id: uuid.UUID
    rejection_reason: str = Field(..., min_length=5)


class AdmissionFeeCollectRequest(BaseModel):
    application_id: uuid.UUID
    fee_type: str = "ADMISSION_FEE"
    amount_paid: float = Field(..., gt=0)
    payment_mode: str = "ONLINE"
    transaction_reference: Optional[str] = None


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_number: str
    application_mode: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    gender: str
    category: str
    course_name: str
    batch_preference: str
    academic_year_code: str
    guardian_name: str
    status: str
    is_locked: bool
    student_id: Optional[uuid.UUID] = None
    created_at: datetime


# ==================== Dashboard & Analytics ====================
class AdmissionDashboardMetrics(BaseModel):
    today_enquiries: int
    admissions_today: int
    pending_applications: int
    verification_pending: int
    waiting_list: int
    total_leads: int
    conversions_count: int
    conversion_rate_pct: float
    total_revenue_collected: float
