from datetime import date, datetime, timezone
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ValidationException
from app.modules.fees.models import (
    Concession,
    Discount,
    FeeCategory,
    FeeHead,
    FeeStructure,
    FeeStructureItem,
    Installment,
    LateFeeRule,
    Payment,
    Receipt,
    Refund,
    Scholarship,
    StudentFeeAssignment,
)
from app.modules.fees.receipt_generator import ReceiptGenerator, number_to_indian_currency_words
from app.modules.fees.repository import FeeRepository
from app.modules.fees.schemas import (
    ConcessionApplyRequest,
    DiscountCreate,
    FeeCategoryCreate,
    FeeHeadCreate,
    FeeStructureCreate,
    LateFeeRuleCreate,
    PaymentCreate,
    RefundRequest,
    ScholarshipCreate,
    StudentFeeAssignmentCreate,
)
from app.modules.fees.validators import FeeBusinessValidators


class FeeManagementService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = FeeRepository(session)

    # 1. Categories & Heads
    async def create_fee_category(self, payload: FeeCategoryCreate) -> FeeCategory:
        cat = FeeCategory(
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            description=payload.description,
            institute_id=payload.institute_id,
            branch_id=payload.branch_id,
        )
        return await self.repo.create_category(cat)

    async def list_categories(self, institute_id: uuid.UUID) -> List[FeeCategory]:
        return await self.repo.get_categories(institute_id)

    async def create_fee_head(self, payload: FeeHeadCreate) -> FeeHead:
        head = FeeHead(
            category_id=payload.category_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            description=payload.description,
            is_refundable=payload.is_refundable,
            default_amount=payload.default_amount,
            institute_id=payload.institute_id,
        )
        return await self.repo.create_fee_head(head)

    async def list_fee_heads(self, institute_id: uuid.UUID, category_id: Optional[uuid.UUID] = None) -> List[FeeHead]:
        return await self.repo.get_fee_heads(institute_id, category_id)

    # 2. Fee Structure Creation
    async def create_fee_structure(self, payload: FeeStructureCreate) -> FeeStructure:
        FeeBusinessValidators.validate_structure_dates(payload.effective_date, payload.validity_date)
        total_amount = FeeBusinessValidators.validate_structure_items(payload.items)
        if payload.installments_plan:
            FeeBusinessValidators.validate_installment_percentages(payload.installments_plan)

        structure = FeeStructure(
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            institute_id=payload.institute_id,
            branch_id=payload.branch_id,
            academic_year_id=payload.academic_year_id,
            program_id=payload.program_id,
            course_id=payload.course_id,
            semester_id=payload.semester_id,
            batch_id=payload.batch_id,
            effective_date=payload.effective_date,
            validity_date=payload.validity_date,
            total_amount=total_amount,
            status="ACTIVE",
        )

        for it in payload.items:
            structure.items.append(
                FeeStructureItem(
                    fee_head_id=it.fee_head_id,
                    amount=it.amount,
                    is_optional=it.is_optional,
                    frequency=it.frequency,
                    due_period=it.due_period,
                )
            )

        if payload.installments_plan:
            for inst in payload.installments_plan:
                inst_amount = round((total_amount * inst.percentage) / 100.0, 2)
                structure.installments.append(
                    Installment(
                        installment_number=inst.installment_number,
                        title=inst.title,
                        due_date=inst.due_date,
                        percentage=inst.percentage,
                        amount=inst_amount,
                        grace_days=inst.grace_days,
                        late_fee_rule_id=inst.late_fee_rule_id,
                    )
                )

        return await self.repo.create_fee_structure(structure)

    async def list_fee_structures(self, institute_id: uuid.UUID) -> List[FeeStructure]:
        return await self.repo.get_fee_structures(institute_id)

    # 3. Student Fee Assignment
    async def assign_fee_to_student(self, payload: StudentFeeAssignmentCreate) -> StudentFeeAssignment:
        structure = await self.repo.get_fee_structure_by_id(payload.fee_structure_id)
        if not structure:
            raise NotFoundException("Fee structure not found.")

        total_fee = structure.total_amount
        assignment = StudentFeeAssignment(
            student_id=payload.student_id,
            fee_structure_id=payload.fee_structure_id,
            institute_id=payload.institute_id,
            branch_id=payload.branch_id,
            academic_year_id=payload.academic_year_id,
            total_fee_amount=total_fee,
            total_discount_amount=0.0,
            total_scholarship_amount=0.0,
            total_payable_amount=total_fee,
            total_paid_amount=0.0,
            total_due_amount=total_fee,
            assignment_type=payload.assignment_type,
            status="PENDING",
        )
        return await self.repo.create_assignment(assignment)

    # 4. Concessions & Scholarships Application
    async def apply_concession(self, payload: ConcessionApplyRequest) -> Concession:
        assignment = await self.repo.get_student_assignment(payload.student_fee_assignment_id)
        if not assignment:
            raise NotFoundException("Student fee assignment not found.")

        if payload.amount > assignment.total_due_amount:
            raise ValidationException(
                f"Concession amount ({payload.amount}) cannot exceed current outstanding due ({assignment.total_due_amount})."
            )

        concession = Concession(
            student_fee_assignment_id=payload.student_fee_assignment_id,
            student_id=payload.student_id,
            scholarship_id=payload.scholarship_id,
            discount_id=payload.discount_id,
            concession_type=payload.concession_type,
            amount=payload.amount,
            reason=payload.reason,
            approval_status="APPROVED",
        )

        if payload.concession_type == "SCHOLARSHIP":
            assignment.total_scholarship_amount += payload.amount
        else:
            assignment.total_discount_amount += payload.amount

        assignment.total_payable_amount = max(0.0, assignment.total_fee_amount - (assignment.total_scholarship_amount + assignment.total_discount_amount))
        assignment.total_due_amount = max(0.0, assignment.total_payable_amount - assignment.total_paid_amount)
        if assignment.total_due_amount == 0.0 and assignment.total_paid_amount > 0:
            assignment.status = "PAID"

        await self.repo.update_assignment(assignment)
        return await self.repo.create_concession(concession)

    # 5. Payment Processing & Receipt Generation
    async def collect_payment(self, payload: PaymentCreate, user_id: Optional[uuid.UUID] = None) -> Payment:
        assignment = await self.repo.get_student_assignment(payload.student_fee_assignment_id)
        if not assignment:
            raise NotFoundException("Student fee assignment not found.")

        if payload.amount_paid > assignment.total_due_amount:
            raise ValidationException(
                f"Amount paid ({payload.amount_paid}) exceeds remaining due ({assignment.total_due_amount})."
            )

        payment_no = f"PAY-{uuid.uuid4().hex[:10].upper()}"
        pay_date = payload.payment_date or date.today()

        payment = Payment(
            student_fee_assignment_id=payload.student_fee_assignment_id,
            student_id=payload.student_id,
            installment_id=payload.installment_id,
            payment_number=payment_no,
            amount_paid=payload.amount_paid,
            payment_mode=payload.payment_mode,
            payment_method_id=payload.payment_method_id,
            transaction_reference=payload.transaction_reference,
            cheque_dd_number=payload.cheque_dd_number,
            bank_name=payload.bank_name,
            payment_date=pay_date,
            status="COMPLETED",
            remarks=payload.remarks,
            created_by_user_id=user_id,
        )
        saved_payment = await self.repo.record_payment(payment)

        # Update assignment balance
        assignment.total_paid_amount += payload.amount_paid
        assignment.total_due_amount = max(0.0, assignment.total_payable_amount - assignment.total_paid_amount)
        assignment.status = "PAID" if assignment.total_due_amount == 0.0 else "PARTIAL"
        await self.repo.update_assignment(assignment)

        # Generate Receipt
        receipt_no = ReceiptGenerator.generate_receipt_number()
        words = number_to_indian_currency_words(payload.amount_paid)
        qr_data = ReceiptGenerator.generate_qr_payload(receipt_no, payload.amount_paid, str(payload.student_id), str(pay_date))
        sig_hash = ReceiptGenerator.generate_digital_signature(receipt_no, payload.amount_paid, str(payload.student_id))

        receipt = Receipt(
            receipt_number=receipt_no,
            payment_id=saved_payment.id,
            student_id=payload.student_id,
            institute_id=assignment.institute_id,
            academic_year_id=assignment.academic_year_id,
            total_amount=payload.amount_paid,
            amount_in_words=words,
            qr_code_data=qr_data,
            barcode_data=receipt_no.replace("-", ""),
            digital_signature_hash=sig_hash,
            receipt_date=pay_date,
            status="GENERATED",
            generated_by_user_id=user_id,
        )
        await self.repo.create_receipt(receipt)

        return saved_payment

    # 6. Refunds
    async def process_refund(self, payload: RefundRequest, user_id: Optional[uuid.UUID] = None) -> Refund:
        refund_no = f"REF-{uuid.uuid4().hex[:10].upper()}"
        refund = Refund(
            payment_id=payload.payment_id,
            student_id=payload.student_id,
            institute_id=payload.institute_id,
            refund_number=refund_no,
            amount=payload.amount,
            refund_type=payload.refund_type,
            reason=payload.reason,
            approval_status="APPROVED",
            approved_by_user_id=user_id,
            payment_mode=payload.payment_mode,
            reference_number=payload.reference_number,
            processed_at=datetime.now(timezone.utc),
        )
        return await self.repo.create_refund(refund)

    # 7. Catalogs
    async def create_scholarship(self, payload: ScholarshipCreate) -> Scholarship:
        item = Scholarship(
            institute_id=payload.institute_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            scholarship_type=payload.scholarship_type,
            calculation_type=payload.calculation_type,
            value=payload.value,
            eligibility_criteria=payload.eligibility_criteria,
            max_beneficiaries=payload.max_beneficiaries,
        )
        return await self.repo.create_scholarship(item)

    async def list_scholarships(self, institute_id: uuid.UUID) -> List[Scholarship]:
        return await self.repo.get_scholarships(institute_id)

    async def create_discount(self, payload: DiscountCreate) -> Discount:
        item = Discount(
            institute_id=payload.institute_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            discount_type=payload.discount_type,
            calculation_type=payload.calculation_type,
            value=payload.value,
            max_discount_amount=payload.max_discount_amount,
        )
        return await self.repo.create_discount(item)

    async def list_discounts(self, institute_id: uuid.UUID) -> List[Discount]:
        return await self.repo.get_discounts(institute_id)

    async def create_late_fee_rule(self, payload: LateFeeRuleCreate) -> LateFeeRule:
        rule = LateFeeRule(
            institute_id=payload.institute_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            calculation_type=payload.calculation_type,
            rate=payload.rate,
            maximum_limit=payload.maximum_limit,
            grace_period_days=payload.grace_period_days,
        )
        return await self.repo.create_late_fee_rule(rule)

    async def list_late_fee_rules(self, institute_id: uuid.UUID) -> List[LateFeeRule]:
        return await self.repo.get_late_fee_rules(institute_id)
