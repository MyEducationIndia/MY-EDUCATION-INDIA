from datetime import date, datetime, time, timezone
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ValidationException
from app.modules.attendance.attendance_engine import AttendanceCalculationEngine
from app.modules.attendance.leave_engine import LeaveWorkflowEngine
from app.modules.attendance.models import (
    AttendanceRule,
    AttendanceSession,
    FacultyAttendance,
    LeaveApproval,
    LeaveRequest,
    LeaveType,
    StaffAttendance,
    StudentAttendance,
)
from app.modules.attendance.repository import AttendanceRepository
from app.modules.attendance.schemas import (
    AttendanceRuleCreate,
    AttendanceSessionCreate,
    FacultyClockInOut,
    LeaveApprovalAction,
    LeaveRequestCreate,
    LeaveTypeCreate,
    StaffClockInOut,
)
from app.modules.attendance.validators import AttendanceValidators


class AttendanceManagementService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = AttendanceRepository(session)

    # 1. Student Attendance Session
    async def create_attendance_session(
        self,
        payload: AttendanceSessionCreate,
        taken_by_user_id: uuid.UUID,
    ) -> AttendanceSession:
        AttendanceValidators.validate_session_dates(payload.session_date)
        AttendanceValidators.validate_student_record_uniqueness(payload.attendance_records)

        sess = AttendanceSession(
            institute_id=payload.institute_id,
            branch_id=payload.branch_id,
            course_id=payload.course_id,
            batch_id=payload.batch_id,
            section_id=payload.section_id,
            subject_id=payload.subject_id,
            session_date=payload.session_date,
            session_type=payload.session_type,
            period_number=payload.period_number,
            start_time=payload.start_time,
            end_time=payload.end_time,
            taken_by_user_id=taken_by_user_id,
            is_locked=False,
        )

        for rec in payload.attendance_records:
            sess.records.append(
                StudentAttendance(
                    student_id=rec.student_id,
                    status=rec.status,
                    check_in_time=rec.check_in_time or time(9, 0),
                    attendance_method="MANUAL",
                    remarks=rec.remarks,
                )
            )

        return await self.repo.create_attendance_session(sess)

    # 2. QR Code Instant Attendance
    async def log_qr_attendance(
        self,
        session_id: uuid.UUID,
        student_id: uuid.UUID,
    ) -> StudentAttendance:
        session_obj = await self.repo.get_session_by_id(session_id)
        if not session_obj:
            raise NotFoundException("Attendance session not found.")
        if session_obj.is_locked:
            raise ValidationException("This attendance session is locked from further updates.")

        # Check existing record
        for existing in session_obj.records:
            if existing.student_id == student_id:
                raise ValidationException("Duplicate scan: Student attendance already logged for this session.")

        rec = StudentAttendance(
            session_id=session_id,
            student_id=student_id,
            status="PRESENT",
            check_in_time=datetime.now().time(),
            attendance_method="QR_CODE",
            remarks="Verified via campus QR scanner",
        )
        return await self.repo.record_student_attendance(rec)

    # 3. Faculty Attendance
    async def log_faculty_attendance(self, payload: FacultyClockInOut) -> FacultyAttendance:
        att_date = payload.attendance_date or date.today()
        record = await self.repo.get_faculty_attendance(payload.faculty_user_id, att_date)

        clock_now = payload.clock_time or datetime.now().time()
        if not record:
            record = FacultyAttendance(
                faculty_user_id=payload.faculty_user_id,
                institute_id=payload.institute_id,
                branch_id=payload.branch_id,
                attendance_date=att_date,
                status="PRESENT",
                clock_in_time=clock_now,
                attendance_method=payload.method,
            )
            return await self.repo.record_faculty_attendance(record)
        else:
            record.clock_out_time = clock_now
            if record.clock_in_time:
                # Calculate hours
                diff = (datetime.combine(att_date, clock_now) - datetime.combine(att_date, record.clock_in_time)).total_seconds()
                record.total_working_hours = round(max(0.0, diff / 3600.0), 2)
            await self.session.commit()
            await self.session.refresh(record)
            return record

    # 4. Leave Management
    async def create_leave_type(self, payload: LeaveTypeCreate) -> LeaveType:
        lt = LeaveType(
            institute_id=payload.institute_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            applicable_to=payload.applicable_to,
            annual_quota_days=payload.annual_quota_days,
            requires_attachment=payload.requires_attachment,
            is_carry_forward=payload.is_carry_forward,
        )
        return await self.repo.create_leave_type(lt)

    async def submit_leave_request(self, payload: LeaveRequestCreate) -> LeaveRequest:
        total_days = AttendanceValidators.validate_leave_dates(payload.start_date, payload.end_date)
        req = LeaveRequest(
            institute_id=payload.institute_id,
            user_id=payload.user_id,
            user_type=payload.user_type,
            leave_type_id=payload.leave_type_id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            total_days=total_days,
            reason=payload.reason,
            attachment_url=payload.attachment_url,
            status="PENDING",
        )
        return await self.repo.create_leave_request(req)

    async def approve_or_reject_leave(
        self,
        payload: LeaveApprovalAction,
        approver_id: uuid.UUID,
    ) -> LeaveRequest:
        req = await self.repo.get_leave_request_by_id(payload.leave_request_id)
        if not req:
            raise NotFoundException("Leave request not found.")

        LeaveWorkflowEngine.validate_transition(req.status, payload.action)
        req.status = payload.action

        approval = LeaveApproval(
            leave_request_id=payload.leave_request_id,
            approver_user_id=approver_id,
            action=payload.action,
            comments=payload.comments,
        )
        await self.repo.record_leave_approval(approval)
        return await self.repo.update_leave_request(req)

    # 5. Rules & Settings
    async def configure_rules(self, payload: AttendanceRuleCreate) -> AttendanceRule:
        rule = AttendanceRule(
            institute_id=payload.institute_id,
            minimum_attendance_pct=payload.minimum_attendance_pct,
            grace_time_minutes=payload.grace_time_minutes,
            half_day_threshold_hours=payload.half_day_threshold_hours,
            consecutive_absent_alert_days=payload.consecutive_absent_alert_days,
            lock_attendance_after_days=payload.lock_attendance_after_days,
            auto_notify_parents_on_absence=payload.auto_notify_parents_on_absence,
            exam_eligibility_threshold_pct=payload.exam_eligibility_threshold_pct,
            is_active=True,
        )
        return await self.repo.save_rule(rule)
