import uuid
from typing import Optional, List
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

class CmsDownloadCategory(Base, TimestampUUIDMixin):
    __tablename__ = "cms_download_categories"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon_name: Mapped[str] = mapped_column(String(64), default="FileText", nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    documents: Mapped[List["CmsDownloadDocument"]] = relationship("CmsDownloadDocument", back_populates="category", cascade="all, delete-orphan")

class CmsDownloadDocument(Base, TimestampUUIDMixin):
    __tablename__ = "cms_download_documents"
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cms_download_categories.id", ondelete="CASCADE"), nullable=False, index=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_audience: Mapped[str] = mapped_column(String(64), default="ALL", nullable=False)
    applicable_program: Mapped[str] = mapped_column(String(128), default="ALL", nullable=False)
    academic_year: Mapped[str] = mapped_column(String(32), default="2026-2027", nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=False)
    file_size_formatted: Mapped[str] = mapped_column(String(32), default="1.2 MB", nullable=False)
    file_format: Mapped[str] = mapped_column(String(16), default="PDF", nullable=False)
    version: Mapped[str] = mapped_column(String(32), default="1.0", nullable=False)
    download_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    category: Mapped["CmsDownloadCategory"] = relationship("CmsDownloadCategory", back_populates="documents")
