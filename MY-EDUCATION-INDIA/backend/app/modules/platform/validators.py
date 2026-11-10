"""
Module 19: Platform Business Validators
"""
import re
import ipaddress

class PlatformBusinessValidators:
    @staticmethod
    def validate_cron_format(cron: str) -> bool:
        parts = cron.strip().split()
        return len(parts) == 5

    @staticmethod
    def validate_ip_cidr(cidr: str) -> bool:
        try:
            ipaddress.ip_network(cidr, strict=False)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_rollout_percentage(pct: float) -> bool:
        return 0.0 <= pct <= 100.0

    @staticmethod
    def validate_password_policy(min_len: int, max_failed: int) -> bool:
        return min_len >= 8 and 1 <= max_failed <= 10
