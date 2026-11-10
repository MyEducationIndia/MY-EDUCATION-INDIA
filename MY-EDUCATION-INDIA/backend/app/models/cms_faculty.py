import uuid
from typing import Optional, List
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

class CmsFacultyMember(Base, TimestampUUIDMixin):
    __tablename__ = "cms_faculty_members"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False)
    department: Mapped[str] = mapped_column(String(128), nullable=False)
    designation: Mapped[str] = mapped_column(String(128), nullable=False)
    qualifications: Mapped[str] = mapped_column(String(255), nullable=False)
    specialization: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    experience_years: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    office_location: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    research_interests: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    teaching_courses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    google_scholar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    orcid_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    researchgate_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_citations: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    h_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    patents_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_head_of_department: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    publications: Mapped[List["CmsResearchPublication"]] = relationship("CmsResearchPublication", back_populates="faculty_member", cascade="all, delete-orphan")

class CmsResearchPublication(Base, TimestampUUIDMixin):
    __tablename__ = "cms_research_publications"
    faculty_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cms_faculty_members.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    journal_or_conference: Mapped[str] = mapped_column(String(255), nullable=False)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
    doi_or_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    citation_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    indexing: Mapped[str] = mapped_column(String(64), default="SCOPUS", nullable=False)
    faculty_member: Mapped["CmsFacultyMember"] = relationship("CmsFacultyMember", back_populates="publications")

class CmsStaffMember(Base, TimestampUUIDMixin):
    __tablename__ = "cms_staff_members"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    division: Mapped[str] = mapped_column(String(128), nullable=False)
    designation: Mapped[str] = mapped_column(String(128), nullable=False)
    office_room_number: Mapped[str] = mapped_column(String(64), nullable=False)
    official_email: Mapped[str] = mapped_column(String(255), nullable=False)
    extension_number: Mapped[str] = mapped_column(String(32), nullable=False)
    visiting_hours: Mapped[str] = mapped_column(String(64), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
