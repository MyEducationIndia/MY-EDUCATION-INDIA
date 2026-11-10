"""Module 11 Migration: Enterprise Examination & Result Management System Schema
Provisions:
1. exam_types
2. exam_sessions
3. exam_schedules
4. exam_subjects
5. hall_tickets
6. seating_plans
7. invigilators
8. mark_entries
9. grade_scales
10. grade_rules
11. result_rules
12. results
13. transcripts
14. revaluation_requests
15. supplementary_exams
16. merit_lists
17. rank_lists
18. exam_reports

Revision ID: 0011_module11_examination_results
Revises: 0010_module10_attendance_leave
Create Date: 2026-11-06 10:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0011_module11_examination_results"
down_revision: Union[str, None] = "0010_module10_attendance_leave"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. exam_types
    op.create_table(
        "exam_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False, server_default="EXTERNAL"),
        sa.Column("default_weightage_pct", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. exam_sessions
    op.create_table(
        "exam_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=48), nullable=False, index=True),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="SCHEDULED"),
        sa.Column("min_attendance_threshold_pct", sa.Float(), nullable=False, server_default="75.0"),
        sa.Column("requires_fee_clearance", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. exam_schedules
    op.create_table(
        "exam_schedules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("exam_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("semester_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("exam_date", sa.Date(), nullable=False, index=True),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. exam_subjects
    op.create_table(
        "exam_subjects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("schedule_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_schedules.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("exam_type_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_types.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("max_marks", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("pass_marks", sa.Float(), nullable=False, server_default="40.0"),
        sa.Column("credits", sa.Float(), nullable=False, server_default="4.0"),
        sa.Column("weightage_internal_pct", sa.Float(), nullable=False, server_default="30.0"),
        sa.Column("weightage_external_pct", sa.Float(), nullable=False, server_default="70.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. hall_tickets
    op.create_table(
        "hall_tickets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("hall_ticket_number", sa.String(length=64), unique=True, nullable=False, index=True),
        sa.Column("schedule_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_schedules.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("assigned_classroom_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("seat_number", sa.String(length=32), nullable=False),
        sa.Column("qr_verification_token", sa.Text(), nullable=False),
        sa.Column("barcode_data", sa.String(length=64), nullable=False),
        sa.Column("is_eligible", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("ineligibility_reason", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="ISSUED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("schedule_id", "student_id", name="uq_hall_ticket_student_schedule"),
    )

    # 6. seating_plans
    op.create_table(
        "seating_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("schedule_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_schedules.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("classroom_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("allocated_students_count", sa.Integer(), nullable=False),
        sa.Column("seat_matrix_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. invigilators
    op.create_table(
        "invigilators",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("schedule_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_schedules.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("classroom_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("faculty_user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="PRIMARY_INVIGILATOR"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="CONFIRMED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. mark_entries
    op.create_table(
        "mark_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("exam_subject_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_subjects.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("internal_marks", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("external_marks", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("practical_marks", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("grace_marks", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("moderation_adjustment", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_marks_obtained", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("is_absent", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("entered_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("exam_subject_id", "student_id", name="uq_mark_entry_subject_student"),
    )

    # 9. grade_scales
    op.create_table(
        "grade_scales",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("scale_name", sa.String(length=64), nullable=False, server_default="UGC_10_POINT"),
        sa.Column("letter_grade", sa.String(length=8), nullable=False),
        sa.Column("grade_point", sa.Float(), nullable=False),
        sa.Column("min_percentage", sa.Float(), nullable=False),
        sa.Column("max_percentage", sa.Float(), nullable=False),
        sa.Column("description", sa.String(length=64), nullable=False),
        sa.Column("is_passing_grade", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. grade_rules
    op.create_table(
        "grade_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("min_pass_percentage", sa.Float(), nullable=False, server_default="40.0"),
        sa.Column("grace_marks_limit", sa.Float(), nullable=False, server_default="5.0"),
        sa.Column("max_backlogs_allowed_for_promotion", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("distinction_threshold_cgpa", sa.Float(), nullable=False, server_default="8.5"),
        sa.Column("first_division_threshold_cgpa", sa.Float(), nullable=False, server_default="6.5"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. result_rules
    op.create_table(
        "result_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("exam_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("publish_status", sa.String(length=24), nullable=False, server_default="DRAFT"),
        sa.Column("publish_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. results
    op.create_table(
        "results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("exam_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("total_credits_registered", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_credits_earned", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_marks_obtained", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_max_marks", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("sgpa", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("cgpa", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("classification", sa.String(length=48), nullable=False, server_default="FIRST_CLASS"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="PASSED"),
        sa.Column("backlog_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rank_in_batch", sa.Integer(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("exam_session_id", "student_id", name="uq_result_session_student"),
    )

    # 13. transcripts
    op.create_table(
        "transcripts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("transcript_number", sa.String(length=64), unique=True, nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("transcript_type", sa.String(length=32), nullable=False, server_default="SEMESTER_GRADE_CARD"),
        sa.Column("academic_data_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("final_cgpa", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("digital_signature_hash", sa.String(length=128), nullable=False),
        sa.Column("qr_code_payload", sa.Text(), nullable=False),
        sa.Column("issued_date", sa.Date(), nullable=False),
        sa.Column("issued_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. revaluation_requests
    op.create_table(
        "revaluation_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("exam_subject_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_subjects.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("original_marks", sa.Float(), nullable=False),
        sa.Column("revised_marks", sa.Float(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("fee_paid", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="APPLIED"),
        sa.Column("reviewed_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. supplementary_exams
    op.create_table(
        "supplementary_exams",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("exam_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("backlog_semester_number", sa.Integer(), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_cleared", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. merit_lists
    op.create_table(
        "merit_lists",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("exam_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("cgpa_or_percentage", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 17. rank_lists
    op.create_table(
        "rank_lists",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("exam_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("batch_rank", sa.Integer(), nullable=False),
        sa.Column("sgpa", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 18. exam_reports
    op.create_table(
        "exam_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("report_type", sa.String(length=32), nullable=False, index=True),
        sa.Column("parameters_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("generated_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("exam_reports")
    op.drop_table("rank_lists")
    op.drop_table("merit_lists")
    op.drop_table("supplementary_exams")
    op.drop_table("revaluation_requests")
    op.drop_table("transcripts")
    op.drop_table("results")
    op.drop_table("result_rules")
    op.drop_table("grade_rules")
    op.drop_table("grade_scales")
    op.drop_table("mark_entries")
    op.drop_table("invigilators")
    op.drop_table("seating_plans")
    op.drop_table("hall_tickets")
    op.drop_table("exam_subjects")
    op.drop_table("exam_schedules")
    op.drop_table("exam_sessions")
    op.drop_table("exam_types")
