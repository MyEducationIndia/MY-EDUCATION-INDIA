import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(Base, TimestampUUIDMixin):
    """
    Immutable compliance audit trail tracking all Login, Logout, CRUD, Settings Changes,
    Security Events, API Calls, Permission Changes, and File Uploads.
    """
    __tablename__ = "audit_logs"

    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    actor_username: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    actor_role: Mapped[str | None] = mapped_column(String(64), nullable=True)

    institute_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="SET NULL"), nullable=True, index=True
    )
    module_key: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    event_category: Mapped[str] = mapped_column(
        String(50), default="CRUD_OPERATION", index=True, nullable=False
    )  # AUTH_LOGIN, AUTH_LOGOUT, CRUD_OPERATION, SETTINGS_CHANGE, SECURITY_EVENT, API_CALL, PERMISSION_CHANGE, FILE_UPLOAD
    severity: Mapped[str] = mapped_column(
        String(20), default="INFO", index=True, nullable=False
    )  # INFO, WARNING, SECURITY_ALERT, CRITICAL

    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    http_method: Mapped[str] = mapped_column(String(16), nullable=False)
    endpoint_path: Mapped[str] = mapped_column(String(255), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(64), nullable=False)
    ip_location: Mapped[str] = mapped_column(String(100), default="Indore, MP, India", nullable=False)
    user_agent: Mapped[str] = mapped_column(String(512), nullable=False)
    request_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    changes_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    payload_checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)

    actor_user: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[actor_user_id], lazy="selectin"
    )
