import uuid
from typing import TYPE_CHECKING, List
from sqlalchemy import Boolean, Column, ForeignKey, String, Table, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.permission import Permission

role_permissions_association = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)


class Role(Base, TimestampUUIDMixin):
    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint("code", "institute_id", name="uq_roles_code_institute"),
    )

    code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    portal_subdomain: Mapped[str] = mapped_column(String(32), default="admin", nullable=False)
    is_system_role: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_custom_role: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    department_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    data_scope: Mapped[str] = mapped_column(String(50), default="ALL_INSTITUTE", nullable=False)
    field_permissions_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    menu_permissions_json: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    institute_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True, index=True
    )

    permissions: Mapped[List["Permission"]] = relationship(
        "Permission",
        secondary=role_permissions_association,
        lazy="selectin",
    )
