import hashlib
import uuid


class DigitalVerificationEngine:
    """Generates secure verification hashes and evaluates cryptographic verification tokens."""

    SECRET_SALT = "MEI_VERIFY_HMAC_SALT_2026_SECURE"

    @staticmethod
    def generate_token_hash(verification_id: str, cert_number: str, recipient_id: str) -> str:
        raw = f"{verification_id}:{cert_number}:{recipient_id}:{DigitalVerificationEngine.SECRET_SALT}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_token(verification_id: str, cert_number: str, recipient_id: str, provided_hash: str) -> bool:
        expected = DigitalVerificationEngine.generate_token_hash(verification_id, cert_number, recipient_id)
        return expected == provided_hash
