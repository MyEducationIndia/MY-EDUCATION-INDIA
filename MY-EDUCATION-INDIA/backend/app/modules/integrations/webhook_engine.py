"""
Webhook Engine
Handles inbound webhook signature verification and outbound webhook dispatching.
"""
import hmac
import hashlib
import json
from typing import Dict, Any

class WebhookEngine:
    @staticmethod
    def verify_inbound_signature(payload_bytes: bytes, signature: str, secret: str) -> bool:
        expected = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def prepare_outbound_payload(event_type: str, data: Dict[str, Any], secret: str) -> Dict[str, Any]:
        payload_json = json.dumps({"event": event_type, "data": data, "timestamp": int(time.time())})
        sig = hmac.new(secret.encode("utf-8"), payload_json.encode("utf-8"), hashlib.sha256).hexdigest()
        return {
            "payload_json": payload_json,
            "signature": sig,
            "signature_header": "X-ERP-Signature"
        }
import time
