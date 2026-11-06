import uuid
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampUUIDMixin

if TYPE_CHECKING:
    from app.models.institute import Institute


class SystemModuleConfig(Base, TimestampUUIDMixin):
    __tablename__ = "system_module_configs"
    __table_args__ = (
        UniqueConstraint("institute_id", "module_key", name="uq_institute_module_key"),
    )

    institute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    module_key: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    subdomain: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_core_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    configuration: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    institute: Mapped["Institute"] = relationship("Institute", back_populates="module_configs")
