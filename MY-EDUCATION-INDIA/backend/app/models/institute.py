from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.academic_session import AcademicSession
    from app.models.module_config import SystemModuleConfig
    from app.models.user import User


class Institute(Base, TimestampUUIDMixin):
    __tablename__ = "institutes"

    code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tagline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    affiliation_number: Mapped[str | None] = mapped_column(String(128), nullable=True)
    official_email: Mapped[str] = mapped_column(String(255), nullable=False)
    official_phone: Mapped[str] = mapped_column(String(32), nullable=False)
    website_domain: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default="India", nullable=False)

    # Cloudinary Hosted Assets & Dynamic Branding
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_color_hex: Mapped[str] = mapped_column(String(7), default="#1E40AF", nullable=False)
    secondary_color_hex: Mapped[str] = mapped_column(String(7), default="#0D9488", nullable=False)

    # Regional, Localization & Academic Configuration
    time_zone: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata", nullable=False)
    default_language: Mapped[str] = mapped_column(String(16), default="en-IN", nullable=False)
    currency_code: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    currency_symbol: Mapped[str] = mapped_column(String(10), default="₹", nullable=False)
    current_academic_year: Mapped[str] = mapped_column(String(64), default="2026-2027", nullable=False)

    # Custom Domain & Geo Mapping
    custom_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    custom_domain_status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)
    google_maps_embed_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    google_maps_latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    google_maps_longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Communication Gateways & Provider Configurations (Stored securely in PostgreSQL JSONB)
    social_media_links: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    smtp_config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    sms_gateway_config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    whatsapp_gateway_config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    payment_gateway_config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    theme_config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    # Dynamic SEO Metadata
    seo_metadata: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    communication_settings: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    users: Mapped[List["User"]] = relationship("User", back_populates="institute", lazy="selectin")
    module_configs: Mapped[List["SystemModuleConfig"]] = relationship(
        "SystemModuleConfig", back_populates="institute", cascade="all, delete-orphan", lazy="selectin"
    )
    academic_sessions: Mapped[List["AcademicSession"]] = relationship(
        "AcademicSession", back_populates="institute", cascade="all, delete-orphan", lazy="selectin"
    )
