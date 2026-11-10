"""Alembic migration for Module 8: Enterprise Academic Management System
Creates:
- acad_departments
- acad_programs
- acad_courses
- acad_specializations
- acad_semesters
- acad_subjects
- acad_curriculums
- acad_curriculum_subjects
- acad_batches
- acad_sections
- acad_classrooms
- acad_faculty_assignments
- acad_timetables
- acad_timetable_slots
- acad_calendar_events
- acad_grading_systems

Revision ID: 0008_module8_academic_engine
Revises: 0007_module7_admission_crm
Create Date: 2026-11-06 13:20:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0008_module8_academic_engine"
down_revision: Union[str, None] = "0007_module7_admission_crm"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. acad_departments table
    op.create_table(
        "acad_departments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="SET NULL"), nullable=True),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("hod_name", sa.String(length=120), nullable=True),
        sa.Column("hod_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_department_code_inst"),
    )
    op.create_index(op.f("ix_acad_departments_code"), "acad_departments", ["code"])
    op.create_index(op.f("ix_acad_departments_institute_id"), "acad_departments", ["institute_id"])

    # 2. acad_programs table
    op.create_table(
        "acad_programs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("level", sa.String(length=32), nullable=False, server_default="UNDERGRADUATE"),
        sa.Column("duration_years", sa.Float(), nullable=False, server_default="3.0"),
        sa.Column("total_credits", sa.Integer(), nullable=False, server_default="120"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_program_code_inst"),
    )

    # 3. acad_courses table
    op.create_table(
        "acad_courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("department_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_departments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("program_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_programs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("duration_months", sa.Integer(), nullable=False, server_default="36"),
        sa.Column("academic_pattern", sa.String(length=32), nullable=False, server_default="SEMESTER"),
        sa.Column("total_semesters_or_years", sa.Integer(), nullable=False, server_default="6"),
        sa.Column("medium_of_instruction", sa.String(length=64), nullable=False, server_default="English"),
        sa.Column("min_intake_capacity", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("max_intake_capacity", sa.Integer(), nullable=False, server_default="120"),
        sa.Column("eligibility_criteria", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_course_code_inst"),
    )
    op.create_index(op.f("ix_acad_courses_code"), "acad_courses", ["code"])

    # 4. acad_specializations table
    op.create_table(
        "acad_specializations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "course_id", name="uq_specialization_code_course"),
    )

    # 5. acad_semesters table
    op.create_table(
        "acad_semesters",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("term_number", sa.Integer(), nullable=False),
        sa.Column("term_label", sa.String(length=64), nullable=False),
        sa.Column("required_credits", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("course_id", "term_number", name="uq_semester_term_course"),
    )

    # 6. acad_subjects table
    op.create_table(
        "acad_subjects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("department_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_departments.id", ondelete="SET NULL"), nullable=True),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("subject_type", sa.String(length=32), nullable=False, server_default="THEORY"),
        sa.Column("credits", sa.Float(), nullable=False, server_default="4.0"),
        sa.Column("theory_hours_per_week", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("practical_hours_per_week", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("internal_max_marks", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("external_max_marks", sa.Integer(), nullable=False, server_default="70"),
        sa.Column("passing_percentage", sa.Float(), nullable=False, server_default="40.0"),
        sa.Column("is_lab_required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("syllabus_summary", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_subject_code_inst"),
    )
    op.create_index(op.f("ix_acad_subjects_code"), "acad_subjects", ["code"])

    # 7. acad_curriculums table
    op.create_table(
        "acad_curriculums",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scheme_year", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("total_credits", sa.Integer(), nullable=False, server_default="160"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("course_id", "scheme_year", name="uq_curriculum_course_year"),
    )

    # 8. acad_curriculum_subjects table
    op.create_table(
        "acad_curriculum_subjects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("curriculum_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_curriculums.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_subjects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("semester_number", sa.Integer(), nullable=False),
        sa.Column("is_elective", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("elective_group", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("curriculum_id", "subject_id", "semester_number", name="uq_curriculum_subj_sem"),
    )

    # 9. acad_batches table
    op.create_table(
        "acad_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("academic_year_code", sa.String(length=32), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("intake_capacity", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("current_strength", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "course_id", "academic_year_code", name="uq_batch_code_course_year"),
    )
    op.create_index(op.f("ix_acad_batches_code"), "acad_batches", ["code"])

    # 10. acad_sections table
    op.create_table(
        "acad_sections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_batches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("classroom_number", sa.String(length=64), nullable=True),
        sa.Column("class_teacher_name", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("name", "batch_id", name="uq_section_batch"),
    )

    # 11. acad_classrooms table
    op.create_table(
        "acad_classrooms",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("room_number", sa.String(length=64), nullable=False),
        sa.Column("building_name", sa.String(length=100), nullable=False, server_default="Main Academic Block"),
        sa.Column("floor", sa.String(length=32), nullable=False, server_default="4th Floor"),
        sa.Column("capacity", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("is_lab", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_smart_class", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("room_number", "branch_id", name="uq_room_branch"),
    )

    # 12. acad_faculty_assignments table
    op.create_table(
        "acad_faculty_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_batches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_sections.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_subjects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("faculty_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("faculty_name", sa.String(length=150), nullable=False),
        sa.Column("role_type", sa.String(length=64), nullable=False, server_default="PRIMARY_LECTURER"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("batch_id", "section_id", "subject_id", "faculty_user_id", name="uq_faculty_assignment"),
    )

    # 13. acad_timetables table
    op.create_table(
        "acad_timetables",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_batches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_sections.id", ondelete="CASCADE"), nullable=False),
        sa.Column("academic_year_code", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("batch_id", "section_id", "academic_year_code", name="uq_timetable_batch_sec_year"),
    )

    # 14. acad_timetable_slots table
    op.create_table(
        "acad_timetable_slots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("timetable_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_timetables.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_subjects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("faculty_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("classroom_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("acad_classrooms.id", ondelete="SET NULL"), nullable=True),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("slot_type", sa.String(length=32), nullable=False, server_default="LECTURE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("timetable_id", "day_of_week", "start_time", name="uq_slot_tt_day_time"),
    )

    # 15. acad_calendar_events table
    op.create_table(
        "acad_calendar_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("academic_year_code", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("event_category", sa.String(length=64), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_mandatory", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. acad_grading_systems table
    op.create_table(
        "acad_grading_systems",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("grade_letter", sa.String(length=8), nullable=False),
        sa.Column("grade_point", sa.Float(), nullable=False),
        sa.Column("min_marks_percentage", sa.Float(), nullable=False),
        sa.Column("max_marks_percentage", sa.Float(), nullable=False),
        sa.Column("qualitative_description", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("acad_grading_systems")
    op.drop_table("acad_calendar_events")
    op.drop_table("acad_timetable_slots")
    op.drop_table("acad_timetables")
    op.drop_table("acad_faculty_assignments")
    op.drop_table("acad_classrooms")
    op.drop_table("acad_sections")
    op.drop_table("acad_batches")
    op.drop_table("acad_curriculum_subjects")
    op.drop_table("acad_curriculums")
    op.drop_table("acad_subjects")
    op.drop_table("acad_semesters")
    op.drop_table("acad_specializations")
    op.drop_table("acad_courses")
    op.drop_table("acad_programs")
    op.drop_table("acad_departments")
