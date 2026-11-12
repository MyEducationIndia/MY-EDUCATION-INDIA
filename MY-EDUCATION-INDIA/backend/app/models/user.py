import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.institute import Institute
    from app.models.refresh_token import RefreshTokenSession
    from app.models.role import Role
    from app.models.user_document import UserDocument

user_roles_association = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base, TimestampUUIDMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(24), index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)

    # Core Status Flags
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    mfa_secret: Mapped[str | None] = mapped_column(String(64), nullable=True)
    mfa_backup_codes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Module 4 Enterprise User Classification
    user_category: Mapped[str] = mapped_column(
        String(32), default="STUDENT", nullable=False, index=True
    )  # STUDENT, FACULTY, STAFF, PARENT, RECEPTION, LIBRARIAN, ACCOUNTANT, EXAM_CELL, CBT_STAFF, LMS_STAFF, SUPER_ADMIN
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    designation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    admission_or_emp_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)

    # Demographics & Media
    dob: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    blood_group: Mapped[str | None] = mapped_column(String(10), nullable=True)
    photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    digital_signature_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Identity Verification
    identity_verification_status: Mapped[str] = mapped_column(
        String(32), default="PENDING", nullable=False
    )  # PENDING, VERIFIED, REJECTED, EXEMPT
    verification_id_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    verification_id_number: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Lifecycle & Soft Delete / Archiving
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    institute_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="SET NULL"), nullable=True, index=True
    )

    institute: Mapped["Institute | None"] = relationship(
        "app.models.institute.Institute",
        back_populates="users",
        lazy="selectin",
    )
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary=user_roles_association,
        lazy="selectin",
    )
    refresh_sessions: Mapped[List["RefreshTokenSession"]] = relationship(
        "RefreshTokenSession",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    documents: Mapped[List["UserDocument"]] = relationship(
        "UserDocument",
        foreign_keys="UserDocument.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
