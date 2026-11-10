"""
Universal API Connector
Features:
- REST, Webhooks
- Circuit Breaker Pattern (CLOSED, OPEN, HALF_OPEN)
- Token Bucket Rate Limiter
- Exponential Backoff Retries
- Configurable Timeouts
- Failover Provider Routing
"""
import time
import json
import hmac
import hashlib
from typing import Dict, Any, Optional

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout_seconds: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.failure_count = 0
        self.state = "CLOSED" # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = 0.0

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout_seconds:
                self.state = "HALF_OPEN"
                return True
            return False
        if self.state == "HALF_OPEN":
            return True
        return True

class UniversalApiConnector:
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}

    def get_circuit_breaker(self, provider_id: str, threshold: int = 5) -> CircuitBreaker:
        if provider_id not in self.circuit_breakers:
            self.circuit_breakers[provider_id] = CircuitBreaker(failure_threshold=threshold)
        return self.circuit_breakers[provider_id]

    def build_authenticated_headers(self, auth_type: str, credentials: Dict[str, Any], custom_headers: Optional[Dict] = None) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "MyEducationIndia-UniversalConnector/2.0"
        }
        if custom_headers:
            headers.update(custom_headers)

        if auth_type == "BEARER":
            token = credentials.get("token") or credentials.get("api_key", "")
            headers["Authorization"] = f"Bearer {token}"
        elif auth_type == "API_KEY":
            header_name = credentials.get("header_name", "X-Api-Key")
            headers[header_name] = credentials.get("api_key", "")
        elif auth_type == "BASIC":
            import base64
            u = credentials.get("username", "")
            p = credentials.get("password", "")
            encoded = base64.b64encode(f"{u}:{p}".encode("utf-8")).decode("utf-8")
            headers["Authorization"] = f"Basic {encoded}"
        elif auth_type == "CUSTOM_HEADER":
            for k, v in credentials.items():
                if k.startswith("header_"):
                    headers[k[7:]] = str(v)
        return headers

    def calculate_hmac_signature(self, payload_bytes: bytes, secret: str) -> str:
        return hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
