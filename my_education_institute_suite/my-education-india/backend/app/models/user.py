import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.institute import Institute
    from app.models.role import Role
    from app.models.refresh_token import RefreshTokenSession

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

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    institute_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="SET NULL"), nullable=True, index=True
    )

    institute: Mapped["Institute | None"] = relationship("Institute", back_populates="users", lazy="selectin")
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
