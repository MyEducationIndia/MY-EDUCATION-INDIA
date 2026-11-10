"""0014_module14_library_knowledge

Revision ID: 0014_lib_knowledge
Revises: 0013_cert_verification
Create Date: 2026-11-06 09:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0014_lib_knowledge'
down_revision = '0013_cert_verification'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Provisions 18 tables for Module 14
    op.create_table(
        'library_categories',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parent_category_id', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('library_categories')
