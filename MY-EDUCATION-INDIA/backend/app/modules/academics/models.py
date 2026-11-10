import uuid
from datetime import date, datetime, time, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin


class Department(Base, TimestampUUIDMixin):
    __tablename__ = "acad_departments"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_department_code_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True
    )
    code: Mapped[str] = mapped_column(String(32), index=True, nullable=False) # e.g. CSE, ECE, MGMT, PHARM, LAW
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    hod_name: Mapped[str | None] = mapped_column(String(120), nullable=True) # Head of Department
    hod_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    courses: Mapped[List["Course"]] = relationship("Course", back_populates="department", cascade="all, delete-orphan", lazy="selectin")


class Program(Base, TimestampUUIDMixin):
    """Academic Program Classification (UG, PG, Diploma, Certificate, PhD, Skill)."""
    __tablename__ = "acad_programs"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_program_code_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(32), index=True, nullable=False) # e.g. UG, PG, DIP, CERT, PHD, SKILL
    name: Mapped[str] = mapped_column(String(120), nullable=False) # Undergraduate, Postgraduate, Diploma
    level: Mapped[str] = mapped_column(String(32), default="UNDERGRADUATE", nullable=False)
    duration_years: Mapped[float] = mapped_column(Float, default=3.0, nullable=False)
    total_credits: Mapped[int] = mapped_column(Integer, default=120, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    courses: Mapped[List["Course"]] = relationship("Course", back_populates="program", cascade="all, delete-orphan", lazy="selectin")


class Course(Base, TimestampUUIDMixin):
    """Master Academic Degree / Course (B.Tech, MBA, BCA, BPT, DCA, etc.)."""
    __tablename__ = "acad_courses"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_course_code_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_departments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    program_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(32), index=True, nullable=False) # e.g. BTECH_CSE, MBA_FIN, BCA, BPT
    name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    duration_months: Mapped[int] = mapped_column(Integer, default=36, nullable=False)
    academic_pattern: Mapped[str] = mapped_column(String(32), default="SEMESTER", nullable=False) # SEMESTER, YEARLY, TRIMESTER
    total_semesters_or_years: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    medium_of_instruction: Mapped[str] = mapped_column(String(64), default="English", nullable=False)
    min_intake_capacity: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    max_intake_capacity: Mapped[int] = mapped_column(Integer, default=120, nullable=False)
    eligibility_criteria: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    department: Mapped[Department] = relationship("Department", back_populates="courses")
    program: Mapped[Program] = relationship("Program", back_populates="courses")
    specializations: Mapped[List["Specialization"]] = relationship("Specialization", back_populates="course", cascade="all, delete-orphan", lazy="selectin")
    curriculums: Mapped[List["Curriculum"]] = relationship("Curriculum", back_populates="course", cascade="all, delete-orphan", lazy="selectin")
    batches: Mapped[List["Batch"]] = relationship("Batch", back_populates="course", cascade="all, delete-orphan", lazy="selectin")


class Specialization(Base, TimestampUUIDMixin):
    __tablename__ = "acad_specializations"
    __table_args__ = (
        UniqueConstraint("code", "course_id", name="uq_specialization_code_course"),
        {"extend_existing": True},
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. AI_ML, CYBER_SEC, CLOUD_COMP, FINTECH
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    course: Mapped[Course] = relationship("Course", back_populates="specializations")


class Semester(Base, TimestampUUIDMixin):
    """Semester or Academic Term definition."""
    __tablename__ = "acad_semesters"
    __table_args__ = (
        UniqueConstraint("course_id", "term_number", name="uq_semester_term_course"),
        {"extend_existing": True},
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    term_number: Mapped[int] = mapped_column(Integer, nullable=False) # 1, 2, 3, 4, 5, 6, 7, 8
    term_label: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. Semester 1, Year 1, Trimester 2
    required_credits: Mapped[int] = mapped_column(Integer, default=20, nullable=False)


class Subject(Base, TimestampUUIDMixin):
    """Master Course Subject / Module (Theory, Practical, Labs)."""
    __tablename__ = "acad_subjects"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_subject_code_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_departments.id", ondelete="SET NULL"), nullable=True, index=True
    )
    code: Mapped[str] = mapped_column(String(32), index=True, nullable=False) # e.g. CS101, MATH201, PHARM302
    name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    subject_type: Mapped[str] = mapped_column(String(32), default="THEORY", nullable=False) # THEORY, PRACTICAL, LAB, PROJECT, ELECTIVE, VIVA
    credits: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    theory_hours_per_week: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    practical_hours_per_week: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    internal_max_marks: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    external_max_marks: Mapped[int] = mapped_column(Integer, default=70, nullable=False)
    passing_percentage: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    is_lab_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    syllabus_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Curriculum(Base, TimestampUUIDMixin):
    """Version-controlled Syllabus & Curriculum Scheme mapped to CBCS / NEP standards."""
    __tablename__ = "acad_curriculums"
    __table_args__ = (
        UniqueConstraint("course_id", "scheme_year", name="uq_curriculum_course_year"),
        {"extend_existing": True},
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scheme_year: Mapped[str] = mapped_column(String(32), nullable=False) # e.g. 2026-CBCS, NEP-2027
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    total_credits: Mapped[int] = mapped_column(Integer, default=160, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    course: Mapped[Course] = relationship("Course", back_populates="curriculums")
    subjects: Mapped[List["CurriculumSubject"]] = relationship("CurriculumSubject", back_populates="curriculum", cascade="all, delete-orphan", lazy="selectin")


class CurriculumSubject(Base, TimestampUUIDMixin):
    __tablename__ = "acad_curriculum_subjects"
    __table_args__ = (
        UniqueConstraint("curriculum_id", "subject_id", "semester_number", name="uq_curriculum_subj_sem"),
        {"extend_existing": True},
    )

    curriculum_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_curriculums.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_subjects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    semester_number: Mapped[int] = mapped_column(Integer, nullable=False) # 1 to 8
    is_elective: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    elective_group: Mapped[str | None] = mapped_column(String(64), nullable=True) # ELECTIVE_1, DISCIPLINE_SPECIFIC

    curriculum: Mapped[Curriculum] = relationship("Curriculum", back_populates="subjects")
    subject: Mapped[Subject] = relationship("Subject", lazy="selectin")


class Batch(Base, TimestampUUIDMixin):
    """Academic Batch Cohort (e.g. B.Tech CSE 2026-2030 Batch)."""
    __tablename__ = "acad_batches"
    __table_args__ = (
        UniqueConstraint("code", "course_id", "academic_year_code", name="uq_batch_code_course_year"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # e.g. BTECH-CSE-2026
    name: Mapped[str] = mapped_column(String(150), nullable=False) # e.g. B.Tech Computer Science 2026-30
    academic_year_code: Mapped[str] = mapped_column(String(32), index=True, nullable=False) # 2026-2027
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    intake_capacity: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    current_strength: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    course: Mapped[Course] = relationship("Course", back_populates="batches")
    sections: Mapped[List["Section"]] = relationship("Section", back_populates="batch", cascade="all, delete-orphan", lazy="selectin")


class Section(Base, TimestampUUIDMixin):
    """Classroom Section / Group (Section A, Section B, Evening Batch)."""
    __tablename__ = "acad_sections"
    __table_args__ = (
        UniqueConstraint("name", "batch_id", name="uq_section_batch"),
        {"extend_existing": True},
    )

    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_batches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False) # A, B, C, Morning, Evening, Online
    capacity: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    classroom_number: Mapped[str | None] = mapped_column(String(64), nullable=True) # e.g. Room 302, Lab 4
    class_teacher_name: Mapped[str | None] = mapped_column(String(120), nullable=True)

    batch: Mapped[Batch] = relationship("Batch", back_populates="sections")


class Classroom(Base, TimestampUUIDMixin):
    __tablename__ = "acad_classrooms"
    __table_args__ = (
        UniqueConstraint("room_number", "branch_id", name="uq_room_branch"),
        {"extend_existing": True},
    )

    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    room_number: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. Room 401, CSE Lab 2
    building_name: Mapped[str] = mapped_column(String(100), default="Main Academic Block", nullable=False)
    floor: Mapped[str] = mapped_column(String(32), default="4th Floor", nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    is_lab: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_smart_class: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class FacultyAssignment(Base, TimestampUUIDMixin):
    """Assigns teacher to Course, Batch, Section, and Subject with collision prevention."""
    __tablename__ = "acad_faculty_assignments"
    __table_args__ = (
        UniqueConstraint("batch_id", "section_id", "subject_id", "faculty_user_id", name="uq_faculty_assignment"),
        {"extend_existing": True},
    )

    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_batches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_sections.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_subjects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    faculty_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    faculty_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role_type: Mapped[str] = mapped_column(String(64), default="PRIMARY_LECTURER", nullable=False) # PRIMARY_LECTURER, LAB_INSTRUCTOR, TEACHING_ASSISTANT


class Timetable(Base, TimestampUUIDMixin):
    """Master Schedule Container for Batch & Section."""
    __tablename__ = "acad_timetables"
    __table_args__ = (
        UniqueConstraint("batch_id", "section_id", "academic_year_code", name="uq_timetable_batch_sec_year"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_batches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_sections.id", ondelete="CASCADE"), nullable=False, index=True
    )
    academic_year_code: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    slots: Mapped[List["TimetableSlot"]] = relationship("TimetableSlot", back_populates="timetable", cascade="all, delete-orphan", lazy="selectin")


class TimetableSlot(Base, TimestampUUIDMixin):
    """Atomic Timetable Slot with collision prevention across Faculty & Classroom."""
    __tablename__ = "acad_timetable_slots"
    __table_args__ = (
        UniqueConstraint("timetable_id", "day_of_week", "start_time", name="uq_slot_tt_day_time"),
        {"extend_existing": True},
    )

    timetable_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_timetables.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_subjects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    faculty_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    classroom_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("acad_classrooms.id", ondelete="SET NULL"), nullable=True, index=True
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False) # 0=Monday, 5=Saturday
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    slot_type: Mapped[str] = mapped_column(String(32), default="LECTURE", nullable=False) # LECTURE, LAB, TUTORIAL, BREAK

    timetable: Mapped[Timetable] = relationship("Timetable", back_populates="slots")
    subject: Mapped[Subject] = relationship("Subject", lazy="selectin")
    classroom: Mapped[Optional[Classroom]] = relationship("Classroom", lazy="selectin")


class AcademicCalendarEvent(Base, TimestampUUIDMixin):
    __tablename__ = "acad_calendar_events"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    academic_year_code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    event_category: Mapped[str] = mapped_column(
        String(64), nullable=False
    ) # CLASSES, EXAM, HOLIDAY, WORKSHOP, SEMINAR, ADMISSION, RESULT, FEE_DUE
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class GradingSystem(Base, TimestampUUIDMixin):
    """10-Point UGC/CBCS Academic Grade Scale."""
    __tablename__ = "acad_grading_systems"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    grade_letter: Mapped[str] = mapped_column(String(8), nullable=False) # O, A+, A, B+, B, C, P, F
    grade_point: Mapped[float] = mapped_column(Float, nullable=False) # 10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 0.0
    min_marks_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    max_marks_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    qualitative_description: Mapped[str] = mapped_column(String(64), nullable=False) # Outstanding, Excellent, Very Good
