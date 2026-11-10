from typing import Any, Dict, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.cbt.models import CandidateAnswer, CandidateSession


class CBTReportEngine:
    @staticmethod
    async def get_candidate_score_report(
        session: AsyncSession,
        candidate_session_id: uuid.UUID,
    ) -> Dict[str, Any]:
        cand = await session.get(CandidateSession, candidate_session_id)
        if not cand:
            return {}

        stmt = select(CandidateAnswer).where(CandidateAnswer.candidate_session_id == candidate_session_id)
        res = await session.execute(stmt)
        answers = res.scalars().all()

        correct = sum(1 for a in answers if a.is_correct is True)
        incorrect = sum(1 for a in answers if a.is_correct is False)
        unanswered = sum(1 for a in answers if a.is_correct is None)

        return {
            "candidate_session_id": str(candidate_session_id),
            "student_id": str(cand.student_id),
            "total_questions": len(answers),
            "correct_count": correct,
            "incorrect_count": incorrect,
            "unanswered_count": unanswered,
            "total_score": cand.total_score,
            "status": cand.status,
            "marks_synced_to_module11": cand.marks_synced_to_module11,
        }
