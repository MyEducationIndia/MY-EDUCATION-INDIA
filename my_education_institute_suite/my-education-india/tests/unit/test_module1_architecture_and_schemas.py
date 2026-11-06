import ast
import os
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestEnterpriseArchitectureAndCompliance(unittest.TestCase):
    def test_required_directories_exist(self) -> None:
        required_dirs = [
            "frontend/src/components",
            "frontend/src/layouts",
            "frontend/src/pages",
            "frontend/src/hooks",
            "frontend/src/services",
            "frontend/src/api",
            "frontend/src/store",
            "frontend/src/utils",
            "frontend/src/styles",
            "frontend/src/routes",
            "frontend/src/types",
            "backend/app/api/v1/endpoints",
            "backend/app/core",
            "backend/app/auth",
            "backend/app/db",
            "backend/app/models",
            "backend/app/schemas",
            "backend/app/repositories",
            "backend/app/services",
            "backend/app/middleware",
            "backend/app/utils",
            "backend/app/permissions",
            "backend/app/logs",
            "backend/alembic/versions",
            "docs",
            "tests",
            "scripts",
            "docker",
        ]
        for rel in required_dirs:
            self.assertTrue(
                (PROJECT_ROOT / rel).is_dir(),
                f"Missing required enterprise directory: {rel}",
            )

    def test_zero_browser_storage_in_frontend_source(self) -> None:
        """Verify that no frontend TypeScript/TSX file invokes localStorage, sessionStorage, or indexedDB."""
        forbidden_tokens = ["localStorage.", "sessionStorage.", "indexedDB."]
        src_dir = PROJECT_ROOT / "frontend/src"
        for ts_file in src_dir.rglob("*.ts*"):
            content = ts_file.read_text(encoding="utf-8")
            for token in forbidden_tokens:
                self.assertNotIn(
                    token,
                    content,
                    f"Forbidden browser storage API '{token}' found in {ts_file}",
                )

    def test_all_python_files_compile_cleanly(self) -> None:
        """Verify every Python file in backend/, scripts/, and tests/ has valid AST syntax."""
        for folder in ["backend", "scripts", "tests"]:
            for py_file in (PROJECT_ROOT / folder).rglob("*.py"):
                source = py_file.read_text(encoding="utf-8")
                try:
                    ast.parse(source, filename=str(py_file))
                except SyntaxError as exc:
                    self.fail(f"SyntaxError in {py_file}: {exc}")

    def test_module_catalog_covers_all_37_enterprise_modules(self) -> None:
        catalog_path = PROJECT_ROOT / "backend/app/permissions/module_catalog.py"
        namespace: dict = {}
        exec(catalog_path.read_text(encoding="utf-8"), namespace)
        catalog = namespace["ENTERPRISE_MODULES_CATALOG"]
        self.assertGreaterEqual(len(catalog), 35)
        keys = {item["module_key"] for item in catalog}
        expected = {
            "authentication",
            "role_management",
            "institute_management",
            "student_management",
            "faculty_management",
            "course_management",
            "batch_management",
            "admission",
            "fees",
            "attendance",
            "exam_management",
            "question_bank",
            "offline_cbt",
            "online_cbt",
            "results",
            "certificates",
            "website_cms",
            "gallery",
            "news",
            "notice_board",
            "library",
            "inventory",
            "hostel",
            "transport",
            "hr",
            "payroll",
            "communication",
            "sms",
            "whatsapp",
            "email",
            "reports",
            "analytics",
            "backup",
            "restore",
            "audit_logs",
            "settings",
            "api_management",
        }
        self.assertTrue(expected.issubset(keys))


if __name__ == "__main__":
    unittest.main()
