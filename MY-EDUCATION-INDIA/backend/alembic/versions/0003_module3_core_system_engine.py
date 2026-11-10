"""Alembic migration for Module 3: Core System Engine
Creates:
- branches
- academic_years
- financial_years
- number_generators
- number_sequences
- currencies
- languages
- timezones
- themes
- holidays
- working_days
- organization_settings

Revision ID: 0003_module3_core_system_engine
Revises: 0002_module2_enterprise_auth
Create Date: 2026-11-06 12:35:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0003_module3_core_system_engine"
down_revision: Union[str, None] = "0002_module2_enterprise_auth"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. branches table
    op.create_table(
        "branches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address_line1", sa.String(length=255), nullable=False),
        sa.Column("address_line2", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("postal_code", sa.String(length=20), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("principal_name", sa.String(length=150), nullable=True),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.Column("opening_time", sa.Time(), nullable=True),
        sa.Column("closing_time", sa.Time(), nullable=True),
        sa.Column("is_main_branch", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_branches_code_institute"),
    )
    op.create_index(op.f("ix_branches_code"), "branches", ["code"])
    op.create_index(op.f("ix_branches_institute_id"), "branches", ["institute_id"])

    # 2. academic_years table
    op.create_table(
        "academic_years",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_academic_years_code_institute"),
    )
    op.create_index(op.f("ix_academic_years_code"), "academic_years", ["code"])
    op.create_index(op.f("ix_academic_years_institute_id"), "academic_years", ["institute_id"])

    # 3. financial_years table
    op.create_table(
        "financial_years",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_closed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("gstin", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_financial_years_code_institute"),
    )
    op.create_index(op.f("ix_financial_years_code"), "financial_years", ["code"])
    op.create_index(op.f("ix_financial_years_institute_id"), "financial_years", ["institute_id"])

    # 4. number_generators table
    op.create_table(
        "number_generators",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("prefix", sa.String(length=32), nullable=True, server_default="MEI"),
        sa.Column("suffix", sa.String(length=32), nullable=True),
        sa.Column("format_template", sa.String(length=150), nullable=False, server_default="{PREFIX}-{YEAR}-{NUMBER}"),
        sa.Column("separator", sa.String(length=4), nullable=False, server_default="-"),
        sa.Column("padding_length", sa.Integer(), nullable=False, server_default="6"),
        sa.Column("reset_rule", sa.String(length=32), nullable=False, server_default="YEARLY"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("entity_type", "institute_id", name="uq_number_gen_entity_inst"),
    )
    op.create_index(op.f("ix_number_generators_entity_type"), "number_generators", ["entity_type"])
    op.create_index(op.f("ix_number_generators_institute_id"), "number_generators", ["institute_id"])

    # 5. number_sequences table
    op.create_table(
        "number_sequences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("generator_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("number_generators.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scope_key", sa.String(length=120), nullable=False, server_default="GLOBAL"),
        sa.Column("current_number", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_issued_value", sa.String(length=120), nullable=True),
        sa.Column("last_issued_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("generator_id", "scope_key", name="uq_number_seq_gen_scope"),
    )
    op.create_index(op.f("ix_number_sequences_generator_id"), "number_sequences", ["generator_id"])
    op.create_index(op.f("ix_number_sequences_scope_key"), "number_sequences", ["scope_key"])

    # 6. currencies table
    op.create_table(
        "currencies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=3), nullable=False, unique=True),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=8), nullable=False),
        sa.Column("decimal_places", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_currencies_code"), "currencies", ["code"])

    # 7. languages table
    op.create_table(
        "languages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False, unique=True),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("native_name", sa.String(length=64), nullable=False),
        sa.Column("is_rtl", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_languages_code"), "languages", ["code"])

    # 8. timezones table
    op.create_table(
        "timezones",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False, unique=True),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("offset_minutes", sa.Integer(), nullable=False, server_default="330"),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_timezones_name"), "timezones", ["name"])

    # 9. themes table
    op.create_table(
        "themes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False, unique=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("primary_color", sa.String(length=7), nullable=False),
        sa.Column("secondary_color", sa.String(length=7), nullable=False),
        sa.Column("accent_color", sa.String(length=7), nullable=False),
        sa.Column("is_dark_mode_supported", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("font_family", sa.String(length=80), nullable=False, server_default="Inter"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_themes_code"), "themes", ["code"])

    # 10. holidays table
    op.create_table(
        "holidays",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="CASCADE"), nullable=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("holiday_date", sa.Date(), nullable=False),
        sa.Column("holiday_type", sa.String(length=32), nullable=False, server_default="NATIONAL"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_holidays_holiday_date"), "holidays", ["holiday_date"])
    op.create_index(op.f("ix_holidays_institute_id"), "holidays", ["institute_id"])

    # 11. working_days table
    op.create_table(
        "working_days",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="CASCADE"), nullable=True),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("day_name", sa.String(length=16), nullable=False),
        sa.Column("is_working_day", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("start_time", sa.Time(), nullable=True),
        sa.Column("end_time", sa.Time(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("institute_id", "branch_id", "day_of_week", name="uq_working_days_inst_branch_day"),
    )

    # 12. organization_settings table
    op.create_table(
        "organization_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("default_currency", sa.String(length=3), nullable=False, server_default="INR"),
        sa.Column("default_language", sa.String(length=10), nullable=False, server_default="en"),
        sa.Column("default_timezone", sa.String(length=80), nullable=False, server_default="Asia/Kolkata"),
        sa.Column("date_format", sa.String(length=32), nullable=False, server_default="DD/MM/YYYY"),
        sa.Column("time_format", sa.String(length=16), nullable=False, server_default="12_HOUR"),
        sa.Column("fiscal_year_start_month", sa.Integer(), nullable=False, server_default="4"),
        sa.Column("academic_year_start_month", sa.Integer(), nullable=False, server_default="6"),
        sa.Column("sidebar_style", sa.String(length=32), nullable=False, server_default="EXPANDED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("institute_id", name="uq_org_settings_institute"),
    )


def downgrade() -> None:
    op.drop_table("organization_settings")
    op.drop_table("working_days")
    op.drop_table("holidays")
    op.drop_table("themes")
    op.drop_table("timezones")
    op.drop_table("languages")
    op.drop_table("currencies")
    op.drop_table("number_sequences")
    op.drop_table("number_generators")
    op.drop_table("financial_years")
    op.drop_table("academic_years")
    op.drop_table("branches")
