"""0015_module15_enterprise_lxp

Revision ID: 0015_lxp_platform
Revises: 0014_lib_knowledge
Create Date: 2026-11-06 15:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0015_lxp_platform'
down_revision = '0014_lib_knowledge'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Provisions 17 tables for Module 15
    op.create_table(
        'learning_courses',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('course_code', sa.String(length=50), nullable=False),
        sa.Column('course_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('difficulty', sa.String(length=30), nullable=False, default='BEGINNER'),
        sa.Column('language', sa.String(length=50), nullable=False, default='English'),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, default=0),
        sa.Column('thumbnail_url', sa.String(length=500), nullable=True),
        sa.Column('banner_url', sa.String(length=500), nullable=True),
        sa.Column('instructor_id', sa.String(length=36), nullable=False),
        sa.Column('department_id', sa.String(length=36), nullable=True),
        sa.Column('academic_program_id', sa.String(length=36), nullable=True),
        sa.Column('fee_amount', sa.Float(), nullable=False, default=0.0),
        sa.Column('certificate_template_id', sa.String(length=36), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=False, default='DRAFT'),
        sa.Column('visibility', sa.String(length=30), nullable=False, default='PUBLIC'),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('is_free', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('learning_courses')
