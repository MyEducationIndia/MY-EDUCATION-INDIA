import uuid
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.institute import Institute


class AcademicSession(Base, TimestampUUIDMixin):
    """
    Academic Year & Session management for MY EDUCATION INDIA ERP.
    """
    __tablename__ = "academic_sessions"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    session_name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_admission_open: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    term_structure: Mapped[str] = mapped_column(String(32), default="SEMESTER", nullable=False)
    terms_count: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    institute: Mapped["Institute"] = relationship("Institute", back_populates="academic_sessions", lazy="selectin")
