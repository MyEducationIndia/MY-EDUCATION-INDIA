"""
Module 19: Platform Service Layer
"""
from app.modules.platform.repository import PlatformRepository
from app.modules.platform.security_engine import PlatformSecurityEngine
from app.modules.platform.backup_engine import EnterpriseBackupEngine
from app.modules.platform.restore_engine import DisasterRecoveryEngine
from app.modules.platform.health_engine import ClusterHealthEngine
from app.modules.platform.feature_flag_engine import FeatureFlagEvaluationEngine

class PlatformAdministrationService:
    def __init__(self, repo: PlatformRepository):
        self.repo = repo

    def evaluate_feature(self, flag_key: str, user_id: str, is_active: bool, rollout_pct: float) -> bool:
        return FeatureFlagEvaluationEngine.is_enabled_for_user(flag_key, user_id, is_active, rollout_pct)

    def get_cluster_health(self) -> dict:
        return ClusterHealthEngine.check_system_telemetry()

    def run_restore_dry_run(self, scope: str) -> list:
        return DisasterRecoveryEngine.generate_dry_run_plan(scope)
