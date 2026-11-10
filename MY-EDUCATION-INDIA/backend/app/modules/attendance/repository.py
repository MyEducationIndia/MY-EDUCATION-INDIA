from datetime import date
from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.attendance.models import (
    AttendanceMethod,
    AttendanceRule,
    AttendanceSession,
    FacultyAttendance,
    LeaveApproval,
    LeaveRequest,
    LeaveType,
    StaffAttendance,
    StudentAttendance,
)


class AttendanceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # Sessions & Student Attendance
    async def create_attendance_session(self, session_obj: AttendanceSession) -> AttendanceSession:
        self.session.add(session_obj)
        await self.session.commit()
        await self.session.refresh(session_obj)
        return session_obj

    async def get_session_by_id(self, session_id: uuid.UUID) -> Optional[AttendanceSession]:
        stmt = (
            select(AttendanceSession)
            .where(AttendanceSession.id == session_id)
            .options(selectinload(AttendanceSession.records))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def record_student_attendance(self, record: StudentAttendance) -> StudentAttendance:
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    # Faculty & Staff Attendance
    async def record_faculty_attendance(self, att: FacultyAttendance) -> FacultyAttendance:
        self.session.add(att)
        await self.session.commit()
        await self.session.refresh(att)
        return att

    async def get_faculty_attendance(self, faculty_id: uuid.UUID, att_date: date) -> Optional[FacultyAttendance]:
        stmt = select(FacultyAttendance).where(
            FacultyAttendance.faculty_user_id == faculty_id,
            FacultyAttendance.attendance_date == att_date,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def record_staff_attendance(self, att: StaffAttendance) -> StaffAttendance:
        self.session.add(att)
        await self.session.commit()
        await self.session.refresh(att)
        return att

    # Leave Management
    async def create_leave_type(self, leave_type: LeaveType) -> LeaveType:
        self.session.add(leave_type)
        await self.session.commit()
        await self.session.refresh(leave_type)
        return leave_type

    async def get_leave_types(self, institute_id: uuid.UUID) -> List[LeaveType]:
        stmt = select(LeaveType).where(LeaveType.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_leave_request(self, req: LeaveRequest) -> LeaveRequest:
        self.session.add(req)
        await self.session.commit()
        await self.session.refresh(req)
        return req

    async def get_leave_request_by_id(self, request_id: uuid.UUID) -> Optional[LeaveRequest]:
        stmt = (
            select(LeaveRequest)
            .where(LeaveRequest.id == request_id)
            .options(selectinload(LeaveRequest.approvals), selectinload(LeaveRequest.leave_type))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_leave_request(self, req: LeaveRequest) -> LeaveRequest:
        await self.session.commit()
        await self.session.refresh(req)
        return req

    async def record_leave_approval(self, approval: LeaveApproval) -> LeaveApproval:
        self.session.add(approval)
        await self.session.commit()
        await self.session.refresh(approval)
        return approval

    # Attendance Rules
    async def get_active_rule(self, institute_id: uuid.UUID) -> Optional[AttendanceRule]:
        stmt = select(AttendanceRule).where(
            AttendanceRule.institute_id == institute_id,
            AttendanceRule.is_active.is_(True),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def save_rule(self, rule: AttendanceRule) -> AttendanceRule:
        self.session.add(rule)
        await self.session.commit()
        await self.session.refresh(rule)
        return rule
