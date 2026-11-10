import uuid
from typing import Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampUUIDMixin

class CmsAlumniSuccessStory(Base, TimestampUUIDMixin):
    __tablename__ = "cms_alumni_success_stories"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    alumni_name: Mapped[str] = mapped_column(String(128), nullable=False)
    degree_program: Mapped[str] = mapped_column(String(128), nullable=False)
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    company_name: Mapped[str] = mapped_column(String(128), nullable=False)
    designation: Mapped[str] = mapped_column(String(128), nullable=False)
    package_lpa: Mapped[str] = mapped_column(String(32), nullable=False)
    testimonial_quote: Mapped[str] = mapped_column(Text, nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_story_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsInternshipOpportunity(Base, TimestampUUIDMixin):
    __tablename__ = "cms_internship_opportunities"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False)
    role_title: Mapped[str] = mapped_column(String(128), nullable=False)
    stipend_monthly: Mapped[str] = mapped_column(String(64), nullable=False)
    duration_months: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    location: Mapped[str] = mapped_column(String(128), nullable=False)
    application_deadline: Mapped[str] = mapped_column(String(32), nullable=False)
    eligibility_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    apply_url: Mapped[str] = mapped_column(Text, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsPlacementDrive(Base, TimestampUUIDMixin):
    __tablename__ = "cms_placement_drives"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False)
    job_role: Mapped[str] = mapped_column(String(128), nullable=False)
    package_ctc: Mapped[str] = mapped_column(String(64), nullable=False)
    drive_date: Mapped[str] = mapped_column(String(32), nullable=False)
    registration_deadline: Mapped[str] = mapped_column(String(32), nullable=False)
    eligible_branches: Mapped[str] = mapped_column(String(255), nullable=False)
    selection_process: Mapped[str] = mapped_column(Text, nullable=False)
    job_location: Mapped[str] = mapped_column(String(128), nullable=False)
    drive_status: Mapped[str] = mapped_column(String(32), default="UPCOMING", nullable=False)
    registration_link: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company_logo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsPlacementStat(Base, TimestampUUIDMixin):
    __tablename__ = "cms_placement_stats"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(32), nullable=False)
    highest_package_lpa: Mapped[str] = mapped_column(String(32), nullable=False)
    average_package_lpa: Mapped[str] = mapped_column(String(32), nullable=False)
    median_package_lpa: Mapped[str] = mapped_column(String(32), nullable=False)
    total_offers: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    placement_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    participating_companies: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsRecruiterPartner(Base, TimestampUUIDMixin):
    __tablename__ = "cms_recruiter_partners"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False)
    sector: Mapped[str] = mapped_column(String(64), nullable=False)
    tier: Mapped[str] = mapped_column(String(32), default="TIER_1", nullable=False)
    highest_package_lpa: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    headquarters: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CmsTrainingProgram(Base, TimestampUUIDMixin):
    __tablename__ = "cms_placement_training_programs"
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    training_type: Mapped[str] = mapped_column(String(64), nullable=False)
    trainer_name: Mapped[str] = mapped_column(String(128), nullable=False)
    duration_weeks: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    start_date: Mapped[str] = mapped_column(String(32), nullable=False)
    end_date: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    syllabus_highlights: Mapped[str] = mapped_column(Text, nullable=False)
    batch_eligibility: Mapped[str] = mapped_column(String(128), nullable=False)
    mode: Mapped[str] = mapped_column(String(32), default="HYBRID", nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
