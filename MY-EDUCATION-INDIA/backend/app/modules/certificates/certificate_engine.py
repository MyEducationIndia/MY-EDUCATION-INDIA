from datetime import date
import uuid


class CertificateSequenceEngine:
    @staticmethod
    def format_certificate_number(prefix: str, year: int, counter: int) -> str:
        return f"{prefix}-{year}-{counter:06d}"

    @staticmethod
    def generate_unique_verification_id() -> str:
        return f"VRF-{uuid.uuid4().hex[:12].upper()}"
