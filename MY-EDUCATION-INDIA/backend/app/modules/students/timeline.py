from datetime import datetime, timezone
from typing import Any, Dict
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.students.models import StudentTimeline


class StudentTimelineService:
    """Records immutable, timestamped lifecycle milestones for students."""

    @staticmethod
    async def record_event(
        session: AsyncSession,
        student_id: uuid.UUID,
        event_category: str,
        event_title: str,
        event_description: str,
        recorded_by: str = "System",
        meta_payload: Dict[str, Any] | None = None,
    ) -> StudentTimeline:
        event = StudentTimeline(
            student_id=student_id,
            event_category=event_category.upper(),
            event_title=event_title,
            event_description=event_description,
            recorded_by=recorded_by,
            occurred_at=datetime.now(timezone.utc),
            meta_payload=meta_payload or {},
        )
        session.add(event)
        await session.flush()
        return event
