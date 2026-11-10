import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import ast
import re

from app.modules.bi.schemas import (
    ReportDefinitionCreate,
    ReportScheduleCreate,
    KpiDefinitionCreate,
    ChartDefinitionCreate
)
from app.modules.bi.validators import BiBusinessValidators
from app.modules.bi.report_engine import UniversalReportQueryEngine
from app.modules.bi.analytics_engine import PredictiveAnalyticsEngine
from app.modules.bi.chart_engine import EChartsOptionBuilder
from app.modules.bi.export_engine import DataExportEngine
from app.modules.bi.kpi_engine import KpiEvaluationEngine
from app.modules.bi.system_health import SystemHealthMonitor

class TestModule18BIBackend(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.bi_backend_dir = os.path.join(self.base_dir, "backend/app/modules/bi")
        self.bi_frontend_dir = os.path.join(self.base_dir, "frontend/src/modules/bi")

    def test_bi_models_and_modules_ast(self):
        """Verify all Module 18 Python source files compile cleanly without syntax errors."""
        self.assertTrue(os.path.exists(self.bi_backend_dir), "BI backend directory missing")
        py_files = [f for f in os.listdir(self.bi_backend_dir) if f.endswith(".py")]
        self.assertGreaterEqual(len(py_files), 12, "Expected at least 12 Python files in BI module")
        for py_file in py_files:
            file_path = os.path.join(self.bi_backend_dir, py_file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                ast.parse(content, filename=py_file)
            except SyntaxError as e:
                self.fail(f"SyntaxError in {py_file}: {e}")

    def test_bi_schemas(self):
        """Test Pydantic schemas for report definitions, schedules, KPIs, and charts."""
        rep = ReportDefinitionCreate(
            report_code="REP-FIN-01",
            report_name="Fee Aging Register",
            category="FINANCIAL",
            source_tables=["fees_receipts", "students"],
            selected_fields=[{"table": "fees_receipts", "field": "amount_paid"}]
        )
        self.assertEqual(rep.report_code, "REP-FIN-01")

        kpi = KpiDefinitionCreate(
            kpi_key="FEE_COLLECTION_PCT",
            kpi_name="Fee Collection Rate",
            category="FINANCIAL",
            calculation_formula="collected / total * 100",
            target_value=90.0,
            warning_threshold=80.0,
            critical_threshold=70.0,
            unit="%"
        )
        self.assertEqual(kpi.target_value, 90.0)

        chart = ChartDefinitionCreate(
            chart_name="Intake Trends 2026",
            chart_type="BAR",
            config_options_json={"title": "Intake"}
        )
        self.assertEqual(chart.chart_type, "BAR")

    def test_bi_business_validators(self):
        """Test chart types, export formats, and cron format validators."""
        self.assertTrue(BiBusinessValidators.validate_chart_type("BAR"))
        self.assertTrue(BiBusinessValidators.validate_chart_type("HEATMAP"))
        self.assertTrue(BiBusinessValidators.validate_chart_type("RADAR"))
        self.assertFalse(BiBusinessValidators.validate_chart_type("INVALID_CHART"))

        self.assertTrue(BiBusinessValidators.validate_export_format("PDF"))
        self.assertTrue(BiBusinessValidators.validate_export_format("EXCEL"))
        self.assertTrue(BiBusinessValidators.validate_export_format("CSV"))
        self.assertFalse(BiBusinessValidators.validate_export_format("EXE"))

        self.assertTrue(BiBusinessValidators.validate_cron_format("0 8 * * 1")) # Every Monday at 8 AM
        self.assertFalse(BiBusinessValidators.validate_cron_format("invalid cron"))

    def test_report_engine(self):
        """Test in-memory filtering and field aggregation in UniversalReportQueryEngine."""
        records = [
            {"department": "CSE", "fee_amount": 50000, "status": "CONFIRMED"},
            {"department": "ECE", "fee_amount": 45000, "status": "CONFIRMED"},
            {"department": "CSE", "fee_amount": 55000, "status": "PENDING"}
        ]
        filtered = UniversalReportQueryEngine.apply_in_memory_filters(
            records, [{"field": "status", "op": "==", "value": "CONFIRMED"}]
        )
        self.assertEqual(len(filtered), 2)

        total_fee = UniversalReportQueryEngine.aggregate_field(records, "fee_amount", "SUM")
        self.assertEqual(total_fee, 150000.0)

        avg_fee = UniversalReportQueryEngine.aggregate_field(records, "fee_amount", "AVG")
        self.assertEqual(avg_fee, 50000.0)

    def test_analytics_and_health_score(self):
        """Test moving average calculation and composite institutional health score."""
        series = [10.0, 20.0, 30.0, 40.0, 50.0]
        ma = PredictiveAnalyticsEngine.compute_moving_average(series, window=3)
        self.assertEqual(len(ma), 5)
        self.assertEqual(ma[2], 20.0) # (10+20+30)/3 = 20.0
        self.assertEqual(ma[4], 40.0) # (30+40+50)/3 = 40.0

        health = PredictiveAnalyticsEngine.compute_institute_health_score(
            attendance_pct=90.0,
            fee_collection_pct=85.0,
            exam_pass_pct=95.0,
            lead_conversion_pct=30.0
        )
        # (90*0.25) + (85*0.35) + (95*0.25) + (30*0.15) = 22.5 + 29.75 + 23.75 + 4.5 = 80.5
        self.assertEqual(health, 80.5)

    def test_chart_engine(self):
        """Test Apache ECharts option generation for bar and pie charts."""
        bar_opts = EChartsOptionBuilder.build_bar_chart(
            "Monthly Admissions", ["Jan", "Feb", "Mar"], [120, 150, 180]
        )
        self.assertIn("series", bar_opts)
        self.assertEqual(bar_opts["xAxis"]["data"], ["Jan", "Feb", "Mar"])

        pie_opts = EChartsOptionBuilder.build_pie_chart(
            "Gender Diversity", [{"name": "Female", "value": 450}, {"name": "Male", "value": 550}]
        )
        self.assertIn("series", pie_opts)
        self.assertEqual(pie_opts["series"][0]["type"], "pie")

    def test_export_and_kpi_engine(self):
        """Test CSV export string generation and KPI threshold status evaluation."""
        records = [{"id": "1", "name": "Aarav"}, {"id": "2", "name": "Ananya"}]
        csv_str = DataExportEngine.to_csv_string(records)
        self.assertIn("id,name", csv_str)
        self.assertIn("Aarav", csv_str)

        # KPI evaluation
        status_normal = KpiEvaluationEngine.evaluate_status(current=92.0, warning=85.0, critical=75.0)
        self.assertEqual(status_normal, "NORMAL")

        status_warning = KpiEvaluationEngine.evaluate_status(current=80.0, warning=85.0, critical=75.0)
        self.assertEqual(status_warning, "WARNING")

        status_critical = KpiEvaluationEngine.evaluate_status(current=65.0, warning=85.0, critical=75.0)
        self.assertEqual(status_critical, "CRITICAL")

    def test_zero_browser_storage_bi(self):
        """Strictly enforce zero usage of localStorage, sessionStorage, or indexedDB in frontend."""
        storage_pattern = re.compile(r'\b(localStorage|sessionStorage|indexedDB)\b')
        violations = []
        for root, _, files in os.walk(self.bi_frontend_dir):
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
