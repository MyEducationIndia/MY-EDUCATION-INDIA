import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class RefreshTokenSession(Base, TimestampUUIDMixin):
    __tablename__ = "refresh_token_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    token_family: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(64), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(512), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    revoked_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="refresh_sessions")
