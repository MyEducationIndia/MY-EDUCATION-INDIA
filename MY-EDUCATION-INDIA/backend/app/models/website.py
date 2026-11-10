import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin


class WebsiteSetting(Base, TimestampUUIDMixin):
    """
    Core website operational settings, header config, single login URL, maintenance mode, and SEO defaults.
    """
    __tablename__ = "website_settings"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    site_title: Mapped[str] = mapped_column(String(255), default="MY EDUCATION INDIA", nullable=False)
    tagline: Mapped[str] = mapped_column(String(500), default="National Flagship Higher Education Institution", nullable=False)
    header_logo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    footer_logo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    favicon_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Header controls
    header_is_sticky: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    header_show_search: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    header_show_login: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    header_login_button_text: Mapped[str] = mapped_column(String(64), default="Login", nullable=False)
    header_login_route: Mapped[str] = mapped_column(String(128), default="/login", nullable=False)

    # Contact & Coordinates
    contact_phone: Mapped[str] = mapped_column(String(64), default="+91 731 245 6789", nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), default="info@myeducation.in", nullable=False)
    contact_address: Mapped[str] = mapped_column(String(500), default="Campus Square, Institutional Sector, Indore, MP 452001", nullable=False)

    # SEO & Meta
    meta_description: Mapped[str] = mapped_column(Text, default="Official Portal of MY EDUCATION INDIA. Autonomous Higher Education & Research Campus.", nullable=False)
    meta_keywords: Mapped[str] = mapped_column(Text, default="education, university, indore, degrees, cbt, admissions", nullable=False)
    og_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    google_analytics_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    # Operational status
    is_maintenance_mode: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    maintenance_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Custom Code Injections
    custom_css: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    custom_head_scripts: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class WebsiteTheme(Base, TimestampUUIDMixin):
    """
    Website theme customization (colors, fonts, radius, shadows, buttons).
    """
    __tablename__ = "website_themes"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    primary_color: Mapped[str] = mapped_column(String(32), default="#1E40AF", nullable=False)
    secondary_color: Mapped[str] = mapped_column(String(32), default="#0D9488", nullable=False)
    accent_color: Mapped[str] = mapped_column(String(32), default="#F59E0B", nullable=False)
    background_color: Mapped[str] = mapped_column(String(32), default="#F8FAFC", nullable=False)
    surface_color: Mapped[str] = mapped_column(String(32), default="#FFFFFF", nullable=False)
    text_primary_color: Mapped[str] = mapped_column(String(32), default="#0F172A", nullable=False)
    text_secondary_color: Mapped[str] = mapped_column(String(32), default="#475569", nullable=False)

    font_family: Mapped[str] = mapped_column(String(64), default="Inter, system-ui, sans-serif", nullable=False)
    heading_font_family: Mapped[str] = mapped_column(String(64), default="Inter, system-ui, sans-serif", nullable=False)
    border_radius: Mapped[str] = mapped_column(String(32), default="0.75rem", nullable=False)
    button_style: Mapped[str] = mapped_column(String(32), default="rounded", nullable=False)
    shadow_style: Mapped[str] = mapped_column(String(32), default="soft", nullable=False)
    animation_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class WebsiteTickerItem(Base, TimestampUUIDMixin):
    """
    Sticky Live Update Ticker items immediately below the main header.
    """
    __tablename__ = "website_ticker_items"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(
        String(64),
        default="Important Notice",
        nullable=False,
        # Admission, Examination, Result, Holiday, Circular, Event, News, Placement, Scholarship, Emergency, Important Notice
    )
    link_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    open_new_tab: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_emergency: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    priority_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False) # 1 normal, 2 high, 3 urgent

    publish_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class WebsiteNavigationMenu(Base, TimestampUUIDMixin):
    """
    Dynamic hierarchical navigation menu trees (Header Nav, Quick Links, Footer Columns).
    """
    __tablename__ = "website_navigation_menus"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    menu_location: Mapped[str] = mapped_column(
        String(64),
        default="HEADER_MAIN",
        nullable=False,
        index=True, # HEADER_MAIN, FOOTER_COL_1, FOOTER_COL_2, FOOTER_COL_3
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    icon_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("website_navigation_menus.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    is_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    open_new_tab: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_mega_menu: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    badge_text: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    children: Mapped[List["WebsiteNavigationMenu"]] = relationship(
        "WebsiteNavigationMenu",
        back_populates="parent",
        cascade="all, delete-orphan",
        order_by="WebsiteNavigationMenu.display_order",
    )
    parent: Mapped[Optional["WebsiteNavigationMenu"]] = relationship(
        "WebsiteNavigationMenu",
        back_populates="children",
        remote_side="WebsiteNavigationMenu.id",
    )


class WebsiteSocialLink(Base, TimestampUUIDMixin):
    """
    Institutional social media profiles.
    """
    __tablename__ = "website_social_links"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    platform: Mapped[str] = mapped_column(String(64), nullable=False) # facebook, twitter, linkedin, youtube, instagram
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class WebsiteSearchIndex(Base, TimestampUUIDMixin):
    """
    Global search catalog supporting indexing across Courses, Notices, News, Events, Faculty, and Pages.
    """
    __tablename__ = "website_search_index"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True) # course, notice, news, event, faculty, page
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_url: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(64), default="GENERAL", nullable=False)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class WebsiteSearchLog(Base):
    """
    Audit log of global site searches for analytics and content gap discovery.
    """
    __tablename__ = "website_search_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    query_text: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category_filter: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    results_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )


class WebsiteQuickLink(Base, TimestampUUIDMixin):
    """
    High-visibility quick navigation links (Admissions 2026, Fees, Portal Login, Anti-Ragging).
    """
    __tablename__ = "website_quick_links"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    icon_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    badge_text: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    target_type: Mapped[str] = mapped_column(String(32), default="INTERNAL", nullable=False)
    is_highlighted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

