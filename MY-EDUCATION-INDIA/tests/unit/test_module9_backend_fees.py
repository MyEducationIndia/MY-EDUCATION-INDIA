"""Unit and Integration Tests for Module 9: Enterprise Fee & Finance Management System
Verifies:
- AST compilation across all Module 9 backend files
- Pydantic v2 schemas validation for fee categories, heads, structures, and payments
- Financial business logic validators (date ranges, 100% installments, duplicate items, refund limits)
- Universal receipt generator & Indian numbering currency words converter (Crores, Lakhs, Thousands)
- Zero browser LocalStorage/SessionStorage/IndexedDB in Module 9 frontend source
"""
import ast
from datetime import date
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
from app.modules.fees.receipt_generator import ReceiptGenerator, number_to_indian_currency_words
from app.modules.fees.schemas import (
    DiscountCreate,
    FeeCategoryCreate,
    FeeHeadCreate,
    FeeStructureCreate,
    FeeStructureItemCreate,
    InstallmentPlanInput,
    LateFeeRuleCreate,
    PaymentCreate,
    ScholarshipCreate,
)
from app.modules.fees.validators import FeeBusinessValidators


class TestModule9BackendFees(unittest.TestCase):

    def test_all_module9_python_files_compile(self) -> None:
        fee_dir = PROJECT_ROOT / "backend/app/modules/fees"
        self.assertTrue(fee_dir.exists(), "fees backend directory must exist")
        for py_file in fee_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_fee_schemas_validation(self) -> None:
        dummy_inst_id = uuid.uuid4()
        dummy_cat_id = uuid.uuid4()
        dummy_head_id = uuid.uuid4()

        cat = FeeCategoryCreate(
            code="TUITION",
            name="Tuition & Instruction Fees",
            institute_id=dummy_inst_id,
        )
        self.assertEqual(cat.code, "TUITION")

        head = FeeHeadCreate(
            category_id=dummy_cat_id,
            code="LAB_FEE",
            name="Computer Science Laboratory Fee",
            default_amount=25000.0,
            institute_id=dummy_inst_id,
        )
        self.assertEqual(head.default_amount, 25000.0)

        sch = ScholarshipCreate(
            institute_id=dummy_inst_id,
            code="MERIT_10",
            name="Merit Scholarship",
            calculation_type="PERCENTAGE",
            value=20.0,
        )
        self.assertEqual(sch.value, 20.0)

        rule = LateFeeRuleCreate(
            institute_id=dummy_inst_id,
            code="DAILY_LATE",
            name="Daily Penalty Rule",
            calculation_type="DAILY",
            rate=50.0,
            maximum_limit=2500.0,
            grace_period_days=7,
        )
        self.assertEqual(rule.grace_period_days, 7)

    def test_financial_business_validators(self) -> None:
        # Date range validation
        with self.assertRaises(ValidationException):
            FeeBusinessValidators.validate_structure_dates(date(2027, 1, 1), date(2026, 1, 1))

        # Duplicate fee head validation
        dummy_head = uuid.uuid4()
        items = [
            FeeStructureItemCreate(fee_head_id=dummy_head, amount=5000.0),
            FeeStructureItemCreate(fee_head_id=dummy_head, amount=10000.0),
        ]
        with self.assertRaises(ValidationException):
            FeeBusinessValidators.validate_structure_items(items)

        # Installment percentage sum validation (must equal 100%)
        invalid_installments = [
            InstallmentPlanInput(installment_number=1, title="Q1", due_date=date(2026, 8, 1), percentage=40.0),
            InstallmentPlanInput(installment_number=2, title="Q2", due_date=date(2026, 11, 1), percentage=50.0), # Sum = 90%
        ]
        with self.assertRaises(ValidationException):
            FeeBusinessValidators.validate_installment_percentages(invalid_installments)

        valid_installments = [
            InstallmentPlanInput(installment_number=1, title="Q1", due_date=date(2026, 8, 1), percentage=50.0),
            InstallmentPlanInput(installment_number=2, title="Q2", due_date=date(2026, 11, 1), percentage=50.0),
        ]
        # Should not raise
        FeeBusinessValidators.validate_installment_percentages(valid_installments)

        # Refund limit validation
        with self.assertRaises(ValidationException):
            FeeBusinessValidators.validate_refund_eligibility(
                payment_amount=50000.0,
                requested_refund=30000.0,
                already_refunded=25000.0, # 25000 + 30000 = 55000 > 50000
            )

    def test_indian_currency_number_to_words(self) -> None:
        w1 = number_to_indian_currency_words(145000.0)
        self.assertIn("One Lakh Forty Five Thousand Rupees Only", w1)

        w2 = number_to_indian_currency_words(72500.0)
        self.assertIn("Seventy Two Thousand Five Hundred Rupees Only", w2)

        w3 = number_to_indian_currency_words(25000000.0)
        self.assertIn("Two Crore Fifty Lakh Rupees Only", w3)

        w0 = number_to_indian_currency_words(0.0)
        self.assertEqual(w0, "Zero Rupees Only")

    def test_receipt_generator_identifiers_and_signatures(self) -> None:
        rec_no = ReceiptGenerator.generate_receipt_number("MEI")
        self.assertTrue(rec_no.startswith("REC-MEI-"))

        sig = ReceiptGenerator.generate_digital_signature(rec_no, 50000.0, "student-uuid")
        self.assertEqual(len(sig), 64) # SHA-256 hex string

    def test_zero_browser_storage_in_fees_frontend(self) -> None:
        fee_fe_dir = PROJECT_ROOT / "frontend/src/modules/fees"
        self.assertTrue(fee_fe_dir.exists(), "Fees frontend directory must exist")
        forbidden = [r"\blocalStorage\b", r"\bsessionStorage\b", r"\bindexedDB\b"]

        for ts_file in fee_fe_dir.rglob("*.ts*"):
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
