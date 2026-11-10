import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin


class CmsHeroSlide(Base, TimestampUUIDMixin):
    """
    Hero slider slide items with background imagery/video, badge callouts, headline, subhead, and CTA buttons.
    """
    __tablename__ = "cms_hero_slides"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    badge_text: Mapped[Optional[str]] = mapped_column(String(128), nullable=True) # e.g. "Admissions Open 2026-27"
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    subtitle: Mapped[str] = mapped_column(Text, nullable=False)
    background_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    primary_cta_text: Mapped[str] = mapped_column(String(64), default="Apply Now", nullable=False)
    primary_cta_link: Mapped[str] = mapped_column(String(255), default="/admissions/apply", nullable=False)
    secondary_cta_text: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    secondary_cta_link: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsStatCounter(Base, TimestampUUIDMixin):
    """
    Key performance indicators / statistics displayed on the homepage (e.g. 15,000+ Students, 100% Placement, 45+ Programs).
    """
    __tablename__ = "cms_stat_counters"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    metric_value: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. "37+", "15,000+", "100%", "₹45 LPA"
    numeric_target: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # for animated counter
    label: Mapped[str] = mapped_column(String(128), nullable=False) # e.g. "Integrated Subsystems"
    subtext: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # e.g. "Real-Time Cloud ERP"
    icon_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True) # Lucide icon name

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsQuickLink(Base, TimestampUUIDMixin):
    """
    Quick access tiles on the homepage (e.g. Online Fees, Admit Card, Prospectus, Verification, Anti-Ragging).
    """
    __tablename__ = "cms_quick_links"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    icon_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    badge_label: Mapped[Optional[str]] = mapped_column(String(32), nullable=True) # e.g. "New", "Important"
    is_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsFeaturedProgram(Base, TimestampUUIDMixin):
    """
    Featured academic programs showcased directly on the homepage.
    """
    __tablename__ = "cms_featured_programs"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. "B.Tech Computer Science & Engineering"
    code: Mapped[str] = mapped_column(String(32), nullable=False) # e.g. "BTECH-CSE"
    category: Mapped[str] = mapped_column(String(64), nullable=False) # Engineering, Management, Computer Applications
    degree_level: Mapped[str] = mapped_column(String(32), default="Undergraduate", nullable=False) # Undergraduate, Postgraduate, Doctoral
    duration: Mapped[str] = mapped_column(String(64), default="4 Years (8 Semesters)", nullable=False)
    annual_fee: Mapped[Optional[str]] = mapped_column(String(64), nullable=True) # e.g. "₹95,000 / Year"
    eligibility_summary: Mapped[str] = mapped_column(String(255), default="10+2 with PCM >= 60%", nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    syllabus_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_admissions_open: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsRecruiterLogo(Base, TimestampUUIDMixin):
    """
    Corporate recruiter partners and placement companies showcased on the homepage.
    """
    __tablename__ = "cms_recruiter_logos"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    company_name: Mapped[str] = mapped_column(String(128), nullable=False)
    tier: Mapped[str] = mapped_column(String(32), default="Tier 1", nullable=False) # Day 0, Tier 1, Regular
    highest_package_lpa: Mapped[Optional[str]] = mapped_column(String(32), nullable=True) # e.g. "45.0 LPA"
    logo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsTestimonial(Base, TimestampUUIDMixin):
    """
    Student, alumni, parent, faculty, and corporate recruiter reviews with ratings,
    video testimonials, and administrative moderation approval workflows.
    """
    __tablename__ = "cms_testimonials"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_name: Mapped[str] = mapped_column(String(128), nullable=False)
    author_role: Mapped[str] = mapped_column(String(128), nullable=False)  # e.g. "B.Tech CSE, Batch 2024 (Placed at Microsoft)"
    author_category: Mapped[str] = mapped_column(String(32), default="Student", nullable=False)  # Student, Alumni, Parent, Faculty, Recruiter
    rating_stars: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    quote: Mapped[str] = mapped_column(Text, nullable=False)
    company_or_institution: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)  # e.g. "Microsoft India", "Parent of Arjun (CSE '25)"
    batch_year: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)  # e.g. "Class of 2024"
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_thumbnail_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_embed_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    moderation_status: Mapped[str] = mapped_column(String(32), default="APPROVED", nullable=False)  # PENDING, APPROVED, REJECTED
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsNewsletterSubscriber(Base, TimestampUUIDMixin):
    """
    Public newsletter email subscriptions captured from the homepage footer/newsletter widget.
    """
    __tablename__ = "cms_newsletter_subscribers"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    subscribed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
