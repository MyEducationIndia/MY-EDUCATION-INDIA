import uuid
from datetime import date, datetime, time, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ExamType(Base):
    __tablename__ = "exam_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False) # SEMESTER, MID_TERM, UNIT_TEST, PRACTICAL, VIVA, PROJECT, CBT
    category: Mapped[str] = mapped_column(String(32), default="EXTERNAL", nullable=False) # INTERNAL, EXTERNAL, CONTINUOUS_EVALUATION
    default_weightage_pct: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExamSession(Base):
    __tablename__ = "exam_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(48), nullable=False, index=True) # e.g. NOV-DEC-2026-MAIN
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="SCHEDULED", nullable=False) # SCHEDULED, ONGOING, COMPLETED, RESULTS_PUBLISHED
    min_attendance_threshold_pct: Mapped[float] = mapped_column(Float, default=75.0, nullable=False)
    requires_fee_clearance: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    schedules: Mapped[List["ExamSchedule"]] = relationship("ExamSchedule", back_populates="exam_session", cascade="all, delete-orphan")


class ExamSchedule(Base):
    __tablename__ = "exam_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    semester_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    batch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    exam_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    exam_session: Mapped["ExamSession"] = relationship("ExamSession", back_populates="schedules")
    subjects: Mapped[List["ExamSubject"]] = relationship("ExamSubject", back_populates="schedule", cascade="all, delete-orphan")
    hall_tickets: Mapped[List["HallTicket"]] = relationship("HallTicket", back_populates="schedule", cascade="all, delete-orphan")


class ExamSubject(Base):
    __tablename__ = "exam_subjects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    exam_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_types.id", ondelete="RESTRICT"), nullable=False, index=True)
    max_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    pass_marks: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    credits: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    weightage_internal_pct: Mapped[float] = mapped_column(Float, default=30.0, nullable=False)
    weightage_external_pct: Mapped[float] = mapped_column(Float, default=70.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    schedule: Mapped["ExamSchedule"] = relationship("ExamSchedule", back_populates="subjects")
    mark_entries: Mapped[List["MarkEntry"]] = relationship("MarkEntry", back_populates="exam_subject", cascade="all, delete-orphan")


class HallTicket(Base):
    __tablename__ = "hall_tickets"
    __table_args__ = (
        UniqueConstraint("schedule_id", "student_id", name="uq_hall_ticket_student_schedule"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hall_ticket_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    schedule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    assigned_classroom_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    seat_number: Mapped[str] = mapped_column(String(32), nullable=False)
    qr_verification_token: Mapped[str] = mapped_column(Text, nullable=False)
    barcode_data: Mapped[str] = mapped_column(String(64), nullable=False)
    is_eligible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    ineligibility_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(24), default="ISSUED", nullable=False) # ISSUED, WITHHELD, CANCELLED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    schedule: Mapped["ExamSchedule"] = relationship("ExamSchedule", back_populates="hall_tickets")


class SeatingPlan(Base):
    __tablename__ = "seating_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    classroom_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    allocated_students_count: Mapped[int] = mapped_column(Integer, nullable=False)
    seat_matrix_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InvigilatorAssignment(Base):
    __tablename__ = "invigilators"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    classroom_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    faculty_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(32), default="PRIMARY_INVIGILATOR", nullable=False) # PRIMARY_INVIGILATOR, RELIEVER, SQUAD
    status: Mapped[str] = mapped_column(String(24), default="CONFIRMED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class MarkEntry(Base):
    __tablename__ = "mark_entries"
    __table_args__ = (
        UniqueConstraint("exam_subject_id", "student_id", name="uq_mark_entry_subject_student"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    internal_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    external_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    practical_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    grace_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    moderation_adjustment: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_marks_obtained: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_absent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    entered_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    exam_subject: Mapped["ExamSubject"] = relationship("ExamSubject", back_populates="mark_entries")


class GradeScale(Base):
    __tablename__ = "grade_scales"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    scale_name: Mapped[str] = mapped_column(String(64), default="UGC_10_POINT", nullable=False) # UGC_10_POINT, AICTE_ABSOLUTE, CBCS
    letter_grade: Mapped[str] = mapped_column(String(8), nullable=False) # O, A+, A, B+, B, C, P, F
    grade_point: Mapped[float] = mapped_column(Float, nullable=False)
    min_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    max_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(64), nullable=False)
    is_passing_grade: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class GradeRule(Base):
    __tablename__ = "grade_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    min_pass_percentage: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    grace_marks_limit: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    max_backlogs_allowed_for_promotion: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    distinction_threshold_cgpa: Mapped[float] = mapped_column(Float, default=8.5, nullable=False)
    first_division_threshold_cgpa: Mapped[float] = mapped_column(Float, default=6.5, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResultRule(Base):
    __tablename__ = "result_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    exam_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    publish_status: Mapped[str] = mapped_column(String(24), default="DRAFT", nullable=False) # DRAFT, APPROVED, PUBLISHED, WITHHELD
    publish_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class Result(Base):
    __tablename__ = "results"
    __table_args__ = (
        UniqueConstraint("exam_session_id", "student_id", name="uq_result_session_student"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    total_credits_registered: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_credits_earned: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_marks_obtained: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_max_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sgpa: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cgpa: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    classification: Mapped[str] = mapped_column(String(48), default="FIRST_CLASS", nullable=False) # DISTINCTION, FIRST_CLASS, SECOND_CLASS, PASS_CLASS, FAILED
    status: Mapped[str] = mapped_column(String(24), default="PASSED", nullable=False) # PASSED, FAILED, PROMOTED_WITH_BACKLOG, DETAINED
    backlog_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rank_in_batch: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class Transcript(Base):
    __tablename__ = "transcripts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transcript_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    transcript_type: Mapped[str] = mapped_column(String(32), default="SEMESTER_GRADE_CARD", nullable=False) # SEMESTER_GRADE_CARD, CONSOLIDATED_TRANSCRIPT
    academic_data_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    final_cgpa: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    digital_signature_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    qr_code_payload: Mapped[Text] = mapped_column(Text, nullable=False)
    issued_date: Mapped[date] = mapped_column(Date, nullable=False)
    issued_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RevaluationRequest(Base):
    __tablename__ = "revaluation_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    exam_subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    original_marks: Mapped[float] = mapped_column(Float, nullable=False)
    revised_marks: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    fee_paid: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="APPLIED", nullable=False) # APPLIED, UNDER_REVIEW, UPDATED, REJECTED
    reviewed_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SupplementaryExam(Base):
    __tablename__ = "supplementary_exams"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    backlog_semester_number: Mapped[int] = mapped_column(Integer, nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_cleared: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class MeritList(Base):
    __tablename__ = "merit_lists"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    cgpa_or_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RankList(Base):
    __tablename__ = "rank_lists"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    batch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    batch_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    sgpa: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExamReport(Base):
    __tablename__ = "exam_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True) # PASS_FAIL_ANALYSIS, SUBJECT_DIFFICULTY, MERIT_ROSTER
    parameters_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    generated_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 4 Module 1: EMS Dashboard Models -------------------
class EMSDashboardConfig(Base):
    __tablename__ = "ems_dashboard_configs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    role_name: Mapped[str] = mapped_column(String(48), nullable=False, index=True)  # ROOT_OWNER, SUPER_ADMIN, CONTROLLER_OF_EXAMINATION, PRINCIPAL, HOD, FACULTY, EVALUATOR, STUDENT
    pinned_widgets_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    default_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    refresh_interval_seconds: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 4 Module 2: Academic Examination Structure Models -------------------
class AcademicSession(Base):
    __tablename__ = "academic_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    session_code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="ACTIVE", nullable=False)  # PLANNING, ACTIVE, COMPLETED, ARCHIVED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    semesters: Mapped[List["AcademicSemester"]] = relationship("AcademicSemester", back_populates="session", cascade="all, delete-orphan")


class AcademicSemester(Base):
    __tablename__ = "academic_semesters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    academic_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("academic_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    semester_code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    semester_type: Mapped[str] = mapped_column(String(24), default="ODD", nullable=False)  # ODD, EVEN, SUMMER, TRIMESTER
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    session: Mapped["AcademicSession"] = relationship("AcademicSession", back_populates="semesters")


class AssessmentComponentType(Base):
    __tablename__ = "assessment_component_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)  # ANNUAL_EXAM, SEMESTER_FINAL, MID_SEMESTER, INTERNAL_CONTINUOUS, UNIT_TEST, PRACTICAL_EXAM, VIVA_VOCE, ASSIGNMENT_EVALUATION, CAPSTONE_PROJECT, UNIVERSITY_EXTERNAL
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    modality: Mapped[str] = mapped_column(String(48), default="THEORY_OFFLINE", nullable=False)  # THEORY_OFFLINE, THEORY_ONLINE, PRACTICAL_LAB, ORAL_VIVA, CONTINUOUS_SUBMISSION, EXTERNAL_BOARD
    default_max_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    default_pass_percentage: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    default_weightage_percentage: Mapped[float] = mapped_column(Float, default=30.0, nullable=False)
    requires_rubric: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_external_examiner: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CourseAssessmentWeightageScheme(Base):
    __tablename__ = "course_weightage_schemes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    academic_semester_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("academic_semesters.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    scheme_name: Mapped[str] = mapped_column(String(180), nullable=False)
    components_weightage_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    total_weightage: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    minimum_aggregate_pass_pct: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    approved_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 4 Module 3: Exam Planning Models -------------------
class ExamDepartmentPlan(Base):
    __tablename__ = "exam_department_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    department_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    plan_code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    department_name: Mapped[str] = mapped_column(String(120), nullable=False)
    head_of_department_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    total_courses_planned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_candidates_eligible: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT", nullable=False)  # DRAFT, SUBMITTED, APPROVED_BY_COE, SCHEDULED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    mappings: Mapped[List["ExamCourseMapping"]] = relationship("ExamCourseMapping", back_populates="plan", cascade="all, delete-orphan")


class ExamTimeSlot(Base):
    __tablename__ = "exam_time_slots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    slot_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=180, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExamCourseMapping(Base):
    __tablename__ = "exam_course_mappings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_department_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False)
    course_title: Mapped[str] = mapped_column(String(180), nullable=False)
    component_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("assessment_component_types.id", ondelete="SET NULL"), nullable=True, index=True)
    component_code: Mapped[str] = mapped_column(String(48), default="SEMESTER_FINAL", nullable=False)
    paper_code: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    max_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    passing_marks: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=180, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    plan: Mapped["ExamDepartmentPlan"] = relationship("ExamDepartmentPlan", back_populates="mappings")


class ExamRoomPlanning(Base):
    __tablename__ = "exam_room_plannings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    center_code: Mapped[str] = mapped_column(String(32), default="TC-IND-01", nullable=False)
    building_name: Mapped[str] = mapped_column(String(120), nullable=False)
    room_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    room_type: Mapped[str] = mapped_column(String(32), default="EXAM_HALL", nullable=False)  # EXAM_HALL, CLASSROOM, COMPUTER_LAB, SEMINAR_HALL
    bench_count: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    seats_per_bench: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    total_capacity: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    buffer_seats: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExamFacultyDutyPlanning(Base):
    __tablename__ = "exam_faculty_duty_plannings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    faculty_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    faculty_name: Mapped[str] = mapped_column(String(120), nullable=False)
    department_name: Mapped[str] = mapped_column(String(120), nullable=False)
    duty_type: Mapped[str] = mapped_column(String(32), default="ROOM_INVIGILATOR", nullable=False)  # CHIEF_SUPERINTENDENT, ROOM_INVIGILATOR, RELIEVER, PAPER_SETTER, SQUAD_MEMBER
    assigned_room_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_room_plannings.id", ondelete="SET NULL"), nullable=True, index=True)
    assigned_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    slot_code: Mapped[str] = mapped_column(String(32), default="SLOT-MORNING-A", nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="ALLOCATED", nullable=False)  # ALLOCATED, CONFIRMED, REPLACED, ABSENT
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExamTimetableSchedule(Base):
    __tablename__ = "exam_timetable_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    department_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    department_name: Mapped[str] = mapped_column(String(120), nullable=False)
    semester_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("academic_semesters.id", ondelete="SET NULL"), nullable=True, index=True)
    semester_code: Mapped[str] = mapped_column(String(32), default="SEM-5", nullable=False)
    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    course_title: Mapped[str] = mapped_column(String(180), nullable=False)
    paper_code: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    component_type: Mapped[str] = mapped_column(String(48), default="THEORY_OFFLINE", nullable=False)
    is_practical: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    batch_name: Mapped[str] = mapped_column(String(48), default="ALL", nullable=False)  # ALL, BATCH-A1, BATCH-A2
    exam_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    time_slot_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_time_slots.id", ondelete="SET NULL"), nullable=True, index=True)
    slot_code: Mapped[str] = mapped_column(String(32), default="SLOT-MORNING-A", nullable=False)
    start_time: Mapped[str] = mapped_column(String(16), default="09:30", nullable=False)
    end_time: Mapped[str] = mapped_column(String(16), default="12:30", nullable=False)
    room_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_room_plannings.id", ondelete="SET NULL"), nullable=True, index=True)
    room_number: Mapped[str] = mapped_column(String(48), default="HALL-A1", nullable=False)
    building_name: Mapped[str] = mapped_column(String(120), default="Main Examination Complex", nullable=False)
    faculty_in_charge_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    faculty_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    max_candidates: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    allocated_candidates: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="SCHEDULED", nullable=False)  # DRAFT, SCHEDULED, CONFLICT_DETECTED, PUBLISHED, ARCHIVED
    conflict_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    conflicts: Mapped[List["ExamTimetableConflict"]] = relationship("ExamTimetableConflict", back_populates="schedule", cascade="all, delete-orphan")


class ExamTimetableConflict(Base):
    __tablename__ = "exam_timetable_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    schedule_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_timetable_schedules.id", ondelete="CASCADE"), nullable=True, index=True)
    conflict_type: Mapped[str] = mapped_column(String(48), nullable=False)  # ROOM_CLASH, FACULTY_CLASH, STUDENT_COHORT_CLASH, STUDY_GAP_VIOLATION, LAB_CAPACITY_EXCEEDED
    severity: Mapped[str] = mapped_column(String(16), default="CRITICAL", nullable=False)  # CRITICAL, WARNING, INFO
    description: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resolved_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    resolution_action: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    schedule: Mapped[Optional["ExamTimetableSchedule"]] = relationship("ExamTimetableSchedule", back_populates="conflicts")


class ExamHallTicket(Base):
    __tablename__ = "exam_hall_tickets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    father_name: Mapped[str] = mapped_column(String(120), default="Shri R. K. Sharma", nullable=False)
    program_name: Mapped[str] = mapped_column(String(120), default="B.Tech Computer Science & Engineering", nullable=False)
    department_name: Mapped[str] = mapped_column(String(120), default="Computer Science & Engineering", nullable=False)
    semester_code: Mapped[str] = mapped_column(String(32), default="SEM-5", nullable=False)
    academic_year: Mapped[str] = mapped_column(String(32), default="2026-2027", nullable=False)
    exam_center_code: Mapped[str] = mapped_column(String(32), default="TC-IND-01", nullable=False)
    exam_center_name: Mapped[str] = mapped_column(String(140), default="Main Examination Complex, MEI Autonomous Campus", nullable=False)
    exam_center_address: Mapped[str] = mapped_column(String(200), default="Campus Ring Road, Indore, Madhya Pradesh - 452010", nullable=False)
    ticket_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    barcode_data: Mapped[str] = mapped_column(String(64), nullable=False)
    qr_verification_code: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    digital_signature_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    controller_name: Mapped[str] = mapped_column(String(120), default="Dr. V. K. Maheshwari, Controller of Examinations", nullable=False)
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    status: Mapped[str] = mapped_column(String(32), default="ISSUED", nullable=False)  # GENERATED, ISSUED, DOWNLOADED, BLOCKED, CANCELLED
    eligibility_status: Mapped[str] = mapped_column(String(48), default="ELIGIBLE", nullable=False)  # ELIGIBLE, CONDITIONAL_ATTENDANCE, FEE_CLEARED, DETAINED
    paper_entries: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    student_instructions: Mapped[List[str]] = mapped_column(JSONB, default=list, nullable=False)
    download_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_downloaded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamBuilding(Base):
    __tablename__ = "exam_buildings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    building_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    building_name: Mapped[str] = mapped_column(String(120), nullable=False)
    total_floors: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    has_elevator: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_accessible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    rooms: Mapped[List["ExamRoomLayout"]] = relationship("ExamRoomLayout", back_populates="building", cascade="all, delete-orphan")


class ExamRoomLayout(Base):
    __tablename__ = "exam_room_layouts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    building_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_buildings.id", ondelete="CASCADE"), nullable=False, index=True)
    room_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    floor_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    room_type: Mapped[str] = mapped_column(String(32), default="CENTRAL_HALL", nullable=False)  # CENTRAL_HALL, CLASSROOM, COMPUTER_LAB, DRAWING_HALL
    rows_count: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    columns_count: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    benches_count: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    seats_per_bench: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    total_capacity: Mapped[int] = mapped_column(Integer, default=120, nullable=False)
    buffer_capacity: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    has_cctv: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_air_conditioned: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    building: Mapped["ExamBuilding"] = relationship("ExamBuilding", back_populates="rooms")
    seating_plans: Mapped[List["ExamSeatingPlan"]] = relationship("ExamSeatingPlan", back_populates="room", cascade="all, delete-orphan")


class ExamSeatingPlan(Base):
    __tablename__ = "exam_seating_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    schedule_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_timetable_schedules.id", ondelete="SET NULL"), nullable=True, index=True)
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_room_layouts.id", ondelete="CASCADE"), nullable=False, index=True)
    room_number: Mapped[str] = mapped_column(String(48), nullable=False)
    exam_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    slot_code: Mapped[str] = mapped_column(String(32), default="SLOT-MORNING-A", nullable=False)
    allocation_strategy: Mapped[str] = mapped_column(String(48), default="CHECKERBOARD_GRID", nullable=False)  # CHECKERBOARD_GRID, RANDOMIZED_JUMBLE, ALTERNATING_DEPARTMENT, SERIAL_ROLL_NUMBER
    total_allocated_seats: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_empty_buffer_seats: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="FINALIZED", nullable=False)  # DRAFT, FINALIZED, DOOR_NOTICE_PUBLISHED
    seating_matrix: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    room: Mapped["ExamRoomLayout"] = relationship("ExamRoomLayout", back_populates="seating_plans")


class ExamInvigilatorProfile(Base):
    __tablename__ = "exam_invigilator_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    invigilator_type: Mapped[str] = mapped_column(String(32), default="INTERNAL_FACULTY", nullable=False)  # INTERNAL_FACULTY, EXTERNAL_EXAMINER, OBSERVER_SQUAD
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    institution_name: Mapped[str] = mapped_column(String(140), default="MY EDUCATION INDIA Autonomous Campus, Indore", nullable=False)
    department_name: Mapped[str] = mapped_column(String(120), nullable=False)
    designation: Mapped[str] = mapped_column(String(80), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    is_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    bank_account_no: Mapped[Optional[str]] = mapped_column(String(48), nullable=True)
    ifsc_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    pan_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    max_duties_per_session: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    allocated_duties_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    rosters: Mapped[List["ExamInvigilatorRoster"]] = relationship("ExamInvigilatorRoster", back_populates="invigilator", cascade="all, delete-orphan")


class ExamInvigilatorRoster(Base):
    __tablename__ = "exam_invigilator_rosters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    invigilator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_invigilator_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    schedule_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_timetable_schedules.id", ondelete="SET NULL"), nullable=True, index=True)
    room_number: Mapped[str] = mapped_column(String(48), nullable=False)
    building_name: Mapped[str] = mapped_column(String(120), default="Main Examination Complex", nullable=False)
    duty_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    slot_code: Mapped[str] = mapped_column(String(32), default="SLOT-MORNING-A", nullable=False)
    start_time: Mapped[str] = mapped_column(String(16), default="09:30", nullable=False)
    end_time: Mapped[str] = mapped_column(String(16), default="12:30", nullable=False)
    duty_role: Mapped[str] = mapped_column(String(32), default="ROOM_INVIGILATOR", nullable=False)  # CHIEF_SUPERINTENDENT, ROOM_INVIGILATOR, RELIEVER_INVIGILATOR, FLYING_SQUAD, OBSERVER
    status: Mapped[str] = mapped_column(String(32), default="ALLOCATED", nullable=False)  # ALLOCATED, CONFIRMED, REPORTED_PRESENT, REPLACED, ABSENT
    check_in_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    check_out_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    replacement_roster_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    replacement_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duty_report_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    booklets_issued: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    booklets_collected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    malpractice_cases_reported: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    honorarium_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    honorarium_status: Mapped[str] = mapped_column(String(24), default="PENDING", nullable=False)  # PENDING, APPROVED, DISBURSED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    invigilator: Mapped["ExamInvigilatorProfile"] = relationship("ExamInvigilatorProfile", back_populates="rosters")


class ExamPracticalAssessment(Base):
    __tablename__ = "exam_practical_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    course_title: Mapped[str] = mapped_column(String(180), nullable=False)
    assessment_type: Mapped[str] = mapped_column(String(32), default="PRACTICAL_EXAM", nullable=False)  # PRACTICAL_EXAM, VIVA_VOCE, CLINICAL_ASSESSMENT, LAB_EXAM, OSPE, OSCE
    lab_room_number: Mapped[str] = mapped_column(String(48), nullable=False)
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    slot_code: Mapped[str] = mapped_column(String(32), default="SLOT-MORNING-A", nullable=False)
    total_candidates: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    total_stations: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    max_marks: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    passing_marks: Mapped[float] = mapped_column(Float, default=20.0, nullable=False)
    internal_examiner_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_invigilator_profiles.id", ondelete="SET NULL"), nullable=True)
    external_examiner_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_invigilator_profiles.id", ondelete="SET NULL"), nullable=True)
    external_examiner_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    external_examiner_institution: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)
    rubrics_definition: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="SCHEDULED", nullable=False)  # SCHEDULED, IN_PROGRESS, EVALUATED, LOCKED_APPROVED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    score_records: Mapped[List["ExamPracticalScoreRecord"]] = relationship("ExamPracticalScoreRecord", back_populates="assessment", cascade="all, delete-orphan")


class ExamPracticalScoreRecord(Base):
    __tablename__ = "exam_practical_score_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_practical_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    batch_name: Mapped[str] = mapped_column(String(48), default="Batch B1", nullable=False)
    station_scores: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    internal_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    external_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    viva_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_marks_obtained: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    examiner_remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evaluated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    assessment: Mapped["ExamPracticalAssessment"] = relationship("ExamPracticalAssessment", back_populates="score_records")


class ExamCandidateAttendance(Base):
    __tablename__ = "exam_candidate_attendances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    schedule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_timetable_schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    hall_ticket_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_hall_tickets.id", ondelete="SET NULL"), nullable=True, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    room_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    seat_number: Mapped[str] = mapped_column(String(48), nullable=False)
    attendance_status: Mapped[str] = mapped_column(String(32), default="PRESENT", nullable=False)  # PRESENT, ABSENT, LATE, MALPRACTICE, MEDICAL_CASE
    entry_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    answer_booklet_barcode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    supplementary_booklet_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    supplementary_booklet_barcodes: Mapped[List[str]] = mapped_column(JSONB, default=list, nullable=False)
    malpractice_category: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    malpractice_evidence_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    medical_contingency_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    invigilator_signature_flag: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    candidate_signature_flag: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamEvaluationBatch(Base):
    __tablename__ = "exam_evaluation_batches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    schedule_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_timetable_schedules.id", ondelete="SET NULL"), nullable=True, index=True)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    paper_code: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    evaluation_mode: Mapped[str] = mapped_column(String(32), default="DIGITAL_ON_SCREEN", nullable=False)  # MANUAL_PHYSICAL, DIGITAL_ON_SCREEN
    evaluation_type: Mapped[str] = mapped_column(String(32), default="DOUBLE_BLIND", nullable=False)  # SINGLE, DOUBLE_BLIND, MODERATION, RECHECKING
    total_scripts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    evaluated_scripts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    moderated_scripts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_marks: Mapped[float] = mapped_column(Float, default=70.0, nullable=False)
    passing_marks: Mapped[float] = mapped_column(Float, default=28.0, nullable=False)
    max_deviation_threshold: Mapped[float] = mapped_column(Float, default=15.0, nullable=False)  # % difference triggering 3rd evaluation / moderation
    evaluator_1_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_invigilator_profiles.id", ondelete="SET NULL"), nullable=True)
    evaluator_2_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_invigilator_profiles.id", ondelete="SET NULL"), nullable=True)
    moderator_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_invigilator_profiles.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="IN_PROGRESS", nullable=False)  # CREATED, ASSIGNED, IN_PROGRESS, MODERATION_REQUIRED, COMPLETED, LOCKED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    scripts: Mapped[List["ExamScriptEvaluation"]] = relationship("ExamScriptEvaluation", back_populates="batch", cascade="all, delete-orphan")


class ExamScriptEvaluation(Base):
    __tablename__ = "exam_script_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_evaluation_batches.id", ondelete="CASCADE"), nullable=False, index=True)
    dummy_barcode: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)  # Blind token: e.g. "DUMMY-CS301-001"
    actual_roll_number: Mapped[str] = mapped_column(String(48), nullable=False)  # Masked until final tabulation
    actual_candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    evaluator_1_marks: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    evaluator_1_breakdown: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    evaluator_2_marks: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    evaluator_2_breakdown: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    moderator_marks: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    moderator_breakdown: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    deviation_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_deviation_triggered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    grace_marks_awarded: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    grace_rule_applied: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    final_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rechecking_status: Mapped[str] = mapped_column(String(32), default="NONE", nullable=False)  # NONE, REQUESTED, SCRUTINIZED, SCORE_REVISED, NO_CHANGE
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    batch: Mapped["ExamEvaluationBatch"] = relationship("ExamEvaluationBatch", back_populates="scripts")


class ExamMarksSubmission(Base):
    __tablename__ = "exam_marks_submissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    course_title: Mapped[str] = mapped_column(String(180), nullable=False)
    component_type: Mapped[str] = mapped_column(String(48), default="THEORY_INTERNAL", nullable=False)  # THEORY_INTERNAL, THEORY_EXTERNAL, PRACTICAL_INTERNAL, PRACTICAL_EXTERNAL, ASSIGNMENT, PROJECT
    semester_code: Mapped[str] = mapped_column(String(32), default="SEM-5", nullable=False)
    faculty_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    faculty_name: Mapped[str] = mapped_column(String(120), nullable=False)
    department_name: Mapped[str] = mapped_column(String(120), nullable=False)
    max_marks: Mapped[float] = mapped_column(Float, default=30.0, nullable=False)
    passing_marks: Mapped[float] = mapped_column(Float, default=12.0, nullable=False)
    submission_mode: Mapped[str] = mapped_column(String(32), default="ONLINE_PORTAL", nullable=False)  # ONLINE_PORTAL, EXCEL_IMPORT, OFFLINE_CSV
    status: Mapped[str] = mapped_column(String(32), default="DRAFT", nullable=False)  # DRAFT, SUBMITTED, HOD_APPROVED, COE_LOCKED, REJECTED_REVISION
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    locked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    hod_approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    hod_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    coe_approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    coe_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    approval_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_students_enrolled: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_marks_entered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    entries: Mapped[List["ExamStudentMarkEntry"]] = relationship("ExamStudentMarkEntry", back_populates="submission", cascade="all, delete-orphan")


class ExamStudentMarkEntry(Base):
    __tablename__ = "exam_student_mark_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_marks_submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    marks_obtained: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_absent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_malpractice: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    grade_letter: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    faculty_remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    submission: Mapped["ExamMarksSubmission"] = relationship("ExamMarksSubmission", back_populates="entries")


class ExamStudentSemesterResult(Base):
    __tablename__ = "exam_student_semester_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    program_name: Mapped[str] = mapped_column(String(120), default="B.Tech Computer Science & Engineering", nullable=False)
    department_name: Mapped[str] = mapped_column(String(120), default="Computer Science & Engineering", nullable=False)
    semester_code: Mapped[str] = mapped_column(String(32), default="SEM-5", nullable=False)
    academic_year: Mapped[str] = mapped_column(String(32), default="2026-2027", nullable=False)
    grading_system: Mapped[str] = mapped_column(String(32), default="ABSOLUTE", nullable=False)  # ABSOLUTE, RELATIVE
    total_credits_registered: Mapped[float] = mapped_column(Float, default=24.0, nullable=False)
    total_credits_earned: Mapped[float] = mapped_column(Float, default=24.0, nullable=False)
    total_marks_obtained: Mapped[float] = mapped_column(Float, default=480.0, nullable=False)
    total_max_marks: Mapped[float] = mapped_column(Float, default=600.0, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, default=80.0, nullable=False)
    sgpa: Mapped[float] = mapped_column(Float, default=8.5, nullable=False)
    cgpa: Mapped[float] = mapped_column(Float, default=8.65, nullable=False)
    overall_grade: Mapped[str] = mapped_column(String(8), default="A", nullable=False)  # O, A+, A, B+, B, C, P, F
    division: Mapped[str] = mapped_column(String(48), default="FIRST_CLASS_DISTINCTION", nullable=False)  # FIRST_CLASS_DISTINCTION, FIRST_CLASS, SECOND_CLASS, PASS_CLASS, FAIL
    class_rank: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    result_status: Mapped[str] = mapped_column(String(32), default="PASSED", nullable=False)  # PASSED, PROMOTED_WITH_BACKLOG, DETAINED, WITHHELD
    course_results: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamMeritList(Base):
    __tablename__ = "exam_merit_lists"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    program_name: Mapped[str] = mapped_column(String(120), default="B.Tech Computer Science & Engineering", nullable=False)
    semester_code: Mapped[str] = mapped_column(String(32), default="SEM-5", nullable=False)
    academic_year: Mapped[str] = mapped_column(String(32), default="2026-2027", nullable=False)
    grading_system: Mapped[str] = mapped_column(String(32), default="ABSOLUTE", nullable=False)
    merit_entries: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)  # [rank, roll, name, cgpa, sgpa, percentage, medal]
    published_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExamRevaluationApplication(Base):
    __tablename__ = "exam_revaluation_applications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    course_name: Mapped[str] = mapped_column(String(120), nullable=False)
    service_type: Mapped[str] = mapped_column(String(32), default="CHALLENGE_REVALUATION", nullable=False)  # RE_TOTALING, PHOTOCOPY_INSPECTION, CHALLENGE_REVALUATION
    application_status: Mapped[str] = mapped_column(String(32), default="SUBMITTED", nullable=False)  # SUBMITTED, FEE_PAID, EVALUATOR_ASSIGNED, UNDER_EVALUATION, COMPLETED, REJECTED
    fee_amount: Mapped[float] = mapped_column(Float, default=1000.0, nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(32), default="PAID", nullable=False)  # PENDING, PAID, REFUNDED, WAIVED
    original_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    original_grade: Mapped[str] = mapped_column(String(8), default="F", nullable=False)
    reval_marks: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    third_eval_marks: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    final_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    updated_grade: Mapped[str] = mapped_column(String(8), default="F", nullable=False)
    is_marks_changed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fee_refunded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    photocopy_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    evaluator_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    evaluator_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    evaluator_remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coe_approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamSupplementaryRegistration(Base):
    __tablename__ = "exam_supplementary_registrations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    course_name: Mapped[str] = mapped_column(String(120), nullable=False)
    credits: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    original_attempt_session: Mapped[str] = mapped_column(String(64), default="AUTUMN-2025", nullable=False)
    fee_amount: Mapped[float] = mapped_column(Float, default=750.0, nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(32), default="PAID", nullable=False)
    hall_ticket_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    exam_status: Mapped[str] = mapped_column(String(32), default="REGISTERED", nullable=False)  # REGISTERED, APPEARED, ABSENT
    marks_obtained: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    grade_obtained: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    is_cleared: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamCertificateRegistry(Base):
    __tablename__ = "exam_certificate_registry"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    program_name: Mapped[str] = mapped_column(String(120), default="B.Tech Computer Science & Engineering", nullable=False)
    department_name: Mapped[str] = mapped_column(String(120), default="Computer Science & Engineering", nullable=False)
    certificate_type: Mapped[str] = mapped_column(String(48), default="CONSOLIDATED_TRANSCRIPT", nullable=False, index=True)  # SEMESTER_GRADE_CARD, CONSOLIDATED_TRANSCRIPT, PROVISIONAL_DEGREE_CERTIFICATE, DEGREE_CONVOCATION_CERTIFICATE, MIGRATION_CERTIFICATE
    serial_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    cgpa: Mapped[float] = mapped_column(Float, default=8.5, nullable=False)
    sgpa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    division: Mapped[str] = mapped_column(String(48), default="FIRST_CLASS_DISTINCTION", nullable=False)
    academic_year: Mapped[str] = mapped_column(String(32), default="2026-2027", nullable=False)
    qr_verification_url: Mapped[str] = mapped_column(String(255), nullable=False)
    verification_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)  # SHA-256
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    revocation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    issued_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    transcript_payload: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamTranscriptRequest(Base):
    __tablename__ = "exam_transcript_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    request_type: Mapped[str] = mapped_column(String(48), default="OFFICIAL_TRANSCRIPT", nullable=False)  # OFFICIAL_TRANSCRIPT, DUPLICATE_GRADE_CARD, PROVISIONAL_CERTIFICATE, WES_DIRECT_DISPATCH
    delivery_mode: Mapped[str] = mapped_column(String(32), default="DIGITAL_DOWNLOAD", nullable=False)  # DIGITAL_DOWNLOAD, HARDCOPY_CAMPUS_PICKUP, POSTAL_DOMESTIC, INTERNATIONAL_COURIER
    copies: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    fee_amount: Mapped[float] = mapped_column(Float, default=500.0, nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(32), default="PAID", nullable=False)
    request_status: Mapped[str] = mapped_column(String(32), default="SUBMITTED", nullable=False)  # SUBMITTED, PROCESSING, PRINTED, DISPATCHED, DELIVERED
    tracking_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    recipient_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamComplianceReport(Base):
    __tablename__ = "exam_compliance_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(32), default="2026-2027", nullable=False)
    report_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)  # UGC_AUTONOMOUS_RETURN, AFFILIATING_UNIVERSITY_TR_GAZETTE, AICTE_EXAMINATION_DISCLOSURE, STATISTICAL_PASS_PERCENTAGE_GAZETTE, ANNUAL_EXAM_AUDIT_REPORT
    regulatory_body: Mapped[str] = mapped_column(String(64), default="UGC", nullable=False)  # UGC, STATE_UNIVERSITY, AICTE, NBA_NAAC, INTERNAL_ACADEMIC_COUNCIL
    reporting_period: Mapped[str] = mapped_column(String(64), default="Autumn Semester 2026-27", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT", nullable=False)  # DRAFT, SUBMITTED, ACKNOWLEDGED, ARCHIVED
    submission_reference: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    document_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metrics_payload: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    generated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamMalpracticeDisciplinaryRecord(Base):
    __tablename__ = "exam_malpractice_disciplinary_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    incident_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    clause_violated: Mapped[str] = mapped_column(String(64), nullable=False)  # UNAUTHORIZED_MATERIAL, ELECTRONIC_DEVICE, IMPERSONATION, ANSWER_SHEET_SMUGGLING, INSUBORDINATION
    severity_level: Mapped[str] = mapped_column(String(32), default="LEVEL_1_WARNING", nullable=False)  # LEVEL_1_WARNING, LEVEL_2_COURSE_CANCELLATION, LEVEL_3_SEMESTER_DEBARMENT, LEVEL_4_EXPULSION
    committee_resolution: Mapped[str] = mapped_column(Text, nullable=False)
    penalty_awarded: Mapped[str] = mapped_column(String(120), nullable=False)
    tribunal_status: Mapped[str] = mapped_column(String(32), default="REPORTED", nullable=False)  # REPORTED, UNDER_INQUIRY, PENALTY_CONFIRMED, APPEALED, CLEARED
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamCourseAnalyticsMetric(Base):
    __tablename__ = "exam_course_analytics_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    course_name: Mapped[str] = mapped_column(String(120), nullable=False)
    total_candidates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pass_percentage: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    difficulty_index: Mapped[float] = mapped_column(Float, default=0.65, nullable=False)  # 0.0 to 1.0 (mean / max_marks)
    discrimination_index: Mapped[float] = mapped_column(Float, default=0.42, nullable=False)  # -1.0 to +1.0
    average_marks: Mapped[float] = mapped_column(Float, default=75.0, nullable=False)
    standard_deviation: Mapped[float] = mapped_column(Float, default=12.5, nullable=False)
    highest_marks: Mapped[float] = mapped_column(Float, default=98.0, nullable=False)
    lowest_marks: Mapped[float] = mapped_column(Float, default=42.0, nullable=False)
    grade_distribution: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamStudentRiskPrediction(Base):
    __tablename__ = "exam_student_risk_predictions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    program_name: Mapped[str] = mapped_column(String(120), default="B.Tech Computer Science & Engineering", nullable=False)
    semester_code: Mapped[str] = mapped_column(String(32), default="SEM-5", nullable=False)
    risk_level: Mapped[str] = mapped_column(String(32), default="LOW_RISK", nullable=False)  # HIGH_RISK, MODERATE_RISK, LOW_RISK
    predicted_backlog_probability: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    flagged_courses: Mapped[List[str]] = mapped_column(JSONB, default=list, nullable=False)
    recommended_interventions: Mapped[List[str]] = mapped_column(JSONB, default=list, nullable=False)
    is_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamStudentPortalSession(Base):
    __tablename__ = "exam_student_portal_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    enrollment_no: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    program_name: Mapped[str] = mapped_column(String(120), default="B.Tech Computer Science & Engineering", nullable=False)
    current_semester: Mapped[str] = mapped_column(String(32), default="SEM-5", nullable=False)
    exam_registration_status: Mapped[str] = mapped_column(String(32), default="CONFIRMED", nullable=False)  # PENDING, CONFIRMED, FEE_PENDING, BLOCKED
    hall_ticket_downloaded: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_portal_access: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamFacultyDutySwap(Base):
    __tablename__ = "exam_faculty_duty_swaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    requesting_faculty_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    requesting_faculty_name: Mapped[str] = mapped_column(String(120), nullable=False)
    target_faculty_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    target_faculty_name: Mapped[str] = mapped_column(String(120), nullable=False)
    duty_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    slot_time: Mapped[str] = mapped_column(String(64), nullable=False)
    room_number: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    swap_status: Mapped[str] = mapped_column(String(32), default="PENDING_PEER_ACCEPTANCE", nullable=False)  # PENDING_PEER_ACCEPTANCE, PEER_ACCEPTED, PEER_REJECTED, COE_APPROVED, REJECTED
    approved_by_coe: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamCoeGovernanceControl(Base):
    __tablename__ = "exam_coe_governance_controls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    session_lifecycle_stage: Mapped[str] = mapped_column(String(48), default="EXAMS_UNDERWAY", nullable=False)  # PLANNING, REGISTRATION_OPEN, TIMETABLE_PUBLISHED, HALL_TICKETS_RELEASED, EXAMS_UNDERWAY, EVALUATION_ACTIVE, RESULTS_PROCESSED, RESULTS_PUBLISHED, SESSION_ARCHIVED
    is_registration_locked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_timetable_locked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_marks_entry_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_result_declaration_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    qp_vault_unlocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    dual_custody_key_hash: Mapped[str] = mapped_column(String(64), default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", nullable=False)
    emergency_override_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    emergency_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coe_digital_signature_serial: Mapped[str] = mapped_column(String(64), default="MEI-COE-DSIG-2026-X991", nullable=False)
    coe_signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    coe_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    audit_events: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ExamEmergencyOverrideLog(Base):
    __tablename__ = "exam_emergency_override_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(64), nullable=False)  # QUESTION_PAPER_SET_SWAP, EMERGENCY_ROOM_REALLOCATION, INVIGILATOR_FORCE_DEPLOYMENT, MARKS_CORRECTION_OVERRIDE, EXAM_POSTPONEMENT
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    authorized_by_coe: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
