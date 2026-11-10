import uuid
from typing import Optional, Dict, Any
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampUUIDMixin

class CmsAdmissionApplication(Base, TimestampUUIDMixin):
    __tablename__ = "cms_admission_applications"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    application_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    applicant_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    preferred_course_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[str] = mapped_column(String(32), nullable=False)
    gender: Mapped[str] = mapped_column(String(32), nullable=False)
    father_or_guardian_name: Mapped[str] = mapped_column(String(128), nullable=False)
    address_city: Mapped[str] = mapped_column(String(128), nullable=False)
    address_state: Mapped[str] = mapped_column(String(128), nullable=False)
    qualifying_exam: Mapped[str] = mapped_column(String(128), nullable=False)
    qualifying_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    entrance_exam_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    entrance_score_or_rank: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="SUBMITTED", nullable=False)
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    documents_uploaded: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    payment_status: Mapped[str] = mapped_column(String(32), default="PENDING", nullable=False)
    payment_transaction_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

class CmsAdmissionEnquiry(Base, TimestampUUIDMixin):
    __tablename__ = "cms_admission_enquiries"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    program_interest: Mapped[str] = mapped_column(String(128), nullable=False)
    city: Mapped[str] = mapped_column(String(128), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="NEW", nullable=False)
    counselor_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class CmsAdmissionStep(Base, TimestampUUIDMixin):
    __tablename__ = "cms_admission_steps"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    timeline_badge: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsFeeStructure(Base, TimestampUUIDMixin):
    __tablename__ = "cms_fee_structures"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    program_name: Mapped[str] = mapped_column(String(255), nullable=False)
    program_code: Mapped[str] = mapped_column(String(64), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(32), nullable=False)
    admission_fee: Mapped[str] = mapped_column(String(64), nullable=False)
    tuition_fee_per_semester: Mapped[str] = mapped_column(String(64), nullable=False)
    development_fee: Mapped[str] = mapped_column(String(64), nullable=False)
    examination_fee: Mapped[str] = mapped_column(String(64), nullable=False)
    caution_deposit_refundable: Mapped[str] = mapped_column(String(64), nullable=False)
    total_annual_fee: Mapped[str] = mapped_column(String(64), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsScholarship(Base, TimestampUUIDMixin):
    __tablename__ = "cms_scholarships"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    eligibility_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    benefit_summary: Mapped[str] = mapped_column(Text, nullable=False)
    waiver_percentage: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    seats_available: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    validity_period: Mapped[str] = mapped_column(String(64), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
