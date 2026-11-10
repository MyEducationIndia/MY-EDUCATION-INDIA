from typing import Dict, List
import uuid
from app.core.exceptions import ValidationException


class LeaveWorkflowEngine:
    """Validates leave quota balances and enforces approval status state transitions."""

    VALID_TRANSITIONS = {
        "PENDING": ["APPROVED", "REJECTED", "CANCELLED"],
        "APPROVED": ["CANCELLED"],
        "REJECTED": [],
        "CANCELLED": [],
    }

    @staticmethod
    def validate_transition(current_status: str, target_status: str) -> None:
        allowed = LeaveWorkflowEngine.VALID_TRANSITIONS.get(current_status, [])
        if target_status not in allowed:
            raise ValidationException(
                f"Invalid leave state transition from '{current_status}' to '{target_status}'."
            )

    @staticmethod
    def verify_quota_availability(annual_quota: int, used_days: float, requested_days: float) -> None:
        if (used_days + requested_days) > annual_quota:
            raise ValidationException(
                f"Requested leave ({requested_days} days) exceeds available quota balance ({annual_quota - used_days} days remaining)."
            )
