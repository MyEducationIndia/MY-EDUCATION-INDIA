import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreateRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=80, pattern=r"^[a-zA-Z0-9_.-]+$")
    phone_number: str = Field(..., min_length=10, max_length=20, pattern=r"^\+?[0-9]{10,15}$")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=12, max_length=128)
    institute_id: uuid.UUID | None = None
    role_ids: List[uuid.UUID] = Field(default_factory=list)
    is_super_admin: bool = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not (
            any(c.isupper() for c in v)
            and any(c.islower() for c in v)
            and any(c.isdigit() for c in v)
            and any(not c.isalnum() for c in v)
        ):
            raise ValueError(
                "Password must contain uppercase, lowercase, numeric, and special characters."
            )
        return v


class UserUpdateStatusRequest(BaseModel):
    is_active: bool
    role_ids: List[uuid.UUID] | None = None


class UserSummaryResponse(BaseModel):
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
    last_login_at: datetime | None
    created_at: datetime
