import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException

# Enterprise-grade password hasher using OWASP-recommended Argon2
password_hasher = PasswordHash((Argon2Hasher(),))


def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


def hash_token_identifier(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def create_access_token(
    subject: str,
    institute_id: str | None,
    roles: list[str],
    permissions: list[str],
) -> tuple[str, datetime]:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: Dict[str, Any] = {
        "sub": subject,
        "inst": institute_id,
        "roles": roles,
        "perms": permissions,
        "type": "access",
        "jti": str(uuid.uuid4()),
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    encoded = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded, expires_at


def create_refresh_token(subject: str, family_id: str | None = None) -> tuple[str, str, datetime]:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token_family = family_id or str(uuid.uuid4())
    jti = str(uuid.uuid4())
    payload: Dict[str, Any] = {
        "sub": subject,
        "fam": token_family,
        "type": "refresh",
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    encoded = jwt.encode(payload, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded, token_family, expires_at


def decode_access_token(token: str) -> Dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            raise UnauthorizedException("Invalid token type.")
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedException("Access token has expired.") from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedException("Invalid access token.") from exc


def decode_refresh_token(token: str) -> Dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token type.")
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedException("Refresh token has expired.") from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedException("Invalid refresh token.") from exc


def generate_csrf_token(session_id: str) -> str:
    settings = get_settings()
    nonce = secrets.token_hex(16)
    message = f"{session_id}:{nonce}".encode("utf-8")
    signature = hmac.new(
        settings.CSRF_SECRET_KEY.encode("utf-8"), message, hashlib.sha256
    ).hexdigest()
    return f"{nonce}.{signature}"


def verify_csrf_token(session_id: str, csrf_token: str) -> bool:
    settings = get_settings()
    if not csrf_token or "." not in csrf_token:
        return False
    nonce, provided_sig = csrf_token.split(".", 1)
    message = f"{session_id}:{nonce}".encode("utf-8")
    expected_sig = hmac.new(
        settings.CSRF_SECRET_KEY.encode("utf-8"), message, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(provided_sig, expected_sig)
