from datetime import date
from typing import Any, Dict, List
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.fees.models import Payment, Refund, StudentFeeAssignment


class FinancialReportEngine:
    """Generates structured multi-dimensional financial ledgers and collection reports."""

    @staticmethod
    async def get_daily_collection_report(
        session: AsyncSession,
        institute_id: uuid.UUID,
        target_date: date,
    ) -> Dict[str, Any]:
        stmt = select(
            Payment.payment_mode,
            func.count(Payment.id).label("transaction_count"),
            func.sum(Payment.amount_paid).label("total_amount"),
        ).join(StudentFeeAssignment, Payment.student_fee_assignment_id == StudentFeeAssignment.id).where(
            StudentFeeAssignment.institute_id == institute_id,
            Payment.payment_date == target_date,
            Payment.status == "COMPLETED",
        ).group_by(Payment.payment_mode)

        res = await session.execute(stmt)
        rows = res.all()

        breakdown = []
        grand_total = 0.0
        total_tx = 0
        for mode, count, amount in rows:
            amt = float(amount or 0.0)
            breakdown.append({
                "payment_mode": mode,
                "count": count,
                "total_amount": amt,
            })
            grand_total += amt
            total_tx += count

        return {
            "report_type": "DAILY_COLLECTION",
            "date": str(target_date),
            "institute_id": str(institute_id),
            "total_transactions": total_tx,
            "grand_total": round(grand_total, 2),
            "breakdown": breakdown,
        }

    @staticmethod
    async def get_outstanding_dues_report(
        session: AsyncSession,
        institute_id: uuid.UUID,
        course_id: uuid.UUID = None,
    ) -> Dict[str, Any]:
        stmt = select(
            StudentFeeAssignment.id,
            StudentFeeAssignment.student_id,
            StudentFeeAssignment.total_payable_amount,
            StudentFeeAssignment.total_paid_amount,
            StudentFeeAssignment.total_due_amount,
            StudentFeeAssignment.status,
        ).where(
            StudentFeeAssignment.institute_id == institute_id,
            StudentFeeAssignment.total_due_amount > 0.0,
        )

        res = await session.execute(stmt)
        assignments = res.all()

        total_due_accumulated = sum(float(a[4] or 0.0) for a in assignments)

        return {
            "report_type": "OUTSTANDING_DUES",
            "institute_id": str(institute_id),
            "total_students_with_dues": len(assignments),
            "total_outstanding_amount": round(total_due_accumulated, 2),
            "records": [
                {
                    "assignment_id": str(a[0]),
                    "student_id": str(a[1]),
                    "total_payable": float(a[2]),
                    "total_paid": float(a[3]),
                    "total_due": float(a[4]),
                    "status": a[5],
                }
                for a in assignments[:100] # Top 100
            ],
        }
