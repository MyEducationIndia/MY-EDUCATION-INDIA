import uuid
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ------------------- Attendance Sessions & Student Records -------------------
class StudentAttendanceItem(BaseModel):
    student_id: uuid.UUID
    status: str = "PRESENT" # PRESENT, ABSENT, LATE, HALF_DAY, LEAVE, ON_DUTY
    check_in_time: Optional[time] = None
    remarks: Optional[str] = None


class AttendanceSessionCreate(BaseModel):
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    course_id: Optional[uuid.UUID] = None
    batch_id: Optional[uuid.UUID] = None
    section_id: Optional[uuid.UUID] = None
    subject_id: Optional[uuid.UUID] = None
    session_date: date
    session_type: str = "DAILY" # DAILY, PERIOD_WISE, LAB
    period_number: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    attendance_records: List[StudentAttendanceItem] = Field(default_factory=list)


class AttendanceSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    session_date: date
    session_type: str
    period_number: Optional[int]
    is_locked: bool
    created_at: datetime


class StudentAttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    student_id: uuid.UUID
    status: str
    check_in_time: Optional[time]
    attendance_method: str
    remarks: Optional[str]
    created_at: datetime


# ------------------- Faculty & Staff Attendance -------------------
class FacultyClockInOut(BaseModel):
    faculty_user_id: uuid.UUID
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    attendance_date: Optional[date] = None
    action_type: str = "CLOCK_IN" # CLOCK_IN, CLOCK_OUT
    clock_time: Optional[time] = None
    method: str = "BIOMETRIC" # BIOMETRIC, QR_CODE, MANUAL


class FacultyAttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    faculty_user_id: uuid.UUID
    attendance_date: date
    status: str
    clock_in_time: Optional[time]
    clock_out_time: Optional[time]
    total_working_hours: float
    attendance_method: str


class StaffClockInOut(BaseModel):
    staff_user_id: uuid.UUID
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    attendance_date: Optional[date] = None
    action_type: str = "CLOCK_IN"
    clock_time: Optional[time] = None
    method: str = "BIOMETRIC"


class StaffAttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    staff_user_id: uuid.UUID
    attendance_date: date
    status: str
    clock_in_time: Optional[time]
    clock_out_time: Optional[time]
    total_working_hours: float
    attendance_method: str


# ------------------- QR Code Attendance -------------------
class QRScanAttendanceRequest(BaseModel):
    student_qr_token: str = Field(..., min_length=10)
    session_id: uuid.UUID
    device_id: Optional[str] = "GATEWAY_READER_01"


# ------------------- Leave Management -------------------
class LeaveTypeCreate(BaseModel):
    institute_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=120)
    applicable_to: str = "ALL" # STUDENT, FACULTY, STAFF, ALL
    annual_quota_days: int = Field(12, ge=0)
    requires_attachment: bool = False
    is_carry_forward: bool = False


class LeaveTypeResponse(LeaveTypeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


class LeaveRequestCreate(BaseModel):
    institute_id: uuid.UUID
    user_id: uuid.UUID
    user_type: str = "STUDENT" # STUDENT, FACULTY, STAFF
    leave_type_id: uuid.UUID
    start_date: date
    end_date: date
    reason: str = Field(..., min_length=5)
    attachment_url: Optional[str] = None


class LeaveApprovalAction(BaseModel):
    leave_request_id: uuid.UUID
    action: str = "APPROVED" # APPROVED, REJECTED
    comments: Optional[str] = None


class LeaveRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    user_id: uuid.UUID
    user_type: str
    leave_type_id: uuid.UUID
    start_date: date
    end_date: date
    total_days: float
    reason: str
    status: str
    applied_at: datetime


# ------------------- Attendance Rules & Settings -------------------
class AttendanceRuleCreate(BaseModel):
    institute_id: uuid.UUID
    minimum_attendance_pct: float = Field(75.0, ge=0.0, le=100.0)
    grace_time_minutes: int = Field(15, ge=0)
    half_day_threshold_hours: float = Field(4.0, ge=0.0)
    consecutive_absent_alert_days: int = Field(3, ge=1)
    lock_attendance_after_days: int = Field(2, ge=0)
    auto_notify_parents_on_absence: bool = True
    exam_eligibility_threshold_pct: float = Field(75.0, ge=0.0, le=100.0)


class AttendanceRuleResponse(AttendanceRuleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


# ------------------- Dashboard & Analytics -------------------
class AttendanceDashboardSummary(BaseModel):
    today_date: date
    total_students_enrolled: int
    students_present_count: int
    students_absent_count: int
    students_late_count: int
    overall_attendance_pct: float
    faculty_present_pct: float
    staff_present_pct: float
    pending_leaves_count: int
    low_attendance_alert_count: int
    weekly_trend: List[Dict[str, Any]]


class StudentAttendanceReportCard(BaseModel):
    student_id: uuid.UUID
    total_working_days: int
    present_days: int
    absent_days: int
    leave_days: int
    late_days: int
    attendance_percentage: float
    is_exam_eligible: bool
