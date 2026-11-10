"""Module 12 Migration: Enterprise Computer Based Testing (CBT) Platform Schema
Provisions:
1. question_banks
2. question_categories
3. question_topics
4. question_tags
5. question_versions
6. question_media
7. question_pools
8. exam_templates
9. cbt_sessions
10. candidate_sessions
11. candidate_answers
12. answer_logs
13. offline_sync_logs
14. live_monitor_logs
15. question_statistics
16. candidate_statistics
17. exam_statistics
18. cbt_reports

Revision ID: 0012_module12_cbt_platform
Revises: 0011_module11_examination_results
Create Date: 2026-11-06 11:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0012_module12_cbt_platform"
down_revision: Union[str, None] = "0011_module11_examination_results"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. question_banks
    op.create_table(
        "question_banks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. question_categories
    op.create_table(
        "question_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("question_bank_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("question_banks.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. question_topics
    op.create_table(
        "question_topics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("question_categories.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. question_tags
    op.create_table(
        "question_tags",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("tag_name", sa.String(length=48), unique=True, nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. question_versions
    op.create_table(
        "question_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("question_topics.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("question_code", sa.String(length=48), nullable=False, index=True),
        sa.Column("question_type", sa.String(length=32), nullable=False, server_default="MCQ"),
        sa.Column("difficulty_level", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("bloom_level", sa.String(length=24), nullable=False, server_default="UNDERSTAND"),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("options_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("correct_answers_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("default_marks", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("negative_marks", sa.Float(), nullable=False, server_default="0.25"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("approval_status", sa.String(length=24), nullable=False, server_default="APPROVED"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. question_media
    op.create_table(
        "question_media",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("question_versions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("media_type", sa.String(length=20), nullable=False),
        sa.Column("media_url", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. question_pools
    op.create_table(
        "question_pools",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("selection_rules_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. exam_templates
    op.create_table(
        "exam_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("total_marks", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("passing_marks", sa.Float(), nullable=False, server_default="40.0"),
        sa.Column("allow_calculator", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("shuffle_questions", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("shuffle_options", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("allow_offline_sync", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("sections_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("instructions", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. cbt_sessions
    op.create_table(
        "cbt_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("template_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_templates.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("exam_subject_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("session_code", sa.String(length=48), unique=True, nullable=False, index=True),
        sa.Column("start_window", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_window", sa.DateTime(timezone=True), nullable=False),
        sa.Column("delivery_mode", sa.String(length=24), nullable=False, server_default="ONLINE"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="SCHEDULED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. candidate_sessions
    op.create_table(
        "candidate_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("cbt_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("random_seed", sa.Integer(), nullable=False, server_default="12345"),
        sa.Column("device_fingerprint", sa.String(length=128), nullable=True),
        sa.Column("ip_address", sa.String(length=48), nullable=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("submit_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("remaining_seconds", sa.Integer(), nullable=False, server_default="3600"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="IN_PROGRESS"),
        sa.Column("total_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("marks_synced_to_module11", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("cbt_session_id", "student_id", name="uq_candidate_cbt_session"),
    )

    # 11. candidate_answers
    op.create_table(
        "candidate_answers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("candidate_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("question_versions.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("selected_options_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("text_answer", sa.Text(), nullable=True),
        sa.Column("is_marked_for_review", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("awarded_marks", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("time_spent_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("candidate_session_id", "question_id", name="uq_candidate_question_answer"),
    )

    # 12. answer_logs
    op.create_table(
        "answer_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("candidate_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("action_type", sa.String(length=32), nullable=False),
        sa.Column("payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. offline_sync_logs
    op.create_table(
        "offline_sync_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("candidate_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("batch_count", sa.Integer(), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="SYNCED"),
        sa.Column("synced_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. live_monitor_logs
    op.create_table(
        "live_monitor_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("cbt_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("candidate_session_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("warning_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("logged_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. question_statistics
    op.create_table(
        "question_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("question_versions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True),
        sa.Column("total_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_correct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_incorrect", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("difficulty_index", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("discrimination_index", sa.Float(), nullable=False, server_default="0.3"),
        sa.Column("average_time_seconds", sa.Float(), nullable=False, server_default="45.0"),
    )

    # 16. candidate_statistics
    op.create_table(
        "candidate_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("candidate_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True),
        sa.Column("attempted_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("correct_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("incorrect_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("accuracy_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("speed_questions_per_minute", sa.Float(), nullable=False, server_default="0.0"),
    )

    # 17. exam_statistics
    op.create_table(
        "exam_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("cbt_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True),
        sa.Column("total_registered", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_appeared", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("average_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("highest_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("lowest_score", sa.Float(), nullable=False, server_default="0.0"),
    )

    # 18. cbt_reports
    op.create_table(
        "cbt_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("report_type", sa.String(length=32), nullable=False, index=True),
        sa.Column("parameters_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("generated_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("cbt_reports")
    op.drop_table("exam_statistics")
    op.drop_table("candidate_statistics")
    op.drop_table("question_statistics")
    op.drop_table("live_monitor_logs")
    op.drop_table("offline_sync_logs")
    op.drop_table("answer_logs")
    op.drop_table("candidate_answers")
    op.drop_table("candidate_sessions")
    op.drop_table("cbt_sessions")
    op.drop_table("exam_templates")
    op.drop_table("question_pools")
    op.drop_table("question_media")
    op.drop_table("question_versions")
    op.drop_table("question_tags")
    op.drop_table("question_topics")
    op.drop_table("question_categories")
    op.drop_table("question_banks")
