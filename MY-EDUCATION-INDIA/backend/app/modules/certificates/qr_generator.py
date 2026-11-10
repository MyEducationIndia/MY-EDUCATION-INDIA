import hashlib
import json


class CertificateQRGenerator:
    @staticmethod
    def generate_verification_qr_payload(
        verification_id: str,
        cert_number: str,
        institute_id: str,
        public_url: str,
    ) -> str:
        payload = {
            "entity": "MY EDUCATION INDIA ERP",
            "document": "OFFICIAL_DIGITAL_CREDENTIAL",
            "cert_no": cert_number,
            "verification_id": verification_id,
            "verify_url": public_url,
            "tamper_proof": True,
        }
        return json.dumps(payload, separators=(",", ":"))
