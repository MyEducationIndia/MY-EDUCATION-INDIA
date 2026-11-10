"""Unit and Integration Tests for Module 3: Core System Engine
Verifies:
- Number Generator Token Rendering ({PREFIX}-{YEAR}-{NUMBER}, custom separators, padding)
- Template validation rules ({NUMBER} presence, permitted tokens)
- Academic Year and Financial Year date range validations
- AST compilation across all Module 3 backend files
"""
import ast
import os
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

os.environ.setdefault("SECRET_KEY", "test_secret_key_minimum_32_characters_long_for_security")
os.environ.setdefault("REFRESH_SECRET_KEY", "test_refresh_secret_key_minimum_32_characters_long")
os.environ.setdefault("CSRF_SECRET_KEY", "test_csrf_secret_key_minimum_32_characters_long_sec")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("SYNC_DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")

from app.modules.system.number_generator import UniversalNumberGeneratorService
from app.modules.system.settings import SETTING_CATEGORIES
from app.modules.system.validators import validate_date_range, validate_format_template
from datetime import date


class TestModule3BackendCoreSystem(unittest.TestCase):

    def test_all_module3_python_files_compile(self) -> None:
        sys_dir = PROJECT_ROOT / "backend/app/modules/system"
        for py_file in sys_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_number_generator_preview_rendering(self) -> None:
        preview = UniversalNumberGeneratorService.render_preview(
            format_template="{PREFIX}-{BRANCH}-{YEAR}-{NUMBER}",
            prefix="MEI",
            separator="-",
            padding_length=6,
            sample_number=123,
            institute_code="MEI",
            branch_code="BPL",
            year=2027,
        )
        self.assertEqual(preview, "MEI-BPL-2027-000123")

        # Test complex department/course numbering
        preview_complex = UniversalNumberGeneratorService.render_preview(
            format_template="{PREFIX}/{BRANCH}/{DEPT}/{YEAR}/{NUMBER}/{SUFFIX}",
            prefix="MEI",
            suffix="REG",
            separator="/",
            padding_length=4,
            sample_number=45,
            branch_code="IND",
            dept_code="CSE",
            year=2026,
        )
        self.assertEqual(preview_complex, "MEI/IND/CSE/2026/0045/REG")

    def test_number_generator_template_validation(self) -> None:
        # Valid template
        validate_format_template("{PREFIX}-{YEAR}-{NUMBER}")

        # Missing {NUMBER} must fail
        with self.assertRaises(ValueError):
            validate_format_template("{PREFIX}-{YEAR}")

        # Disallowed token must fail
        with self.assertRaises(ValueError):
            validate_format_template("{PREFIX}-{INVALID_TOKEN}-{NUMBER}")

    def test_date_range_validation(self) -> None:
        # Valid range
        validate_date_range(date(2026, 4, 1), date(2027, 3, 31))

        # Reversed range must fail
        with self.assertRaises(ValueError):
            validate_date_range(date(2027, 4, 1), date(2026, 3, 31))

        # Identical dates must fail
        with self.assertRaises(ValueError):
            validate_date_range(date(2026, 4, 1), date(2026, 4, 1))

    def test_setting_categories_coverage(self) -> None:
        self.assertGreaterEqual(len(SETTING_CATEGORIES), 20)
        expected = {
            "general", "institute", "authentication", "communication", "website",
            "appearance", "security", "backup", "academic", "financial",
            "examination", "certificates", "attendance", "fees", "admissions",
            "library", "hostel", "transport", "inventory", "lms", "api", "developer"
        }
        self.assertTrue(expected.issubset(set(SETTING_CATEGORIES)))


if __name__ == "__main__":
    unittest.main()
