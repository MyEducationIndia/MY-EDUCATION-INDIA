import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampUUIDMixin
from app.modules.auth.models import LoginHistory  # noqa: F401


class OtpVerification(Base, TimestampUUIDMixin):
    """
    OTP verification records (disabled by default under strict User ID + Password policy).
    """
    __tablename__ = "otp_verifications"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    identifier: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    channel: Mapped[str] = mapped_column(String(32), default="EMAIL", nullable=False)
    otp_type: Mapped[str] = mapped_column(String(32), default="LOGIN", nullable=False)
    otp_code_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class SecurityPolicyConfig(Base, TimestampUUIDMixin):
    """
    Enterprise security and password policy configuration per institute.
    """
    __tablename__ = "security_policy_configs"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=True,
        unique=True,
        index=True,
    )
    min_password_length: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    require_uppercase: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    require_lowercase: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    require_digit: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    require_special_char: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    password_expiry_days: Mapped[int] = mapped_column(Integer, default=90, nullable=False)
    max_failed_attempts: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    lockout_duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    session_timeout_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    idle_timeout_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    max_concurrent_sessions: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    allow_otp_login: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    allow_forgot_password: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
