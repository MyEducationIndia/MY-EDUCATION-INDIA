"""0019_module19_platform_admin_devops

Revision ID: 0019_platform_devops
Revises: 0018_bi_platform
Create Date: 2026-11-06 17:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0019_platform_devops'
down_revision = '0018_bi_platform'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. platform_settings
    op.create_table(
        'platform_settings',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('setting_key', sa.String(length=100), nullable=False),
        sa.Column('setting_value', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, default='GENERAL'),
        sa.Column('is_system', sa.Boolean(), nullable=False, default=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. security_policies
    op.create_table(
        'security_policies',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('policy_name', sa.String(length=100), nullable=False),
        sa.Column('min_password_length', sa.Integer(), nullable=False, default=10),
        sa.Column('require_uppercase', sa.Boolean(), nullable=False, default=True),
        sa.Column('require_numbers', sa.Boolean(), nullable=False, default=True),
        sa.Column('require_special_chars', sa.Boolean(), nullable=False, default=True),
        sa.Column('password_expiry_days', sa.Integer(), nullable=False, default=90),
        sa.Column('max_failed_attempts', sa.Integer(), nullable=False, default=5),
        sa.Column('lockout_duration_minutes', sa.Integer(), nullable=False, default=30),
        sa.Column('session_timeout_minutes', sa.Integer(), nullable=False, default=60),
        sa.Column('allowed_ip_ranges', sa.JSON(), nullable=True),
        sa.Column('enforce_2fa', sa.Boolean(), nullable=False, default=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 3. backup_jobs
    op.create_table(
        'backup_jobs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('job_name', sa.String(length=150), nullable=False),
        sa.Column('backup_type', sa.String(length=50), nullable=False, default='FULL'),
        sa.Column('schedule_cron', sa.String(length=50), nullable=False, default='0 2 * * *'),
        sa.Column('storage_destination', sa.String(length=50), nullable=False, default='LOCAL'),
        sa.Column('is_encrypted', sa.Boolean(), nullable=False, default=True),
        sa.Column('compression_algorithm', sa.String(length=20), nullable=False, default='GZIP'),
        sa.Column('retention_days', sa.Integer(), nullable=False, default=30),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_run_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 4. backup_history
    op.create_table(
        'backup_history',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('job_id', sa.String(length=36), sa.ForeignKey('backup_jobs.id'), nullable=True),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('backup_type', sa.String(length=50), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=False, default=0),
        sa.Column('checksum_sha256', sa.String(length=64), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, default='COMPLETED'),
        sa.Column('duration_seconds', sa.Integer(), nullable=False, default=0),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. feature_flags
    op.create_table(
        'feature_flags',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('flag_key', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=False, default=False),
        sa.Column('rollout_percentage', sa.Float(), nullable=False, default=100.0),
        sa.Column('target_roles', sa.JSON(), nullable=True),
        sa.Column('target_branches', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. maintenance_windows
    op.create_table(
        'maintenance_windows',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=False),
        sa.Column('whitelist_user_ids', sa.JSON(), nullable=True),
        sa.Column('custom_banner_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('maintenance_windows')
    op.drop_table('feature_flags')
    op.drop_table('backup_history')
    op.drop_table('backup_jobs')
    op.drop_table('security_policies')
    op.drop_table('platform_settings')
