"""Module 20: Immutable Audit Engine"""
from datetime import datetime

class ImmutableAuditEngine:
    @staticmethod
    def prepare_audit_entry(user_id: str, event_type: str, resource: str, old_val: dict, new_val: dict) -> dict:
        return {
            'user_id': user_id,
            'event_type': event_type,
            'resource_type': resource,
            'old_values': old_val,
            'new_values': new_val,
            'timestamp': datetime.utcnow().isoformat(),
            'is_immutable': True
        }
