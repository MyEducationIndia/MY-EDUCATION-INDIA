import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin


class Notification(Base, TimestampUUIDMixin):
    __tablename__ = "notifications"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    institute_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(
        String(64), default="SYSTEM", index=True, nullable=False
    ) # SYSTEM, FEE_DUE, ADMISSION, EXAM, ATTENDANCE, BACKUP, SERVER, SMS, WHATSAPP, EMAIL
    priority: Mapped[str] = mapped_column(
        String(32), default="NORMAL", index=True, nullable=False
    ) # LOW, NORMAL, HIGH, CRITICAL
    action_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    meta_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class DashboardWidget(Base, TimestampUUIDMixin):
    """Configurable widget registry and user dashboard preferences."""
    __tablename__ = "dashboard_widgets"
    __table_args__ = (
        UniqueConstraint("widget_key", "user_id", name="uq_widget_user"),
        {"extend_existing": True},
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    institute_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True, index=True
    )
    widget_key: Mapped[str] = mapped_column(String(80), index=True, nullable=False) # e.g. stats_kpi, admission_trends, fee_collection, recent_activities
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(64), default="ANALYTICS", nullable=False) # STATS, CHARTS, ACTIVITIES, NOTIFICATIONS, SYSTEM
    grid_position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    grid_width: Mapped[int] = mapped_column(Integer, default=6, nullable=False) # 1 to 12 cols
    grid_height: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    configuration: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class UserPinnedModule(Base, TimestampUUIDMixin):
    """Tracks user sidebar favorites and quick pinned navigation items."""
    __tablename__ = "user_pinned_modules"
    __table_args__ = (
        UniqueConstraint("user_id", "module_key", name="uq_user_pinned_module"),
        {"extend_existing": True},
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    module_key: Mapped[str] = mapped_column(String(64), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class DashboardActivity(Base, TimestampUUIDMixin):
    """High-value domain activity feed specifically optimized for dashboard timeline."""
    __tablename__ = "dashboard_activities"
    __table_args__ = {"extend_existing": True}

    institute_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="SET NULL"), nullable=True, index=True
    )
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True
    )
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    actor_name: Mapped[str] = mapped_column(String(120), nullable=False)
    action_type: Mapped[str] = mapped_column(String(80), index=True, nullable=False) # STUDENT_CREATED, ADMISSION_APPROVED, FEE_PAID, CERTIFICATE_GENERATED, USER_LOGIN, BACKUP_COMPLETED, SETTINGS_UPDATED
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False) # student, admission, fee, certificate, user, backup
    entity_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    detail_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True, nullable=False)
