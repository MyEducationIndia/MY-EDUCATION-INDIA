import uuid
from datetime import date, datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin


class LeadSource(Base, TimestampUUIDMixin):
    __tablename__ = "crm_lead_sources"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_lead_source_code_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # WEBSITE, WALK_IN, PHONE_CALL, WHATSAPP, FACEBOOK, INSTAGRAM, GOOGLE_ADS, REFERRAL, EXISTING_STUDENT, EDUCATION_FAIR, MANUAL
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Lead(Base, TimestampUUIDMixin):
    __tablename__ = "crm_leads"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True
    )
    lead_number: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False) # e.g. LEAD-2027-0001
    full_name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(24), index=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_channel: Mapped[str] = mapped_column(String(64), default="WEBSITE", index=True, nullable=False)
    interested_course: Mapped[str | None] = mapped_column(String(150), index=True, nullable=True)
    preferred_batch: Mapped[str | None] = mapped_column(String(100), nullable=True)
    assigned_counsellor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    priority: Mapped[str] = mapped_column(String(32), default="HOT", index=True, nullable=False) # HOT, WARM, COLD
    status: Mapped[str] = mapped_column(
        String(32), default="NEW", index=True, nullable=False
    ) # NEW, CONTACTED, COUNSELLING_SCHEDULED, APPLICATION_SUBMITTED, ADMITTED, LOST, JUNK
    next_followup_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    estimated_budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    score: Mapped[int] = mapped_column(Integer, default=50, nullable=False) # Lead Quality Score 0-100
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    followups: Mapped[List["LeadFollowup"]] = relationship("LeadFollowup", back_populates="lead", cascade="all, delete-orphan", lazy="selectin")
    counselling_sessions: Mapped[List["CounsellingSession"]] = relationship("CounsellingSession", back_populates="lead", cascade="all, delete-orphan", lazy="selectin")


class LeadFollowup(Base, TimestampUUIDMixin):
    __tablename__ = "crm_lead_followups"
    __table_args__ = {"extend_existing": True}

    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("crm_leads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    counsellor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    channel: Mapped[str] = mapped_column(String(32), default="CALL", nullable=False) # CALL, WHATSAPP, EMAIL, MEETING, SMS
    discussion_notes: Mapped[str] = mapped_column(Text, nullable=False)
    outcome: Mapped[str] = mapped_column(String(64), nullable=False) # INTERESTED, CALLBACK_REQUESTED, NOT_REACHABLE, ADMISSION_PROMISED, NOT_INTERESTED
    scheduled_next_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    followed_up_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    lead: Mapped[Lead] = relationship("Lead", back_populates="followups")


class CounsellingSession(Base, TimestampUUIDMixin):
    __tablename__ = "crm_counselling_sessions"
    __table_args__ = {"extend_existing": True}

    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("crm_leads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    counsellor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    session_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    meeting_mode: Mapped[str] = mapped_column(String(32), default="IN_PERSON", nullable=False) # IN_PERSON, VIDEO_CALL, TELEPHONIC
    recommendations: Mapped[str] = mapped_column(Text, nullable=False)
    career_aspiration: Mapped[str | None] = mapped_column(String(255), nullable=True)
    scholarship_suggested_pct: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    outcome: Mapped[str] = mapped_column(String(64), default="APPLICATION_ISSUED", nullable=False)

    lead: Mapped[Lead] = relationship("Lead", back_populates="counselling_sessions")


class Application(Base, TimestampUUIDMixin):
    """Master Admission Application Form (Online or Offline)."""
    __tablename__ = "admission_applications"
    __table_args__ = (
        UniqueConstraint("application_number", "institute_id", name="uq_app_num_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("crm_leads.id", ondelete="SET NULL"), nullable=True, index=True
    )
    student_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="SET NULL"), nullable=True, index=True
    )

    application_number: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # e.g. APP-2027-0001
    application_mode: Mapped[str] = mapped_column(String(32), default="ONLINE", nullable=False) # ONLINE, OFFLINE_RECEPTION

    # Candidate Primary Details
    first_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(24), index=True, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[str] = mapped_column(String(32), default="GENERAL", nullable=False) # GENERAL, OBC, SC, ST, EWS

    # Academic Choices & Cycle
    course_name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    batch_preference: Mapped[str] = mapped_column(String(100), nullable=False)
    academic_year_code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)

    # Guardian & Emergency Details
    guardian_name: Mapped[str] = mapped_column(String(150), nullable=False)
    guardian_phone: Mapped[str] = mapped_column(String(24), nullable=False)
    guardian_relation: Mapped[str] = mapped_column(String(32), default="FATHER", nullable=False)

    # Address
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)

    # Prior Education
    previous_institution: Mapped[str | None] = mapped_column(String(200), nullable=True)
    previous_marks_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Workflow Status
    status: Mapped[str] = mapped_column(
        String(32), default="PENDING", index=True, nullable=False
    ) # PENDING, VERIFIED, ENTRANCE_QUALIFIED, APPROVED, FEE_PAID, CONVERTED, REJECTED, WAITING_LIST, CANCELLED

    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # Locked upon approval
    approved_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Dynamic Custom Form Field Payloads
    custom_form_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    # Relationships
    documents: Mapped[List["ApplicationDocument"]] = relationship("ApplicationDocument", back_populates="application", cascade="all, delete-orphan", lazy="selectin")
    entrance_result: Mapped[Optional["EntranceResult"]] = relationship("EntranceResult", back_populates="application", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    scholarship: Mapped[Optional["ScholarshipAllocation"]] = relationship("ScholarshipAllocation", back_populates="application", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    fees: Mapped[List["AdmissionFeeReceipt"]] = relationship("AdmissionFeeReceipt", back_populates="application", cascade="all, delete-orphan", lazy="selectin")
    timeline: Mapped[List["AdmissionTimeline"]] = relationship("AdmissionTimeline", back_populates="application", cascade="all, delete-orphan", lazy="selectin")


class ApplicationDocument(Base, TimestampUUIDMixin):
    __tablename__ = "admission_application_documents"
    __table_args__ = {"extend_existing": True}

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admission_applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    document_type: Mapped[str] = mapped_column(String(64), nullable=False) # PHOTO, SIGNATURE, AADHAAR, 10TH_MARKSHEET, 12TH_MARKSHEET, TRANSFER_CERTIFICATE, CASTE_CERTIFICATE
    document_title: Mapped[str] = mapped_column(String(150), nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=False) # Cloudinary URL
    verification_status: Mapped[str] = mapped_column(String(32), default="PENDING", nullable=False) # PENDING, VERIFIED, REJECTED, CORRECTION_REQUIRED
    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)
    verified_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    application: Mapped[Application] = relationship("Application", back_populates="documents")


class EntranceTest(Base, TimestampUUIDMixin):
    __tablename__ = "admission_entrance_tests"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    test_code: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # e.g. MEI-CET-2027
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    course_name: Mapped[str] = mapped_column(String(150), nullable=False)
    test_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    max_marks: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    passing_marks: Mapped[int] = mapped_column(Integer, default=40, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class EntranceResult(Base, TimestampUUIDMixin):
    __tablename__ = "admission_entrance_results"
    __table_args__ = (
        UniqueConstraint("application_id", "test_id", name="uq_app_test_result"),
        {"extend_existing": True},
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admission_applications.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    test_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admission_entrance_tests.id", ondelete="CASCADE"), nullable=False, index=True
    )
    marks_obtained: Mapped[float] = mapped_column(Float, nullable=False)
    percentile: Mapped[float | None] = mapped_column(Float, nullable=True)
    merit_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_qualified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    application: Mapped[Application] = relationship("Application", back_populates="entrance_result")


class SeatManagement(Base, TimestampUUIDMixin):
    """Configurable Course & Category-wise Seat Allocation Quota."""
    __tablename__ = "admission_seat_management"
    __table_args__ = (
        UniqueConstraint("institute_id", "branch_id", "course_name", "academic_year_code", "category", name="uq_seat_quota"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_name: Mapped[str] = mapped_column(String(150), nullable=False)
    academic_year_code: Mapped[str] = mapped_column(String(32), nullable=False)
    category: Mapped[str] = mapped_column(String(32), default="GENERAL", nullable=False) # GENERAL, OBC, SC, ST, EWS, MANAGEMENT
    total_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    filled_seats: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    waiting_seats: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Scholarship(Base, TimestampUUIDMixin):
    __tablename__ = "admission_scholarships"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False) # e.g. National Merit Excellence Scholarship
    code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    discount_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    fixed_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    criteria_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ScholarshipAllocation(Base, TimestampUUIDMixin):
    __tablename__ = "admission_scholarship_allocations"
    __table_args__ = {"extend_existing": True}

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admission_applications.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    scholarship_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admission_scholarships.id", ondelete="CASCADE"), nullable=False, index=True
    )
    awarded_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    awarded_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    approved_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    approval_status: Mapped[str] = mapped_column(String(32), default="APPROVED", nullable=False)

    application: Mapped[Application] = relationship("Application", back_populates="scholarship")


class AdmissionFeeReceipt(Base, TimestampUUIDMixin):
    __tablename__ = "admission_fee_receipts"
    __table_args__ = {"extend_existing": True}

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admission_applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    receipt_number: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False) # RCPT-2027-0012
    fee_type: Mapped[str] = mapped_column(String(64), default="ADMISSION_FEE", nullable=False) # REGISTRATION_FEE, ADMISSION_FEE, BOOKING_AMOUNT
    amount_paid: Mapped[float] = mapped_column(Float, nullable=False)
    payment_mode: Mapped[str] = mapped_column(String(32), default="ONLINE", nullable=False) # ONLINE, CASH, CHEQUE, UPI, DD
    transaction_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="SUCCESS", nullable=False)
    collected_by: Mapped[str] = mapped_column(String(100), default="Payment Gateway", nullable=False)

    application: Mapped[Application] = relationship("Application", back_populates="fees")


class AdmissionTimeline(Base, TimestampUUIDMixin):
    __tablename__ = "admission_timeline"
    __table_args__ = {"extend_existing": True}

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admission_applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    stage: Mapped[str] = mapped_column(String(64), nullable=False) # LEAD, ENQUIRY, COUNSELLING, APPLICATION, VERIFICATION, ENTRANCE, FEE, APPROVAL, SIMS_CONVERSION
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    actor_name: Mapped[str] = mapped_column(String(100), default="System", nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    metadata_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    application: Mapped[Application] = relationship("Application", back_populates="timeline")
