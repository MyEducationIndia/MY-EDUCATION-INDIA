import uuid
from typing import List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.students.models import (
    Student,
    StudentAddress,
    StudentCustomField,
    StudentCustomValue,
    StudentDocument,
    StudentGuardian,
    StudentMedical,
    StudentNote,
    StudentPhoto,
    StudentProfile,
    StudentQRCode,
    StudentStatusHistory,
    StudentTimeline,
)


class StudentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_student_by_id(self, student_id: uuid.UUID) -> Optional[Student]:
        stmt = (
            select(Student)
            .options(
                selectinload(Student.profile),
                selectinload(Student.addresses),
                selectinload(Student.guardians),
                selectinload(Student.medical),
                selectinload(Student.documents),
                selectinload(Student.timeline),
                selectinload(Student.custom_values).selectinload(StudentCustomValue.field_definition),
                selectinload(Student.qr_code),
                selectinload(Student.photo),
            )
            .where(Student.id == student_id, Student.is_deleted.is_(False))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_student_by_reg_number(self, reg_num: str, institute_id: uuid.UUID) -> Optional[Student]:
        stmt = (
            select(Student)
            .where(
                Student.registration_number == reg_num.strip(),
                Student.institute_id == institute_id,
                Student.is_deleted.is_(False),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def search_students_paginated(
        self,
        institute_id: uuid.UUID,
        query: Optional[str] = None,
        course_name: Optional[str] = None,
        batch_name: Optional[str] = None,
        status: Optional[str] = None,
        branch_id: Optional[uuid.UUID] = None,
        academic_year_code: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Student], int]:
        stmt = (
            select(Student)
            .options(selectinload(Student.photo))
            .where(Student.institute_id == institute_id, Student.is_deleted.is_(False))
        )
        count_stmt = select(func.count(Student.id)).where(Student.institute_id == institute_id, Student.is_deleted.is_(False))

        if branch_id:
            stmt = stmt.where(Student.branch_id == branch_id)
            count_stmt = count_stmt.where(Student.branch_id == branch_id)
        if course_name:
            stmt = stmt.where(Student.course_name.ilike(f"%{course_name.strip()}%"))
            count_stmt = count_stmt.where(Student.course_name.ilike(f"%{course_name.strip()}%"))
        if batch_name:
            stmt = stmt.where(Student.batch_name.ilike(f"%{batch_name.strip()}%"))
            count_stmt = count_stmt.where(Student.batch_name.ilike(f"%{batch_name.strip()}%"))
        if status:
            stmt = stmt.where(Student.status == status.upper())
            count_stmt = count_stmt.where(Student.status == status.upper())
        if academic_year_code:
            stmt = stmt.where(Student.academic_year_code == academic_year_code)
            count_stmt = count_stmt.where(Student.academic_year_code == academic_year_code)

        if query:
            pat = f"%{query.strip()}%"
            filter_expr = or_(
                Student.registration_number.ilike(pat),
                Student.enrollment_number.ilike(pat),
                Student.roll_number.ilike(pat),
                Student.erp_id.ilike(pat),
                Student.first_name.ilike(pat),
                Student.last_name.ilike(pat),
                Student.email.ilike(pat),
                Student.phone_number.ilike(pat),
            )
            stmt = stmt.where(filter_expr)
            count_stmt = count_stmt.where(filter_expr)

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar_one() or 0)

        stmt = stmt.order_by(Student.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        res = await self.session.execute(stmt)
        return list(res.scalars().all()), total

    async def create_student(self, student: Student) -> Student:
        self.session.add(student)
        await self.session.flush()
        return student

    async def list_custom_fields(self, institute_id: uuid.UUID) -> List[StudentCustomField]:
        stmt = select(StudentCustomField).where(StudentCustomField.institute_id == institute_id).order_by(StudentCustomField.display_order.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def save_custom_field(self, field: StudentCustomField) -> StudentCustomField:
        self.session.add(field)
        await self.session.flush()
        return field
