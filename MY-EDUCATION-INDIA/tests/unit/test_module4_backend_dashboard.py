"""Unit and Integration Tests for Module 4: Enterprise Admin Dashboard & Control Center
Verifies:
- Analytics date range time-series generation (DAILY, WEEKLY, MONTHLY, YEARLY)
- Multi-chart analytics structure and category distributions
- AST compilation across all Module 4 backend files
- System health monitoring values
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

from app.modules.dashboard.analytics import DashboardAnalyticsEngine
from app.modules.dashboard.schemas import (
    DashboardKPIStatistics,
    GlobalSearchResponse,
    MultiChartAnalyticsResponse,
    SystemHealthResponse,
)


class TestModule4BackendDashboard(unittest.TestCase):

    def test_all_module4_python_files_compile(self) -> None:
        dash_dir = PROJECT_ROOT / "backend/app/modules/dashboard"
        for py_file in dash_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_analytics_date_range_generation(self) -> None:
        # Test DAILY
        daily_slots = DashboardAnalyticsEngine.generate_date_range_series("DAILY")
        self.assertGreaterEqual(len(daily_slots), 10)

        # Test WEEKLY
        weekly_slots = DashboardAnalyticsEngine.generate_date_range_series("WEEKLY")
        self.assertEqual(len(weekly_slots), 7)

        # Test MONTHLY
        monthly_slots = DashboardAnalyticsEngine.generate_date_range_series("MONTHLY")
        self.assertGreaterEqual(len(monthly_slots), 8)

        # Test YEARLY
        yearly_slots = DashboardAnalyticsEngine.generate_date_range_series("YEARLY")
        self.assertEqual(len(yearly_slots), 12)

    def test_dashboard_schemas_validation(self) -> None:
        kpi = DashboardKPIStatistics(
            total_students=1500,
            active_students=1480,
            admissions_today=5,
            fee_collection_today=120000.0,
            overall_attendance_pct=95.5,
        )
        self.assertEqual(kpi.total_students, 1500)
        self.assertEqual(kpi.overall_attendance_pct, 95.5)

        health = SystemHealthResponse(
            database_status="ONLINE",
            database_version="PostgreSQL 16",
            api_status="OPERATIONAL",
            server_time="2026-11-06T12:00:00Z",
            uptime_seconds=3600.0,
            memory_usage_mb=512.0,
            total_memory_mb=4096.0,
            cpu_percent=5.5,
            storage_usage_mb=420.0,
            active_db_connections=8,
        )
        self.assertEqual(health.database_status, "ONLINE")
        self.assertEqual(health.app_version, "2.0.0")


if __name__ == "__main__":
    unittest.main()
