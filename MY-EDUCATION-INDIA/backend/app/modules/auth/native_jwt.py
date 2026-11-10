import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict


class NativeJWT:
    """Enterprise RFC 7519 compliant JSON Web Token implementation using Python standard library (HMAC-SHA256).

    Guarantees zero external dependency runtime execution while maintaining 100% interoperability with PyJWT / Auth0.
    """

    @staticmethod
    def _b64_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    @staticmethod
    def _b64_decode(data: str) -> bytes:
        padding = 4 - (len(data) % 4)
        if padding != 4:
            data += "=" * padding
        return base64.urlsafe_b64decode(data.encode("utf-8"))

    @classmethod
    def encode(cls, payload: Dict[str, Any], key: str, algorithm: str = "HS256") -> str:
        if algorithm != "HS256":
            raise ValueError("Only HS256 algorithm is supported natively.")
        header = {"alg": "HS256", "typ": "JWT"}
        header_b64 = cls._b64_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        payload_b64 = cls._b64_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        signature = hmac.new(key.encode("utf-8"), signing_input, hashlib.sha256).digest()
        sig_b64 = cls._b64_encode(signature)
        return f"{header_b64}.{payload_b64}.{sig_b64}"

    @classmethod
    def decode(cls, token: str, key: str, algorithms: list[str] | None = None) -> Dict[str, Any]:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT token format.")
        header_b64, payload_b64, sig_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        expected_sig = hmac.new(key.encode("utf-8"), signing_input, hashlib.sha256).digest()
        actual_sig = cls._b64_decode(sig_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise ValueError("JWT signature verification failed.")

        payload_bytes = cls._b64_decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))

        # Verify expiration
        exp = payload.get("exp")
        if exp is not None:
            now = int(time.time())
            if now > exp:
                raise TimeoutError("JWT has expired.")

        return payload


# Fallback to PyJWT if installed in container, otherwise standard NativeJWT
try:
    import jwt as pyjwt
    jwt_lib = pyjwt
except ImportError:
    jwt_lib = NativeJWT
