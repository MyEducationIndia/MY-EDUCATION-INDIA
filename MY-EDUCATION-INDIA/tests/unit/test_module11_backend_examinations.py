"""Unit and Integration Tests for Module 11: Enterprise Examination & Result Management System
Verifies:
- AST compilation across all Module 11 backend files
- Pydantic v2 schemas validation for exam types, sessions, schedules, mark batches
- UGC/AICTE CBCS & NEP 10-Point Letter Grading Engine (O, A+, A, B+, B, C, P, F) & Division classifications
- ResultCalculationEngine (SGPA, CGPA, Earned Credits, Backlog counts, Pass/Fail status)
- Hall Ticket & Transcript generation with QR payloads and cryptographic signature hashes
- Zero browser LocalStorage/SessionStorage/IndexedDB in Module 11 frontend source
"""
import ast
from datetime import date, time
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
from app.modules.examinations.grading_engine import UGCGradingEngine
from app.modules.examinations.hall_ticket_generator import HallTicketGenerator
from app.modules.examinations.result_engine import ResultCalculationEngine
from app.modules.examinations.schemas import (
    ExamScheduleCreate,
    ExamSessionCreate,
    ExamSubjectItemCreate,
    ExamTypeCreate,
    StudentMarkItem,
)
from app.modules.examinations.transcript_generator import TranscriptGenerator
from app.modules.examinations.validators import ExamBusinessValidators


class TestModule11BackendExaminations(unittest.TestCase):

    def test_all_module11_python_files_compile(self) -> None:
        exam_dir = PROJECT_ROOT / "backend/app/modules/examinations"
        self.assertTrue(exam_dir.exists(), "examinations backend directory must exist")
        for py_file in exam_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_exam_schemas_validation(self) -> None:
        dummy_inst_id = uuid.uuid4()
        dummy_ay_id = uuid.uuid4()
        dummy_course_id = uuid.uuid4()
        dummy_session_id = uuid.uuid4()
        dummy_sub_id = uuid.uuid4()
        dummy_type_id = uuid.uuid4()

        et = ExamTypeCreate(
            institute_id=dummy_inst_id,
            code="SEMESTER_MAIN",
            name="Semester End Examination",
            category="EXTERNAL",
            default_weightage_pct=70.0,
        )
        self.assertEqual(et.code, "SEMESTER_MAIN")
        self.assertEqual(et.default_weightage_pct, 70.0)

        sess = ExamSessionCreate(
            institute_id=dummy_inst_id,
            academic_year_id=dummy_ay_id,
            code="NOV-DEC-2026-MAIN",
            name="Winter Semester 2026 Examination",
            start_date=date(2026, 11, 20),
            end_date=date(2026, 12, 10),
            min_attendance_threshold_pct=75.0,
            requires_fee_clearance=True,
        )
        self.assertEqual(sess.min_attendance_threshold_pct, 75.0)

        sched = ExamScheduleCreate(
            exam_session_id=dummy_session_id,
            course_id=dummy_course_id,
            exam_date=date(2026, 11, 20),
            start_time=time(10, 0),
            end_time=time(13, 0),
            subjects=[
                ExamSubjectItemCreate(
                    subject_id=dummy_sub_id,
                    exam_type_id=dummy_type_id,
                    max_marks=100.0,
                    pass_marks=40.0,
                    credits=4.0,
                    weightage_internal_pct=30.0,
                    weightage_external_pct=70.0,
                )
            ],
        )
        self.assertEqual(len(sched.subjects), 1)

    def test_ugc_grading_engine(self) -> None:
        # Check standard percentages
        self.assertEqual(UGCGradingEngine.percentage_to_grade(95.0)[0], "O")
        self.assertEqual(UGCGradingEngine.percentage_to_grade(85.0)[0], "A+")
        self.assertEqual(UGCGradingEngine.percentage_to_grade(75.0)[0], "A")
        self.assertEqual(UGCGradingEngine.percentage_to_grade(65.0)[0], "B+")
        self.assertEqual(UGCGradingEngine.percentage_to_grade(57.0)[0], "B")
        self.assertEqual(UGCGradingEngine.percentage_to_grade(52.0)[0], "C")
        self.assertEqual(UGCGradingEngine.percentage_to_grade(45.0)[0], "P")
        self.assertEqual(UGCGradingEngine.percentage_to_grade(35.0)[0], "F")
        self.assertFalse(UGCGradingEngine.percentage_to_grade(35.0)[3]) # is_passing is False

        # Division classification
        self.assertEqual(UGCGradingEngine.get_division(9.2), "FIRST_CLASS_WITH_DISTINCTION")
        self.assertEqual(UGCGradingEngine.get_division(7.5), "FIRST_CLASS")
        self.assertEqual(UGCGradingEngine.get_division(5.8), "SECOND_CLASS")
        self.assertEqual(UGCGradingEngine.get_division(3.2), "FAILED")

    def test_result_calculation_engine_sgpa(self) -> None:
        # 3 subjects:
        # 1. CS101: 4 credits, 85 marks (A+ = 9.0) -> 36 points
        # 2. CS102: 4 credits, 75 marks (A = 8.0) -> 32 points
        # 3. CS103: 2 credits, 95 marks (O = 10.0) -> 20 points
        # Total credits = 10. Total points = 88. SGPA = 8.80
        records = [
            {"credits": 4.0, "max_marks": 100.0, "total_marks_obtained": 85.0, "is_absent": False},
            {"credits": 4.0, "max_marks": 100.0, "total_marks_obtained": 75.0, "is_absent": False},
            {"credits": 2.0, "max_marks": 100.0, "total_marks_obtained": 95.0, "is_absent": False},
        ]
        res = ResultCalculationEngine.compute_sgpa(records)
        self.assertEqual(res["total_credits_registered"], 10.0)
        self.assertEqual(res["total_credits_earned"], 10.0)
        self.assertEqual(res["sgpa"], 8.8)
        self.assertEqual(res["status"], "PASSED")
        self.assertEqual(res["backlog_count"], 0)

        # In case of failure:
        fail_records = [
            {"credits": 4.0, "max_marks": 100.0, "total_marks_obtained": 85.0, "is_absent": False},
            {"credits": 4.0, "max_marks": 100.0, "total_marks_obtained": 30.0, "is_absent": False}, # Failed
        ]
        fail_res = ResultCalculationEngine.compute_sgpa(fail_records)
        self.assertEqual(fail_res["backlog_count"], 1)
        self.assertEqual(fail_res["status"], "PROMOTED_WITH_BACKLOG")

    def test_exam_business_validators(self) -> None:
        # Inverted session dates
        with self.assertRaises(ValidationException):
            ExamBusinessValidators.validate_session_dates(date(2026, 12, 1), date(2026, 11, 1))

        # Weightages not equal to 100%
        invalid_item = ExamSubjectItemCreate(
            subject_id=uuid.uuid4(),
            exam_type_id=uuid.uuid4(),
            weightage_internal_pct=40.0,
            weightage_external_pct=40.0, # Sum = 80% != 100%
        )
        with self.assertRaises(ValidationException):
            ExamBusinessValidators.validate_subject_weightages(invalid_item)

        # Marks exceed maximum
        mark_item = StudentMarkItem(
            student_id=uuid.uuid4(),
            internal_marks=25.0,
            external_marks=80.0, # 25 + 80 = 105 > 100
        )
        with self.assertRaises(ValidationException):
            ExamBusinessValidators.validate_marks_within_limits(mark_item, max_marks=100.0)

    def test_hall_ticket_and_transcript_generators(self) -> None:
        ht_no = HallTicketGenerator.generate_hall_ticket_number("NOV2026", "MEI-CS-0042")
        self.assertTrue(ht_no.startswith("HT-NOV2026-MEICS0042"))

        qr_payload = HallTicketGenerator.generate_qr_payload(ht_no, "student-id", "session-id")
        self.assertIn("OFFICIAL_EXAM_HALL_TICKET", qr_payload)

        trn_no = TranscriptGenerator.generate_transcript_number("MEI")
        self.assertTrue(trn_no.startswith("TRN-MEI-"))

        sig = TranscriptGenerator.sign_transcript(trn_no, "student-id", 9.45)
        self.assertEqual(len(sig), 64)

    def test_zero_browser_storage_in_examinations_frontend(self) -> None:
        exam_fe_dir = PROJECT_ROOT / "frontend/src/modules/examinations"
        self.assertTrue(exam_fe_dir.exists(), "Examinations frontend directory must exist")
        forbidden = [r"\blocalStorage\b", r"\bsessionStorage\b", r"\bindexedDB\b"]

        for ts_file in exam_fe_dir.rglob("*.ts*"):
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
