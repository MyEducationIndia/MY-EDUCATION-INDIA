"""
Module 19: Feature Flag Engine
"""
import hashlib

class FeatureFlagEvaluationEngine:
    @staticmethod
    def is_enabled_for_user(flag_key: str, user_id: str, is_active: bool, rollout_pct: float, target_roles: list = None, user_role: str = None) -> bool:
        if not is_active:
            return False
        if target_roles and user_role and user_role in target_roles:
            return True
        if rollout_pct >= 100.0:
            return True
        if rollout_pct <= 0.0:
            return False
        
        # Deterministic hash bucket 0-99
        hash_val = int(hashlib.md5(f"{flag_key}:{user_id}".encode("utf-8")).hexdigest(), 16)
        bucket = hash_val % 100
        return bucket < rollout_pct
