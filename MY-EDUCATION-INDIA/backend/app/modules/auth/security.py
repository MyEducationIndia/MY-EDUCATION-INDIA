import re
import secrets
import hashlib
from typing import List, Tuple
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from app.modules.auth.exceptions import PasswordPolicyException, PasswordHistoryException

# Production password hasher supporting Argon2id with Bcrypt fallback
password_hasher = PasswordHash((Argon2Hasher(), BcryptHasher()))


def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


def generate_secure_token(length_bytes: int = 32) -> Tuple[str, str]:
    """Generates a raw URL-safe token and its SHA-256 hash for database storage."""
    raw_token = secrets.token_urlsafe(length_bytes)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    return raw_token, token_hash


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def validate_password_policy(
    password: str,
    policy: dict,
) -> None:
    min_length = policy.get("password_min_length", 10)
    req_upper = policy.get("password_require_uppercase", True)
    req_lower = policy.get("password_require_lowercase", True)
    req_num = policy.get("password_require_number", True)
    req_special = policy.get("password_require_special", True)

    violations = []
    if len(password) < min_length:
        violations.append(f"Password must be at least {min_length} characters long")
    if req_upper and not any(c.isupper() for c in password):
        violations.append("Password must contain at least one uppercase letter (A-Z)")
    if req_lower and not any(c.islower() for c in password):
        violations.append("Password must contain at least one lowercase letter (a-z)")
    if req_num and not any(c.isdigit() for c in password):
        violations.append("Password must contain at least one number (0-9)")
    if req_special and not any(not c.isalnum() for c in password):
        violations.append("Password must contain at least one special character (!@#$%^&*...)")

    if violations:
        raise PasswordPolicyException(
            message="; ".join(violations),
            violations=violations,
        )


def verify_password_history(
    plain_password: str,
    password_history: List[str],
) -> None:
    for old_hash in password_history:
        if verify_password(plain_password, old_hash):
            raise PasswordHistoryException("New password matches a recently used password.")
