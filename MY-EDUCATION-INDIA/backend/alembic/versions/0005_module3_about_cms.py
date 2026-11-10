"""Alembic migration for Phase 1 Module 3: About Institute CMS
Adds:
- cms_milestones
- cms_leadership_messages
- cms_accreditations
- cms_campus_infrastructure

Revision ID: 0005_module3_about_cms
Revises: 0004_module2_home_page_cms
Create Date: 2026-11-07 18:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0005_module3_about_cms"
down_revision: Union[str, None] = "0004_module2_home_page_cms"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. cms_milestones
    op.create_table(
        "cms_milestones",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("year", sa.String(length=16), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("icon_name", sa.String(length=64), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_milestones_institute_id"), "cms_milestones", ["institute_id"], unique=False)

    # 2. cms_leadership_messages
    op.create_table(
        "cms_leadership_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("leader_name", sa.String(length=128), nullable=False),
        sa.Column("leader_designation", sa.String(length=128), nullable=False),
        sa.Column("role_category", sa.String(length=64), nullable=False),
        sa.Column("salutation_title", sa.String(length=255), nullable=False),
        sa.Column("message_body", sa.Text(), nullable=False),
        sa.Column("portrait_image_url", sa.Text(), nullable=True),
        sa.Column("signature_image_url", sa.Text(), nullable=True),
        sa.Column("video_address_url", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_leadership_messages_institute_id"), "cms_leadership_messages", ["institute_id"], unique=False)
    op.create_index(op.f("ix_cms_leadership_messages_role_category"), "cms_leadership_messages", ["role_category"], unique=False)

    # 3. cms_accreditations
    op.create_table(
        "cms_accreditations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("accrediting_body", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("approval_reference_number", sa.String(length=128), nullable=False),
        sa.Column("valid_from", sa.String(length=32), nullable=True),
        sa.Column("valid_upto", sa.String(length=32), nullable=True),
        sa.Column("certificate_pdf_url", sa.Text(), nullable=True),
        sa.Column("logo_badge_url", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_accreditations_institute_id"), "cms_accreditations", ["institute_id"], unique=False)

    # 4. cms_campus_infrastructure
    op.create_table(
        "cms_campus_infrastructure",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("facility_name", sa.String(length=128), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("capacity_metric", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("floor_or_location", sa.String(length=128), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_campus_infrastructure_institute_id"), "cms_campus_infrastructure", ["institute_id"], unique=False)


def downgrade() -> None:
    op.drop_table("cms_campus_infrastructure")
    op.drop_table("cms_accreditations")
    op.drop_table("cms_leadership_messages")
    op.drop_table("cms_milestones")
