from datetime import date
from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.modules.auth.dependencies import get_current_user, require_permissions
from app.modules.attendance.analytics import AttendanceAnalyticsEngine
from app.modules.attendance.reports import AttendanceReportEngine
from app.modules.attendance.schemas import (
    AttendanceDashboardSummary,
    AttendanceRuleCreate,
    AttendanceRuleResponse,
    AttendanceSessionCreate,
    AttendanceSessionResponse,
    FacultyAttendanceResponse,
    FacultyClockInOut,
    LeaveApprovalAction,
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveTypeCreate,
    LeaveTypeResponse,
    QRScanAttendanceRequest,
    StudentAttendanceResponse,
)
from app.modules.attendance.service import AttendanceManagementService

attendance_router = APIRouter(prefix="/attendance", tags=["Enterprise Attendance & Leave Management"])


# 1. Sessions & Daily Student Attendance
@attendance_router.post("/sessions", response_model=AttendanceSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_attendance_session(
    payload: AttendanceSessionCreate,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(require_permissions("attendance.mark")),
) -> AttendanceSessionResponse:
    service = AttendanceManagementService(db)
    user_id = getattr(user, "id", uuid.uuid4())
    session_obj = await service.create_attendance_session(payload, taken_by_user_id=user_id)
    return AttendanceSessionResponse.model_validate(session_obj)


# 2. QR Code Attendance Scan
@attendance_router.post("/qr-scan", response_model=StudentAttendanceResponse, status_code=status.HTTP_201_CREATED)
async def scan_qr_attendance(
    payload: QRScanAttendanceRequest,
    student_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("attendance.mark")),
) -> StudentAttendanceResponse:
    service = AttendanceManagementService(db)
    rec = await service.log_qr_attendance(payload.session_id, student_id)
    return StudentAttendanceResponse.model_validate(rec)


# 3. Faculty & Staff Attendance
@attendance_router.post("/faculty/clock", response_model=FacultyAttendanceResponse)
async def faculty_clock_in_out(
    payload: FacultyClockInOut,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> FacultyAttendanceResponse:
    service = AttendanceManagementService(db)
    record = await service.log_faculty_attendance(payload)
    return FacultyAttendanceResponse.model_validate(record)


# 4. Leave Management
@attendance_router.get("/leave-types", response_model=List[LeaveTypeResponse])
async def list_leave_types(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[LeaveTypeResponse]:
    service = AttendanceManagementService(db)
    types = await service.repo.get_leave_types(institute_id)
    return [LeaveTypeResponse.model_validate(t) for t in types]


@attendance_router.post("/leave-types", response_model=LeaveTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_leave_type(
    payload: LeaveTypeCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("leaves.manage")),
) -> LeaveTypeResponse:
    service = AttendanceManagementService(db)
    item = await service.create_leave_type(payload)
    return LeaveTypeResponse.model_validate(item)


@attendance_router.post("/leaves/apply", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
async def submit_leave_request(
    payload: LeaveRequestCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> LeaveRequestResponse:
    service = AttendanceManagementService(db)
    req = await service.submit_leave_request(payload)
    return LeaveRequestResponse.model_validate(req)


@attendance_router.post("/leaves/action", response_model=LeaveRequestResponse)
async def approve_or_reject_leave(
    payload: LeaveApprovalAction,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(require_permissions("leaves.approve")),
) -> LeaveRequestResponse:
    service = AttendanceManagementService(db)
    approver_id = getattr(user, "id", uuid.uuid4())
    req = await service.approve_or_reject_leave(payload, approver_id=approver_id)
    return LeaveRequestResponse.model_validate(req)


# 5. Reports & Analytics
@attendance_router.get("/reports/daily")
async def get_daily_report(
    institute_id: uuid.UUID = Query(...),
    report_date: date = Query(default=date.today()),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("attendance.view")),
) -> Dict[str, Any]:
    return await AttendanceReportEngine.get_daily_attendance_summary(db, institute_id, report_date)


@attendance_router.get("/analytics", response_model=AttendanceDashboardSummary)
async def get_attendance_analytics(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("attendance.view")),
) -> AttendanceDashboardSummary:
    summary = await AttendanceAnalyticsEngine.get_dashboard_kpis(db, institute_id)
    return AttendanceDashboardSummary.model_validate(summary)


# 6. Rules & Settings
@attendance_router.post("/rules", response_model=AttendanceRuleResponse, status_code=status.HTTP_201_CREATED)
async def configure_attendance_rules(
    payload: AttendanceRuleCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("attendance.manage")),
) -> AttendanceRuleResponse:
    service = AttendanceManagementService(db)
    rule = await service.configure_rules(payload)
    return AttendanceRuleResponse.model_validate(rule)
