import uuid
from datetime import date, datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

# Association Table: News <-> Tags
news_tags = Table(
    "cms_news_tags",
    Base.metadata,
    ForeignKey("cms_tags.id", ondelete="CASCADE"),
    extend_existing=True,
)


class Page(Base, TimestampUUIDMixin):
    __tablename__ = "cms_pages"
    __table_args__ = (
        UniqueConstraint("slug", "institute_id", name="uq_pages_slug_institute"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    featured_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT", index=True, nullable=False) # DRAFT, PUBLISHED, SCHEDULED, ARCHIVED
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scheduled_publish_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_homepage: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    template_type: Mapped[str] = mapped_column(String(64), default="DEFAULT", nullable=False) # DEFAULT, FULL_WIDTH, LANDING, BLANK
    custom_css: Mapped[str | None] = mapped_column(Text, nullable=True)
    custom_js: Mapped[str | None] = mapped_column(Text, nullable=True) # Super Admin restricted
    meta_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_keywords: Mapped[str | None] = mapped_column(String(500), nullable=True)
    canonical_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    og_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    sections: Mapped[List["PageSection"]] = relationship("PageSection", back_populates="page", cascade="all, delete-orphan", lazy="selectin")


class PageSection(Base, TimestampUUIDMixin):
    """Reusable Drag & Drop Content Block / Section."""
    __tablename__ = "cms_page_sections"
    __table_args__ = {"extend_existing": True}

    page_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cms_pages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    section_key: Mapped[str] = mapped_column(String(80), nullable=False) # hero_banner, course_grid, faculty_cards, faq_accordion, cta_banner
    block_type: Mapped[str] = mapped_column(String(64), nullable=False) # HERO, HEADING, PARAGRAPH, BUTTON, CARD, GALLERY, SLIDER, ACCORDION, FAQ, COUNTER, TIMELINE, TABLE, TESTIMONIAL, MAP, CONTACT_FORM, ADMISSION_FORM, COURSE_LIST, NEWS_GRID, BLOG_GRID, DOWNLOADS, HTML
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    container_width: Mapped[str] = mapped_column(String(32), default="BOXED", nullable=False) # BOXED, FULL_WIDTH
    background_color: Mapped[str | None] = mapped_column(String(32), nullable=True)
    background_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    padding_top: Mapped[int] = mapped_column(Integer, default=40, nullable=False)
    padding_bottom: Mapped[int] = mapped_column(Integer, default=40, nullable=False)
    content_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    page: Mapped[Page] = relationship("Page", back_populates="sections")


class Menu(Base, TimestampUUIDMixin):
    __tablename__ = "cms_menus"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_menus_code_institute"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # HEADER_MENU, FOOTER_MENU, SIDEBAR_MENU, MOBILE_MENU
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    location: Mapped[str] = mapped_column(String(64), default="HEADER", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    items: Mapped[List["MenuItem"]] = relationship("MenuItem", back_populates="menu", cascade="all, delete-orphan", lazy="selectin")


class MenuItem(Base, TimestampUUIDMixin):
    __tablename__ = "cms_menu_items"
    __table_args__ = {"extend_existing": True}

    menu_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cms_menus.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cms_menu_items.id", ondelete="CASCADE"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    target: Mapped[str] = mapped_column(String(16), default="_self", nullable=False) # _self, _blank
    icon_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    badge_label: Mapped[str | None] = mapped_column(String(32), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    menu: Mapped[Menu] = relationship("Menu", back_populates="items")
    children: Mapped[List["MenuItem"]] = relationship("MenuItem", lazy="selectin")


class MediaAsset(Base, TimestampUUIDMixin):
    __tablename__ = "cms_media"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    folder_path: Mapped[str] = mapped_column(String(255), default="/", index=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(32), nullable=False) # IMAGE, VIDEO, PDF, DOCUMENT, ARCHIVE, ICON
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False) # Cloudinary URL
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    alt_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    caption: Mapped[str | None] = mapped_column(String(500), nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Banner(Base, TimestampUUIDMixin):
    __tablename__ = "cms_banners"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(500), nullable=True)
    banner_type: Mapped[str] = mapped_column(String(64), default="DESKTOP", nullable=False) # DESKTOP, MOBILE, POPUP, ADMISSION, COURSE, SCHOLARSHIP, EVENT, ANNOUNCEMENT
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    mobile_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    cta_text: Mapped[str | None] = mapped_column(String(64), nullable=True)
    cta_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Category(Base, TimestampUUIDMixin):
    __tablename__ = "cms_categories"
    __table_args__ = (
        UniqueConstraint("slug", "category_type", "institute_id", name="uq_categories_slug_type_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_type: Mapped[str] = mapped_column(String(64), default="NEWS", nullable=False) # NEWS, BLOG, DOWNLOAD, GALLERY, EVENT
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class Tag(Base, TimestampUUIDMixin):
    __tablename__ = "cms_tags"
    __table_args__ = (
        UniqueConstraint("name", "institute_id", name="uq_tags_name_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), index=True, nullable=False)


class NewsArticle(Base, TimestampUUIDMixin):
    __tablename__ = "cms_news"
    __table_args__ = (
        UniqueConstraint("slug", "institute_id", name="uq_news_slug_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author_name: Mapped[str] = mapped_column(String(120), default="Editorial Team", nullable=False)
    featured_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cms_categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_trending: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="PUBLISHED", nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    meta_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class BlogPost(Base, TimestampUUIDMixin):
    __tablename__ = "cms_blogs"
    __table_args__ = (
        UniqueConstraint("slug", "institute_id", name="uq_blogs_slug_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author_name: Mapped[str] = mapped_column(String(120), default="Faculty & Research Group", nullable=False)
    featured_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cms_categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    reading_time_minutes: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="PUBLISHED", nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class GalleryAlbum(Base, TimestampUUIDMixin):
    __tablename__ = "cms_albums"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_image_url: Mapped[str] = mapped_column(Text, nullable=False)
    event_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    items: Mapped[List["GalleryItem"]] = relationship("GalleryItem", back_populates="album", cascade="all, delete-orphan", lazy="selectin")


class GalleryItem(Base, TimestampUUIDMixin):
    __tablename__ = "cms_gallery"
    __table_args__ = {"extend_existing": True}

    album_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cms_albums.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    media_type: Mapped[str] = mapped_column(String(32), default="PHOTO", nullable=False) # PHOTO, VIDEO
    media_url: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    album: Mapped[GalleryAlbum] = relationship("GalleryAlbum", back_populates="items")


class DownloadableResource(Base, TimestampUUIDMixin):
    __tablename__ = "cms_downloads"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False) # BROCHURE, PROSPECTUS, ACADEMIC_CALENDAR, TIMETABLE, EXAM_FORM, NOTICE, SYLLABUS, PREVIOUS_PAPER, ASSIGNMENT
    file_url: Mapped[str] = mapped_column(Text, nullable=False)
    file_size_formatted: Mapped[str] = mapped_column(String(32), default="1.2 MB", nullable=False)
    download_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Testimonial(Base, TimestampUUIDMixin):
    __tablename__ = "cms_testimonials"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author_name: Mapped[str] = mapped_column(String(120), nullable=False)
    author_role: Mapped[str] = mapped_column(String(100), nullable=False) # Student, Parent, Faculty, Recruiter, Alumni
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    rating_stars: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    company_or_course: Mapped[str | None] = mapped_column(String(150), nullable=True)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class CampusEvent(Base, TimestampUUIDMixin):
    __tablename__ = "cms_events"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    venue: Mapped[str] = mapped_column(String(200), nullable=False)
    banner_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    registration_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Enquiry(Base, TimestampUUIDMixin):
    __tablename__ = "cms_enquiries"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True
    )
    enquiry_type: Mapped[str] = mapped_column(String(64), default="GENERAL", nullable=False) # ADMISSION, GENERAL, CALLBACK, GRIEVANCE
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(32), nullable=False)
    course_interested: Mapped[str | None] = mapped_column(String(150), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="NEW", nullable=False) # NEW, IN_PROGRESS, RESOLVED, CLOSED
    source_channel: Mapped[str] = mapped_column(String(64), default="WEBSITE", nullable=False)


class WebsiteSettings(Base, TimestampUUIDMixin):
    __tablename__ = "cms_website_settings"
    __table_args__ = (
        UniqueConstraint("institute_id", name="uq_website_settings_inst"),
        {"extend_existing": True},
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    website_title: Mapped[str] = mapped_column(String(200), default="MY EDUCATION INDIA", nullable=False)
    tagline: Mapped[str] = mapped_column(String(300), default="Premier Educational Institute & Assessment Center", nullable=False)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_color: Mapped[str] = mapped_column(String(7), default="#1D4ED8", nullable=False)
    secondary_color: Mapped[str] = mapped_column(String(7), default="#0D9488", nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(32), default="+91 755 2400000", nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), default="contact@myeducationindia.edu.in", nullable=False)
    whatsapp_number: Mapped[str | None] = mapped_column(String(32), default="+919999999999", nullable=True)
    address_display: Mapped[str] = mapped_column(String(300), default="Main Institutional Area, Bhopal, MP 462011", nullable=False)
    social_links: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False) # facebook, twitter, linkedin, youtube, instagram
    footer_text: Mapped[str] = mapped_column(String(500), default="© 2026 MY EDUCATION INDIA. All rights reserved.", nullable=False)
    analytics_tracking_code: Mapped[str | None] = mapped_column(Text, nullable=True)
