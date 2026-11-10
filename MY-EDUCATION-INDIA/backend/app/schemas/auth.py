import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=255, description="Institutional User ID (e.g. STU240001, FAC240001, EMP240001, ADM000001, ROOT000001)")
    password: str = Field(..., min_length=8, max_length=128)
    remember_me: bool = False


class OtpRequestPayload(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=255, description="Email or Phone Number")
    channel: str = Field(default="EMAIL")  # EMAIL or SMS
    otp_type: str = Field(default="LOGIN")  # LOGIN or PASSWORD_RESET


class OtpVerifyPayload(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=255)
    otp_code: str = Field(..., min_length=6, max_length=6)
    otp_type: str = Field(default="LOGIN")


class MfaSetupResponse(BaseModel):
    mfa_secret: str
    totp_uri: str
    backup_codes: List[str]


class MfaVerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=8)


class PasswordResetRequestPayload(BaseModel):
    email: EmailStr


class PasswordResetConfirmPayload(BaseModel):
    email: EmailStr
    otp_code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=10, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(not c.isalnum() for c in v)
        if not (has_upper and has_lower and has_digit and has_special):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, "
                "one digit, and one special character."
            )
        return v


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=128)
    new_password: str = Field(..., min_length=10, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(not c.isalnum() for c in v)
        if not (has_upper and has_lower and has_digit and has_special):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, "
                "one digit, and one special character."
            )
        return v


class AuthenticatedUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    username: str
    phone_number: str
    first_name: str
    last_name: str
    is_active: bool
    is_super_admin: bool
    is_verified: bool
    mfa_enabled: bool = False
    institute_id: uuid.UUID | None
    roles: List[str]
    permissions: List[str]
    last_login_at: datetime | None


class TokenSessionResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_at: datetime
    csrf_token: str
    user: AuthenticatedUserResponse


class ActiveSessionItem(BaseModel):
    id: uuid.UUID
    device_name: str
    ip_address: str
    user_agent: str
    is_current: bool
    expires_at: datetime
    last_active_at: datetime
    created_at: datetime


class LoginHistoryItem(BaseModel):
    id: uuid.UUID
    email: str
    ip_address: str
    user_agent: str
    device_name: str
    status: str
    failure_reason: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime


class SecurityPolicyResponse(BaseModel):
    policy_name: str
    min_password_length: int
    require_uppercase: bool
    require_numbers: bool
    require_special_chars: bool
    password_expiry_days: int
    max_failed_attempts: int
    lockout_duration_minutes: int
    session_timeout_minutes: int
    enforce_2fa: bool
    allow_remember_me: bool
    remember_me_days: int


class SecurityPolicyUpdateRequest(BaseModel):
    min_password_length: Optional[int] = None
    require_uppercase: Optional[bool] = None
    require_numbers: Optional[bool] = None
    require_special_chars: Optional[bool] = None
    password_expiry_days: Optional[int] = None
    max_failed_attempts: Optional[int] = None
    lockout_duration_minutes: Optional[int] = None
    session_timeout_minutes: Optional[int] = None
    enforce_2fa: Optional[bool] = None
    allow_remember_me: Optional[bool] = None
    remember_me_days: Optional[int] = None
