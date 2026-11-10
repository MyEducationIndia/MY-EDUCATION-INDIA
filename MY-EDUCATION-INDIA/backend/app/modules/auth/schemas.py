import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ConfigurableLoginRequest(BaseModel):
    identifier: str = Field(..., min_length=2, max_length=255, description="Username, Email, Roll No, ERP ID, Registration No, Enrollment No, or Mobile No")
    password: str = Field(..., min_length=1, max_length=128)
    remember_me: bool = Field(default=False)
    login_criterion: Optional[str] = Field(default=None, description="Explicit criterion used if selected by user e.g. roll_number or erp_id")


class PasswordResetInitiateRequest(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=255)


class PasswordResetConfirmRequest(BaseModel):
    token: str = Field(..., min_length=32, max_length=256)
    new_password: str = Field(..., min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)


class RoleSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    portal_subdomain: str
    is_system_role: bool


class PermissionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    module_key: str
    description: Optional[str] = None


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    username: str
    phone_number: str
    first_name: str
    last_name: str
    registration_number: Optional[str] = None
    enrollment_number: Optional[str] = None
    roll_number: Optional[str] = None
    erp_id: Optional[str] = None
    student_id: Optional[str] = None
    is_active: bool
    is_super_admin: bool
    is_verified: bool
    institute_id: Optional[uuid.UUID] = None
    roles: List[RoleSummary]
    permissions: List[str]
    last_login_at: Optional[datetime] = None


class AuthSessionResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_at: datetime
    csrf_token: str
    user: UserProfileResponse


class ActiveSessionItem(BaseModel):
    id: uuid.UUID
    device_info: str
    ip_address: str
    user_agent: str
    created_at: datetime
    expires_at: datetime
    is_current: bool = False


class LoginHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    identifier_used: str
    login_criterion: str
    status: str
    failure_reason: Optional[str] = None
    ip_address: str
    device_type: str
    browser: str
    os: str
    logged_in_at: datetime
    logged_out_at: Optional[datetime] = None


class SystemAuthSettingsResponse(BaseModel):
    login_criteria: List[str]
    allow_remember_me: bool
    password_min_length: int
    password_require_uppercase: bool
    password_require_lowercase: bool
    password_require_number: bool
    password_require_special: bool
    session_timeout_minutes: int


class UpdateAuthSettingsRequest(BaseModel):
    login_criteria: Optional[List[str]] = None
    allow_remember_me: Optional[bool] = None
    password_min_length: Optional[int] = Field(default=None, ge=8, le=64)
    password_require_uppercase: Optional[bool] = None
    password_require_lowercase: Optional[bool] = None
    password_require_number: Optional[bool] = None
    password_require_special: Optional[bool] = None
    password_expiry_days: Optional[int] = Field(default=None, ge=0, le=365)
    password_history_limit: Optional[int] = Field(default=None, ge=0, le=20)
    max_failed_attempts: Optional[int] = Field(default=None, ge=3, le=20)
    lockout_duration_minutes: Optional[int] = Field(default=None, ge=1, le=1440)
    access_token_expire_minutes: Optional[int] = Field(default=None, ge=5, le=120)
    refresh_token_expire_days: Optional[int] = Field(default=None, ge=1, le=90)
    session_timeout_minutes: Optional[int] = Field(default=None, ge=15, le=1440)


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=80)
    phone_number: str = Field(..., min_length=10, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)
    registration_number: Optional[str] = None
    enrollment_number: Optional[str] = None
    roll_number: Optional[str] = None
    erp_id: Optional[str] = None
    student_id: Optional[str] = None
    role_ids: List[uuid.UUID] = Field(default_factory=list)
    institute_id: Optional[uuid.UUID] = None
    is_super_admin: bool = False


class UpdateUserRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    registration_number: Optional[str] = None
    enrollment_number: Optional[str] = None
    roll_number: Optional[str] = None
    erp_id: Optional[str] = None
    student_id: Optional[str] = None
    is_active: Optional[bool] = None
    role_ids: Optional[List[uuid.UUID]] = None


class AdminResetPasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=8, max_length=128)


class CreateCustomRoleRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=64, pattern=r"^[A-Z0-9_]+$")
    name: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = None
    portal_subdomain: str = Field(default="admin", max_length=32)
    permission_codes: List[str] = Field(default_factory=list)


class AssignRolePermissionsRequest(BaseModel):
    permission_codes: List[str]
