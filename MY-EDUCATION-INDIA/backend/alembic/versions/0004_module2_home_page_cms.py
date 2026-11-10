"""Alembic migration for Phase 1 Module 2: Home Page CMS
Adds:
- cms_hero_slides
- cms_stat_counters
- cms_quick_links
- cms_featured_programs
- cms_recruiter_logos
- cms_testimonials
- cms_newsletter_subscribers

Revision ID: 0004_module2_home_page_cms
Revises: 0003_public_website_framework
Create Date: 2026-11-07 14:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0004_module2_home_page_cms"
down_revision: Union[str, None] = "0003_public_website_framework"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. cms_hero_slides
    op.create_table(
        "cms_hero_slides",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("badge_text", sa.String(length=128), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("subtitle", sa.Text(), nullable=False),
        sa.Column("background_image_url", sa.Text(), nullable=True),
        sa.Column("video_url", sa.Text(), nullable=True),
        sa.Column("primary_cta_text", sa.String(length=64), nullable=False, server_default="Apply Now"),
        sa.Column("primary_cta_link", sa.String(length=255), nullable=False, server_default="/admissions/apply"),
        sa.Column("secondary_cta_text", sa.String(length=64), nullable=True),
        sa.Column("secondary_cta_link", sa.String(length=255), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_hero_slides_institute_id"), "cms_hero_slides", ["institute_id"], unique=False)

    # 2. cms_stat_counters
    op.create_table(
        "cms_stat_counters",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("metric_value", sa.String(length=64), nullable=False),
        sa.Column("numeric_target", sa.Integer(), nullable=True),
        sa.Column("label", sa.String(length=128), nullable=False),
        sa.Column("subtext", sa.String(length=255), nullable=True),
        sa.Column("icon_name", sa.String(length=64), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_stat_counters_institute_id"), "cms_stat_counters", ["institute_id"], unique=False)

    # 3. cms_quick_links
    op.create_table(
        "cms_quick_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("path", sa.String(length=255), nullable=False),
        sa.Column("icon_name", sa.String(length=64), nullable=True),
        sa.Column("badge_label", sa.String(length=32), nullable=True),
        sa.Column("is_external", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_quick_links_institute_id"), "cms_quick_links", ["institute_id"], unique=False)

    # 4. cms_featured_programs
    op.create_table(
        "cms_featured_programs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("degree_level", sa.String(length=32), nullable=False, server_default="Undergraduate"),
        sa.Column("duration", sa.String(length=64), nullable=False, server_default="4 Years (8 Semesters)"),
        sa.Column("annual_fee", sa.String(length=64), nullable=True),
        sa.Column("eligibility_summary", sa.String(length=255), nullable=False, server_default="10+2 with PCM >= 60%"),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("syllabus_url", sa.Text(), nullable=True),
        sa.Column("is_admissions_open", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_featured_programs_institute_id"), "cms_featured_programs", ["institute_id"], unique=False)
    op.create_index(op.f("ix_cms_featured_programs_code"), "cms_featured_programs", ["code"], unique=False)

    # 5. cms_recruiter_logos
    op.create_table(
        "cms_recruiter_logos",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("company_name", sa.String(length=128), nullable=False),
        sa.Column("tier", sa.String(length=32), nullable=False, server_default="Tier 1"),
        sa.Column("highest_package_lpa", sa.String(length=32), nullable=True),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.Column("website_url", sa.String(length=500), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_recruiter_logos_institute_id"), "cms_recruiter_logos", ["institute_id"], unique=False)

    # 6. cms_testimonials
    op.create_table(
        "cms_testimonials",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_name", sa.String(length=128), nullable=False),
        sa.Column("author_role", sa.String(length=128), nullable=False),
        sa.Column("author_category", sa.String(length=32), nullable=False, server_default="Student"),
        sa.Column("rating_stars", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("quote", sa.Text(), nullable=False),
        sa.Column("avatar_url", sa.Text(), nullable=True),
        sa.Column("video_url", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_testimonials_institute_id"), "cms_testimonials", ["institute_id"], unique=False)

    # 7. cms_newsletter_subscribers
    op.create_table(
        "cms_newsletter_subscribers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("subscribed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_newsletter_subscribers_institute_id"), "cms_newsletter_subscribers", ["institute_id"], unique=False)
    op.create_index(op.f("ix_cms_newsletter_subscribers_email"), "cms_newsletter_subscribers", ["email"], unique=False)


def downgrade() -> None:
    op.drop_table("cms_newsletter_subscribers")
    op.drop_table("cms_testimonials")
    op.drop_table("cms_recruiter_logos")
    op.drop_table("cms_featured_programs")
    op.drop_table("cms_quick_links")
    op.drop_table("cms_stat_counters")
    op.drop_table("cms_hero_slides")
