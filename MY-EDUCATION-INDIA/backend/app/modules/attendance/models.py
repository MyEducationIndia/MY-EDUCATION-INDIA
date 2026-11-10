import uuid
from datetime import date, datetime, time, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    batch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    section_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    session_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    session_type: Mapped[str] = mapped_column(String(32), default="DAILY", nullable=False) # DAILY, PERIOD_WISE, LAB, PRACTICAL, SEMINAR
    period_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    start_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    end_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    taken_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    records: Mapped[List["StudentAttendance"]] = relationship("StudentAttendance", back_populates="session", cascade="all, delete-orphan")


class StudentAttendance(Base):
    __tablename__ = "student_attendance"
    __table_args__ = (
        UniqueConstraint("session_id", "student_id", name="uq_student_attendance_session"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("attendance_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(24), default="PRESENT", nullable=False) # PRESENT, ABSENT, LATE, HALF_DAY, LEAVE, MEDICAL_LEAVE, ON_DUTY
    check_in_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    attendance_method: Mapped[str] = mapped_column(String(32), default="MANUAL", nullable=False) # MANUAL, QR_CODE, BARCODE, RFID, BIOMETRIC
    remarks: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    session: Mapped["AttendanceSession"] = relationship("AttendanceSession", back_populates="records")


class FacultyAttendance(Base):
    __tablename__ = "faculty_attendance"
    __table_args__ = (
        UniqueConstraint("faculty_user_id", "attendance_date", name="uq_faculty_daily_attendance"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(24), default="PRESENT", nullable=False) # PRESENT, ABSENT, LATE, HALF_DAY, ON_DUTY, LEAVE
    clock_in_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    clock_out_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    total_working_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    attendance_method: Mapped[str] = mapped_column(String(32), default="BIOMETRIC", nullable=False)
    remarks: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StaffAttendance(Base):
    __tablename__ = "staff_attendance"
    __table_args__ = (
        UniqueConstraint("staff_user_id", "attendance_date", name="uq_staff_daily_attendance"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(24), default="PRESENT", nullable=False)
    clock_in_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    clock_out_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    total_working_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    attendance_method: Mapped[str] = mapped_column(String(32), default="BIOMETRIC", nullable=False)
    remarks: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AttendanceMethod(Base):
    __tablename__ = "attendance_methods"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    method_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True) # MANUAL, QR_CODE, BARCODE, RFID, BIOMETRIC, GEO_FENCE
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    configuration_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AttendanceRule(Base):
    __tablename__ = "attendance_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    minimum_attendance_pct: Mapped[float] = mapped_column(Float, default=75.0, nullable=False) # UGC/AICTE 75% rule
    grace_time_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    half_day_threshold_hours: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    consecutive_absent_alert_days: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    lock_attendance_after_days: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    auto_notify_parents_on_absence: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    exam_eligibility_threshold_pct: Mapped[float] = mapped_column(Float, default=75.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    user_type: Mapped[str] = mapped_column(String(24), nullable=False) # STUDENT, FACULTY, STAFF
    log_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    log_type: Mapped[str] = mapped_column(String(20), nullable=False) # IN, OUT, BREAK_IN, BREAK_OUT
    device_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    method: Mapped[str] = mapped_column(String(32), default="QR_CODE", nullable=False)
    location_coordinates: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    raw_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class LeaveType(Base):
    __tablename__ = "leave_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    applicable_to: Mapped[str] = mapped_column(String(24), default="ALL", nullable=False) # STUDENT, FACULTY, STAFF, ALL
    annual_quota_days: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    requires_attachment: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_carry_forward: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    user_type: Mapped[str] = mapped_column(String(24), nullable=False) # STUDENT, FACULTY, STAFF
    leave_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leave_types.id", ondelete="RESTRICT"), nullable=False, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_days: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    attachment_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(24), default="PENDING", nullable=False) # PENDING, APPROVED, REJECTED, CANCELLED
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    leave_type: Mapped["LeaveType"] = relationship("LeaveType")
    approvals: Mapped[List["LeaveApproval"]] = relationship("LeaveApproval", back_populates="request", cascade="all, delete-orphan")


class LeaveApproval(Base):
    __tablename__ = "leave_approvals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    leave_request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leave_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    approver_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    action: Mapped[str] = mapped_column(String(24), nullable=False) # APPROVED, REJECTED
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    request: Mapped["LeaveRequest"] = relationship("LeaveRequest", back_populates="approvals")


class AttendanceReport(Base):
    __tablename__ = "attendance_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True) # DAILY, MONTHLY, SEMESTER, DEFICIENCY_LIST
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_records: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    parameters_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    generated_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AttendanceAnalytics(Base):
    __tablename__ = "attendance_analytics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    metric_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    student_attendance_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    faculty_attendance_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    staff_attendance_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    metrics_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AttendanceNotification(Base):
    __tablename__ = "attendance_notifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipient_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    recipient_role: Mapped[str] = mapped_column(String(24), nullable=False) # PARENT, STUDENT, FACULTY
    notification_type: Mapped[str] = mapped_column(String(32), nullable=False) # ABSENCE_ALERT, LOW_ATTENDANCE_WARNING, LEAVE_STATUS
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    message: Mapped[Text] = mapped_column(Text, nullable=False)
    is_sent: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
