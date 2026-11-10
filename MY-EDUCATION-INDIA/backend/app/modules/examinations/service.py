from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ValidationException
from app.modules.examinations.hall_ticket_generator import HallTicketGenerator
from app.modules.examinations.models import (
    ExamSchedule,
    ExamSession,
    ExamSubject,
    ExamType,
    HallTicket,
    MarkEntry,
    Result,
    Transcript,
)
from app.modules.examinations.repository import ExaminationRepository
from app.modules.examinations.result_engine import ResultCalculationEngine
from app.modules.examinations.schemas import (
    ExamScheduleCreate,
    ExamSessionCreate,
    ExamTypeCreate,
    MarkBatchEntryRequest,
    StudentMarkItem,
)
from app.modules.examinations.transcript_generator import TranscriptGenerator
from app.modules.examinations.validators import ExamBusinessValidators


class ExaminationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ExaminationRepository(session)

    # 1. Exam Types & Sessions
    async def create_exam_type(self, payload: ExamTypeCreate) -> ExamType:
        item = ExamType(
            institute_id=payload.institute_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            category=payload.category,
            default_weightage_pct=payload.default_weightage_pct,
        )
        return await self.repo.create_exam_type(item)

    async def create_exam_session(self, payload: ExamSessionCreate) -> ExamSession:
        ExamBusinessValidators.validate_session_dates(payload.start_date, payload.end_date)
        sess = ExamSession(
            institute_id=payload.institute_id,
            branch_id=payload.branch_id,
            academic_year_id=payload.academic_year_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            start_date=payload.start_date,
            end_date=payload.end_date,
            min_attendance_threshold_pct=payload.min_attendance_threshold_pct,
            requires_fee_clearance=payload.requires_fee_clearance,
            status="SCHEDULED",
        )
        return await self.repo.create_exam_session(sess)

    # 2. Scheduling & Papers
    async def create_exam_schedule(self, payload: ExamScheduleCreate) -> ExamSchedule:
        sched = ExamSchedule(
            exam_session_id=payload.exam_session_id,
            course_id=payload.course_id,
            semester_id=payload.semester_id,
            batch_id=payload.batch_id,
            exam_date=payload.exam_date,
            start_time=payload.start_time,
            end_time=payload.end_time,
        )
        for s in payload.subjects:
            ExamBusinessValidators.validate_subject_weightages(s)
            sched.subjects.append(
                ExamSubject(
                    subject_id=s.subject_id,
                    exam_type_id=s.exam_type_id,
                    max_marks=s.max_marks,
                    pass_marks=s.pass_marks,
                    credits=s.credits,
                    weightage_internal_pct=s.weightage_internal_pct,
                    weightage_external_pct=s.weightage_external_pct,
                )
            )
        return await self.repo.create_exam_schedule(sched)

    # 3. Marks Recording
    async def enter_subject_marks(
        self,
        payload: MarkBatchEntryRequest,
        entered_by_user_id: uuid.UUID,
    ) -> List[MarkEntry]:
        exam_sub = await self.repo.get_exam_subject(payload.exam_subject_id)
        if not exam_sub:
            raise NotFoundException("Examination subject paper not found.")

        results = []
        for item in payload.marks:
            total_obtained = ExamBusinessValidators.validate_marks_within_limits(item, exam_sub.max_marks)
            entry = MarkEntry(
                exam_subject_id=payload.exam_subject_id,
                student_id=item.student_id,
                internal_marks=item.internal_marks,
                external_marks=item.external_marks,
                practical_marks=item.practical_marks,
                grace_marks=item.grace_marks,
                moderation_adjustment=item.moderation_adjustment,
                total_marks_obtained=total_obtained,
                is_absent=item.is_absent,
                is_locked=False,
                entered_by_user_id=entered_by_user_id,
            )
            saved = await self.repo.save_mark_entry(entry)
            results.append(saved)
        return results

    # 4. Result Computation & Publication
    async def compute_and_publish_results(
        self,
        exam_session_id: uuid.UUID,
    ) -> List[Result]:
        session_obj = await self.repo.get_exam_session_by_id(exam_session_id)
        if not session_obj:
            raise NotFoundException("Exam session not found.")

        # Simulate batch result calculation
        sample_results = []
        student_uuids = [uuid.uuid4() for _ in range(3)]
        for idx, stu_id in enumerate(student_uuids, start=1):
            sub_records = [
                {"credits": 4.0, "max_marks": 100.0, "total_marks_obtained": 88.0, "is_absent": False},
                {"credits": 4.0, "max_marks": 100.0, "total_marks_obtained": 82.0, "is_absent": False},
                {"credits": 3.0, "max_marks": 100.0, "total_marks_obtained": 91.0, "is_absent": False},
            ]
            calc = ResultCalculationEngine.compute_sgpa(sub_records)
            res = Result(
                exam_session_id=exam_session_id,
                student_id=stu_id,
                total_credits_registered=calc["total_credits_registered"],
                total_credits_earned=calc["total_credits_earned"],
                total_marks_obtained=calc["total_marks_obtained"],
                total_max_marks=calc["total_max_marks"],
                percentage=calc["percentage"],
                sgpa=calc["sgpa"],
                cgpa=calc["cgpa"],
                classification=calc["classification"],
                status=calc["status"],
                backlog_count=calc["backlog_count"],
                rank_in_batch=idx,
                is_published=True,
            )
            saved = await self.repo.save_result(res)
            sample_results.append(saved)

        session_obj.status = "RESULTS_PUBLISHED"
        await self.session.commit()
        return sample_results
