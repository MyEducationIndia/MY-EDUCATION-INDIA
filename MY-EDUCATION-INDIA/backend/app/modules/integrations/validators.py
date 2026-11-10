"""
API Integration Validators
"""
import re

class ApiIntegrationValidators:
    @staticmethod
    def validate_url(url: str) -> bool:
        if not url:
            return False
        return bool(re.match(r'^(https?|smtp)://[^\s/$.?#].[^\s]*$', url))

    @staticmethod
    def validate_provider_key(key: str) -> bool:
        if not key or len(key) < 2 or len(key) > 60:
            return False
        return bool(re.match(r'^[a-z0-9_-]+$', key.lower()))

    @staticmethod
    def validate_timeout_and_retries(timeout: int, max_retries: int) -> bool:
        return 1 <= timeout <= 120 and 0 <= max_retries <= 10
