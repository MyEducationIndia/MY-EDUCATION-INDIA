import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import unittest
import os
import ast
import re
from datetime import datetime, timedelta

from app.modules.library.schemas import (
    LibraryCategoryCreate,
    LibraryBookCreate,
    LibraryMemberCreate,
    BookIssueRequest
)
from app.modules.library.validators import LibraryBusinessValidators
from app.modules.library.issue_engine import CirculationEngine
from app.modules.library.fine_engine import LibraryFineEngine
from app.modules.library.barcode_generator import generate_accession_barcode
from app.modules.library.qr_generator import generate_book_copy_qr_payload

class TestModule14LibraryBackend(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.lib_backend_dir = os.path.join(self.base_dir, "backend/app/modules/library")
        self.lib_frontend_dir = os.path.join(self.base_dir, "frontend/src/modules/library")

    def test_library_models_and_modules_ast(self):
        """Verify all Module 14 Python source files compile cleanly without syntax errors."""
        self.assertTrue(os.path.exists(self.lib_backend_dir), "Library backend directory missing")
        py_files = [f for f in os.listdir(self.lib_backend_dir) if f.endswith(".py")]
        self.assertGreaterEqual(len(py_files), 12, "Expected at least 12 Python files in library module")
        for py_file in py_files:
            file_path = os.path.join(self.lib_backend_dir, py_file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                ast.parse(content, filename=py_file)
            except SyntaxError as e:
                self.fail(f"SyntaxError in {py_file}: {e}")

    def test_library_schemas(self):
        """Test Pydantic schemas for book and category creation."""
        cat_data = LibraryCategoryCreate(
            code="CS-ENG",
            name="Computer Science & Engineering",
            description="Core engineering books",
            is_active=True
        )
        self.assertEqual(cat_data.code, "CS-ENG")

        book_data = LibraryBookCreate(
            isbn="978-0131103627",
            title="The C Programming Language",
            author_name="Brian W. Kernighan",
            category_id="cat_123",
            initial_copies_count=5,
            purchase_price_per_copy=450.0
        )
        self.assertEqual(book_data.initial_copies_count, 5)
        self.assertEqual(book_data.purchase_price_per_copy, 450.0)

    def test_library_business_validators(self):
        """Test ISBN-10, ISBN-13 formats and borrow limits."""
        # Valid ISBN-10
        self.assertTrue(LibraryBusinessValidators.validate_isbn("0-13-110362-8"))
        # Valid ISBN-13
        self.assertTrue(LibraryBusinessValidators.validate_isbn("978-0-13-110362-7"))
        # Invalid ISBN
        self.assertFalse(LibraryBusinessValidators.validate_isbn("12345"))
        self.assertFalse(LibraryBusinessValidators.validate_isbn("978-0-13-110362-9"))

        # Member borrow limit eligibility
        self.assertTrue(LibraryBusinessValidators.validate_member_borrow_limit(2, 3))
        self.assertFalse(LibraryBusinessValidators.validate_member_borrow_limit(3, 3))

        # Fine threshold eligibility (max limit INR 200)
        self.assertTrue(LibraryBusinessValidators.validate_overdue_fine_eligibility(50.0, 200.0))
        self.assertFalse(LibraryBusinessValidators.validate_overdue_fine_eligibility(250.0, 200.0))

    def test_circulation_engine(self):
        """Test loan period calculation and renewal thresholds."""
        now = datetime(2026, 11, 1, 10, 0, 0)
        due = CirculationEngine.calculate_due_date(now, 14)
        self.assertEqual(due, datetime(2026, 11, 15, 10, 0, 0))

        # Renewals eligibility
        self.assertTrue(CirculationEngine.can_renew(0, 2))
        self.assertTrue(CirculationEngine.can_renew(1, 2))
        self.assertFalse(CirculationEngine.can_renew(2, 2))

    def test_fine_engine(self):
        """Test overdue fine calculations with grace period and maximum cap."""
        due_date = datetime(2026, 11, 1, 10, 0, 0)

        # On-time return
        on_time = LibraryFineEngine.calculate_overdue_fine(due_date, datetime(2026, 11, 1, 9, 0, 0))
        self.assertEqual(on_time["fine_amount"], 0.0)

        # Within 1-day grace period
        within_grace = LibraryFineEngine.calculate_overdue_fine(due_date, datetime(2026, 11, 2, 10, 0, 0), grace_days=1)
        self.assertEqual(within_grace["fine_amount"], 0.0)

        # Overdue past grace period (5 days diff, 1 grace day = 4 billable days @ 5 INR/day = 20 INR)
        overdue = LibraryFineEngine.calculate_overdue_fine(due_date, datetime(2026, 11, 6, 10, 0, 0), daily_rate=5.0, grace_days=1)
        self.assertEqual(overdue["overdue_days"], 5)
        self.assertEqual(overdue["billable_days"], 4)
        self.assertEqual(overdue["fine_amount"], 20.0)

        # Excessive overdue capping at max_fine (e.g. 200 days overdue capped at 500 INR)
        capped = LibraryFineEngine.calculate_overdue_fine(due_date, datetime(2027, 6, 1, 10, 0, 0), daily_rate=5.0, max_fine=500.0)
        self.assertEqual(capped["fine_amount"], 500.0)

    def test_generators(self):
        """Test accession barcode and QR payload generation."""
        barcode = generate_accession_barcode("inst_001", 42)
        self.assertTrue(barcode.startswith("ACC-"))
        self.assertTrue(barcode.endswith("000042"))

        qr_payload = generate_book_copy_qr_payload("ACC-001-000042", "The C Programming Language", "978-0131103627")
        self.assertIn("ACC-001-000042", qr_payload)
        self.assertIn("LIBRARY_BOOK_COPY", qr_payload)

    def test_zero_browser_storage_library(self):
        """Strictly enforce zero usage of localStorage, sessionStorage, or indexedDB in frontend."""
        storage_pattern = re.compile(r'\b(localStorage|sessionStorage|indexedDB)\b')
        violations = []
        for root, _, files in os.walk(self.lib_frontend_dir):
            for file in files:
                if file.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        for line_idx, line in enumerate(f, 1):
                            if storage_pattern.search(line):
                                violations.append(f"{file}:{line_idx}")
        self.assertEqual(violations, [], f"Found forbidden browser storage usage: {violations}")

if __name__ == "__main__":
    unittest.main()
