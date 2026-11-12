import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class UserDocument(Base, TimestampUUIDMixin):
    """
    User verification documents (e.g. Aadhaar, 10th Marksheet, Degree, Joining Letter).
    """
    __tablename__ = "user_documents"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    document_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    document_title: Mapped[str] = mapped_column(String(150), nullable=False)
    document_url: Mapped[str] = mapped_column(Text, nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(64), default="application/pdf", nullable=False)
    verification_status: Mapped[str] = mapped_column(String(32), default="PENDING", nullable=False)
    verified_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="documents", lazy="selectin")
