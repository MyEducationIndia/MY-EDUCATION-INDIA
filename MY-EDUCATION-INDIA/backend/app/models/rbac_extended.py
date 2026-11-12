import uuid
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampUUIDMixin


class PermissionGroup(Base, TimestampUUIDMixin):
    """
    Logical grouping of granular permissions (e.g. Admissions Pipeline, Exam Governance, Finance & Dues).
    """
    __tablename__ = "permission_groups"

    group_key: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    group_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="GENERAL", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class RoleTemplate(Base, TimestampUUIDMixin):
    """
    Pre-configured role templates for instant custom role creation (e.g. Junior Lecturer, Fee Accountant, CBT Proctor).
    """
    __tablename__ = "role_templates"

    template_key: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[str] = mapped_column(String(100), default="General", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_permissions: Mapped[List[str]] = mapped_column(JSONB, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
