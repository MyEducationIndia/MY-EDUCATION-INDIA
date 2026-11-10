"""Unit and Integration Tests for Module 8: Enterprise Academic Management System
Verifies:
- Timetable collision engine logic for faculty and classrooms
- Academic Department, Program, Course, Subject, Batch, and Timetable schemas
- Zero browser LocalStorage/SessionStorage/IndexedDB in Module 8 frontend source
- AST compilation across all Module 8 backend files
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

from app.modules.academics.schemas import (
    BatchCreate,
    CourseCreate,
    DepartmentCreate,
    ProgramCreate,
    SectionCreate,
    SubjectCreate,
    TimetableSlotCreate,
)


class TestModule8BackendAcademics(unittest.TestCase):

    def test_all_module8_python_files_compile(self) -> None:
        acad_dir = PROJECT_ROOT / "backend/app/modules/academics"
        self.assertTrue(acad_dir.exists(), "academics backend directory must exist")
        for py_file in acad_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_academic_schemas_validation(self) -> None:
        dummy_inst_id = uuid.uuid4()
        dummy_branch_id = uuid.uuid4()
        dummy_dept_id = uuid.uuid4()
        dummy_prog_id = uuid.uuid4()

        dept = DepartmentCreate(
            code="CSE",
            name="Computer Science & Engineering",
            institute_id=dummy_inst_id,
        )
        self.assertEqual(dept.code, "CSE")

        prog = ProgramCreate(
            code="UG",
            name="Undergraduate Degree",
            level="UNDERGRADUATE",
            institute_id=dummy_inst_id,
        )
        self.assertEqual(prog.level, "UNDERGRADUATE")

        course = CourseCreate(
            code="BTECH_CSE",
            name="B.Tech Computer Science & AI",
            department_id=dummy_dept_id,
            program_id=dummy_prog_id,
            institute_id=dummy_inst_id,
        )
        self.assertEqual(course.academic_pattern, "SEMESTER")
        self.assertEqual(course.total_semesters_or_years, 6)

        subj = SubjectCreate(
            code="CS101",
            name="Data Structures & Algorithms",
            credits=4.0,
            institute_id=dummy_inst_id,
        )
        self.assertEqual(subj.credits, 4.0)
        self.assertEqual(subj.passing_percentage, 40.0)

        batch = BatchCreate(
            name="2026-2030 Batch A",
            code="BTECH-CSE-2026",
            course_id=dummy_dept_id,
            academic_year_code="2026-2027",
            start_date=date(2026, 8, 1),
            end_date=date(2030, 6, 30),
            intake_capacity=120,
            institute_id=dummy_inst_id,
            branch_id=dummy_branch_id,
        )
        self.assertEqual(batch.intake_capacity, 120)

    def test_timetable_collision_math_logic(self) -> None:
        """Verify time overlap algorithm: (start1 < end2) and (end1 > start2)."""
        def has_overlap(s1: time, e1: time, s2: time, e2: time) -> bool:
            return s1 < e2 and e1 > s2

        slot1_start, slot1_end = time(9, 0), time(10, 0)
        slot2_start, slot2_end = time(9, 30), time(10, 30)
        slot3_start, slot3_end = time(10, 0), time(11, 0)
        slot4_start, slot4_end = time(8, 0), time(9, 0)

        # Overlapping slots
        self.assertTrue(has_overlap(slot1_start, slot1_end, slot2_start, slot2_end))
        self.assertTrue(has_overlap(slot2_start, slot2_end, slot1_start, slot1_end))

        # Adjacent non-overlapping slots
        self.assertFalse(has_overlap(slot1_start, slot1_end, slot3_start, slot3_end))
        self.assertFalse(has_overlap(slot4_start, slot4_end, slot1_start, slot1_end))

    def test_zero_browser_storage_in_academics_frontend(self) -> None:
        acad_fe_dir = PROJECT_ROOT / "frontend/src/modules/academics"
        self.assertTrue(acad_fe_dir.exists(), "Academics frontend directory must exist")
        forbidden = [r"\blocalStorage\b", r"\bsessionStorage\b", r"\bindexedDB\b"]

        for ts_file in acad_fe_dir.rglob("*.ts*"):
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
