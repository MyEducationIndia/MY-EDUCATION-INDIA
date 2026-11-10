"""Module 9 Migration: Enterprise Fee & Finance Management System Schema
Provisions:
1. fee_categories
2. fee_heads
3. fee_structures
4. fee_structure_items
5. installments
6. late_fee_rules
7. student_fee_assignments
8. payment_methods
9. payments
10. receipts
11. scholarships
12. discounts
13. concessions
14. refunds
15. fee_due_history
16. financial_reports

Revision ID: 0009_module9_fee_finance
Revises: 0008_module8_academic_engine
Create Date: 2026-11-06 08:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0009_module9_fee_finance"
down_revision: Union[str, None] = "0008_module8_academic_engine"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. fee_categories
    op.create_table(
        "fee_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. fee_heads
    op.create_table(
        "fee_heads",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fee_categories.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_refundable", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("default_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. late_fee_rules
    op.create_table(
        "late_fee_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("calculation_type", sa.String(length=24), nullable=False, server_default="DAILY"),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.Column("maximum_limit", sa.Float(), nullable=False, server_default="5000.0"),
        sa.Column("grace_period_days", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. fee_structures
    op.create_table(
        "fee_structures",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=48), nullable=False, index=True),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("program_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("semester_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("validity_date", sa.Date(), nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. fee_structure_items
    op.create_table(
        "fee_structure_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("fee_structure_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fee_structures.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("fee_head_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fee_heads.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("is_optional", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("frequency", sa.String(length=30), nullable=False, server_default="ONE_TIME"),
        sa.Column("due_period", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. installments
    op.create_table(
        "installments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("fee_structure_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fee_structures.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("installment_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("grace_days", sa.Integer(), nullable=False, server_default="7"),
        sa.Column("late_fee_rule_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("late_fee_rules.id", ondelete="SET NULL"), nullable=True),
        sa.Column("reminder_days_before", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="SCHEDULED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. student_fee_assignments
    op.create_table(
        "student_fee_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("fee_structure_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fee_structures.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("total_fee_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_discount_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_scholarship_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_payable_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_paid_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_due_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("assignment_type", sa.String(length=32), nullable=False, server_default="INDIVIDUAL"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="PENDING"),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. payment_methods
    op.create_table(
        "payment_methods",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("is_online", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("configuration_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. payments
    op.create_table(
        "payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_fee_assignment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("student_fee_assignments.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("installment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("installments.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("payment_number", sa.String(length=64), unique=True, nullable=False, index=True),
        sa.Column("amount_paid", sa.Float(), nullable=False),
        sa.Column("payment_mode", sa.String(length=32), nullable=False),
        sa.Column("payment_method_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("payment_methods.id", ondelete="SET NULL"), nullable=True),
        sa.Column("transaction_reference", sa.String(length=128), nullable=True, index=True),
        sa.Column("cheque_dd_number", sa.String(length=64), nullable=True),
        sa.Column("bank_name", sa.String(length=128), nullable=True),
        sa.Column("payment_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="COMPLETED"),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. receipts
    op.create_table(
        "receipts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("receipt_number", sa.String(length=64), unique=True, nullable=False, index=True),
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("payments.id", ondelete="RESTRICT"), nullable=False, unique=True, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("amount_in_words", sa.String(length=300), nullable=False),
        sa.Column("qr_code_data", sa.Text(), nullable=False),
        sa.Column("barcode_data", sa.String(length=128), nullable=False),
        sa.Column("digital_signature_hash", sa.String(length=128), nullable=False),
        sa.Column("receipt_date", sa.Date(), nullable=False),
        sa.Column("pdf_url", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="GENERATED"),
        sa.Column("generated_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. scholarships
    op.create_table(
        "scholarships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("scholarship_type", sa.String(length=32), nullable=False, server_default="MERIT"),
        sa.Column("calculation_type", sa.String(length=24), nullable=False, server_default="PERCENTAGE"),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("eligibility_criteria", sa.Text(), nullable=True),
        sa.Column("approval_workflow_status", sa.String(length=24), nullable=False, server_default="APPROVED"),
        sa.Column("approved_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("max_beneficiaries", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. discounts
    op.create_table(
        "discounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("discount_type", sa.String(length=32), nullable=False, server_default="SIBLING"),
        sa.Column("calculation_type", sa.String(length=24), nullable=False, server_default="PERCENTAGE"),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("max_discount_amount", sa.Float(), nullable=False, server_default="20000.0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. concessions
    op.create_table(
        "concessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_fee_assignment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("student_fee_assignments.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("scholarship_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scholarships.id", ondelete="SET NULL"), nullable=True),
        sa.Column("discount_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("discounts.id", ondelete="SET NULL"), nullable=True),
        sa.Column("concession_type", sa.String(length=32), nullable=False, server_default="SCHOLARSHIP"),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("approved_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("approval_status", sa.String(length=24), nullable=False, server_default="APPROVED"),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. refunds
    op.create_table(
        "refunds",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("payments.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("refund_number", sa.String(length=64), unique=True, nullable=False, index=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("refund_type", sa.String(length=24), nullable=False, server_default="PARTIAL"),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("approval_status", sa.String(length=24), nullable=False, server_default="PENDING"),
        sa.Column("approved_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("payment_mode", sa.String(length=32), nullable=False, server_default="BANK_TRANSFER"),
        sa.Column("reference_number", sa.String(length=128), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. fee_due_history
    op.create_table(
        "fee_due_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_fee_assignment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("student_fee_assignments.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("installment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("installments.id", ondelete="SET NULL"), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("due_amount", sa.Float(), nullable=False),
        sa.Column("penalty_amount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("reminder_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_reminder_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="UNPAID"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. financial_reports
    op.create_table(
        "financial_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("report_type", sa.String(length=32), nullable=False, index=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("total_records", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_amount_calculated", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("parameters_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("generated_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("financial_reports")
    op.drop_table("fee_due_history")
    op.drop_table("refunds")
    op.drop_table("concessions")
    op.drop_table("discounts")
    op.drop_table("scholarships")
    op.drop_table("receipts")
    op.drop_table("payments")
    op.drop_table("payment_methods")
    op.drop_table("student_fee_assignments")
    op.drop_table("installments")
    op.drop_table("fee_structure_items")
    op.drop_table("fee_structures")
    op.drop_table("late_fee_rules")
    op.drop_table("fee_heads")
    op.drop_table("fee_categories")
