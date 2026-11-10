import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampUUIDMixin

class CmsContactInquiry(Base, TimestampUUIDMixin):
    __tablename__ = "cms_contact_inquiries"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False, default="GENERAL")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="NEW")
    admin_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    responded_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)

class CmsDepartmentContact(Base, TimestampUUIDMixin):
    __tablename__ = "cms_department_contacts"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    department_name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False)
    contact_person: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_numbers: Mapped[str] = mapped_column(String(128), nullable=False)
    office_location: Mapped[str] = mapped_column(String(255), nullable=False)
    operating_hours: Mapped[str] = mapped_column(String(128), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsFaqItem(Base, TimestampUUIDMixin):
    __tablename__ = "cms_faq_items"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    question: Mapped[str] = mapped_column(String(512), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsSupportFeedback(Base, TimestampUUIDMixin):
    __tablename__ = "cms_support_feedbacks"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_type: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    feedback_type: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    rating_satisfaction: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="NEW", nullable=False)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
