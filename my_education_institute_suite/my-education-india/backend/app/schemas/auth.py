import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=255, description="Email or username")
    password: str = Field(..., min_length=8, max_length=128)


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=128)
    new_password: str = Field(..., min_length=12, max_length=128)

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
