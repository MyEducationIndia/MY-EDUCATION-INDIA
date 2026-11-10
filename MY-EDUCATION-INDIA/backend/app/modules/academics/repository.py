import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.academics.models import (
    AcademicCalendarEvent,
    Batch,
    Classroom,
    Course,
    Curriculum,
    Department,
    FacultyAssignment,
    GradingSystem,
    Program,
    Section,
    Subject,
    Timetable,
    TimetableSlot,
)


class AcademicRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ==================== Departments ====================
    async def list_departments(self, institute_id: uuid.UUID) -> List[Department]:
        stmt = select(Department).where(Department.institute_id == institute_id, Department.is_active.is_(True)).order_by(Department.name.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_department(self, dept: Department) -> Department:
        self.session.add(dept)
        await self.session.flush()
        return dept

    # ==================== Programs & Courses ====================
    async def list_programs(self, institute_id: uuid.UUID) -> List[Program]:
        stmt = select(Program).where(Program.institute_id == institute_id, Program.is_active.is_(True)).order_by(Program.name.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_program(self, program: Program) -> Program:
        self.session.add(program)
        await self.session.flush()
        return program

    async def list_courses(self, institute_id: uuid.UUID) -> List[Course]:
        stmt = (
            select(Course)
            .options(selectinload(Course.department), selectinload(Course.program))
            .where(Course.institute_id == institute_id, Course.is_active.is_(True))
            .order_by(Course.name.asc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_course(self, course: Course) -> Course:
        self.session.add(course)
        await self.session.flush()
        return course

    # ==================== Subjects ====================
    async def list_subjects(self, institute_id: uuid.UUID) -> List[Subject]:
        stmt = select(Subject).where(Subject.institute_id == institute_id, Subject.is_active.is_(True)).order_by(Subject.name.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_subject(self, subject: Subject) -> Subject:
        self.session.add(subject)
        await self.session.flush()
        return subject

    # ==================== Batches & Sections ====================
    async def list_batches(self, institute_id: uuid.UUID) -> List[Batch]:
        stmt = (
            select(Batch)
            .options(selectinload(Batch.course), selectinload(Batch.sections))
            .where(Batch.institute_id == institute_id, Batch.is_active.is_(True))
            .order_by(Batch.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_batch(self, batch: Batch) -> Batch:
        self.session.add(batch)
        await self.session.flush()
        return batch

    async def create_section(self, section: Section) -> Section:
        self.session.add(section)
        await self.session.flush()
        return section

    # ==================== Timetable ====================
    async def get_timetable_by_batch_section(self, batch_id: uuid.UUID, section_id: uuid.UUID) -> Optional[Timetable]:
        stmt = (
            select(Timetable)
            .options(
                selectinload(Timetable.slots).selectinload(TimetableSlot.subject),
                selectinload(Timetable.slots).selectinload(TimetableSlot.classroom),
            )
            .where(Timetable.batch_id == batch_id, Timetable.section_id == section_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_timetable(self, tt: Timetable) -> Timetable:
        self.session.add(tt)
        await self.session.flush()
        return tt

    async def add_timetable_slot(self, slot: TimetableSlot) -> TimetableSlot:
        self.session.add(slot)
        await self.session.flush()
        return slot
