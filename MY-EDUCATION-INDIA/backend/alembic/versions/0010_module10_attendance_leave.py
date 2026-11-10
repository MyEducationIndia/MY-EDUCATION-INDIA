"""Module 10 Migration: Enterprise Attendance & Leave Management System Schema
Provisions:
1. attendance_sessions
2. student_attendance
3. faculty_attendance
4. staff_attendance
5. attendance_methods
6. attendance_rules
7. attendance_logs
8. leave_types
9. leave_requests
10. leave_approvals
11. attendance_reports
12. attendance_analytics
13. attendance_notifications

Revision ID: 0010_module10_attendance_leave
Revises: 0009_module9_fee_finance
Create Date: 2026-11-06 09:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0010_module10_attendance_leave"
down_revision: Union[str, None] = "0009_module9_fee_finance"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. attendance_sessions
    op.create_table(
        "attendance_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("section_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("session_date", sa.Date(), nullable=False, index=True),
        sa.Column("session_type", sa.String(length=32), nullable=False, server_default="DAILY"),
        sa.Column("period_number", sa.Integer(), nullable=True),
        sa.Column("start_time", sa.Time(), nullable=True),
        sa.Column("end_time", sa.Time(), nullable=True),
        sa.Column("taken_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. student_attendance
    op.create_table(
        "student_attendance",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("attendance_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="PRESENT"),
        sa.Column("check_in_time", sa.Time(), nullable=True),
        sa.Column("attendance_method", sa.String(length=32), nullable=False, server_default="MANUAL"),
        sa.Column("remarks", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("session_id", "student_id", name="uq_student_attendance_session"),
    )

    # 3. faculty_attendance
    op.create_table(
        "faculty_attendance",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("faculty_user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("attendance_date", sa.Date(), nullable=False, index=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="PRESENT"),
        sa.Column("clock_in_time", sa.Time(), nullable=True),
        sa.Column("clock_out_time", sa.Time(), nullable=True),
        sa.Column("total_working_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("attendance_method", sa.String(length=32), nullable=False, server_default="BIOMETRIC"),
        sa.Column("remarks", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("faculty_user_id", "attendance_date", name="uq_faculty_daily_attendance"),
    )

    # 4. staff_attendance
    op.create_table(
        "staff_attendance",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("staff_user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("attendance_date", sa.Date(), nullable=False, index=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="PRESENT"),
        sa.Column("clock_in_time", sa.Time(), nullable=True),
        sa.Column("clock_out_time", sa.Time(), nullable=True),
        sa.Column("total_working_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("attendance_method", sa.String(length=32), nullable=False, server_default="BIOMETRIC"),
        sa.Column("remarks", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("staff_user_id", "attendance_date", name="uq_staff_daily_attendance"),
    )

    # 5. attendance_methods
    op.create_table(
        "attendance_methods",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("method_code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("configuration_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. attendance_rules
    op.create_table(
        "attendance_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("minimum_attendance_pct", sa.Float(), nullable=False, server_default="75.0"),
        sa.Column("grace_time_minutes", sa.Integer(), nullable=False, server_default="15"),
        sa.Column("half_day_threshold_hours", sa.Float(), nullable=False, server_default="4.0"),
        sa.Column("consecutive_absent_alert_days", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("lock_attendance_after_days", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("auto_notify_parents_on_absence", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("exam_eligibility_threshold_pct", sa.Float(), nullable=False, server_default="75.0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. attendance_logs
    op.create_table(
        "attendance_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("user_type", sa.String(length=24), nullable=False),
        sa.Column("log_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("log_type", sa.String(length=20), nullable=False),
        sa.Column("device_id", sa.String(length=64), nullable=True),
        sa.Column("method", sa.String(length=32), nullable=False, server_default="QR_CODE"),
        sa.Column("location_coordinates", sa.String(length=64), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. leave_types
    op.create_table(
        "leave_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("applicable_to", sa.String(length=24), nullable=False, server_default="ALL"),
        sa.Column("annual_quota_days", sa.Integer(), nullable=False, server_default="12"),
        sa.Column("requires_attachment", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_carry_forward", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. leave_requests
    op.create_table(
        "leave_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("user_type", sa.String(length=24), nullable=False),
        sa.Column("leave_type_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("leave_types.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("total_days", sa.Float(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("attachment_url", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="PENDING"),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. leave_approvals
    op.create_table(
        "leave_approvals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("leave_request_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("leave_requests.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("approver_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=24), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("action_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. attendance_reports
    op.create_table(
        "attendance_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("report_type", sa.String(length=32), nullable=False, index=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("total_records", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("parameters_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("generated_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. attendance_analytics
    op.create_table(
        "attendance_analytics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("metric_date", sa.Date(), nullable=False, index=True),
        sa.Column("student_attendance_pct", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("faculty_attendance_pct", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("staff_attendance_pct", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("metrics_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. attendance_notifications
    op.create_table(
        "attendance_notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("recipient_user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("recipient_role", sa.String(length=24), nullable=False),
        sa.Column("notification_type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_sent", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("attendance_notifications")
    op.drop_table("attendance_analytics")
    op.drop_table("attendance_reports")
    op.drop_table("leave_approvals")
    op.drop_table("leave_requests")
    op.drop_table("leave_types")
    op.drop_table("attendance_logs")
    op.drop_table("attendance_rules")
    op.drop_table("attendance_methods")
    op.drop_table("staff_attendance")
    op.drop_table("faculty_attendance")
    op.drop_table("student_attendance")
    op.drop_table("attendance_sessions")
