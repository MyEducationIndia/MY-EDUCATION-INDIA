from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.examinations.models import (
    ExamSchedule,
    ExamSession,
    ExamSubject,
    ExamType,
    GradeScale,
    HallTicket,
    MarkEntry,
    Result,
    Transcript,
)


class ExaminationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # Types & Sessions
    async def create_exam_type(self, item: ExamType) -> ExamType:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_exam_types(self, institute_id: uuid.UUID) -> List[ExamType]:
        stmt = select(ExamType).where(ExamType.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_exam_session(self, sess: ExamSession) -> ExamSession:
        self.session.add(sess)
        await self.session.commit()
        await self.session.refresh(sess)
        return sess

    async def get_exam_sessions(self, institute_id: uuid.UUID) -> List[ExamSession]:
        stmt = select(ExamSession).where(ExamSession.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_exam_session_by_id(self, session_id: uuid.UUID) -> Optional[ExamSession]:
        stmt = select(ExamSession).where(ExamSession.id == session_id).options(selectinload(ExamSession.schedules))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # Schedules & Subjects
    async def create_exam_schedule(self, sched: ExamSchedule) -> ExamSchedule:
        self.session.add(sched)
        await self.session.commit()
        await self.session.refresh(sched)
        return sched

    async def get_exam_subject(self, exam_subject_id: uuid.UUID) -> Optional[ExamSubject]:
        return await self.session.get(ExamSubject, exam_subject_id)

    # Marks
    async def save_mark_entry(self, entry: MarkEntry) -> MarkEntry:
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def get_marks_for_subject(self, exam_subject_id: uuid.UUID) -> List[MarkEntry]:
        stmt = select(MarkEntry).where(MarkEntry.exam_subject_id == exam_subject_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # Results & Transcripts
    async def save_result(self, res_obj: Result) -> Result:
        self.session.add(res_obj)
        await self.session.commit()
        await self.session.refresh(res_obj)
        return res_obj

    async def get_results_by_session(self, session_id: uuid.UUID) -> List[Result]:
        stmt = select(Result).where(Result.exam_session_id == session_id).order_by(Result.percentage.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def save_transcript(self, t: Transcript) -> Transcript:
        self.session.add(t)
        await self.session.commit()
        await self.session.refresh(t)
        return t
