"""0017_module17_crm_marketing_franchise

Revision ID: 0017_crm_franchise
Revises: 0016_api_framework
Create Date: 2026-11-06 16:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0017_crm_franchise'
down_revision = '0016_api_framework'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. crm_lead_sources
    op.create_table(
        'crm_lead_sources',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('source_name', sa.String(length=100), nullable=False),
        sa.Column('source_code', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. crm_leads
    op.create_table(
        'crm_leads',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('lead_code', sa.String(length=50), nullable=False),
        sa.Column('full_name', sa.String(length=200), nullable=False),
        sa.Column('mobile', sa.String(length=30), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('guardian_name', sa.String(length=200), nullable=True),
        sa.Column('course_interested_id', sa.String(length=36), nullable=True),
        sa.Column('source_id', sa.String(length=36), sa.ForeignKey('crm_lead_sources.id'), nullable=True),
        sa.Column('priority', sa.String(length=20), nullable=False, default='MEDIUM'),
        sa.Column('assigned_counsellor_id', sa.String(length=36), nullable=True),
        sa.Column('stage', sa.String(length=50), nullable=False, default='NEW_LEAD'),
        sa.Column('status', sa.String(length=30), nullable=False, default='ACTIVE'),
        sa.Column('expected_admission_date', sa.Date(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=False, default=50),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('custom_fields', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 3. crm_enquiries
    op.create_table(
        'crm_enquiries',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('enquiry_code', sa.String(length=50), nullable=False),
        sa.Column('enquirer_name', sa.String(length=200), nullable=False),
        sa.Column('mobile', sa.String(length=30), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('source_type', sa.String(length=50), nullable=False, default='WEBSITE'),
        sa.Column('course_id', sa.String(length=36), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('is_converted_to_lead', sa.Boolean(), nullable=False, default=False),
        sa.Column('lead_id', sa.String(length=36), sa.ForeignKey('crm_leads.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 4. crm_followups
    op.create_table(
        'crm_followups',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('lead_id', sa.String(length=36), sa.ForeignKey('crm_leads.id'), nullable=False),
        sa.Column('counsellor_id', sa.String(length=36), nullable=False),
        sa.Column('channel', sa.String(length=30), nullable=False, default='CALL'),
        sa.Column('scheduled_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('outcome', sa.String(length=50), nullable=True),
        sa.Column('next_followup_date', sa.DateTime(), nullable=True),
        sa.Column('is_reminder_sent', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. crm_pipeline
    op.create_table(
        'crm_pipeline',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('stage_key', sa.String(length=50), nullable=False),
        sa.Column('stage_name', sa.String(length=100), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False, default=1),
        sa.Column('probability_percentage', sa.Float(), nullable=False, default=10.0),
        sa.Column('is_won_stage', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_lost_stage', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. crm_campaigns
    op.create_table(
        'crm_campaigns',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('campaign_name', sa.String(length=200), nullable=False),
        sa.Column('channel', sa.String(length=50), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('allocated_budget', sa.Float(), nullable=False, default=0.0),
        sa.Column('actual_spent', sa.Float(), nullable=False, default=0.0),
        sa.Column('status', sa.String(length=30), nullable=False, default='ACTIVE'),
        sa.Column('utm_source', sa.String(length=100), nullable=True),
        sa.Column('utm_campaign', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 7. crm_campaign_results
    op.create_table(
        'crm_campaign_results',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('campaign_id', sa.String(length=36), sa.ForeignKey('crm_campaigns.id'), nullable=False),
        sa.Column('leads_generated', sa.Integer(), nullable=False, default=0),
        sa.Column('admissions_converted', sa.Integer(), nullable=False, default=0),
        sa.Column('revenue_generated', sa.Float(), nullable=False, default=0.0),
        sa.Column('cost_per_lead', sa.Float(), nullable=False, default=0.0),
        sa.Column('roi_percentage', sa.Float(), nullable=False, default=0.0),
        sa.Column('recorded_date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 8. franchise_centers
    op.create_table(
        'franchise_centers',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('institute_id', sa.String(length=36), nullable=False),
        sa.Column('center_code', sa.String(length=50), nullable=False, unique=True),
        sa.Column('center_name', sa.String(length=200), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=100), nullable=False),
        sa.Column('contact_email', sa.String(length=150), nullable=False),
        sa.Column('contact_phone', sa.String(length=30), nullable=False),
        sa.Column('royalty_percentage', sa.Float(), nullable=False, default=15.0),
        sa.Column('status', sa.String(length=30), nullable=False, default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 9. franchise_users
    op.create_table(
        'franchise_users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('center_id', sa.String(length=36), sa.ForeignKey('franchise_centers.id'), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, default='COUNSELLOR'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('franchise_users')
    op.drop_table('franchise_centers')
    op.drop_table('crm_campaign_results')
    op.drop_table('crm_campaigns')
    op.drop_table('crm_pipeline')
    op.drop_table('crm_followups')
    op.drop_table('crm_enquiries')
    op.drop_table('crm_leads')
    op.drop_table('crm_lead_sources')
