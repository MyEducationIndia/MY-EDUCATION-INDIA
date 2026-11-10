from typing import Any, Dict, List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.admissions.models import AdmissionFeeReceipt, Application, Lead


class AdmissionReportService:
    """Generates structured tabular reports across lead channels, counselors, and conversion stages."""

    @staticmethod
    async def generate_lead_source_summary(session: AsyncSession, institute_id) -> List[Dict[str, Any]]:
        stmt = (
            select(Lead.source_channel, func.count(Lead.id), func.avg(Lead.score))
            .where(Lead.institute_id == institute_id)
            .group_by(Lead.source_channel)
        )
        res = await session.execute(stmt)
        return [
            {
                "source": row[0],
                "lead_count": int(row[1]),
                "average_score": round(float(row[2] or 0), 1),
            }
            for row in res.all()
        ]

    @staticmethod
    async def generate_admission_status_summary(session: AsyncSession, institute_id) -> List[Dict[str, Any]]:
        stmt = (
            select(Application.status, func.count(Application.id))
            .where(Application.institute_id == institute_id)
            .group_by(Application.status)
        )
        res = await session.execute(stmt)
        return [{"status": row[0], "count": int(row[1])} for row in res.all()]
