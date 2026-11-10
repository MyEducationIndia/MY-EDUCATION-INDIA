"""
Module 19: Enterprise Backup Engine
"""
import hashlib
from datetime import datetime

class EnterpriseBackupEngine:
    @staticmethod
    def compute_sha256(content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    @staticmethod
    def generate_backup_filename(institute_id: str, backup_type: str, timestamp: datetime) -> str:
        ts = timestamp.strftime("%Y%m%d_%H%M%S")
        return f"backup_{institute_id[:8]}_{backup_type.lower()}_{ts}.tar.gz"

    @staticmethod
    def should_retain(backup_created_at: datetime, retention_days: int, current_time: datetime) -> bool:
        age_days = (current_time - backup_created_at).days
        return age_days <= retention_days
