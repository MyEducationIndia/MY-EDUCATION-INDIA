import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ------------------- Fee Category & Heads -------------------
class FeeCategoryCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = None
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None


class FeeCategoryResponse(FeeCategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


class FeeHeadCreate(BaseModel):
    category_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    is_refundable: bool = False
    default_amount: float = Field(0.0, ge=0.0)
    institute_id: uuid.UUID


class FeeHeadResponse(FeeHeadCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


# ------------------- Fee Structure & Items -------------------
class FeeStructureItemCreate(BaseModel):
    fee_head_id: uuid.UUID
    amount: float = Field(..., gt=0.0)
    is_optional: bool = False
    frequency: str = "ONE_TIME" # ONE_TIME, ANNUAL, SEMESTER, MONTHLY
    due_period: Optional[str] = None


class FeeStructureItemResponse(FeeStructureItemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    fee_structure_id: uuid.UUID
    created_at: datetime


class InstallmentPlanInput(BaseModel):
    installment_number: int = Field(..., ge=1)
    title: str = Field(..., min_length=2, max_length=120)
    due_date: date
    percentage: float = Field(..., ge=0.0, le=100.0)
    grace_days: int = Field(7, ge=0)
    late_fee_rule_id: Optional[uuid.UUID] = None


class InstallmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    fee_structure_id: uuid.UUID
    installment_number: int
    title: str
    due_date: date
    percentage: float
    amount: float
    grace_days: int
    status: str
    created_at: datetime


class FeeStructureCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=48)
    name: str = Field(..., min_length=3, max_length=180)
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    academic_year_id: uuid.UUID
    program_id: Optional[uuid.UUID] = None
    course_id: Optional[uuid.UUID] = None
    semester_id: Optional[uuid.UUID] = None
    batch_id: Optional[uuid.UUID] = None
    effective_date: date
    validity_date: date
    items: List[FeeStructureItemCreate] = Field(..., min_items=1)
    installments_plan: Optional[List[InstallmentPlanInput]] = None


class FeeStructureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    code: str
    name: str
    version: int
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID]
    academic_year_id: uuid.UUID
    effective_date: date
    validity_date: date
    total_amount: float
    status: str
    items: List[FeeStructureItemResponse] = []
    installments: List[InstallmentResponse] = []
    created_at: datetime


# ------------------- Student Fee Assignment -------------------
class StudentFeeAssignmentCreate(BaseModel):
    student_id: uuid.UUID
    fee_structure_id: uuid.UUID
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    academic_year_id: uuid.UUID
    assignment_type: str = "INDIVIDUAL" # INDIVIDUAL, BATCH, COURSE, AUTOMATIC_ADMISSION


class BulkFeeAssignmentCreate(BaseModel):
    student_ids: List[uuid.UUID] = Field(..., min_items=1)
    fee_structure_id: uuid.UUID
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    academic_year_id: uuid.UUID


class StudentFeeAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    student_id: uuid.UUID
    fee_structure_id: uuid.UUID
    institute_id: uuid.UUID
    total_fee_amount: float
    total_discount_amount: float
    total_scholarship_amount: float
    total_payable_amount: float
    total_paid_amount: float
    total_due_amount: float
    assignment_type: str
    status: str
    assigned_at: datetime
    created_at: datetime


# ------------------- Payment & Collection -------------------
class PaymentCreate(BaseModel):
    student_fee_assignment_id: uuid.UUID
    student_id: uuid.UUID
    installment_id: Optional[uuid.UUID] = None
    amount_paid: float = Field(..., gt=0.0)
    payment_mode: str = "UPI" # CASH, UPI, CREDIT_CARD, DEBIT_CARD, NET_BANKING, CHEQUE, DEMAND_DRAFT, BANK_TRANSFER
    payment_method_id: Optional[uuid.UUID] = None
    transaction_reference: Optional[str] = None
    cheque_dd_number: Optional[str] = None
    bank_name: Optional[str] = None
    payment_date: Optional[date] = None
    remarks: Optional[str] = None


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    student_fee_assignment_id: uuid.UUID
    student_id: uuid.UUID
    installment_id: Optional[uuid.UUID]
    payment_number: str
    amount_paid: float
    payment_mode: str
    transaction_reference: Optional[str]
    payment_date: date
    status: str
    remarks: Optional[str]
    created_at: datetime


# ------------------- Receipt -------------------
class ReceiptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    receipt_number: str
    payment_id: uuid.UUID
    student_id: uuid.UUID
    institute_id: uuid.UUID
    academic_year_id: uuid.UUID
    total_amount: float
    amount_in_words: str
    qr_code_data: str
    barcode_data: str
    digital_signature_hash: str
    receipt_date: date
    status: str
    created_at: datetime


# ------------------- Scholarship & Concession -------------------
class ScholarshipCreate(BaseModel):
    institute_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=3, max_length=150)
    scholarship_type: str = "MERIT"
    calculation_type: str = "PERCENTAGE" # PERCENTAGE, FIXED_AMOUNT
    value: float = Field(..., gt=0.0)
    eligibility_criteria: Optional[str] = None
    max_beneficiaries: int = 100


class ScholarshipResponse(ScholarshipCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    approval_workflow_status: str
    is_active: bool
    created_at: datetime


class DiscountCreate(BaseModel):
    institute_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=3, max_length=120)
    discount_type: str = "SIBLING"
    calculation_type: str = "PERCENTAGE"
    value: float = Field(..., gt=0.0)
    max_discount_amount: float = 20000.0


class DiscountResponse(DiscountCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


class ConcessionApplyRequest(BaseModel):
    student_fee_assignment_id: uuid.UUID
    student_id: uuid.UUID
    scholarship_id: Optional[uuid.UUID] = None
    discount_id: Optional[uuid.UUID] = None
    concession_type: str = "SCHOLARSHIP"
    amount: float = Field(..., gt=0.0)
    reason: str = Field(..., min_length=3, max_length=255)


class ConcessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    student_fee_assignment_id: uuid.UUID
    student_id: uuid.UUID
    amount: float
    reason: str
    approval_status: str
    applied_at: datetime


# ------------------- Late Fee Rules -------------------
class LateFeeRuleCreate(BaseModel):
    institute_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=3, max_length=120)
    calculation_type: str = "DAILY" # FIXED_AMOUNT, PERCENTAGE, DAILY, WEEKLY, MONTHLY
    rate: float = Field(..., gt=0.0)
    maximum_limit: float = 5000.0
    grace_period_days: int = 5


class LateFeeRuleResponse(LateFeeRuleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


# ------------------- Refunds -------------------
class RefundRequest(BaseModel):
    payment_id: uuid.UUID
    student_id: uuid.UUID
    institute_id: uuid.UUID
    amount: float = Field(..., gt=0.0)
    refund_type: str = "PARTIAL" # FULL, PARTIAL
    reason: str = Field(..., min_length=5)
    payment_mode: str = "BANK_TRANSFER"
    reference_number: Optional[str] = None


class RefundResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    refund_number: str
    payment_id: uuid.UUID
    student_id: uuid.UUID
    amount: float
    refund_type: str
    reason: str
    approval_status: str
    payment_mode: str
    reference_number: Optional[str]
    created_at: datetime


# ------------------- Financial Reports & Analytics -------------------
class FinancialReportFilter(BaseModel):
    institute_id: uuid.UUID
    report_type: str # DAILY_COLLECTION, MONTHLY_COLLECTION, YEARLY_COLLECTION, OUTSTANDING, REFUND, CASH_REGISTER
    start_date: date
    end_date: date
    payment_mode: Optional[str] = None
    course_id: Optional[uuid.UUID] = None


class FeeAnalyticsSummary(BaseModel):
    total_projected_revenue: float
    total_collected_revenue: float
    total_outstanding_dues: float
    collection_percentage: float
    total_scholarships_granted: float
    total_discounts_granted: float
    total_refunds_processed: float
    today_collection: float
    month_collection: float
    payment_mode_distribution: Dict[str, float]
    monthly_trend: List[Dict[str, Any]]
