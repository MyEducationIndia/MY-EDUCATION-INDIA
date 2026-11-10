import uuid
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ==================== Department Schemas ====================
class DepartmentCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=32, pattern=r"^[A-Z0-9_-]+$")
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    hod_name: Optional[str] = None
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None


class DepartmentResponse(DepartmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    created_at: datetime


# ==================== Program Schemas ====================
class ProgramCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=120)
    level: str = "UNDERGRADUATE"
    duration_years: float = 3.0
    total_credits: int = 120
    institute_id: uuid.UUID


class ProgramResponse(ProgramCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    created_at: datetime


# ==================== Course Schemas ====================
class CourseCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=32, pattern=r"^[A-Z0-9_-]+$")
    name: str = Field(..., min_length=2, max_length=150)
    duration_months: int = 36
    academic_pattern: str = "SEMESTER"
    total_semesters_or_years: int = 6
    min_intake_capacity: int = 20
    max_intake_capacity: int = 120
    eligibility_criteria: Optional[str] = None
    department_id: uuid.UUID
    program_id: uuid.UUID
    institute_id: uuid.UUID


class CourseResponse(CourseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    created_at: datetime


# ==================== Subject Schemas ====================
class SubjectCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=150)
    subject_type: str = "THEORY"
    credits: float = 4.0
    theory_hours_per_week: int = 3
    practical_hours_per_week: int = 2
    internal_max_marks: int = 30
    external_max_marks: int = 70
    passing_percentage: float = 40.0
    is_lab_required: bool = False
    syllabus_summary: Optional[str] = None
    department_id: Optional[uuid.UUID] = None
    institute_id: uuid.UUID


class SubjectResponse(SubjectCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    created_at: datetime


# ==================== Batch & Section Schemas ====================
class BatchCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=64)
    name: str = Field(..., min_length=2, max_length=150)
    academic_year_code: str = "2026-2027"
    start_date: date
    end_date: date
    intake_capacity: int = 60
    course_id: uuid.UUID
    institute_id: uuid.UUID
    branch_id: uuid.UUID


class BatchResponse(BatchCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    current_strength: int
    is_active: bool
    created_at: datetime


class SectionCreate(BaseModel):
    batch_id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=64)
    capacity: int = 60
    classroom_number: Optional[str] = None
    class_teacher_name: Optional[str] = None


class SectionResponse(SectionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# ==================== Timetable Schemas ====================
class TimetableSlotCreate(BaseModel):
    timetable_id: uuid.UUID
    subject_id: uuid.UUID
    faculty_user_id: Optional[uuid.UUID] = None
    classroom_id: Optional[uuid.UUID] = None
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: time
    end_time: time
    slot_type: str = "LECTURE"


class TimetableSlotResponse(TimetableSlotCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class TimetableCreate(BaseModel):
    institute_id: uuid.UUID
    batch_id: uuid.UUID
    section_id: uuid.UUID
    academic_year_code: str = "2026-2027"


class TimetableResponse(TimetableCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    slots: List[TimetableSlotResponse] = Field(default_factory=list)
    created_at: datetime
