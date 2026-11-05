import base64
import hashlib
import hmac
import json
import os
import re
import time
import uuid
from typing import Any, Callable, Dict, List, Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# Optional passlib/bcrypt integration with zero-compilation PBKDF2-HMAC-SHA256 fallback
try:
    from passlib.context import CryptContext
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    _HAS_BCRYPT = True
except Exception:
    _pwd_context = None
    _HAS_BCRYPT = False

# In-memory token revocation registry (augmented by database audit log)
_REVOKED_TOKENS: Dict[str, float] = {}

bearer_scheme = HTTPBearer(auto_error=False)


def validate_password_strength(password: str) -> bool:
    """
    Validates password complexity policy (minimum 6 characters; supports DOB format YYYY-MM-DD for students).
    """
    if not password or len(password.strip()) < 6:
        return False
    return True


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
    Hashes password using bcrypt when available or PBKDF2-HMAC-SHA256 (100,000 iterations).
    """
    if _HAS_BCRYPT and _pwd_context is not None and salt is None:
        try:
            return _pwd_context.hash(password)
        except Exception:
            pass
    if not salt:
        salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    ).hex()
    return f"{salt}${pwd_hash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against either a bcrypt hash ($2b$...) or PBKDF2 hash (salt$hash).
    """
    if not plain_password or not hashed_password:
        return False
    try:
        if hashed_password.startswith(("$2a$", "$2b$", "$2y$")) and _HAS_BCRYPT and _pwd_context is not None:
            return bool(_pwd_context.verify(plain_password, hashed_password))
        if "$" in hashed_password:
            salt, expected_hash = hashed_password.split("$", 1)
            actual_hash = hashlib.pbkdf2_hmac(
                "sha256",
                plain_password.encode("utf-8"),
                salt.encode("utf-8"),
                100000,
            ).hex()
            return hmac.compare_digest(actual_hash, expected_hash)
        return False
    except Exception as exc:
        logger.warning("Password verification failed: %s", exc)
        return False


def _sign_jwt_payload(payload: Dict[str, Any]) -> str:
    header = {"alg": settings.ALGORITHM, "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(
        json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).decode("utf-8").rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).decode("utf-8").rstrip("=")
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    sig_bytes = hmac.new(
        settings.effective_jwt_secret.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()
    sig_b64 = base64.urlsafe_b64encode(sig_bytes).decode("utf-8").rstrip("=")
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    to_encode = data.copy()
    now = int(time.time())
    expire = now + (expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    to_encode.update({
        "iat": now,
        "exp": expire,
        "jti": uuid.uuid4().hex,
        "type": "access",
    })
    return _sign_jwt_payload(to_encode)


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    to_encode = data.copy()
    now = int(time.time())
    expire = now + (expires_delta or settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400)
    to_encode.update({
        "iat": now,
        "exp": expire,
        "jti": uuid.uuid4().hex,
        "type": "refresh",
    })
    return _sign_jwt_payload(to_encode)


def decode_access_token(token: str, expected_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
    try:
        if not token or token in _REVOKED_TOKENS:
            return None
        parts = token.split(".")
        if len(parts) == 3:
            header_b64, payload_b64, sig_b64 = parts
            signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
            expected_sig_bytes = hmac.new(
                settings.effective_jwt_secret.encode("utf-8"),
                signing_input,
                hashlib.sha256,
            ).digest()
            expected_sig_b64 = base64.urlsafe_b64encode(expected_sig_bytes).decode("utf-8").rstrip("=")
            if not hmac.compare_digest(expected_sig_b64, sig_b64):
                return None
        elif len(parts) == 2:
            payload_b64, signature = parts
            expected_sig = hmac.new(
                settings.effective_jwt_secret.encode("utf-8"),
                payload_b64.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            if not hmac.compare_digest(expected_sig, signature):
                return None
        else:
            return None

        padding = "=" * ((4 - len(payload_b64) % 4) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
        payload: Dict[str, Any] = json.loads(payload_bytes.decode("utf-8"))
        if payload.get("exp", 0) < time.time():
            return None
        jti = payload.get("jti")
        if jti and jti in _REVOKED_TOKENS:
            return None
        if expected_type and payload.get("type") and payload.get("type") != expected_type:
            return None
        return payload
    except Exception as exc:
        logger.debug("Token decode error: %s", exc)
        return None


def revoke_token(token: str) -> None:
    """
    Revokes a JWT token on logout so it can no longer be used.
    """
    now = time.time()
    # Prune expired entries
    expired_keys = [k for k, exp in _REVOKED_TOKENS.items() if exp < now]
    for k in expired_keys:
        _REVOKED_TOKENS.pop(k, None)

    payload = decode_access_token(token)
    exp = float(payload.get("exp", now + 86400)) if payload else (now + 86400)
    _REVOKED_TOKENS[token] = exp
    if payload and payload.get("jti"):
        _REVOKED_TOKENS[str(payload["jti"])] = exp


def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Optional[Dict[str, Any]]:
    token: Optional[str] = None
    if credentials and credentials.credentials:
        token = credentials.credentials
    else:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ", 1)[1].strip()
    if not token:
        return None
    return decode_access_token(token)


def get_current_user(
    user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
) -> Dict[str, Any]:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(allowed_roles: List[str]) -> Callable:
    def _role_checker(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        role = str(user.get("role", "")).lower()
        if role not in [r.lower() for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' is not authorized to perform this operation.",
            )
        return user
    return _role_checker


def sanitize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    cleaned = re.sub(r"<script\b[^<]*(?:(?!</script>)<[^<]*)*</script>", "", str(value), flags=re.IGNORECASE)
    return cleaned.strip()
