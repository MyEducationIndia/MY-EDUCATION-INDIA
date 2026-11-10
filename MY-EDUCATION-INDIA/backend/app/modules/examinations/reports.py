from typing import Any, Dict, List
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.examinations.models import Result


class ExamReportEngine:
    @staticmethod
    async def get_merit_list(
        session: AsyncSession,
        exam_session_id: uuid.UUID,
        top_n: int = 10,
    ) -> List[Dict[str, Any]]:
        stmt = (
            select(Result)
            .where(
                Result.exam_session_id == exam_session_id,
                Result.status == "PASSED",
            )
            .order_by(Result.cgpa.desc())
            .limit(top_n)
        )
        res = await session.execute(stmt)
        records = res.scalars().all()

        merit = []
        for idx, r in enumerate(records, start=1):
            merit.append({
                "rank": idx,
                "student_id": str(r.student_id),
                "cgpa": r.cgpa,
                "percentage": r.percentage,
                "classification": r.classification,
            })
        return merit
