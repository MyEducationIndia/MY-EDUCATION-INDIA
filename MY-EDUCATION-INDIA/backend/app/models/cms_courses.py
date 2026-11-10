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


class CmsCourseCategory(Base, TimestampUUIDMixin):
    """
    Course classification / faculty department category (e.g. Engineering & Technology, Management, Computing, Sciences).
    """
    __tablename__ = "cms_course_categories"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon_name: Mapped[Optional[str]] = mapped_column(String(64), default="BookOpen", nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    courses: Mapped[List["CmsCourse"]] = relationship(
        "CmsCourse",
        back_populates="category",
        cascade="all, delete-orphan",
        order_by="CmsCourse.display_order",
    )


class CmsCourse(Base, TimestampUUIDMixin):
    """
    Individual Degree, Diploma, or Certificate Program with academic specifications, fees, and career pathways.
    """
    __tablename__ = "cms_courses"

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cms_course_categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(64), nullable=False)
    degree_level: Mapped[str] = mapped_column(String(64), nullable=False) # UNDERGRADUATE, POSTGRADUATE, DIPLOMA, DOCTORAL
    duration: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. "4 Years (8 Semesters)"
    study_mode: Mapped[str] = mapped_column(String(64), default="Full-Time On-Campus", nullable=False)
    annual_fee: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. "₹1,25,000 / Year"
    total_fee: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    seats_intake: Mapped[int] = mapped_column(Integer, default=60, nullable=False)

    eligibility_summary: Mapped[str] = mapped_column(Text, nullable=False)
    admission_process: Mapped[str] = mapped_column(Text, nullable=False)
    career_prospects: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    overview: Mapped[str] = mapped_column(Text, nullable=False)

    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    brochure_pdf_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    syllabus_pdf_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_admissions_open: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    category: Mapped["CmsCourseCategory"] = relationship(
        "CmsCourseCategory",
        back_populates="courses",
    )
    curricula: Mapped[List["CmsCourseCurriculum"]] = relationship(
        "CmsCourseCurriculum",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="CmsCourseCurriculum.semester_number",
    )
    faculty_members: Mapped[List["CmsCourseFaculty"]] = relationship(
        "CmsCourseFaculty",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="CmsCourseFaculty.display_order",
    )


class CmsCourseCurriculum(Base, TimestampUUIDMixin):
    """
    Semester-wise curriculum breakdowns including subject modules, lab units, and credits.
    """
    __tablename__ = "cms_course_curricula"

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cms_courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    semester_number: Mapped[int] = mapped_column(Integer, nullable=False) # 1, 2, 3...
    semester_title: Mapped[str] = mapped_column(String(128), nullable=False) # e.g. "Semester I: Computing Core"
    credits: Mapped[int] = mapped_column(Integer, default=24, nullable=False)
    subjects: Mapped[dict] = mapped_column(JSONB, default=list, nullable=False) # list of {code, title, credits, type}

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    course: Mapped["CmsCourse"] = relationship(
        "CmsCourse",
        back_populates="curricula",
    )


class CmsCourseFaculty(Base, TimestampUUIDMixin):
    """
    Key faculty mentors, department heads, and professors associated with a course.
    """
    __tablename__ = "cms_course_faculty"

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cms_courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    faculty_name: Mapped[str] = mapped_column(String(128), nullable=False)
    designation: Mapped[str] = mapped_column(String(128), nullable=False)
    qualifications: Mapped[str] = mapped_column(String(255), nullable=False)
    specialization: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    course: Mapped["CmsCourse"] = relationship(
        "CmsCourse",
        back_populates="faculty_members",
    )
