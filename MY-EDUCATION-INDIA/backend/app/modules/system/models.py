import uuid
from datetime import date, datetime, time
from typing import List
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin
from app.models.institute import Institute


class Branch(Base, TimestampUUIDMixin):
    __tablename__ = "branches"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_branches_code_institute"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)  # e.g. BPL, IND, DEL
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    principal_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    opening_time: Mapped[time | None] = mapped_column(Time, default=time(8, 30), nullable=True)
    closing_time: Mapped[time | None] = mapped_column(Time, default=time(16, 30), nullable=True)
    is_main_branch: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    institute: Mapped[Institute] = relationship(Institute)


class AcademicYear(Base, TimestampUUIDMixin):
    __tablename__ = "academic_years"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_academic_years_code_institute"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)  # e.g. 2026-2027, 2027-2028
    name: Mapped[str] = mapped_column(String(120), nullable=False)  # e.g. Academic Year 2026-27
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    institute: Mapped[Institute] = relationship(Institute)


class FinancialYear(Base, TimestampUUIDMixin):
    __tablename__ = "financial_years"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_financial_years_code_institute"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)  # e.g. FY2026-27
    name: Mapped[str] = mapped_column(String(120), nullable=False)  # e.g. Financial Year 2026-2027
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    gstin: Mapped[str | None] = mapped_column(String(20), nullable=True)

    institute: Mapped[Institute] = relationship(Institute)


class SystemSetting(Base, TimestampUUIDMixin):
    __tablename__ = "system_settings"
    __table_args__ = (
        UniqueConstraint("category", "key", "institute_id", name="uq_system_settings_category_key_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True, index=True
    )
    category: Mapped[str] = mapped_column(String(64), index=True, nullable=False)  # e.g. general, auth, appearance, fees
    key: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class NumberGenerator(Base, TimestampUUIDMixin):
    """Configurable Numbering Template for every entity in the enterprise."""
    __tablename__ = "number_generators"
    __table_args__ = (
        UniqueConstraint("entity_type", "institute_id", name="uq_number_gen_entity_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    entity_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    prefix: Mapped[str | None] = mapped_column(String(32), default="MEI", nullable=True)
    suffix: Mapped[str | None] = mapped_column(String(32), nullable=True)
    format_template: Mapped[str] = mapped_column(String(150), default="{PREFIX}-{YEAR}-{NUMBER}", nullable=False)
    separator: Mapped[str] = mapped_column(String(4), default="-", nullable=False)
    padding_length: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    reset_rule: Mapped[str] = mapped_column(String(32), default="YEARLY", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    sequences: Mapped[List["NumberSequence"]] = relationship(
        "NumberSequence", back_populates="generator", cascade="all, delete-orphan", lazy="selectin"
    )


class NumberSequence(Base, TimestampUUIDMixin):
    """Tracks running counter for specific partition/scope (e.g. branch, year, course)."""
    __tablename__ = "number_sequences"
    __table_args__ = (
        UniqueConstraint("generator_id", "scope_key", name="uq_number_seq_gen_scope"),
        {"extend_existing": True},
    )

    generator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("number_generators.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scope_key: Mapped[str] = mapped_column(String(120), default="GLOBAL", index=True, nullable=False)
    current_number: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_issued_value: Mapped[str | None] = mapped_column(String(120), nullable=True)
    last_issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    generator: Mapped[NumberGenerator] = relationship("NumberGenerator", back_populates="sequences")


class Currency(Base, TimestampUUIDMixin):
    __tablename__ = "currencies"
    __table_args__ = {"extend_existing": True}

    code: Mapped[str] = mapped_column(String(3), unique=True, index=True, nullable=False)  # INR, USD, EUR
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    symbol: Mapped[str] = mapped_column(String(8), nullable=False)  # ₹, $, €
    decimal_places: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Language(Base, TimestampUUIDMixin):
    __tablename__ = "languages"
    __table_args__ = {"extend_existing": True}

    code: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)  # en, hi, ta, te
    name: Mapped[str] = mapped_column(String(64), nullable=False)  # English, Hindi
    native_name: Mapped[str] = mapped_column(String(64), nullable=False)  # English, हिन्दी
    is_rtl: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Timezone(Base, TimestampUUIDMixin):
    __tablename__ = "timezones"
    __table_args__ = {"extend_existing": True}

    name: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)  # Asia/Kolkata
    label: Mapped[str] = mapped_column(String(120), nullable=False)  # (GMT+05:30) India Standard Time
    offset_minutes: Mapped[int] = mapped_column(Integer, default=330, nullable=False)  # +330 for IST
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Theme(Base, TimestampUUIDMixin):
    __tablename__ = "themes"
    __table_args__ = {"extend_existing": True}

    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    primary_color: Mapped[str] = mapped_column(String(7), nullable=False)
    secondary_color: Mapped[str] = mapped_column(String(7), nullable=False)
    accent_color: Mapped[str] = mapped_column(String(7), nullable=False)
    is_dark_mode_supported: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    font_family: Mapped[str] = mapped_column(String(80), default="Inter", nullable=False)


class Holiday(Base, TimestampUUIDMixin):
    __tablename__ = "holidays"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    holiday_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    holiday_type: Mapped[str] = mapped_column(String(32), default="NATIONAL", nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class WorkingDay(Base, TimestampUUIDMixin):
    __tablename__ = "working_days"
    __table_args__ = (
        UniqueConstraint("institute_id", "branch_id", "day_of_week", name="uq_working_days_inst_branch_day"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=True, index=True
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    day_name: Mapped[str] = mapped_column(String(16), nullable=False)
    is_working_day: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    start_time: Mapped[time | None] = mapped_column(Time, default=time(8, 30), nullable=True)
    end_time: Mapped[time | None] = mapped_column(Time, default=time(16, 30), nullable=True)


class OrganizationSetting(Base, TimestampUUIDMixin):
    __tablename__ = "organization_settings"
    __table_args__ = (
        UniqueConstraint("institute_id", name="uq_org_settings_institute"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    default_currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    default_language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    default_timezone: Mapped[str] = mapped_column(String(80), default="Asia/Kolkata", nullable=False)
    date_format: Mapped[str] = mapped_column(String(32), default="DD/MM/YYYY", nullable=False)
    time_format: Mapped[str] = mapped_column(String(16), default="12_HOUR", nullable=False)
    fiscal_year_start_month: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    academic_year_start_month: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    sidebar_style: Mapped[str] = mapped_column(String(32), default="EXPANDED", nullable=False)
