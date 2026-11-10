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


class Student(Base, TimestampUUIDMixin):
    """Master Student Record linked to Institute and User account."""
    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("registration_number", "institute_id", name="uq_student_reg_inst"),
        UniqueConstraint("enrollment_number", "institute_id", name="uq_student_enroll_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Identifiers generated via Universal Number Generator
    registration_number: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # e.g. MEI-BPL-2027-000124
    enrollment_number: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    roll_number: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    erp_id: Mapped[str | None] = mapped_column(String(64), unique=True, index=True, nullable=True)
    library_card_number: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Primary Name & Identification
    first_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(24), index=True, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False) # MALE, FEMALE, OTHER

    # Academic & Cohort Allocation
    course_name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    batch_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    academic_year_code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    admission_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    semester_or_year: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Status & Soft Delete
    status: Mapped[str] = mapped_column(
        String(32), default="ACTIVE", index=True, nullable=False
    ) # ACTIVE, INACTIVE, PENDING_ADMISSION, TRANSFERRED, SUSPENDED, PASSED, DROPPED, ALUMNI, ARCHIVED
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    profile: Mapped["StudentProfile"] = relationship("StudentProfile", back_populates="student", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    addresses: Mapped[List["StudentAddress"]] = relationship("StudentAddress", back_populates="student", cascade="all, delete-orphan", lazy="selectin")
    guardians: Mapped[List["StudentGuardian"]] = relationship("StudentGuardian", back_populates="student", cascade="all, delete-orphan", lazy="selectin")
    documents: Mapped[List["StudentDocument"]] = relationship("StudentDocument", back_populates="student", cascade="all, delete-orphan", lazy="selectin")
    medical: Mapped["StudentMedical"] = relationship("StudentMedical", back_populates="student", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    custom_values: Mapped[List["StudentCustomValue"]] = relationship("StudentCustomValue", back_populates="student", cascade="all, delete-orphan", lazy="selectin")
    status_history: Mapped[List["StudentStatusHistory"]] = relationship("StudentStatusHistory", back_populates="student", cascade="all, delete-orphan", lazy="selectin")
    timeline: Mapped[List["StudentTimeline"]] = relationship("StudentTimeline", back_populates="student", cascade="all, delete-orphan", lazy="selectin")
    notes: Mapped[List["StudentNote"]] = relationship("StudentNote", back_populates="student", cascade="all, delete-orphan", lazy="selectin")
    photo: Mapped["StudentPhoto"] = relationship("StudentPhoto", back_populates="student", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    qr_code: Mapped["StudentQRCode"] = relationship("StudentQRCode", back_populates="student", uselist=False, cascade="all, delete-orphan", lazy="selectin")


class StudentProfile(Base, TimestampUUIDMixin):
    __tablename__ = "student_profiles"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    aadhaar_number: Mapped[str | None] = mapped_column(String(20), nullable=True) # Stored encrypted or masked
    pan_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    apaar_id: Mapped[str | None] = mapped_column(String(32), nullable=True) # Indian Automated Permanent Academic Account Registry
    abc_account_id: Mapped[str | None] = mapped_column(String(32), nullable=True) # Academic Bank of Credits ID
    religion: Mapped[str | None] = mapped_column(String(50), nullable=True)
    caste_category: Mapped[str | None] = mapped_column(String(50), nullable=True) # GENERAL, OBC, SC, ST, EWS
    nationality: Mapped[str] = mapped_column(String(64), default="Indian", nullable=False)
    mother_tongue: Mapped[str | None] = mapped_column(String(50), default="Hindi", nullable=True)
    previous_school: Mapped[str | None] = mapped_column(String(200), nullable=True)
    previous_qualification: Mapped[str | None] = mapped_column(String(100), nullable=True)
    previous_marks_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)

    student: Mapped[Student] = relationship("Student", back_populates="profile")


class StudentAddress(Base, TimestampUUIDMixin):
    __tablename__ = "student_addresses"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    address_type: Mapped[str] = mapped_column(String(32), default="PERMANENT", nullable=False) # PERMANENT, CORRESPONDENCE, LOCAL_GUARDIAN
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default="India", nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="addresses")


class StudentGuardian(Base, TimestampUUIDMixin):
    __tablename__ = "student_guardians"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relationship_type: Mapped[str] = mapped_column(String(32), nullable=False) # FATHER, MOTHER, LEGAL_GUARDIAN
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(24), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    occupation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    annual_income: Mapped[float | None] = mapped_column(Float, nullable=True)
    qualification: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_emergency_contact: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="guardians")


class StudentDocument(Base, TimestampUUIDMixin):
    __tablename__ = "student_documents"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    document_type: Mapped[str] = mapped_column(
        String(64), nullable=False
    ) # AADHAAR, PAN, BIRTH_CERTIFICATE, TRANSFER_CERTIFICATE, MIGRATION_CERTIFICATE, 10TH_MARKSHEET, 12TH_MARKSHEET, GRADUATION_MARKSHEET, CASTE_CERTIFICATE, INCOME_CERTIFICATE, MEDICAL_CERTIFICATE, PASSPORT, VISA, OTHER
    document_title: Mapped[str] = mapped_column(String(150), nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=False) # Cloudinary URL
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="application/pdf", nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verified_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    student: Mapped[Student] = relationship("Student", back_populates="documents")


class StudentMedical(Base, TimestampUUIDMixin):
    __tablename__ = "student_medical"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    blood_group: Mapped[str | None] = mapped_column(String(8), nullable=True) # A+, A-, B+, B-, O+, O-, AB+, AB-
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    allergies: Mapped[str | None] = mapped_column(Text, nullable=True)
    medical_conditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    emergency_doctor_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    emergency_doctor_phone: Mapped[str | None] = mapped_column(String(24), nullable=True)
    insurance_policy_number: Mapped[str | None] = mapped_column(String(100), nullable=True)

    student: Mapped[Student] = relationship("Student", back_populates="medical")


class StudentCustomField(Base, TimestampUUIDMixin):
    """Configurable dynamic fields created by Administrator without code modifications."""
    __tablename__ = "student_custom_fields"
    __table_args__ = (
        UniqueConstraint("field_key", "institute_id", name="uq_custom_field_key_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field_key: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # e.g. transport_route, hostel_room, scholarship_name, counsellor
    field_label: Mapped[str] = mapped_column(String(120), nullable=False)
    field_type: Mapped[str] = mapped_column(String(32), default="TEXT", nullable=False) # TEXT, NUMBER, SELECT, DATE, BOOLEAN
    is_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    options_list: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)


class StudentCustomValue(Base, TimestampUUIDMixin):
    __tablename__ = "student_custom_values"
    __table_args__ = (
        UniqueConstraint("student_id", "custom_field_id", name="uq_student_custom_value"),
        {"extend_existing": True},
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    custom_field_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("student_custom_fields.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field_value: Mapped[str] = mapped_column(Text, nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="custom_values")
    field_definition: Mapped[StudentCustomField] = relationship("StudentCustomField", lazy="selectin")


class StudentStatusHistory(Base, TimestampUUIDMixin):
    __tablename__ = "student_status_history"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    previous_status: Mapped[str] = mapped_column(String(32), nullable=False)
    new_status: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    changed_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="status_history")


class StudentTimeline(Base, TimestampUUIDMixin):
    """Immutable chronological timeline of all events in student lifecycle."""
    __tablename__ = "student_timeline"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_category: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    ) # ADMISSION, ACADEMIC, FEE, ATTENDANCE, EXAM, CERTIFICATE, TRANSFER, HOSTEL, LIBRARY, COMMUNICATION, STATUS_CHANGE
    event_title: Mapped[str] = mapped_column(String(150), nullable=False)
    event_description: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_by: Mapped[str] = mapped_column(String(100), default="System", nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True, nullable=False)
    meta_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="timeline")


class StudentNote(Base, TimestampUUIDMixin):
    __tablename__ = "student_notes"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author_name: Mapped[str] = mapped_column(String(120), nullable=False)
    note_title: Mapped[str] = mapped_column(String(150), nullable=False)
    note_content: Mapped[str] = mapped_column(Text, nullable=False)
    is_confidential: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="notes")


class StudentPhoto(Base, TimestampUUIDMixin):
    __tablename__ = "student_photos"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    photo_url: Mapped[str] = mapped_column(Text, nullable=False) # Cloudinary URL
    signature_url: Mapped[str | None] = mapped_column(Text, nullable=True) # Digital Signature URL

    student: Mapped[Student] = relationship("Student", back_populates="photo")


class StudentQRCode(Base, TimestampUUIDMixin):
    __tablename__ = "student_qr_codes"
    __table_args__ = {"extend_existing": True}

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    qr_payload: Mapped[str] = mapped_column(Text, nullable=False) # Encrypted verification string
    qr_svg: Mapped[str] = mapped_column(Text, nullable=False) # Inline SVG string for high-res ID cards & scanning
    barcode_value: Mapped[str] = mapped_column(String(64), nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="qr_code")
