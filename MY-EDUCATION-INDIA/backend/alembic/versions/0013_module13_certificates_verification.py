"""Module 13 Migration: Enterprise Certificate, Document Generation & Digital Verification System Schema
Provisions:
1. document_types
2. certificate_templates
3. certificate_fields
4. certificate_layouts
5. certificate_numbers
6. issued_certificates
7. generated_documents
8. verification_tokens
9. verification_logs
10. digital_signatures
11. certificate_status_history
12. id_cards
13. document_archives
14. certificate_reports
15. certificate_analytics

Revision ID: 0013_module13_certificates_verification
Revises: 0012_module12_cbt_platform
Create Date: 2026-11-06 12:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0013_module13_certificates_verification"
down_revision: Union[str, None] = "0012_module12_cbt_platform"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. document_types
    op.create_table(
        "document_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("code", sa.String(length=32), nullable=False, index=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=32), nullable=False, server_default="ACADEMIC"),
        sa.Column("requires_approval", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("has_expiry", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("validity_months", sa.Integer(), nullable=False, server_default="12"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. certificate_templates
    op.create_table(
        "certificate_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("document_type_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("document_types.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("template_code", sa.String(length=48), nullable=False, index=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("page_orientation", sa.String(length=16), nullable=False, server_default="LANDSCAPE"),
        sa.Column("page_size", sa.String(length=16), nullable=False, server_default="A4"),
        sa.Column("background_image_url", sa.Text(), nullable=True),
        sa.Column("html_markup", sa.Text(), nullable=False),
        sa.Column("css_styles", sa.Text(), nullable=False, server_default=""),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. certificate_fields
    op.create_table(
        "certificate_fields",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("template_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("certificate_templates.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("field_key", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("field_type", sa.String(length=32), nullable=False, server_default="TEXT"),
        sa.Column("is_required", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("default_value", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. certificate_layouts
    op.create_table(
        "certificate_layouts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("template_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("certificate_templates.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("elements_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. certificate_numbers
    op.create_table(
        "certificate_numbers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("prefix", sa.String(length=24), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("current_counter", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. issued_certificates
    op.create_table(
        "issued_certificates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("certificate_number", sa.String(length=64), unique=True, nullable=False, index=True),
        sa.Column("verification_id", sa.String(length=64), unique=True, nullable=False, index=True),
        sa.Column("template_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("certificate_templates.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("recipient_type", sa.String(length=24), nullable=False, server_default="STUDENT"),
        sa.Column("recipient_user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("issue_date", sa.Date(), nullable=False, index=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("payload_data_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("pdf_document_url", sa.Text(), nullable=True),
        sa.Column("qr_code_payload", sa.Text(), nullable=False),
        sa.Column("barcode_data", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="ISSUED"),
        sa.Column("revocation_reason", sa.Text(), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("issued_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. generated_documents
    op.create_table(
        "generated_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("document_type_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("document_types.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mime_type", sa.String(length=64), nullable=False, server_default="application/pdf"),
        sa.Column("generated_for_user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. verification_tokens
    op.create_table(
        "verification_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("certificate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("issued_certificates.id", ondelete="CASCADE"), nullable=False, unique=True, index=True),
        sa.Column("token_hash", sa.String(length=128), unique=True, nullable=False, index=True),
        sa.Column("public_verification_url", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. verification_logs
    op.create_table(
        "verification_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("token_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("verification_tokens.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("ip_address", sa.String(length=48), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("result_status", sa.String(length=24), nullable=False, server_default="VALID"),
    )

    # 10. digital_signatures
    op.create_table(
        "digital_signatures",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("certificate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("issued_certificates.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("signatory_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("signature_type", sa.String(length=24), nullable=False, server_default="PKI_CRYPTO_HASH"),
        sa.Column("signature_hash", sa.String(length=128), nullable=False),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. certificate_status_history
    op.create_table(
        "certificate_status_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("certificate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("issued_certificates.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("previous_status", sa.String(length=24), nullable=False),
        sa.Column("new_status", sa.String(length=24), nullable=False),
        sa.Column("changed_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. id_cards
    op.create_table(
        "id_cards",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("card_number", sa.String(length=64), unique=True, nullable=False, index=True),
        sa.Column("holder_type", sa.String(length=24), nullable=False, server_default="STUDENT"),
        sa.Column("holder_user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("blood_group", sa.String(length=8), nullable=True),
        sa.Column("emergency_contact", sa.String(length=32), nullable=True),
        sa.Column("valid_until", sa.Date(), nullable=False),
        sa.Column("qr_code_payload", sa.Text(), nullable=False),
        sa.Column("barcode_data", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. document_archives
    op.create_table(
        "document_archives",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("certificate_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("archived_reason", sa.Text(), nullable=False),
        sa.Column("archived_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. certificate_reports
    op.create_table(
        "certificate_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("report_type", sa.String(length=32), nullable=False, index=True),
        sa.Column("parameters_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("generated_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. certificate_analytics
    op.create_table(
        "certificate_analytics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("snapshot_date", sa.Date(), nullable=False, index=True),
        sa.Column("total_issued", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_verified", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_revoked", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("metrics_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("certificate_analytics")
    op.drop_table("certificate_reports")
    op.drop_table("document_archives")
    op.drop_table("id_cards")
    op.drop_table("certificate_status_history")
    op.drop_table("digital_signatures")
    op.drop_table("verification_logs")
    op.drop_table("verification_tokens")
    op.drop_table("generated_documents")
    op.drop_table("issued_certificates")
    op.drop_table("certificate_numbers")
    op.drop_table("certificate_layouts")
    op.drop_table("certificate_fields")
    op.drop_table("certificate_templates")
    op.drop_table("document_types")
