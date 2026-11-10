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
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class FeeCategory(Base):
    __tablename__ = "fee_categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    fee_heads: Mapped[List["FeeHead"]] = relationship("FeeHead", back_populates="category", cascade="all, delete-orphan")


class FeeHead(Base):
    __tablename__ = "fee_heads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fee_categories.id", ondelete="CASCADE"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_refundable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    default_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    category: Mapped["FeeCategory"] = relationship("FeeCategory", back_populates="fee_heads")
    structure_items: Mapped[List["FeeStructureItem"]] = relationship("FeeStructureItem", back_populates="fee_head")


class FeeStructure(Base):
    __tablename__ = "fee_structures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    program_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    semester_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    batch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    validity_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE", nullable=False) # DRAFT, ACTIVE, ARCHIVED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    items: Mapped[List["FeeStructureItem"]] = relationship("FeeStructureItem", back_populates="fee_structure", cascade="all, delete-orphan")
    installments: Mapped[List["Installment"]] = relationship("Installment", back_populates="fee_structure", cascade="all, delete-orphan")
    assignments: Mapped[List["StudentFeeAssignment"]] = relationship("StudentFeeAssignment", back_populates="fee_structure")


class FeeStructureItem(Base):
    __tablename__ = "fee_structure_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fee_structure_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fee_structures.id", ondelete="CASCADE"), nullable=False, index=True)
    fee_head_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fee_heads.id", ondelete="RESTRICT"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    is_optional: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    frequency: Mapped[str] = mapped_column(String(30), default="ONE_TIME", nullable=False) # ONE_TIME, ANNUAL, SEMESTER, MONTHLY
    due_period: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    fee_structure: Mapped["FeeStructure"] = relationship("FeeStructure", back_populates="items")
    fee_head: Mapped["FeeHead"] = relationship("FeeHead", back_populates="structure_items")


class Installment(Base):
    __tablename__ = "installments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fee_structure_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fee_structures.id", ondelete="CASCADE"), nullable=False, index=True)
    installment_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    grace_days: Mapped[int] = mapped_column(Integer, default=7, nullable=False)
    late_fee_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("late_fee_rules.id", ondelete="SET NULL"), nullable=True)
    reminder_days_before: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="SCHEDULED", nullable=False) # SCHEDULED, OPEN, CLOSED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    fee_structure: Mapped["FeeStructure"] = relationship("FeeStructure", back_populates="installments")
    late_fee_rule: Mapped[Optional["LateFeeRule"]] = relationship("LateFeeRule")


class LateFeeRule(Base):
    __tablename__ = "late_fee_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    calculation_type: Mapped[str] = mapped_column(String(24), default="DAILY", nullable=False) # FIXED_AMOUNT, PERCENTAGE, DAILY, WEEKLY, MONTHLY
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    maximum_limit: Mapped[float] = mapped_column(Float, default=5000.0, nullable=False)
    grace_period_days: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StudentFeeAssignment(Base):
    __tablename__ = "student_fee_assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    fee_structure_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fee_structures.id", ondelete="RESTRICT"), nullable=False, index=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    total_fee_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_discount_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_scholarship_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_payable_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_paid_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_due_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    assignment_type: Mapped[str] = mapped_column(String(32), default="INDIVIDUAL", nullable=False) # INDIVIDUAL, BATCH, COURSE, AUTOMATIC_ADMISSION
    status: Mapped[str] = mapped_column(String(24), default="PENDING", nullable=False) # PENDING, PARTIAL, PAID, OVERDUE
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    fee_structure: Mapped["FeeStructure"] = relationship("FeeStructure", back_populates="assignments")
    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="fee_assignment", cascade="all, delete-orphan")
    concessions: Mapped[List["Concession"]] = relationship("Concession", back_populates="fee_assignment", cascade="all, delete-orphan")
    due_history: Mapped[List["FeeDueHistory"]] = relationship("FeeDueHistory", back_populates="fee_assignment", cascade="all, delete-orphan")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    configuration_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_fee_assignment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("student_fee_assignments.id", ondelete="RESTRICT"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    installment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("installments.id", ondelete="SET NULL"), nullable=True, index=True)
    payment_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    amount_paid: Mapped[float] = mapped_column(Float, nullable=False)
    payment_mode: Mapped[str] = mapped_column(String(32), nullable=False) # CASH, UPI, CREDIT_CARD, DEBIT_CARD, NET_BANKING, CHEQUE, DEMAND_DRAFT, BANK_TRANSFER, WALLET, ONLINE_GATEWAY
    payment_method_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("payment_methods.id", ondelete="SET NULL"), nullable=True)
    transaction_reference: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    cheque_dd_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    bank_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="COMPLETED", nullable=False) # COMPLETED, PENDING, FAILED, BOUNCED, REFUNDED
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    fee_assignment: Mapped["StudentFeeAssignment"] = relationship("StudentFeeAssignment", back_populates="payments")
    receipt: Mapped[Optional["Receipt"]] = relationship("Receipt", back_populates="payment", uselist=False)
    refunds: Mapped[List["Refund"]] = relationship("Refund", back_populates="payment")


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    receipt_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    payment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("payments.id", ondelete="RESTRICT"), nullable=False, unique=True, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    amount_in_words: Mapped[str] = mapped_column(String(300), nullable=False)
    qr_code_data: Mapped[str] = mapped_column(Text, nullable=False)
    barcode_data: Mapped[str] = mapped_column(String(128), nullable=False)
    digital_signature_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    receipt_date: Mapped[date] = mapped_column(Date, nullable=False)
    pdf_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(24), default="GENERATED", nullable=False) # GENERATED, CANCELLED
    generated_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    payment: Mapped["Payment"] = relationship("Payment", back_populates="receipt")


class Scholarship(Base):
    __tablename__ = "scholarships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    scholarship_type: Mapped[str] = mapped_column(String(32), default="MERIT", nullable=False) # GOVERNMENT, PRIVATE, MERIT, SPORTS, STAFF, NEED_BASED, CUSTOM
    calculation_type: Mapped[str] = mapped_column(String(24), default="PERCENTAGE", nullable=False) # PERCENTAGE, FIXED_AMOUNT
    value: Mapped[float] = mapped_column(Float, nullable=False)
    eligibility_criteria: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    approval_workflow_status: Mapped[str] = mapped_column(String(24), default="APPROVED", nullable=False) # PENDING, APPROVED, REJECTED
    approved_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    max_beneficiaries: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class Discount(Base):
    __tablename__ = "discounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    discount_type: Mapped[str] = mapped_column(String(32), default="SIBLING", nullable=False) # SIBLING, EARLY_PAYMENT, EMPLOYEE, SPECIAL, MANUAL, AUTOMATIC_RULE
    calculation_type: Mapped[str] = mapped_column(String(24), default="PERCENTAGE", nullable=False) # PERCENTAGE, FIXED_AMOUNT
    value: Mapped[float] = mapped_column(Float, nullable=False)
    max_discount_amount: Mapped[float] = mapped_column(Float, default=20000.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class Concession(Base):
    __tablename__ = "concessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_fee_assignment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("student_fee_assignments.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    scholarship_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("scholarships.id", ondelete="SET NULL"), nullable=True)
    discount_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("discounts.id", ondelete="SET NULL"), nullable=True)
    concession_type: Mapped[str] = mapped_column(String(32), default="SCHOLARSHIP", nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    approved_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    approval_status: Mapped[str] = mapped_column(String(24), default="APPROVED", nullable=False)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    fee_assignment: Mapped["StudentFeeAssignment"] = relationship("StudentFeeAssignment", back_populates="concessions")


class Refund(Base):
    __tablename__ = "refunds"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("payments.id", ondelete="RESTRICT"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    refund_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    refund_type: Mapped[str] = mapped_column(String(24), default="PARTIAL", nullable=False) # FULL, PARTIAL
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    approval_status: Mapped[str] = mapped_column(String(24), default="PENDING", nullable=False) # PENDING, APPROVED, REJECTED, PROCESSED
    approved_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    payment_mode: Mapped[str] = mapped_column(String(32), default="BANK_TRANSFER", nullable=False)
    reference_number: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    payment: Mapped["Payment"] = relationship("Payment", back_populates="refunds")


class FeeDueHistory(Base):
    __tablename__ = "fee_due_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_fee_assignment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("student_fee_assignments.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    installment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("installments.id", ondelete="SET NULL"), nullable=True)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_amount: Mapped[float] = mapped_column(Float, nullable=False)
    penalty_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reminder_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_reminder_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(24), default="UNPAID", nullable=False) # UNPAID, PARTIAL, CLEARED, WAIVED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    fee_assignment: Mapped["StudentFeeAssignment"] = relationship("StudentFeeAssignment", back_populates="due_history")


class FinancialReport(Base):
    __tablename__ = "financial_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True) # DAILY_COLLECTION, MONTHLY_COLLECTION, YEARLY_COLLECTION, OUTSTANDING, SCHOLARSHIP, DISCOUNT, REFUND, CASH_REGISTER, BANK_STATEMENT
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_records: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_amount_calculated: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    parameters_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    generated_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
