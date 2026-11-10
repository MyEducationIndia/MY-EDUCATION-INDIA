from datetime import date
from typing import List
from app.core.exceptions import ValidationException
from app.modules.fees.schemas import FeeStructureItemCreate, InstallmentPlanInput


class FeeBusinessValidators:
    @staticmethod
    def validate_structure_dates(effective_date: date, validity_date: date) -> None:
        if effective_date >= validity_date:
            raise ValidationException("Effective date must precede the validity expiry date.")

    @staticmethod
    def validate_structure_items(items: List[FeeStructureItemCreate]) -> float:
        if not items:
            raise ValidationException("A fee structure must contain at least one fee head item.")
        total = 0.0
        seen_heads = set()
        for item in items:
            if item.fee_head_id in seen_heads:
                raise ValidationException("Duplicate fee head detected in fee structure items.")
            seen_heads.add(item.fee_head_id)
            total += item.amount
        return round(total, 2)

    @staticmethod
    def validate_installment_percentages(installments: List[InstallmentPlanInput]) -> None:
        if not installments:
            return
        total_pct = sum(inst.percentage for inst in installments)
        if abs(total_pct - 100.0) > 0.01:
            raise ValidationException(f"Installment percentages must sum to 100.0%. Current sum: {total_pct}%")

    @staticmethod
    def validate_refund_eligibility(payment_amount: float, requested_refund: float, already_refunded: float) -> None:
        if requested_refund <= 0:
            raise ValidationException("Refund amount must be strictly greater than 0.")
        if (already_refunded + requested_refund) > payment_amount:
            raise ValidationException(
                f"Requested refund (INR {requested_refund}) exceeds refundable balance (INR {payment_amount - already_refunded})."
            )
