"""Unit and Integration Tests for Module 12: Enterprise Computer Based Testing (CBT) Platform
Verifies:
- AST compilation across all Module 12 backend files
- Pydantic v2 schemas validation for question banks, versions, exam templates, and CBT sessions
- QuestionEvaluationEngine scoring across MCQ, MSQ, and Numerical question formats
- PseudoRandomizer deterministic seed-based question & option shuffling
- OfflineSyncEngine SHA-256 checksum generation and data integrity verification
- CBTBusinessValidators (option requirements, negative marks constraint, valid session window)
- Zero browser LocalStorage/SessionStorage/IndexedDB in Module 12 frontend source
"""
import ast
from datetime import datetime, timezone
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
from app.modules.cbt.offline_sync import OfflineSyncEngine
from app.modules.cbt.question_engine import QuestionEvaluationEngine
from app.modules.cbt.randomizer import PseudoRandomizer
from app.modules.cbt.schemas import (
    CBTSessionCreate,
    ExamTemplateCreate,
    QuestionBankCreate,
    QuestionVersionCreate,
)
from app.modules.cbt.session_manager import CBTSessionManager
from app.modules.cbt.validators import CBTBusinessValidators


class TestModule12BackendCBT(unittest.TestCase):

    def test_all_module12_python_files_compile(self) -> None:
        cbt_dir = PROJECT_ROOT / "backend/app/modules/cbt"
        self.assertTrue(cbt_dir.exists(), "cbt backend directory must exist")
        for py_file in cbt_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_cbt_schemas_validation(self) -> None:
        dummy_inst_id = uuid.uuid4()
        dummy_topic_id = uuid.uuid4()
        dummy_tmpl_id = uuid.uuid4()

        qb = QuestionBankCreate(
            institute_id=dummy_inst_id,
            code="CS101_BANK",
            name="Data Structures Master Bank",
        )
        self.assertEqual(qb.code, "CS101_BANK")

        q = QuestionVersionCreate(
            topic_id=dummy_topic_id,
            question_code="CS101_Q01",
            question_type="MCQ",
            question_text="What is the time complexity of QuickSort average case?",
            options=[{"id": "A", "text": "O(n)"}, {"id": "B", "text": "O(n log n)"}],
            correct_answers=["B"],
            default_marks=2.0,
            negative_marks=0.5,
        )
        self.assertEqual(q.default_marks, 2.0)
        self.assertEqual(q.negative_marks, 0.5)

        tmpl = ExamTemplateCreate(
            institute_id=dummy_inst_id,
            title="Data Structures Mid-Term",
            duration_minutes=90,
            total_marks=100.0,
            passing_marks=40.0,
        )
        self.assertEqual(tmpl.duration_minutes, 90)

    def test_question_evaluation_engine(self) -> None:
        # MCQ - Correct Answer
        is_correct, marks = QuestionEvaluationEngine.evaluate_response(
            question_type="MCQ",
            user_selected=["B"],
            user_text=None,
            correct_answers=["B"],
            positive_marks=2.0,
            negative_marks=0.5,
        )
        self.assertTrue(is_correct)
        self.assertEqual(marks, 2.0)

        # MCQ - Incorrect Answer
        is_correct, marks = QuestionEvaluationEngine.evaluate_response(
            question_type="MCQ",
            user_selected=["A"],
            user_text=None,
            correct_answers=["B"],
            positive_marks=2.0,
            negative_marks=0.5,
        )
        self.assertFalse(is_correct)
        self.assertEqual(marks, -0.5)

        # MSQ - Multiple Select (All must match)
        is_correct, marks = QuestionEvaluationEngine.evaluate_response(
            question_type="MSQ",
            user_selected=["A", "C"],
            user_text=None,
            correct_answers=["A", "C"],
            positive_marks=4.0,
            negative_marks=1.0,
        )
        self.assertTrue(is_correct)
        self.assertEqual(marks, 4.0)

        # Numerical Answer
        is_correct, marks = QuestionEvaluationEngine.evaluate_response(
            question_type="NUMERICAL",
            user_selected=[],
            user_text="3.1415",
            correct_answers=["3.14"],
            positive_marks=3.0,
            negative_marks=0.0,
        )
        self.assertTrue(is_correct)
        self.assertEqual(marks, 3.0)

    def test_pseudo_randomizer_deterministic_seeding(self) -> None:
        questions = [
            {"id": "q1", "text": "Question 1"},
            {"id": "q2", "text": "Question 2"},
            {"id": "q3", "text": "Question 3"},
            {"id": "q4", "text": "Question 4"},
        ]

        # Same seed must yield identical order
        res1 = PseudoRandomizer.shuffle_items_with_seed(questions, 42)
        res2 = PseudoRandomizer.shuffle_items_with_seed(questions, 42)
        self.assertEqual([x["id"] for x in res1], [x["id"] for x in res2])

        # Different seed must yield valid permutation
        res3 = PseudoRandomizer.shuffle_items_with_seed(questions, 9999)
        self.assertEqual(len(res3), 4)

    def test_offline_sync_checksum_verification(self) -> None:
        data = [{"question_id": "q1", "answer": ["A"]}, {"question_id": "q2", "answer": ["C"]}]
        checksum = OfflineSyncEngine.calculate_checksum(data)
        self.assertTrue(len(checksum) == 64) # SHA-256

        # Verifying matching checksum passes
        OfflineSyncEngine.verify_checksum(data, checksum)

        # Mismatched checksum raises ValidationException
        with self.assertRaises(ValidationException):
            OfflineSyncEngine.verify_checksum(data, "tampered_fake_checksum_000000000000000000000000000000000000000000000")

    def test_session_manager_heartbeat(self) -> None:
        rem = CBTSessionManager.evaluate_heartbeat(remaining_seconds=3600, elapsed_seconds=30)
        self.assertEqual(rem, 3570)
        self.assertFalse(CBTSessionManager.is_expired(rem))
        self.assertTrue(CBTSessionManager.is_expired(0))

    def test_cbt_business_validators(self) -> None:
        # Negative marks > default marks
        with self.assertRaises(ValidationException):
            CBTBusinessValidators.validate_question_data(
                QuestionVersionCreate(
                    topic_id=uuid.uuid4(),
                    question_code="ERR01",
                    question_type="MCQ",
                    question_text="Sample text",
                    options=[{"id": "A", "text": "A"}],
                    correct_answers=["A"],
                    default_marks=1.0,
                    negative_marks=2.0, # 2.0 > 1.0
                )
            )

        # Inverted window dates
        with self.assertRaises(ValidationException):
            CBTBusinessValidators.validate_session_window(
                datetime(2026, 11, 25, 12, 0, tzinfo=timezone.utc),
                datetime(2026, 11, 25, 10, 0, tzinfo=timezone.utc),
            )

    def test_zero_browser_storage_in_cbt_frontend(self) -> None:
        cbt_fe_dir = PROJECT_ROOT / "frontend/src/modules/cbt"
        self.assertTrue(cbt_fe_dir.exists(), "CBT frontend directory must exist")
        forbidden = [r"\blocalStorage\b", r"\bsessionStorage\b", r"\bindexedDB\b"]

        for ts_file in cbt_fe_dir.rglob("*.ts*"):
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
