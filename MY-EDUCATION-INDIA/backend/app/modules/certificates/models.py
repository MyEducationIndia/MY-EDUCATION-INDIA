import uuid
from datetime import date, datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class DocumentType(Base):
    __tablename__ = "document_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True) # e.g. BONAFIDE, DEGREE, TC, TRANSCRIPT, ID_CARD
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(32), default="ACADEMIC", nullable=False) # ACADEMIC, ADMINISTRATIVE, IDENTIFICATION
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_expiry: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validity_months: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    templates: Mapped[List["CertificateTemplate"]] = relationship("CertificateTemplate", back_populates="document_type")


class CertificateTemplate(Base):
    __tablename__ = "certificate_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    document_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("document_types.id", ondelete="CASCADE"), nullable=False, index=True)
    template_code: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    page_orientation: Mapped[str] = mapped_column(String(16), default="LANDSCAPE", nullable=False) # LANDSCAPE, PORTRAIT
    page_size: Mapped[str] = mapped_column(String(16), default="A4", nullable=False) # A4, LETTER, LEGAL, ID_CARD_CR80
    background_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    html_markup: Mapped[str] = mapped_column(Text, nullable=False)
    css_styles: Mapped[str] = mapped_column(Text, default="", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    document_type: Mapped["DocumentType"] = relationship("DocumentType", back_populates="templates")
    fields: Mapped[List["CertificateField"]] = relationship("CertificateField", back_populates="template", cascade="all, delete-orphan")
    layouts: Mapped[List["CertificateLayout"]] = relationship("CertificateLayout", back_populates="template", cascade="all, delete-orphan")
    issued_certificates: Mapped[List["IssuedCertificate"]] = relationship("IssuedCertificate", back_populates="template")


class CertificateField(Base):
    __tablename__ = "certificate_fields"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("certificate_templates.id", ondelete="CASCADE"), nullable=False, index=True)
    field_key: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. student_name, enrollment_no, course_name, cgpa, issue_date
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    field_type: Mapped[str] = mapped_column(String(32), default="TEXT", nullable=False) # TEXT, NUMBER, DATE, QR_CODE, BARCODE, PHOTO, SIGNATURE
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    default_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    template: Mapped["CertificateTemplate"] = relationship("CertificateTemplate", back_populates="fields")


class CertificateLayout(Base):
    __tablename__ = "certificate_layouts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("certificate_templates.id", ondelete="CASCADE"), nullable=False, index=True)
    elements_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False) # Drag-and-drop elements with X, Y coordinates, fonts, colors
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    template: Mapped["CertificateTemplate"] = relationship("CertificateTemplate", back_populates="layouts")


class CertificateNumber(Base):
    __tablename__ = "certificate_numbers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    prefix: Mapped[str] = mapped_column(String(24), nullable=False) # e.g. CERT, BONA, DEG
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    current_counter: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class IssuedCertificate(Base):
    __tablename__ = "issued_certificates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    certificate_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    verification_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("certificate_templates.id", ondelete="RESTRICT"), nullable=False, index=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    recipient_type: Mapped[str] = mapped_column(String(24), default="STUDENT", nullable=False) # STUDENT, FACULTY, STAFF, EXTERNAL
    recipient_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    payload_data_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    pdf_document_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    qr_code_payload: Mapped[str] = mapped_column(Text, nullable=False)
    barcode_data: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="ISSUED", nullable=False) # DRAFT, PENDING_REVIEW, APPROVED, ISSUED, REVOKED, ARCHIVED
    revocation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    issued_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    template: Mapped["CertificateTemplate"] = relationship("CertificateTemplate", back_populates="issued_certificates")
    status_history: Mapped[List["CertificateStatusHistory"]] = relationship("CertificateStatusHistory", back_populates="certificate", cascade="all, delete-orphan")
    verification_token: Mapped[Optional["VerificationToken"]] = relationship("VerificationToken", back_populates="certificate", uselist=False)


class GeneratedDocument(Base):
    __tablename__ = "generated_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    document_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("document_types.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(64), default="application/pdf", nullable=False)
    generated_for_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    certificate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("issued_certificates.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    public_verification_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    certificate: Mapped["IssuedCertificate"] = relationship("IssuedCertificate", back_populates="verification_token")
    verification_logs: Mapped[List["VerificationLog"]] = relationship("VerificationLog", back_populates="token_record", cascade="all, delete-orphan")


class VerificationLog(Base):
    __tablename__ = "verification_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("verification_tokens.id", ondelete="CASCADE"), nullable=False, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(48), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    result_status: Mapped[str] = mapped_column(String(24), default="VALID", nullable=False) # VALID, INVALID, REVOKED, EXPIRED

    token_record: Mapped["VerificationToken"] = relationship("VerificationToken", back_populates="verification_logs")


class DigitalSignature(Base):
    __tablename__ = "digital_signatures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    certificate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("issued_certificates.id", ondelete="CASCADE"), nullable=False, index=True)
    signatory_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    signature_type: Mapped[str] = mapped_column(String(24), default="PKI_CRYPTO_HASH", nullable=False) # PKI_CRYPTO_HASH, DSC_USB, ESIGN
    signature_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CertificateStatusHistory(Base):
    __tablename__ = "certificate_status_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    certificate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("issued_certificates.id", ondelete="CASCADE"), nullable=False, index=True)
    previous_status: Mapped[str] = mapped_column(String(24), nullable=False)
    new_status: Mapped[str] = mapped_column(String(24), nullable=False)
    changed_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    certificate: Mapped["IssuedCertificate"] = relationship("IssuedCertificate", back_populates="status_history")


class IDCard(Base):
    __tablename__ = "id_cards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    card_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    holder_type: Mapped[str] = mapped_column(String(24), default="STUDENT", nullable=False) # STUDENT, FACULTY, STAFF, VISITOR
    holder_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    blood_group: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    qr_code_payload: Mapped[str] = mapped_column(Text, nullable=False)
    barcode_data: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="ACTIVE", nullable=False) # ACTIVE, EXPIRED, BLOCKED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentArchive(Base):
    __tablename__ = "document_archives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    certificate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    archived_reason: Mapped[str] = mapped_column(Text, nullable=False)
    archived_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    archived_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CertificateReport(Base):
    __tablename__ = "certificate_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    parameters_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    generated_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CertificateAnalytics(Base):
    __tablename__ = "certificate_analytics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    total_issued: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_verified: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_revoked: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    metrics_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
