import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import ast
import re
from datetime import datetime, timedelta

from app.modules.platform.schemas import (
    PlatformSettingCreate,
    SecurityPolicyCreate,
    BackupJobCreate,
    TriggerRestoreRequest,
    FeatureFlagCreate
)
from app.modules.platform.validators import PlatformBusinessValidators
from app.modules.platform.backup_engine import EnterpriseBackupEngine
from app.modules.platform.restore_engine import DisasterRecoveryEngine
from app.modules.platform.security_engine import PlatformSecurityEngine
from app.modules.platform.feature_flag_engine import FeatureFlagEvaluationEngine
from app.modules.platform.health_engine import ClusterHealthEngine

class TestModule19PlatformBackend(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.plt_backend_dir = os.path.join(self.base_dir, "backend/app/modules/platform")
        self.plt_frontend_dir = os.path.join(self.base_dir, "frontend/src/modules/platform")

    def test_platform_models_and_modules_ast(self):
        """Verify all Module 19 Python source files compile cleanly without syntax errors."""
        self.assertTrue(os.path.exists(self.plt_backend_dir), "Platform backend directory missing")
        py_files = [f for f in os.listdir(self.plt_backend_dir) if f.endswith(".py")]
        self.assertGreaterEqual(len(py_files), 12, "Expected at least 12 Python files in Platform module")
        for py_file in py_files:
            file_path = os.path.join(self.plt_backend_dir, py_file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                ast.parse(content, filename=py_file)
            except SyntaxError as e:
                self.fail(f"SyntaxError in {py_file}: {e}")

    def test_platform_schemas(self):
        """Test Pydantic schemas for platform settings, security policies, backup jobs, and feature flags."""
        setting = PlatformSettingCreate(
            setting_key="INSTITUTION_TIMEZONE",
            setting_value="Asia/Kolkata",
            category="LOCALIZATION"
        )
        self.assertEqual(setting.setting_key, "INSTITUTION_TIMEZONE")

        sec = SecurityPolicyCreate(
            policy_name="Enterprise Hardened Tier",
            min_password_length=12,
            require_uppercase=True,
            require_numbers=True,
            require_special_chars=True,
            max_failed_attempts=5,
            lockout_duration_minutes=30
        )
        self.assertEqual(sec.min_password_length, 12)

        job = BackupJobCreate(
            job_name="Weekly Full Cold Backup",
            backup_type="FULL",
            schedule_cron="0 3 * * 0",
            storage_destination="AWS_S3"
        )
        self.assertEqual(job.backup_type, "FULL")

        flag = FeatureFlagCreate(
            flag_key="BETA_NEW_CBT_UI",
            is_enabled=True,
            rollout_percentage=50.0
        )
        self.assertEqual(flag.rollout_percentage, 50.0)

    def test_platform_validators(self):
        """Test cron syntax, IP CIDR, rollout percentage, and password policy validators."""
        self.assertTrue(PlatformBusinessValidators.validate_cron_format("0 2 * * *"))
        self.assertFalse(PlatformBusinessValidators.validate_cron_format("invalid cron"))

        self.assertTrue(PlatformBusinessValidators.validate_ip_cidr("192.168.1.0/24"))
        self.assertTrue(PlatformBusinessValidators.validate_ip_cidr("10.0.0.0/8"))
        self.assertFalse(PlatformBusinessValidators.validate_ip_cidr("999.999.999.999/99"))

        self.assertTrue(PlatformBusinessValidators.validate_rollout_percentage(50.0))
        self.assertTrue(PlatformBusinessValidators.validate_rollout_percentage(0.0))
        self.assertTrue(PlatformBusinessValidators.validate_rollout_percentage(100.0))
        self.assertFalse(PlatformBusinessValidators.validate_rollout_percentage(-5.0))
        self.assertFalse(PlatformBusinessValidators.validate_rollout_percentage(105.0))

        self.assertTrue(PlatformBusinessValidators.validate_password_policy(min_len=10, max_failed=5))
        self.assertFalse(PlatformBusinessValidators.validate_password_policy(min_len=4, max_failed=5))

    def test_backup_and_restore_engines(self):
        """Test SHA-256 checksum calculation, archive naming, retention policy, and dry-run restore plan."""
        data = b"PostgreSQL database dump contents for ERP"
        checksum = EnterpriseBackupEngine.compute_sha256(data)
        self.assertEqual(len(checksum), 64)

        now = datetime(2026, 11, 6, 12, 0, 0)
        filename = EnterpriseBackupEngine.generate_backup_filename("inst_001", "FULL", now)
        self.assertTrue(filename.startswith("backup_inst_001_full_"))
        self.assertTrue(filename.endswith(".tar.gz"))

        # Retention check
        created_at = datetime(2026, 10, 1, 10, 0, 0)
        self.assertFalse(EnterpriseBackupEngine.should_retain(created_at, retention_days=30, current_time=now))
        recent = datetime(2026, 11, 1, 10, 0, 0)
        self.assertTrue(EnterpriseBackupEngine.should_retain(recent, retention_days=30, current_time=now))

        # Restore checks
        prereq = DisasterRecoveryEngine.validate_restore_prerequisites("COMPLETED", True)
        self.assertTrue(prereq["can_restore"])

        plan = DisasterRecoveryEngine.generate_dry_run_plan("DATABASE_ONLY")
        self.assertGreaterEqual(len(plan), 3)

    def test_security_engine(self):
        """Test password complexity evaluation and lockout thresholds."""
        strong = PlatformSecurityEngine.verify_password_strength("EduIndia#2026!", min_len=10)
        self.assertTrue(strong["is_valid"])

        weak = PlatformSecurityEngine.verify_password_strength("simple", min_len=10)
        self.assertFalse(weak["is_valid"])
        self.assertGreaterEqual(len(weak["violations"]), 2)

        self.assertTrue(PlatformSecurityEngine.is_locked_out(failed_attempts=5, max_attempts=5))
        self.assertFalse(PlatformSecurityEngine.is_locked_out(failed_attempts=3, max_attempts=5))

    def test_feature_flag_evaluation(self):
        """Test deterministic hash bucket rollout and targeting."""
        # 100% rollout
        self.assertTrue(FeatureFlagEvaluationEngine.is_enabled_for_user("FLAG_A", "user_1", True, 100.0))
        # 0% rollout
        self.assertFalse(FeatureFlagEvaluationEngine.is_enabled_for_user("FLAG_A", "user_1", True, 0.0))
        # Inactive flag
        self.assertFalse(FeatureFlagEvaluationEngine.is_enabled_for_user("FLAG_A", "user_1", False, 100.0))

        # Role targeting override
        self.assertTrue(FeatureFlagEvaluationEngine.is_enabled_for_user(
            "FLAG_A", "user_99", True, 0.0, target_roles=["SUPER_ADMIN"], user_role="SUPER_ADMIN"
        ))

    def test_cluster_health_engine(self):
        """Test health telemetry overview."""
        telemetry = ClusterHealthEngine.check_system_telemetry()
        self.assertEqual(telemetry["cluster_status"], "HEALTHY")
        self.assertEqual(telemetry["api_gateway"]["status"], "HEALTHY")
        self.assertEqual(telemetry["database_postgres"]["status"], "HEALTHY")

    def test_zero_browser_storage_platform(self):
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
