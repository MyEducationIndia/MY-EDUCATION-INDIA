import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.modules.academics.models import (
    Batch,
    Course,
    Department,
    Program,
    Section,
    Subject,
    Timetable,
    TimetableSlot,
)
from app.modules.academics.repository import AcademicRepository
from app.modules.academics.schemas import (
    BatchCreate,
    CourseCreate,
    DepartmentCreate,
    ProgramCreate,
    SectionCreate,
    SubjectCreate,
    TimetableCreate,
    TimetableSlotCreate,
)
from app.modules.academics.timetable_engine import TimetableConflictEngine


class AcademicManagementService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = AcademicRepository(session)

    async def create_department(self, payload: DepartmentCreate) -> Department:
        dept = Department(**payload.model_dump())
        created = await self.repo.create_department(dept)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def create_program(self, payload: ProgramCreate) -> Program:
        prog = Program(**payload.model_dump())
        created = await self.repo.create_program(prog)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def create_course(self, payload: CourseCreate) -> Course:
        course = Course(**payload.model_dump())
        created = await self.repo.create_course(course)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def create_subject(self, payload: SubjectCreate) -> Subject:
        subj = Subject(**payload.model_dump())
        created = await self.repo.create_subject(subj)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def create_batch(self, payload: BatchCreate) -> Batch:
        batch = Batch(**payload.model_dump())
        created = await self.repo.create_batch(batch)
        # Automatically provision Default Section A
        sec_a = Section(batch_id=created.id, name="Section A", capacity=payload.intake_capacity)
        await self.repo.create_section(sec_a)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def add_timetable_slot(self, payload: TimetableSlotCreate) -> TimetableSlot:
        # Collision prevention engine check
        await TimetableConflictEngine.verify_no_collisions(
            session=self.session,
            day_of_week=payload.day_of_week,
            start_time=payload.start_time,
            end_time=payload.end_time,
            faculty_user_id=payload.faculty_user_id,
            classroom_id=payload.classroom_id,
        )

        slot = TimetableSlot(**payload.model_dump())
        created = await self.repo.add_timetable_slot(slot)
        await self.session.commit()
        await self.session.refresh(created)
        return created
