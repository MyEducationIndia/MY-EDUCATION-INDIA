"""0016_future_api_integration_framework

Revision ID: 0016_api_framework
Revises: 0015_lxp_platform
Create Date: 2026-11-06 15:45:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0016_api_framework'
down_revision = '0015_lxp_platform'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Provisions 6 core tables for Universal API Integration Framework
    op.create_table(
        'api_providers',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('provider_key', sa.String(length=60), nullable=False),
        sa.Column('display_name', sa.String(length=150), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('auth_type', sa.String(length=50), nullable=False, default='API_KEY'),
        sa.Column('base_url', sa.String(length=500), nullable=False),
        sa.Column('is_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_default', sa.Boolean(), nullable=False, default=False),
        sa.Column('failover_provider_id', sa.String(length=36), nullable=True),
        sa.Column('rate_limit_per_minute', sa.Integer(), nullable=False, default=120),
        sa.Column('timeout_seconds', sa.Integer(), nullable=False, default=10),
        sa.Column('retry_max_attempts', sa.Integer(), nullable=False, default=3),
        sa.Column('retry_backoff_factor', sa.Float(), nullable=False, default=2.0),
        sa.Column('circuit_breaker_threshold', sa.Integer(), nullable=False, default=5),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('api_providers')
