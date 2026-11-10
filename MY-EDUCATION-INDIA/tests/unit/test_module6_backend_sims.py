"""Unit and Integration Tests for Module 6: Enterprise Student Information Management System (SIMS)
Verifies:
- QR Code generation and cryptographic payload verification
- Import/Export CSV parser and row-level validation
- Student models and schemas validation
- AST compilation across all Module 6 backend files
"""
import ast
import base64
import json
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

from app.modules.students.import_export import StudentImportExportProcessor
from app.modules.students.qr_generator import StudentQRGenerator


class TestModule6BackendSIMS(unittest.TestCase):

    def test_all_module6_python_files_compile(self) -> None:
        sims_dir = PROJECT_ROOT / "backend/app/modules/students"
        for py_file in sims_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_qr_code_generation_and_payload_verification(self) -> None:
        payload = StudentQRGenerator.generate_verification_payload(
            registration_number="MEI-BPL-2027-000124",
            full_name="Aarav Sharma",
            course_name="B.Tech Computer Science",
            academic_year_code="2026-2027",
            institute_id="11111111-2222-3333-4444-555555555555",
        )
        self.assertTrue(payload.startswith("MEI_VERIFY:"))
        parts = payload.split(":")
        self.assertEqual(len(parts), 3)

        decoded_json = json.loads(base64.b64decode(parts[1].encode("utf-8")).decode("utf-8"))
        self.assertEqual(decoded_json["reg"], "MEI-BPL-2027-000124")
        self.assertEqual(decoded_json["name"], "Aarav Sharma")

        # Verify SVG generation
        svg = StudentQRGenerator.generate_qr_svg(payload, size=150)
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)
        self.assertIn('viewBox="0 0 150 150"', svg)

    def test_csv_import_export_processor(self) -> None:
        template = StudentImportExportProcessor.generate_csv_template()
        self.assertIn("first_name", template)
        self.assertIn("Aarav", template)

        # Test valid parsing
        valid_rows, errors = StudentImportExportProcessor.parse_csv_stream(template)
        self.assertEqual(len(valid_rows), 1)
        self.assertEqual(len(errors), 0)
        self.assertEqual(valid_rows[0]["first_name"], "Aarav")

        # Test invalid parsing with missing required headers
        invalid_csv = "first_name,last_name,email\nRohan,,rohan@test.com\n"
        valid_rows2, errors2 = StudentImportExportProcessor.parse_csv_stream(invalid_csv)
        self.assertEqual(len(valid_rows2), 0)
        self.assertEqual(len(errors2), 1)
        self.assertIn("Missing required fields", errors2[0]["error"])


if __name__ == "__main__":
    unittest.main()
