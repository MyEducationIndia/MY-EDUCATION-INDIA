"""Alembic migration for Module 4: Enterprise Admin Dashboard & Control Center
Creates:
- notifications
- dashboard_widgets
- user_pinned_modules
- dashboard_activities

Revision ID: 0004_module4_dashboard_control_center
Revises: 0003_module3_core_system_engine
Create Date: 2026-11-06 12:45:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0004_module4_dashboard_control_center"
down_revision: Union[str, None] = "0003_module3_core_system_engine"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. notifications table
    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="SYSTEM"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="NORMAL"),
        sa.Column("action_url", sa.String(length=255), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("meta_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_notifications_user_id"), "notifications", ["user_id"])
    op.create_index(op.f("ix_notifications_institute_id"), "notifications", ["institute_id"])
    op.create_index(op.f("ix_notifications_category"), "notifications", ["category"])
    op.create_index(op.f("ix_notifications_priority"), "notifications", ["priority"])
    op.create_index(op.f("ix_notifications_is_read"), "notifications", ["is_read"])

    # 2. dashboard_widgets table
    op.create_table(
        "dashboard_widgets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True),
        sa.Column("widget_key", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="ANALYTICS"),
        sa.Column("grid_position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("grid_width", sa.Integer(), nullable=False, server_default="6"),
        sa.Column("grid_height", sa.Integer(), nullable=False, server_default="4"),
        sa.Column("is_visible", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_pinned", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("configuration", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("widget_key", "user_id", name="uq_widget_user"),
    )
    op.create_index(op.f("ix_dashboard_widgets_user_id"), "dashboard_widgets", ["user_id"])
    op.create_index(op.f("ix_dashboard_widgets_widget_key"), "dashboard_widgets", ["widget_key"])

    # 3. user_pinned_modules table
    op.create_table(
        "user_pinned_modules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("module_key", sa.String(length=64), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "module_key", name="uq_user_pinned_module"),
    )
    op.create_index(op.f("ix_user_pinned_modules_user_id"), "user_pinned_modules", ["user_id"])

    # 4. dashboard_activities table
    op.create_table(
        "dashboard_activities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="SET NULL"), nullable=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="SET NULL"), nullable=True),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("actor_name", sa.String(length=120), nullable=False),
        sa.Column("action_type", sa.String(length=80), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=True),
        sa.Column("summary", sa.String(length=255), nullable=False),
        sa.Column("detail_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_dashboard_activities_action_type"), "dashboard_activities", ["action_type"])
    op.create_index(op.f("ix_dashboard_activities_occurred_at"), "dashboard_activities", ["occurred_at"])


def downgrade() -> None:
    op.drop_table("dashboard_activities")
    op.drop_table("user_pinned_modules")
    op.drop_table("dashboard_widgets")
    op.drop_table("notifications")
