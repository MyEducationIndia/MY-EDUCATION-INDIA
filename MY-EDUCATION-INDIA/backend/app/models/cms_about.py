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
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampUUIDMixin


class CmsMilestone(Base, TimestampUUIDMixin):
    """
    Historical timeline milestones for the About Institute pages (Foundation to Present).
    """
    __tablename__ = "cms_milestones"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    year: Mapped[str] = mapped_column(String(16), nullable=False) # e.g. "2010", "2015", "2020", "2026"
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True) # Lucide icon name

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsLeadershipMessage(Base, TimestampUUIDMixin):
    """
    Executive leadership statements (Chairman, Director, Principal, Dean).
    """
    __tablename__ = "cms_leadership_messages"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    leader_name: Mapped[str] = mapped_column(String(128), nullable=False)
    leader_designation: Mapped[str] = mapped_column(String(128), nullable=False) # e.g. "Director & Head of Campus"
    role_category: Mapped[str] = mapped_column(String(64), nullable=False) # CHAIRMAN, DIRECTOR, PRINCIPAL, DEAN
    salutation_title: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. "Fostering Innovation in Higher Education"
    message_body: Mapped[str] = mapped_column(Text, nullable=False)
    portrait_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    signature_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_address_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsAccreditation(Base, TimestampUUIDMixin):
    """
    Statutory government recognitions, affiliations, and quality rankings (UGC, AICTE, NAAC, NBA).
    """
    __tablename__ = "cms_accreditations"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    accrediting_body: Mapped[str] = mapped_column(String(128), nullable=False) # UGC, AICTE, NAAC, NBA, State University
    title: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. "All India Council for Technical Education (AICTE)"
    approval_reference_number: Mapped[str] = mapped_column(String(128), nullable=False)
    valid_from: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    valid_upto: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    certificate_pdf_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logo_badge_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CmsCampusInfrastructure(Base, TimestampUUIDMixin):
    """
    Campus facilities and infrastructure showcase (Central Library, High-Performance CBT Labs, Robotics Wing, Sports Arena).
    """
    __tablename__ = "cms_campus_infrastructure"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    facility_name: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False) # ACADEMIC, RESEARCH, SPORTS, RESIDENTIAL, DIGITAL
    capacity_metric: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. "500+ Seating Capacity", "10Gbps Fiber Backbone"
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    floor_or_location: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
