"""Alembic migration for Module 2: Enterprise Authentication & Authorization
Adds:
- login_history
- refresh_tokens
- password_reset_tokens
- email_verification_tokens
- system_settings
- Extends users table with institutional identifier criteria and password history/lockout columns
- Extends audit_logs table with device_info and browser columns

Revision ID: 0002_module2_enterprise_auth
Revises: 0001_initial_module1
Create Date: 2026-11-06 11:30:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002_module2_enterprise_auth"
down_revision: Union[str, None] = "0001_initial_module1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Extend users table with configurable institutional criteria and password policy tracking
    op.add_column("users", sa.Column("registration_number", sa.String(length=64), nullable=True))
    op.add_column("users", sa.Column("enrollment_number", sa.String(length=64), nullable=True))
    op.add_column("users", sa.Column("roll_number", sa.String(length=64), nullable=True))
    op.add_column("users", sa.Column("erp_id", sa.String(length=64), nullable=True))
    op.add_column("users", sa.Column("student_id", sa.String(length=64), nullable=True))
    op.add_column("users", sa.Column("custom_field_identifier", sa.String(length=128), nullable=True))
    op.add_column("users", sa.Column("password_changed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("password_history", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"))

    op.create_index(op.f("ix_users_registration_number"), "users", ["registration_number"], unique=True)
    op.create_index(op.f("ix_users_enrollment_number"), "users", ["enrollment_number"], unique=True)
    op.create_index(op.f("ix_users_roll_number"), "users", ["roll_number"], unique=False)
    op.create_index(op.f("ix_users_erp_id"), "users", ["erp_id"], unique=True)
    op.create_index(op.f("ix_users_student_id"), "users", ["student_id"], unique=False)

    # 2. Extend audit_logs table with device_info and browser
    op.add_column("audit_logs", sa.Column("device_info", sa.String(length=255), nullable=False, server_default="Desktop"))
    op.add_column("audit_logs", sa.Column("browser", sa.String(length=64), nullable=False, server_default="Unknown"))

    # 3. Create login_history table
    op.create_table(
        "login_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="SET NULL"), nullable=True),
        sa.Column("identifier_used", sa.String(length=255), nullable=False),
        sa.Column("login_criterion", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("failure_reason", sa.String(length=255), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=False),
        sa.Column("user_agent", sa.String(length=512), nullable=False),
        sa.Column("device_type", sa.String(length=64), nullable=False, server_default="Desktop"),
        sa.Column("browser", sa.String(length=64), nullable=False, server_default="Unknown"),
        sa.Column("os", sa.String(length=64), nullable=False, server_default="Unknown"),
        sa.Column("session_id", sa.String(length=64), nullable=True),
        sa.Column("logged_in_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("logged_out_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_login_history_user_id"), "login_history", ["user_id"])
    op.create_index(op.f("ix_login_history_identifier_used"), "login_history", ["identifier_used"])
    op.create_index(op.f("ix_login_history_status"), "login_history", ["status"])

    # 4. Create refresh_tokens table (with device info and revocation timestamp)
    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False, unique=True),
        sa.Column("token_family", sa.String(length=64), nullable=False),
        sa.Column("ip_address", sa.String(length=64), nullable=False),
        sa.Column("user_agent", sa.String(length=512), nullable=False),
        sa.Column("device_info", sa.String(length=255), nullable=False, server_default="Desktop"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("revoked_reason", sa.String(length=255), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_refresh_tokens_user_id"), "refresh_tokens", ["user_id"])
    op.create_index(op.f("ix_refresh_tokens_token_hash"), "refresh_tokens", ["token_hash"])
    op.create_index(op.f("ix_refresh_tokens_token_family"), "refresh_tokens", ["token_family"])

    # 5. Create password_reset_tokens table
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_password_reset_tokens_user_id"), "password_reset_tokens", ["user_id"])
    op.create_index(op.f("ix_password_reset_tokens_token_hash"), "password_reset_tokens", ["token_hash"])

    # 6. Create email_verification_tokens table
    op.create_table(
        "email_verification_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_email_verification_tokens_user_id"), "email_verification_tokens", ["user_id"])

    # 7. Create system_settings table
    op.create_table(
        "system_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="auth"),
        sa.Column("value", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("key", "institute_id", name="uq_system_settings_key_institute"),
    )
    op.create_index(op.f("ix_system_settings_key"), "system_settings", ["key"])


def downgrade() -> None:
    op.drop_table("system_settings")
    op.drop_table("email_verification_tokens")
    op.drop_table("password_reset_tokens")
    op.drop_table("refresh_tokens")
    op.drop_table("login_history")
    op.drop_column("audit_logs", "browser")
    op.drop_column("audit_logs", "device_info")
    op.drop_column("users", "password_history")
    op.drop_column("users", "password_changed_at")
    op.drop_column("users", "custom_field_identifier")
    op.drop_column("users", "student_id")
    op.drop_column("users", "erp_id")
    op.drop_column("users", "roll_number")
    op.drop_column("users", "enrollment_number")
    op.drop_column("users", "registration_number")
