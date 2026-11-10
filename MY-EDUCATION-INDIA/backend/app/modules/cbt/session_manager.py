from datetime import datetime, timezone
from typing import Dict
import uuid


class CBTSessionManager:
    """Manages candidate active heartbeat state, auto-submission timeouts, and proctoring warnings."""

    @staticmethod
    def evaluate_heartbeat(remaining_seconds: int, elapsed_seconds: int) -> int:
        updated = max(0, remaining_seconds - elapsed_seconds)
        return updated

    @staticmethod
    def is_expired(remaining_seconds: int) -> bool:
        return remaining_seconds <= 0
