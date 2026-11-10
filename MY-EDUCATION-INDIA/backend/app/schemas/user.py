import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.schemas.role import RoleResponse


class UserDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    document_type: str
    document_title: str
    document_url: str
    file_size_bytes: int
    mime_type: str
    verification_status: str
    verified_by_user_id: Optional[uuid.UUID] = None
    verified_at: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: datetime


class UserDocumentCreateRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=64)
    document_title: str = Field(..., min_length=2, max_length=150)
    document_url: str = Field(..., min_length=5)
    file_size_bytes: int = Field(default=0, ge=0)
    mime_type: str = Field(default="application/pdf", max_length=64)
    remarks: Optional[str] = None


class UserDocumentVerifyRequest(BaseModel):
    verification_status: str = Field(..., pattern=r"^(VERIFIED|REJECTED|PENDING)$")
    remarks: Optional[str] = None


class UserCreateRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=80, pattern=r"^[a-zA-Z0-9_.-]+$")
    phone_number: str = Field(..., min_length=10, max_length=20, pattern=r"^\+?[0-9]{10,15}$")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=10, max_length=128)
    institute_id: uuid.UUID | None = None
    role_ids: List[uuid.UUID] = Field(default_factory=list)
    is_super_admin: bool = False

    # Module 4 Enterprise Attributes
    user_category: str = Field(default="STUDENT", max_length=32)
    department: Optional[str] = Field(default=None, max_length=100)
    designation: Optional[str] = Field(default=None, max_length=100)
    admission_or_emp_id: Optional[str] = Field(default=None, max_length=64)
    dob: Optional[date] = None
    gender: Optional[str] = Field(default=None, max_length=20)
    blood_group: Optional[str] = Field(default=None, max_length=10)
    photo_url: Optional[str] = None
    digital_signature_url: Optional[str] = None
    verification_id_type: Optional[str] = Field(default=None, max_length=50)
    verification_id_number: Optional[str] = Field(default=None, max_length=100)

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


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(default=None, min_length=10, max_length=20)
    user_category: Optional[str] = Field(default=None, max_length=32)
    department: Optional[str] = Field(default=None, max_length=100)
    designation: Optional[str] = Field(default=None, max_length=100)
    admission_or_emp_id: Optional[str] = Field(default=None, max_length=64)
    dob: Optional[date] = None
    gender: Optional[str] = Field(default=None, max_length=20)
    blood_group: Optional[str] = Field(default=None, max_length=10)
    photo_url: Optional[str] = None
    digital_signature_url: Optional[str] = None
    identity_verification_status: Optional[str] = Field(default=None, max_length=32)
    verification_id_type: Optional[str] = Field(default=None, max_length=50)
    verification_id_number: Optional[str] = Field(default=None, max_length=100)
    role_ids: Optional[List[uuid.UUID]] = None
    is_active: Optional[bool] = None


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
    user_category: str = "STUDENT"
    department: Optional[str] = None
    designation: Optional[str] = None
    admission_or_emp_id: Optional[str] = None
    photo_url: Optional[str] = None
    identity_verification_status: str = "PENDING"
    is_archived: bool = False
    institute_id: uuid.UUID | None = None
    last_login_at: datetime | None = None
    created_at: datetime


class UserDetailResponse(UserSummaryResponse):
    dob: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    digital_signature_url: Optional[str] = None
    verification_id_type: Optional[str] = None
    verification_id_number: Optional[str] = None
    archived_at: Optional[datetime] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    roles: List[RoleResponse] = Field(default_factory=list)
    documents: List[UserDocumentResponse] = Field(default_factory=list)


class UserBulkActionRequest(BaseModel):
    user_ids: List[uuid.UUID]
    action: str = Field(..., pattern=r"^(ACTIVATE|DEACTIVATE|ARCHIVE|RESTORE|ASSIGN_ROLE)$")
    role_id: Optional[uuid.UUID] = None


class UserBulkImportItem(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=80)
    phone_number: str = Field(..., min_length=10, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    user_category: str = Field(default="STUDENT", max_length=32)
    department: Optional[str] = None
    designation: Optional[str] = None
    admission_or_emp_id: Optional[str] = None
    gender: Optional[str] = None


class UserBulkImportRequest(BaseModel):
    users: List[UserBulkImportItem]
    default_password: str = Field(default="Welcome@MEI2026", min_length=10)
