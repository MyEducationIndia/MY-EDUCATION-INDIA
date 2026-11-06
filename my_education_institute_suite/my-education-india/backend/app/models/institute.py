from typing import TYPE_CHECKING, List
from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.module_config import SystemModuleConfig


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

    # Dynamic Provider & SEO Metadata stored in PostgreSQL JSONB
    seo_metadata: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    communication_settings: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    users: Mapped[List["User"]] = relationship("User", back_populates="institute", lazy="selectin")
    module_configs: Mapped[List["SystemModuleConfig"]] = relationship(
        "SystemModuleConfig", back_populates="institute", cascade="all, delete-orphan", lazy="selectin"
    )
