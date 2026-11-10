import hashlib
import json
from typing import Any, List
from app.core.exceptions import ValidationException


class OfflineSyncEngine:
    """Validates offline payload integrity using SHA-256 checksums and handles sync batches."""

    @staticmethod
    def calculate_checksum(data: List[dict]) -> str:
        serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_checksum(data: List[dict], client_checksum: str) -> None:
        computed = OfflineSyncEngine.calculate_checksum(data)
        if computed != client_checksum:
            raise ValidationException("Data integrity verification failed: Checksum mismatch in offline sync batch.")
