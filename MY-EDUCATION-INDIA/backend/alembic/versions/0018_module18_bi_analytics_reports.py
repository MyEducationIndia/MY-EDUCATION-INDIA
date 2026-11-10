"""0018_module18_bi_analytics_reports

Revision ID: 0018_bi_platform
Revises: 0017_crm_franchise
Create Date: 2026-11-06 16:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0018_bi_platform'
down_revision = '0017_crm_franchise'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. report_definitions
    op.create_table(
        'report_definitions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('report_code', sa.String(length=50), nullable=False),
        sa.Column('report_name', sa.String(length=200), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source_tables', sa.JSON(), nullable=False),
        sa.Column('selected_fields', sa.JSON(), nullable=False),
        sa.Column('filter_config', sa.JSON(), nullable=True),
        sa.Column('aggregation_config', sa.JSON(), nullable=True),
        sa.Column('sort_config', sa.JSON(), nullable=True),
        sa.Column('is_system_report', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_by_user_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. report_templates
    op.create_table(
        'report_templates',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('template_name', sa.String(length=200), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('layout_type', sa.String(length=30), nullable=False, default='TABULAR'),
        sa.Column('definition_json', sa.JSON(), nullable=False),
        sa.Column('is_prebuilt', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 3. report_schedules
    op.create_table(
        'report_schedules',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('report_id', sa.String(length=36), sa.ForeignKey('report_definitions.id'), nullable=False),
        sa.Column('frequency', sa.String(length=30), nullable=False, default='WEEKLY'),
        sa.Column('cron_expression', sa.String(length=50), nullable=False),
        sa.Column('export_format', sa.String(length=20), nullable=False, default='PDF'),
        sa.Column('delivery_channel', sa.String(length=30), nullable=False, default='EMAIL'),
        sa.Column('recipient_list', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_run_at', sa.DateTime(), nullable=True),
        sa.Column('next_run_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 4. kpi_definitions
    op.create_table(
        'kpi_definitions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('kpi_key', sa.String(length=60), nullable=False),
        sa.Column('kpi_name', sa.String(length=150), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('calculation_formula', sa.String(length=255), nullable=False),
        sa.Column('target_value', sa.Float(), nullable=False),
        sa.Column('warning_threshold', sa.Float(), nullable=False),
        sa.Column('critical_threshold', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=30), nullable=False, default='%'),
        sa.Column('current_value', sa.Float(), nullable=False, default=0.0),
        sa.Column('trend_direction', sa.String(length=10), nullable=False, default='UP'),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. chart_definitions
    op.create_table(
        'chart_definitions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('chart_name', sa.String(length=150), nullable=False),
        sa.Column('chart_type', sa.String(length=30), nullable=False, default='BAR'),
        sa.Column('config_options_json', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. analytics_snapshots
    op.create_table(
        'analytics_snapshots',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('snapshot_date', sa.Date(), nullable=False),
        sa.Column('domain', sa.String(length=50), nullable=False),
        sa.Column('metrics_payload', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 7. system_health_logs
    op.create_table(
        'system_health_logs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('component_name', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, default='HEALTHY'),
        sa.Column('latency_ms', sa.Float(), nullable=False, default=0.0),
        sa.Column('error_rate_percentage', sa.Float(), nullable=False, default=0.0),
        sa.Column('details_json', sa.JSON(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('system_health_logs')
    op.drop_table('analytics_snapshots')
    op.drop_table('chart_definitions')
    op.drop_table('kpi_definitions')
    op.drop_table('report_schedules')
    op.drop_table('report_templates')
    op.drop_table('report_definitions')
