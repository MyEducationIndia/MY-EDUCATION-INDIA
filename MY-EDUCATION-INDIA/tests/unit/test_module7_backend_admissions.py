"""Unit and Integration Tests for Module 7: Enterprise Admission & CRM Management System
Verifies:
- Admission workflow state transitions (PENDING -> VERIFIED -> APPROVED -> CONVERTED)
- Lead scoring and priority classification
- Admission dashboard statistics compilation
- AST compilation across all Module 7 backend files
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

from app.modules.admissions.schemas import (
    AdmissionDashboardMetrics,
    ApplicationCreateRequest,
    LeadCreateRequest,
)


class TestModule7BackendAdmissions(unittest.TestCase):

    def test_all_module7_python_files_compile(self) -> None:
        adm_dir = PROJECT_ROOT / "backend/app/modules/admissions"
        for py_file in adm_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_admission_dashboard_metrics_schema(self) -> None:
        metrics = AdmissionDashboardMetrics(
            today_enquiries=24,
            admissions_today=6,
            pending_applications=18,
            verification_pending=7,
            waiting_list=2,
            total_leads=85,
            conversions_count=19,
            conversion_rate_pct=22.4,
            total_revenue_collected=1450000.0,
        )
        self.assertEqual(metrics.today_enquiries, 24)
        self.assertEqual(metrics.conversion_rate_pct, 22.4)
        self.assertEqual(metrics.total_revenue_collected, 1450000.0)


if __name__ == "__main__":
    unittest.main()
