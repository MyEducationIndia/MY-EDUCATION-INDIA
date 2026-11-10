import uuid
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==================== Multi-Branch ====================
class BranchBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=32, pattern=r"^[A-Z0-9_-]+$")
    name: str = Field(..., min_length=2, max_length=255)
    address_line1: str = Field(..., min_length=3, max_length=255)
    address_line2: Optional[str] = None
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=4, max_length=20)
    phone: str = Field(..., min_length=8, max_length=32)
    email: EmailStr
    principal_name: Optional[str] = None
    logo_url: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    is_main_branch: bool = False
    is_active: bool = True


class BranchCreate(BranchBase):
    institute_id: uuid.UUID


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    principal_name: Optional[str] = None
    logo_url: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    is_main_branch: Optional[bool] = None
    is_active: Optional[bool] = None


class BranchResponse(BranchBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ==================== Academic Years ====================
class AcademicYearBase(BaseModel):
    code: str = Field(..., min_length=4, max_length=32) # e.g. 2026-2027
    name: str = Field(..., min_length=2, max_length=120)
    start_date: date
    end_date: date
    is_current: bool = False
    is_locked: bool = False


class AcademicYearCreate(AcademicYearBase):
    institute_id: uuid.UUID


class AcademicYearUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    is_locked: Optional[bool] = None


class AcademicYearResponse(AcademicYearBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ==================== Financial Years ====================
class FinancialYearBase(BaseModel):
    code: str = Field(..., min_length=4, max_length=32) # e.g. FY2026-27
    name: str = Field(..., min_length=2, max_length=120)
    start_date: date
    end_date: date
    is_current: bool = False
    is_closed: bool = False
    gstin: Optional[str] = None


class FinancialYearCreate(FinancialYearBase):
    institute_id: uuid.UUID


class FinancialYearUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    is_closed: Optional[bool] = None
    gstin: Optional[str] = None


class FinancialYearResponse(FinancialYearBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ==================== Number Generator ====================
class NumberGeneratorBase(BaseModel):
    entity_type: str = Field(..., min_length=2, max_length=64)
    name: str = Field(..., min_length=2, max_length=150)
    prefix: Optional[str] = "MEI"
    suffix: Optional[str] = None
    format_template: str = Field(default="{PREFIX}-{YEAR}-{NUMBER}", max_length=150)
    separator: str = Field(default="-", max_length=4)
    padding_length: int = Field(default=6, ge=3, le=12)
    reset_rule: str = Field(default="YEARLY", pattern=r"^(NEVER|YEARLY|ACADEMIC_YEAR|FINANCIAL_YEAR|MONTHLY|BRANCH)$")
    is_active: bool = True


class NumberGeneratorCreate(NumberGeneratorBase):
    institute_id: uuid.UUID


class NumberGeneratorUpdate(BaseModel):
    name: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    format_template: Optional[str] = None
    separator: Optional[str] = None
    padding_length: Optional[int] = Field(default=None, ge=3, le=12)
    reset_rule: Optional[str] = None
    is_active: Optional[bool] = None


class NumberGeneratorResponse(NumberGeneratorBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class NumberPreviewRequest(BaseModel):
    prefix: Optional[str] = "MEI"
    suffix: Optional[str] = None
    format_template: str = "{PREFIX}-{YEAR}-{NUMBER}"
    separator: str = "-"
    padding_length: int = 6
    sample_number: int = 123
    institute_code: Optional[str] = "MEI"
    branch_code: Optional[str] = "BPL"
    course_code: Optional[str] = "BTECH"
    dept_code: Optional[str] = "CSE"
    year: Optional[int] = 2027
    month: Optional[int] = 6


class NumberGenerateRequest(BaseModel):
    entity_type: str
    institute_id: uuid.UUID
    branch_code: Optional[str] = None
    course_code: Optional[str] = None
    dept_code: Optional[str] = None
    academic_year_code: Optional[str] = None
    financial_year_code: Optional[str] = None


# ==================== Holidays & Working Days ====================
class HolidayCreate(BaseModel):
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    name: str = Field(..., min_length=2, max_length=150)
    holiday_date: date
    holiday_type: str = Field(default="NATIONAL", pattern=r"^(NATIONAL|INSTITUTE|BRANCH|OPTIONAL)$")
    description: Optional[str] = None


class HolidayResponse(HolidayCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class WorkingDayUpdateItem(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    day_name: str
    is_working_day: bool
    start_time: Optional[time] = None
    end_time: Optional[time] = None


class WorkingDaysBatchUpdate(BaseModel):
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    days: List[WorkingDayUpdateItem]


class WorkingDayResponse(WorkingDayUpdateItem):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None


# ==================== System Settings & Organization ====================
class SettingSaveRequest(BaseModel):
    category: str = Field(..., min_length=2, max_length=64)
    key: str = Field(..., min_length=2, max_length=100)
    value: Dict[str, Any]
    description: Optional[str] = None
    is_public: bool = False
    institute_id: Optional[uuid.UUID] = None


class SettingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    category: str
    key: str
    value: Dict[str, Any]
    description: Optional[str] = None
    is_public: bool
    institute_id: Optional[uuid.UUID] = None
    updated_at: datetime


class OrganizationSettingsUpdate(BaseModel):
    default_currency: Optional[str] = None
    default_language: Optional[str] = None
    default_timezone: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
    fiscal_year_start_month: Optional[int] = Field(default=None, ge=1, le=12)
    academic_year_start_month: Optional[int] = Field(default=None, ge=1, le=12)
    sidebar_style: Optional[str] = None


class OrganizationSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institute_id: uuid.UUID
    default_currency: str
    default_language: str
    default_timezone: str
    date_format: str
    time_format: str
    fiscal_year_start_month: int
    academic_year_start_month: int
    sidebar_style: str
