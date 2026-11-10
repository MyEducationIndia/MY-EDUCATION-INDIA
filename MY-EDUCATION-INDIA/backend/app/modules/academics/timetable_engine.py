from datetime import time
from typing import List, Optional
import uuid
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictException
from app.modules.academics.models import TimetableSlot


class TimetableConflictEngine:
    """Automated collision detection for faculty, classrooms, and batch schedules."""

    @staticmethod
    async def verify_no_collisions(
        session: AsyncSession,
        day_of_week: int,
        start_time: time,
        end_time: time,
        faculty_user_id: Optional[uuid.UUID] = None,
        classroom_id: Optional[uuid.UUID] = None,
        exclude_slot_id: Optional[uuid.UUID] = None,
    ) -> None:
        # Check time overlap: (start1 < end2) and (end1 > start2)
        stmt = select(TimetableSlot).where(
            TimetableSlot.day_of_week == day_of_week,
            TimetableSlot.start_time < end_time,
            TimetableSlot.end_time > start_time,
        )

        if exclude_slot_id:
            stmt = stmt.where(TimetableSlot.id != exclude_slot_id)

        predicates = []
        if faculty_user_id:
            predicates.append(TimetableSlot.faculty_user_id == faculty_user_id)
        if classroom_id:
            predicates.append(TimetableSlot.classroom_id == classroom_id)

        if predicates:
            stmt = stmt.where(or_(*predicates))
            res = await session.execute(stmt)
            conflicts = list(res.scalars().all())

            for c in conflicts:
                if faculty_user_id and c.faculty_user_id == faculty_user_id:
                    raise ConflictException(
                        f"Faculty collision: Assigned faculty is already booked on Day {day_of_week} between {c.start_time} and {c.end_time}."
                    )
                if classroom_id and c.classroom_id == classroom_id:
                    raise ConflictException(
                        f"Classroom collision: Classroom is already occupied on Day {day_of_week} between {c.start_time} and {c.end_time}."
                    )
