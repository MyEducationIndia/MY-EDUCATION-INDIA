import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple
import jwt
from app.core.config import get_settings
from app.modules.auth.exceptions import TokenRevokedException
from app.core.exceptions import UnauthorizedException


def create_access_token(
    user_id: str,
    institute_id: str | None,
    roles: List[str],
    permissions: List[str],
    custom_claims: Dict[str, Any] | None = None,
    expire_minutes: int | None = None,
) -> Tuple[str, datetime]:
    settings = get_settings()
    minutes = expire_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=minutes)

    payload: Dict[str, Any] = {
        "sub": user_id,
        "inst": institute_id,
        "roles": roles,
        "perms": permissions,
        "type": "access",
        "jti": str(uuid.uuid4()),
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    if custom_claims:
        payload.update(custom_claims)

    encoded = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded, expires_at


def create_refresh_token(
    user_id: str,
    family_id: str | None = None,
    remember_me: bool = False,
    expire_days: int | None = None,
) -> Tuple[str, str, datetime]:
    settings = get_settings()
    days = expire_days or (30 if remember_me else settings.REFRESH_TOKEN_EXPIRE_DAYS)
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=days)
    token_family = family_id or str(uuid.uuid4())
    jti = str(uuid.uuid4())

    payload: Dict[str, Any] = {
        "sub": user_id,
        "fam": token_family,
        "type": "refresh",
        "rem": remember_me,
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
            raise UnauthorizedException("Invalid token type. Expected access token.")
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedException("Access token has expired.") from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedException("Malformed or invalid access token.") from exc


def decode_refresh_token(token: str) -> Dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid token type. Expected refresh token.")
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise TokenRevokedException("Refresh token has expired.") from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedException("Malformed or invalid refresh token.") from exc
