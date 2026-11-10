"""Alembic migration for Module 6: Enterprise Student Information Management System (SIMS)
Creates:
- students
- student_profiles
- student_addresses
- student_guardians
- student_documents
- student_medical
- student_custom_fields
- student_custom_values
- student_status_history
- student_timeline
- student_notes
- student_photos
- student_qr_codes

Revision ID: 0006_module6_sims_engine
Revises: 0005_module5_cms_engine
Create Date: 2026-11-06 13:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0006_module6_sims_engine"
down_revision: Union[str, None] = "0005_module5_cms_engine"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. students table
    op.create_table(
        "students",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("registration_number", sa.String(length=64), nullable=False),
        sa.Column("enrollment_number", sa.String(length=64), nullable=True),
        sa.Column("roll_number", sa.String(length=64), nullable=True),
        sa.Column("erp_id", sa.String(length=64), nullable=True, unique=True),
        sa.Column("library_card_number", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("middle_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=24), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", sa.String(length=20), nullable=False),
        sa.Column("course_name", sa.String(length=150), nullable=False),
        sa.Column("batch_name", sa.String(length=100), nullable=False),
        sa.Column("academic_year_code", sa.String(length=32), nullable=False),
        sa.Column("admission_date", sa.Date(), nullable=False),
        sa.Column("semester_or_year", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("registration_number", "institute_id", name="uq_student_reg_inst"),
        sa.UniqueConstraint("enrollment_number", "institute_id", name="uq_student_enroll_inst"),
    )
    op.create_index(op.f("ix_students_institute_id"), "students", ["institute_id"])
    op.create_index(op.f("ix_students_branch_id"), "students", ["branch_id"])
    op.create_index(op.f("ix_students_registration_number"), "students", ["registration_number"])
    op.create_index(op.f("ix_students_email"), "students", ["email"])
    op.create_index(op.f("ix_students_status"), "students", ["status"])

    # 2. student_profiles table
    op.create_table(
        "student_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("aadhaar_number", sa.String(length=20), nullable=True),
        sa.Column("pan_number", sa.String(length=20), nullable=True),
        sa.Column("apaar_id", sa.String(length=32), nullable=True),
        sa.Column("abc_account_id", sa.String(length=32), nullable=True),
        sa.Column("religion", sa.String(length=50), nullable=True),
        sa.Column("caste_category", sa.String(length=50), nullable=True),
        sa.Column("nationality", sa.String(length=64), nullable=False, server_default="Indian"),
        sa.Column("mother_tongue", sa.String(length=50), nullable=True, server_default="Hindi"),
        sa.Column("previous_school", sa.String(length=200), nullable=True),
        sa.Column("previous_qualification", sa.String(length=100), nullable=True),
        sa.Column("previous_marks_percentage", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. student_addresses table
    op.create_table(
        "student_addresses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("address_type", sa.String(length=32), nullable=False, server_default="PERMANENT"),
        sa.Column("address_line1", sa.String(length=255), nullable=False),
        sa.Column("address_line2", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("district", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("postal_code", sa.String(length=20), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=False, server_default="India"),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_student_addresses_student_id"), "student_addresses", ["student_id"])

    # 4. student_guardians table
    op.create_table(
        "student_guardians",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relationship_type", sa.String(length=32), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("mobile_number", sa.String(length=24), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("occupation", sa.String(length=100), nullable=True),
        sa.Column("annual_income", sa.Float(), nullable=True),
        sa.Column("qualification", sa.String(length=100), nullable=True),
        sa.Column("is_emergency_contact", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_student_guardians_student_id"), "student_guardians", ["student_id"])

    # 5. student_documents table
    op.create_table(
        "student_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("document_type", sa.String(length=64), nullable=False),
        sa.Column("document_title", sa.String(length=150), nullable=False),
        sa.Column("file_url", sa.Text(), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mime_type", sa.String(length=100), nullable=False, server_default="application/pdf"),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("verified_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_student_documents_student_id"), "student_documents", ["student_id"])

    # 6. student_medical table
    op.create_table(
        "student_medical",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("blood_group", sa.String(length=8), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("allergies", sa.Text(), nullable=True),
        sa.Column("medical_conditions", sa.Text(), nullable=True),
        sa.Column("emergency_doctor_name", sa.String(length=120), nullable=True),
        sa.Column("emergency_doctor_phone", sa.String(length=24), nullable=True),
        sa.Column("insurance_policy_number", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. student_custom_fields table
    op.create_table(
        "student_custom_fields",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("field_key", sa.String(length=64), nullable=False),
        sa.Column("field_label", sa.String(length=120), nullable=False),
        sa.Column("field_type", sa.String(length=32), nullable=False, server_default="TEXT"),
        sa.Column("is_required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("options_list", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("field_key", "institute_id", name="uq_custom_field_key_inst"),
    )

    # 8. student_custom_values table
    op.create_table(
        "student_custom_values",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("custom_field_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("student_custom_fields.id", ondelete="CASCADE"), nullable=False),
        sa.Column("field_value", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("student_id", "custom_field_id", name="uq_student_custom_value"),
    )

    # 9. student_status_history table
    op.create_table(
        "student_status_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("previous_status", sa.String(length=32), nullable=False),
        sa.Column("new_status", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("changed_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. student_timeline table
    op.create_table(
        "student_timeline",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_category", sa.String(length=64), nullable=False),
        sa.Column("event_title", sa.String(length=150), nullable=False),
        sa.Column("event_description", sa.Text(), nullable=False),
        sa.Column("recorded_by", sa.String(length=100), nullable=False, server_default="System"),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("meta_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_student_timeline_student_id"), "student_timeline", ["student_id"])

    # 11. student_notes table
    op.create_table(
        "student_notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_name", sa.String(length=120), nullable=False),
        sa.Column("note_title", sa.String(length=150), nullable=False),
        sa.Column("note_content", sa.Text(), nullable=False),
        sa.Column("is_confidential", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. student_photos table
    op.create_table(
        "student_photos",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("photo_url", sa.Text(), nullable=False),
        sa.Column("signature_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. student_qr_codes table
    op.create_table(
        "student_qr_codes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("qr_payload", sa.Text(), nullable=False),
        sa.Column("qr_svg", sa.Text(), nullable=False),
        sa.Column("barcode_value", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("student_qr_codes")
    op.drop_table("student_photos")
    op.drop_table("student_notes")
    op.drop_table("student_timeline")
    op.drop_table("student_status_history")
    op.drop_table("student_custom_values")
    op.drop_table("student_custom_fields")
    op.drop_table("student_medical")
    op.drop_table("student_documents")
    op.drop_table("student_guardians")
    op.drop_table("student_addresses")
    op.drop_table("student_profiles")
    op.drop_table("students")
