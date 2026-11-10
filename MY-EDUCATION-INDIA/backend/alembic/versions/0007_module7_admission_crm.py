"""Alembic migration for Module 7: Enterprise Admission & CRM Management System
Creates:
- crm_lead_sources
- crm_leads
- crm_lead_followups
- crm_counselling_sessions
- admission_applications
- admission_application_documents
- admission_entrance_tests
- admission_entrance_results
- admission_seat_management
- admission_scholarships
- admission_scholarship_allocations
- admission_fee_receipts
- admission_timeline

Revision ID: 0007_module7_admission_crm
Revises: 0006_module6_sims_engine
Create Date: 2026-11-06 13:10:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0007_module7_admission_crm"
down_revision: Union[str, None] = "0006_module6_sims_engine"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. crm_lead_sources table
    op.create_table(
        "crm_lead_sources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_lead_source_code_inst"),
    )

    # 2. crm_leads table
    op.create_table(
        "crm_leads",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="SET NULL"), nullable=True),
        sa.Column("lead_number", sa.String(length=64), nullable=False, unique=True),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("phone_number", sa.String(length=24), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("source_channel", sa.String(length=64), nullable=False, server_default="WEBSITE"),
        sa.Column("interested_course", sa.String(length=150), nullable=True),
        sa.Column("preferred_batch", sa.String(length=100), nullable=True),
        sa.Column("assigned_counsellor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="HOT"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="NEW"),
        sa.Column("next_followup_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("estimated_budget", sa.Float(), nullable=True),
        sa.Column("score", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_crm_leads_institute_id"), "crm_leads", ["institute_id"])
    op.create_index(op.f("ix_crm_leads_lead_number"), "crm_leads", ["lead_number"])
    op.create_index(op.f("ix_crm_leads_full_name"), "crm_leads", ["full_name"])
    op.create_index(op.f("ix_crm_leads_status"), "crm_leads", ["status"])

    # 3. crm_lead_followups table
    op.create_table(
        "crm_lead_followups",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("lead_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("crm_leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("counsellor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="CALL"),
        sa.Column("discussion_notes", sa.Text(), nullable=False),
        sa.Column("outcome", sa.String(length=64), nullable=False),
        sa.Column("scheduled_next_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("followed_up_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_crm_lead_followups_lead_id"), "crm_lead_followups", ["lead_id"])

    # 4. crm_counselling_sessions table
    op.create_table(
        "crm_counselling_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("lead_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("crm_leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("counsellor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("session_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("meeting_mode", sa.String(length=32), nullable=False, server_default="IN_PERSON"),
        sa.Column("recommendations", sa.Text(), nullable=False),
        sa.Column("career_aspiration", sa.String(length=255), nullable=True),
        sa.Column("scholarship_suggested_pct", sa.Float(), nullable=True, server_default="0.0"),
        sa.Column("outcome", sa.String(length=64), nullable=False, server_default="APPLICATION_ISSUED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. admission_applications table
    op.create_table(
        "admission_applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lead_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("crm_leads.id", ondelete="SET NULL"), nullable=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="SET NULL"), nullable=True),
        sa.Column("application_number", sa.String(length=64), nullable=False),
        sa.Column("application_mode", sa.String(length=32), nullable=False, server_default="ONLINE"),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("middle_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=24), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", sa.String(length=20), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False, server_default="GENERAL"),
        sa.Column("course_name", sa.String(length=150), nullable=False),
        sa.Column("batch_preference", sa.String(length=100), nullable=False),
        sa.Column("academic_year_code", sa.String(length=32), nullable=False),
        sa.Column("guardian_name", sa.String(length=150), nullable=False),
        sa.Column("guardian_phone", sa.String(length=24), nullable=False),
        sa.Column("guardian_relation", sa.String(length=32), nullable=False, server_default="FATHER"),
        sa.Column("address_line1", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("postal_code", sa.String(length=20), nullable=False),
        sa.Column("previous_institution", sa.String(length=200), nullable=True),
        sa.Column("previous_marks_percentage", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("approved_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejection_reason", sa.String(length=500), nullable=True),
        sa.Column("custom_form_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("application_number", "institute_id", name="uq_app_num_inst"),
    )
    op.create_index(op.f("ix_admission_applications_institute_id"), "admission_applications", ["institute_id"])
    op.create_index(op.f("ix_admission_applications_application_number"), "admission_applications", ["application_number"])
    op.create_index(op.f("ix_admission_applications_status"), "admission_applications", ["status"])

    # 6. admission_application_documents table
    op.create_table(
        "admission_application_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("admission_applications.id", ondelete="CASCADE"), nullable=False),
        sa.Column("document_type", sa.String(length=64), nullable=False),
        sa.Column("document_title", sa.String(length=150), nullable=False),
        sa.Column("file_url", sa.Text(), nullable=False),
        sa.Column("verification_status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("remarks", sa.String(length=255), nullable=True),
        sa.Column("verified_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. admission_entrance_tests table
    op.create_table(
        "admission_entrance_tests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("test_code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("course_name", sa.String(length=150), nullable=False),
        sa.Column("test_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("max_marks", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("passing_marks", sa.Integer(), nullable=False, server_default="40"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. admission_entrance_results table
    op.create_table(
        "admission_entrance_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("admission_applications.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("test_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("admission_entrance_tests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("marks_obtained", sa.Float(), nullable=False),
        sa.Column("percentile", sa.Float(), nullable=True),
        sa.Column("merit_rank", sa.Integer(), nullable=True),
        sa.Column("is_qualified", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("application_id", "test_id", name="uq_app_test_result"),
    )

    # 9. admission_seat_management table
    op.create_table(
        "admission_seat_management",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_name", sa.String(length=150), nullable=False),
        sa.Column("academic_year_code", sa.String(length=32), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False, server_default="GENERAL"),
        sa.Column("total_seats", sa.Integer(), nullable=False),
        sa.Column("filled_seats", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("waiting_seats", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("institute_id", "branch_id", "course_name", "academic_year_code", "category", name="uq_seat_quota"),
    )

    # 10. admission_scholarships table
    op.create_table(
        "admission_scholarships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("discount_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("fixed_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("criteria_description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. admission_scholarship_allocations table
    op.create_table(
        "admission_scholarship_allocations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("admission_applications.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("scholarship_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("admission_scholarships.id", ondelete="CASCADE"), nullable=False),
        sa.Column("awarded_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("awarded_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("approved_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("approval_status", sa.String(length=32), nullable=False, server_default="APPROVED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. admission_fee_receipts table
    op.create_table(
        "admission_fee_receipts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("admission_applications.id", ondelete="CASCADE"), nullable=False),
        sa.Column("receipt_number", sa.String(length=64), nullable=False, unique=True),
        sa.Column("fee_type", sa.String(length=64), nullable=False, server_default="ADMISSION_FEE"),
        sa.Column("amount_paid", sa.Float(), nullable=False),
        sa.Column("payment_mode", sa.String(length=32), nullable=False, server_default="ONLINE"),
        sa.Column("transaction_reference", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="SUCCESS"),
        sa.Column("collected_by", sa.String(length=100), nullable=False, server_default="Payment Gateway"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. admission_timeline table
    op.create_table(
        "admission_timeline",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("admission_applications.id", ondelete="CASCADE"), nullable=False),
        sa.Column("stage", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("actor_name", sa.String(length=100), nullable=False, server_default="System"),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metadata_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_admission_timeline_application_id"), "admission_timeline", ["application_id"])


def downgrade() -> None:
    op.drop_table("admission_timeline")
    op.drop_table("admission_fee_receipts")
    op.drop_table("admission_scholarship_allocations")
    op.drop_table("admission_scholarships")
    op.drop_table("admission_seat_management")
    op.drop_table("admission_entrance_results")
    op.drop_table("admission_entrance_tests")
    op.drop_table("admission_application_documents")
    op.drop_table("admission_applications")
    op.drop_table("crm_counselling_sessions")
    op.drop_table("crm_lead_followups")
    op.drop_table("crm_leads")
    op.drop_table("crm_lead_sources")
