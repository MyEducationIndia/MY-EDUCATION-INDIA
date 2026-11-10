"""0020_module20_enterprise_experience_platform

Revision ID: 0020_experience_platform
Revises: 0019_platform_devops
Create Date: 2026-11-06 17:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0020_experience_platform'
down_revision = '0019_platform_devops'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. root_owner_controls
    op.create_table(
        'root_owner_controls',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('owner_username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('hashed_passphrase', sa.String(length=255), nullable=False),
        sa.Column('emergency_lockdown_active', sa.Boolean(), nullable=False, default=False),
        sa.Column('developer_mode_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('license_tier', sa.String(length=50), nullable=False, default='UNLIMITED_PROPRIETARY'),
        sa.Column('global_encryption_key_hash', sa.String(length=128), nullable=False),
        sa.Column('platform_clone_token', sa.String(length=128), nullable=True),
        sa.Column('last_root_login_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. portal_configurations
    op.create_table(
        'portal_configurations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('portal_type', sa.String(length=50), nullable=False),
        sa.Column('display_title', sa.String(length=150), nullable=False),
        sa.Column('theme_palette', sa.JSON(), nullable=True),
        sa.Column('allowed_roles', sa.JSON(), nullable=False),
        sa.Column('default_route', sa.String(length=100), nullable=False, default='/dashboard'),
        sa.Column('is_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('navigation_tree_json', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 3. user_portal_preferences
    op.create_table(
        'user_portal_preferences',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('portal_type', sa.String(length=50), nullable=False),
        sa.Column('dark_mode', sa.Boolean(), nullable=False, default=False),
        sa.Column('sidebar_collapsed', sa.Boolean(), nullable=False, default=False),
        sa.Column('accent_color', sa.String(length=20), nullable=False, default='#4f46e5'),
        sa.Column('dashboard_layout_id', sa.String(length=36), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 4. dynamic_menus
    op.create_table(
        'dynamic_menus',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('menu_key', sa.String(length=60), nullable=False),
        sa.Column('menu_name', sa.String(length=150), nullable=False),
        sa.Column('target_portal', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. page_definitions
    op.create_table(
        'page_definitions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('page_slug', sa.String(length=150), nullable=False),
        sa.Column('page_title', sa.String(length=200), nullable=False),
        sa.Column('content_blocks_json', sa.JSON(), nullable=False),
        sa.Column('seo_meta_tags', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=False, default='PUBLISHED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. form_definitions
    op.create_table(
        'form_definitions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('form_key', sa.String(length=60), nullable=False),
        sa.Column('form_title', sa.String(length=200), nullable=False),
        sa.Column('schema_fields_json', sa.JSON(), nullable=False),
        sa.Column('target_module', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 7. support_tickets
    op.create_table(
        'support_tickets',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('ticket_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('submitted_by_user_id', sa.String(length=36), nullable=False),
        sa.Column('subject', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, default='TECHNICAL'),
        sa.Column('priority', sa.String(length=20), nullable=False, default='MEDIUM'),
        sa.Column('status', sa.String(length=30), nullable=False, default='OPEN'),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('support_tickets')
    op.drop_table('form_definitions')
    op.drop_table('page_definitions')
    op.drop_table('dynamic_menus')
    op.drop_table('user_portal_preferences')
    op.drop_table('portal_configurations')
    op.drop_table('root_owner_controls')
