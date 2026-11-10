from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.fees.models import (
    Concession,
    Discount,
    FeeCategory,
    FeeHead,
    FeeStructure,
    Installment,
    LateFeeRule,
    Payment,
    Receipt,
    Refund,
    Scholarship,
    StudentFeeAssignment,
)


class FeeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # Categories & Heads
    async def get_categories(self, institute_id: uuid.UUID) -> List[FeeCategory]:
        stmt = select(FeeCategory).where(FeeCategory.institute_id == institute_id).order_by(FeeCategory.name)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_category_by_id(self, category_id: uuid.UUID) -> Optional[FeeCategory]:
        return await self.session.get(FeeCategory, category_id)

    async def create_category(self, category: FeeCategory) -> FeeCategory:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def get_fee_heads(self, institute_id: uuid.UUID, category_id: Optional[uuid.UUID] = None) -> List[FeeHead]:
        stmt = select(FeeHead).where(FeeHead.institute_id == institute_id)
        if category_id:
            stmt = stmt.where(FeeHead.category_id == category_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_fee_head(self, head: FeeHead) -> FeeHead:
        self.session.add(head)
        await self.session.commit()
        await self.session.refresh(head)
        return head

    # Fee Structures
    async def get_fee_structures(self, institute_id: uuid.UUID) -> List[FeeStructure]:
        stmt = (
            select(FeeStructure)
            .where(FeeStructure.institute_id == institute_id)
            .options(selectinload(FeeStructure.items), selectinload(FeeStructure.installments))
            .order_by(FeeStructure.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_fee_structure_by_id(self, structure_id: uuid.UUID) -> Optional[FeeStructure]:
        stmt = (
            select(FeeStructure)
            .where(FeeStructure.id == structure_id)
            .options(selectinload(FeeStructure.items), selectinload(FeeStructure.installments))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_fee_structure(self, structure: FeeStructure) -> FeeStructure:
        self.session.add(structure)
        await self.session.commit()
        await self.session.refresh(structure)
        return structure

    # Student Fee Assignment
    async def get_student_assignment(self, assignment_id: uuid.UUID) -> Optional[StudentFeeAssignment]:
        stmt = (
            select(StudentFeeAssignment)
            .where(StudentFeeAssignment.id == assignment_id)
            .options(selectinload(StudentFeeAssignment.payments), selectinload(StudentFeeAssignment.concessions))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_assignment(self, assignment: StudentFeeAssignment) -> StudentFeeAssignment:
        self.session.add(assignment)
        await self.session.commit()
        await self.session.refresh(assignment)
        return assignment

    async def update_assignment(self, assignment: StudentFeeAssignment) -> StudentFeeAssignment:
        await self.session.commit()
        await self.session.refresh(assignment)
        return assignment

    # Payments & Receipts
    async def record_payment(self, payment: Payment) -> Payment:
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def create_receipt(self, receipt: Receipt) -> Receipt:
        self.session.add(receipt)
        await self.session.commit()
        await self.session.refresh(receipt)
        return receipt

    async def get_receipt_by_payment(self, payment_id: uuid.UUID) -> Optional[Receipt]:
        stmt = select(Receipt).where(Receipt.payment_id == payment_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # Scholarships & Discounts
    async def get_scholarships(self, institute_id: uuid.UUID) -> List[Scholarship]:
        stmt = select(Scholarship).where(Scholarship.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_scholarship(self, scholarship: Scholarship) -> Scholarship:
        self.session.add(scholarship)
        await self.session.commit()
        await self.session.refresh(scholarship)
        return scholarship

    async def get_discounts(self, institute_id: uuid.UUID) -> List[Discount]:
        stmt = select(Discount).where(Discount.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_discount(self, discount: Discount) -> Discount:
        self.session.add(discount)
        await self.session.commit()
        await self.session.refresh(discount)
        return discount

    async def create_concession(self, concession: Concession) -> Concession:
        self.session.add(concession)
        await self.session.commit()
        await self.session.refresh(concession)
        return concession

    # Late Fees & Refunds
    async def get_late_fee_rules(self, institute_id: uuid.UUID) -> List[LateFeeRule]:
        stmt = select(LateFeeRule).where(LateFeeRule.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_late_fee_rule(self, rule: LateFeeRule) -> LateFeeRule:
        self.session.add(rule)
        await self.session.commit()
        await self.session.refresh(rule)
        return rule

    async def create_refund(self, refund: Refund) -> Refund:
        self.session.add(refund)
        await self.session.commit()
        await self.session.refresh(refund)
        return refund
