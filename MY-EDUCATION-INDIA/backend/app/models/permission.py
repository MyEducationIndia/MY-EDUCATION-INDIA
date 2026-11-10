from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampUUIDMixin


class Permission(Base, TimestampUUIDMixin):
    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    module_key: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    group_key: Mapped[str] = mapped_column(String(64), default="GENERAL", nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(32), default="READ", nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
