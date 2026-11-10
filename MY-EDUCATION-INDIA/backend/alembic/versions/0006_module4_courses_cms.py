"""Alembic migration for Phase 1 Module 4: Course Management CMS
Adds:
- cms_course_categories
- cms_courses
- cms_course_curricula
- cms_course_faculty

Revision ID: 0006_module4_courses_cms
Revises: 0005_module3_about_cms
Create Date: 2026-11-08 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0006_module4_courses_cms"
down_revision: Union[str, None] = "0005_module3_about_cms"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. cms_course_categories
    op.create_table(
        "cms_course_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("icon_name", sa.String(length=64), server_default="BookOpen", nullable=True),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index("ix_cms_course_categories_institute_id", "cms_course_categories", ["institute_id"])
    op.create_index("ix_cms_course_categories_slug", "cms_course_categories", ["slug"])

    # 2. cms_courses
    op.create_table(
        "cms_courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cms_course_categories.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("short_name", sa.String(length=64), nullable=False),
        sa.Column("degree_level", sa.String(length=64), nullable=False),
        sa.Column("duration", sa.String(length=64), nullable=False),
        sa.Column("study_mode", sa.String(length=64), server_default="Full-Time On-Campus", nullable=False),
        sa.Column("annual_fee", sa.String(length=64), nullable=False),
        sa.Column("total_fee", sa.String(length=64), nullable=True),
        sa.Column("seats_intake", sa.Integer(), server_default="60", nullable=False),
        sa.Column("eligibility_summary", sa.Text(), nullable=False),
        sa.Column("admission_process", sa.Text(), nullable=False),
        sa.Column("career_prospects", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("overview", sa.Text(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("brochure_pdf_url", sa.Text(), nullable=True),
        sa.Column("syllabus_pdf_url", sa.Text(), nullable=True),
        sa.Column("is_admissions_open", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("is_featured", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index("ix_cms_courses_institute_id", "cms_courses", ["institute_id"])
    op.create_index("ix_cms_courses_category_id", "cms_courses", ["category_id"])
    op.create_index("ix_cms_courses_code", "cms_courses", ["code"])
    op.create_index("ix_cms_courses_slug", "cms_courses", ["slug"])

    # 3. cms_course_curricula
    op.create_table(
        "cms_course_curricula",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cms_courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("semester_number", sa.Integer(), nullable=False),
        sa.Column("semester_title", sa.String(length=128), nullable=False),
        sa.Column("credits", sa.Integer(), server_default="24", nullable=False),
        sa.Column("subjects", postgresql.JSONB(astext_type=sa.Text()), server_default="[]", nullable=False),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index("ix_cms_course_curricula_course_id", "cms_course_curricula", ["course_id"])

    # 4. cms_course_faculty
    op.create_table(
        "cms_course_faculty",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cms_courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("faculty_name", sa.String(length=128), nullable=False),
        sa.Column("designation", sa.String(length=128), nullable=False),
        sa.Column("qualifications", sa.String(length=255), nullable=False),
        sa.Column("specialization", sa.String(length=255), nullable=False),
        sa.Column("avatar_url", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index("ix_cms_course_faculty_course_id", "cms_course_faculty", ["course_id"])


def downgrade() -> None:
    op.drop_table("cms_course_faculty")
    op.drop_table("cms_course_curricula")
    op.drop_table("cms_courses")
    op.drop_table("cms_course_categories")
