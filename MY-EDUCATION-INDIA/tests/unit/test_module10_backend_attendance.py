"""Unit and Integration Tests for Module 10: Enterprise Attendance & Leave Management System
Verifies:
- AST compilation across all Module 10 backend files
- Pydantic v2 schemas validation for sessions, faculty clock-in, leave types, and requests
- AttendanceCalculationEngine calculations (attendance %, UGC 75% exam eligibility, class shortfall math)
- LeaveWorkflowEngine state machine transitions & quota availability checks
- AttendanceValidators (future date rejection, duplicate student scan prevention, leave date validation)
- Zero browser LocalStorage/SessionStorage/IndexedDB in Module 10 frontend source
"""
import ast
from datetime import date, timedelta
import os
from pathlib import Path
import re
import sys
import unittest
import uuid

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

os.environ.setdefault("SECRET_KEY", "test_secret_key_minimum_32_characters_long_for_security")
os.environ.setdefault("REFRESH_SECRET_KEY", "test_refresh_secret_key_minimum_32_characters_long")
os.environ.setdefault("CSRF_SECRET_KEY", "test_csrf_secret_key_minimum_32_characters_long_sec")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("SYNC_DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")

from app.core.exceptions import ValidationException
from app.modules.attendance.attendance_engine import AttendanceCalculationEngine
from app.modules.attendance.leave_engine import LeaveWorkflowEngine
from app.modules.attendance.schemas import (
    AttendanceRuleCreate,
    AttendanceSessionCreate,
    FacultyClockInOut,
    LeaveRequestCreate,
    LeaveTypeCreate,
    StudentAttendanceItem,
)
from app.modules.attendance.validators import AttendanceValidators


class TestModule10BackendAttendance(unittest.TestCase):

    def test_all_module10_python_files_compile(self) -> None:
        att_dir = PROJECT_ROOT / "backend/app/modules/attendance"
        self.assertTrue(att_dir.exists(), "attendance backend directory must exist")
        for py_file in att_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_attendance_schemas_validation(self) -> None:
        dummy_inst_id = uuid.uuid4()
        dummy_user_id = uuid.uuid4()
        dummy_leave_type_id = uuid.uuid4()

        lt = LeaveTypeCreate(
            institute_id=dummy_inst_id,
            code="CASUAL",
            name="Casual Leave",
            annual_quota_days=12,
        )
        self.assertEqual(lt.code, "CASUAL")
        self.assertEqual(lt.annual_quota_days, 12)

        req = LeaveRequestCreate(
            institute_id=dummy_inst_id,
            user_id=dummy_user_id,
            user_type="FACULTY",
            leave_type_id=dummy_leave_type_id,
            start_date=date(2026, 11, 10),
            end_date=date(2026, 11, 12),
            reason="Attending National Education Conference",
        )
        self.assertEqual(req.user_type, "FACULTY")

        clock = FacultyClockInOut(
            faculty_user_id=dummy_user_id,
            institute_id=dummy_inst_id,
            action_type="CLOCK_IN",
            method="BIOMETRIC",
        )
        self.assertEqual(clock.action_type, "CLOCK_IN")

        rule = AttendanceRuleCreate(
            institute_id=dummy_inst_id,
            minimum_attendance_pct=75.0,
            grace_time_minutes=15,
            half_day_threshold_hours=4.0,
            consecutive_absent_alert_days=3,
        )
        self.assertEqual(rule.minimum_attendance_pct, 75.0)

    def test_attendance_calculation_engine_and_exam_eligibility(self) -> None:
        # 1. 80 out of 100 classes = 80.0% -> Eligible
        res1 = AttendanceCalculationEngine.check_exam_eligibility(100, 80, threshold_pct=75.0)
        self.assertTrue(res1["is_exam_eligible"])
        self.assertEqual(res1["attendance_percentage"], 80.0)
        self.assertEqual(res1["classes_shortfall"], 0)

        # 2. 70 out of 100 classes = 70.0% -> Ineligible with shortfall
        res2 = AttendanceCalculationEngine.check_exam_eligibility(100, 70, threshold_pct=75.0)
        self.assertFalse(res2["is_exam_eligible"])
        self.assertEqual(res2["attendance_percentage"], 70.0)
        self.assertGreater(res2["classes_shortfall"], 0)

    def test_leave_workflow_engine_state_transitions(self) -> None:
        # Valid: PENDING -> APPROVED
        LeaveWorkflowEngine.validate_transition("PENDING", "APPROVED")
        # Valid: PENDING -> REJECTED
        LeaveWorkflowEngine.validate_transition("PENDING", "REJECTED")

        # Invalid: REJECTED -> APPROVED must raise ValidationException
        with self.assertRaises(ValidationException):
            LeaveWorkflowEngine.validate_transition("REJECTED", "APPROVED")

        # Quota verification: 10 used out of 12, requesting 3 (10+3=13 > 12) must fail
        with self.assertRaises(ValidationException):
            LeaveWorkflowEngine.verify_quota_availability(annual_quota=12, used_days=10.0, requested_days=3.0)

        # Quota verification: 5 used out of 12, requesting 2 (5+2=7 <= 12) must pass
        LeaveWorkflowEngine.verify_quota_availability(annual_quota=12, used_days=5.0, requested_days=2.0)

    def test_attendance_validators(self) -> None:
        # Future date validation
        future_date = date.today() + timedelta(days=5)
        with self.assertRaises(ValidationException):
            AttendanceValidators.validate_session_dates(future_date)

        # Duplicate student in session
        dup_student_id = uuid.uuid4()
        dup_records = [
            StudentAttendanceItem(student_id=dup_student_id, status="PRESENT"),
            StudentAttendanceItem(student_id=dup_student_id, status="ABSENT"),
        ]
        with self.assertRaises(ValidationException):
            AttendanceValidators.validate_student_record_uniqueness(dup_records)

        # Inverted leave dates
        with self.assertRaises(ValidationException):
            AttendanceValidators.validate_leave_dates(date(2026, 11, 15), date(2026, 11, 10))

    def test_zero_browser_storage_in_attendance_frontend(self) -> None:
        att_fe_dir = PROJECT_ROOT / "frontend/src/modules/attendance"
        self.assertTrue(att_fe_dir.exists(), "Attendance frontend directory must exist")
        forbidden = [r"\blocalStorage\b", r"\bsessionStorage\b", r"\bindexedDB\b"]

        for ts_file in att_fe_dir.rglob("*.ts*"):
            content = ts_file.read_text(encoding="utf-8")
            for pattern in forbidden:
                matches = re.findall(pattern, content, re.IGNORECASE)
                self.assertEqual(
                    matches,
                    [],
                    f"Forbidden storage API found in {ts_file.name}: {matches}",
                )


if __name__ == "__main__":
    unittest.main()
