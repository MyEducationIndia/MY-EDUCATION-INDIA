from datetime import date
from typing import List, Set
import uuid
from app.core.exceptions import ValidationException
from app.modules.attendance.schemas import StudentAttendanceItem


class AttendanceValidators:
    @staticmethod
    def validate_session_dates(session_date: date, lock_days: int = 2) -> None:
        today = date.today()
        if session_date > today:
            raise ValidationException("Attendance cannot be recorded for a future date.")
        delta = (today - session_date).days
        if delta > lock_days:
            raise ValidationException(f"Attendance for this date is locked ({lock_days} days limit exceeded).")

    @staticmethod
    def validate_student_record_uniqueness(records: List[StudentAttendanceItem]) -> None:
        seen: Set[uuid.UUID] = set()
        for rec in records:
            if rec.student_id in seen:
                raise ValidationException(f"Duplicate student record detected in attendance session: {rec.student_id}")
            seen.add(rec.student_id)

    @staticmethod
    def validate_leave_dates(start_date: date, end_date: date) -> float:
        if start_date > end_date:
            raise ValidationException("Leave start date cannot be after end date.")
        total_days = (end_date - start_date).days + 1
        return float(total_days)
