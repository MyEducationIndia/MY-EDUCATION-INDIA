import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import ast
import re

from app.modules.platform.experience_schemas import (
    RootOwnerOverview,
    PortalConfigResponse,
    DynamicMenuCreate,
    FormDefinitionCreate,
    GlobalSearchResult
)
from app.modules.platform.portal_engine import EnterprisePortalEngine
from app.modules.platform.feature_engine import DynamicFeatureEngine
from app.modules.platform.dashboard_engine import DashboardBuilderEngine
from app.modules.platform.menu_engine import DynamicMenuEngine
from app.modules.platform.form_engine import DynamicFormEngine
from app.modules.platform.api_gateway import EnterpriseApiGateway
from app.modules.platform.developer_engine import DeveloperPlatformEngine
from app.modules.platform.search_engine import GlobalSearchEngine
from app.modules.platform.audit_engine import ImmutableAuditEngine

class TestModule20EnterpriseExperience(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.plt_backend_dir = os.path.join(self.base_dir, "backend/app/modules/platform")
        self.plt_frontend_dir = os.path.join(self.base_dir, "frontend/src/modules/platform")

    def test_experience_models_and_engines_ast(self):
        """Verify all Module 20 backend Python files compile cleanly without syntax errors."""
        self.assertTrue(os.path.exists(self.plt_backend_dir))
        py_files = [f for f in os.listdir(self.plt_backend_dir) if f.endswith(".py")]
        self.assertGreaterEqual(len(py_files), 12)
        for py_file in py_files:
            file_path = os.path.join(self.plt_backend_dir, py_file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                ast.parse(content, filename=py_file)
            except SyntaxError as e:
                self.fail(f"SyntaxError in {py_file}: {e}")

    def test_portal_engine_role_resolution(self):
        """Test portal resolution and access permissions across institutional roles."""
        self.assertEqual(EnterprisePortalEngine.resolve_portal_for_role("STUDENT"), "STUDENT")
        self.assertEqual(EnterprisePortalEngine.resolve_portal_for_role("PROFESSOR"), "FACULTY")
        self.assertEqual(EnterprisePortalEngine.resolve_portal_for_role("SUPER_ADMIN"), "SUPER_ADMIN")
        self.assertEqual(EnterprisePortalEngine.resolve_portal_for_role("ACCOUNTANT"), "ACCOUNTANT")

        self.assertTrue(EnterprisePortalEngine.can_access_portal("STUDENT", "STUDENT"))
        self.assertFalse(EnterprisePortalEngine.can_access_portal("STUDENT", "SUPER_ADMIN"))
        # Root owner sovereign access
        self.assertTrue(EnterprisePortalEngine.can_access_portal("ROOT_OWNER", "DEVELOPER"))

    def test_dashboard_and_menu_engines(self):
        """Test grid validation and menu hierarchy tree synthesis with permission pruning."""
        valid_grid = [{"width": 6, "height": 4}, {"width": 12, "height": 6}]
        invalid_grid = [{"width": 15, "height": 4}]
        self.assertTrue(DashboardBuilderEngine.validate_layout_grid(valid_grid))
        self.assertFalse(DashboardBuilderEngine.validate_layout_grid(invalid_grid))

        # Menu tree
        raw_items = [
            {"id": "m1", "label": "Academic", "parent_item_id": None, "required_permission": "ACADEMIC_VIEW"},
            {"id": "m2", "label": "Courses", "parent_item_id": "m1", "required_permission": "ACADEMIC_VIEW"},
            {"id": "m3", "label": "Super Admin Only", "parent_item_id": None, "required_permission": "SUPER_ADMIN"}
        ]
        tree_scholar = DynamicMenuEngine.build_navigation_tree(raw_items, ["ACADEMIC_VIEW"])
        self.assertEqual(len(tree_scholar), 1)
        self.assertEqual(tree_scholar[0]["label"], "Academic")
        self.assertEqual(len(tree_scholar[0]["children"]), 1)

    def test_form_engine_validation_and_ref(self):
        """Test dynamic form reference generation and schema field validation."""
        ref = DynamicFormEngine.generate_form_reference("ADMISSION_FORM")
        self.assertTrue(ref.startswith("ADMISS-"))

        fields = [
            {"name": "student_name", "label": "Full Name", "required": True},
            {"name": "phone", "label": "Mobile", "required": True},
            {"name": "notes", "label": "Notes", "required": False}
        ]
        # Valid payload
        errors_clean = DynamicFormEngine.validate_submission_payload(fields, {"student_name": "Aarav", "phone": "9876543210"})
        self.assertEqual(errors_clean, [])

        # Missing required field
        errors_missing = DynamicFormEngine.validate_submission_payload(fields, {"student_name": "Aarav"})
        self.assertEqual(len(errors_missing), 1)
        self.assertIn("Mobile", errors_missing[0])

    def test_api_gateway_rate_limiter(self):
        """Test API Gateway sliding-window rate limit counters."""
        gw = EnterpriseApiGateway()
        client = "api_client_001"
        # First 5 calls pass limit of 5
        for _ in range(5):
            self.assertTrue(gw.check_rate_limit(client, limit_per_minute=5))
        # 6th call exceeded
        self.assertFalse(gw.check_rate_limit(client, limit_per_minute=5))

    def test_global_search_engine(self):
        """Test unified cross-module full-text search index matching."""
        records = [
            {"title": "Aarav Sharma", "subtitle": "CSE Scholar", "keywords_tsv": "aarav cse btech"},
            {"title": "Physics 101", "subtitle": "Semester I Course", "keywords_tsv": "physics science"}
        ]
        res = GlobalSearchEngine.filter_search_index(records, "aarav")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["title"], "Aarav Sharma")

        res_none = GlobalSearchEngine.filter_search_index(records, "nonexistent")
        self.assertEqual(len(res_none), 0)

    def test_developer_and_audit_engines(self):
        """Test developer diagnostics and immutable audit log generation."""
        diag = DeveloperPlatformEngine.get_system_diagnostics()
        self.assertEqual(diag["app_version"], "2.0.0-ENTERPRISE")
        self.assertEqual(diag["active_modules_count"], 20)

        audit = ImmutableAuditEngine.prepare_audit_entry(
            user_id="usr_01", event_type="CONFIG_EDIT", resource="PORTAL",
            old_val={"theme": "LIGHT"}, new_val={"theme": "DARK"}
        )
        self.assertTrue(audit["is_immutable"])
        self.assertEqual(audit["new_values"]["theme"], "DARK")

    def test_zero_browser_storage_experience(self):
        """Strictly enforce zero usage of localStorage, sessionStorage, or indexedDB in frontend."""
        storage_pattern = re.compile(r'\b(localStorage|sessionStorage|indexedDB)\b')
        violations = []
        for root, _, files in os.walk(self.plt_frontend_dir):
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
