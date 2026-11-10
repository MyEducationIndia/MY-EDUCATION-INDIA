import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.modules.academics.models import Batch, Course, Department, Program, Subject, Timetable
from app.modules.academics.schemas import (
    BatchCreate,
    BatchResponse,
    CourseCreate,
    CourseResponse,
    DepartmentCreate,
    DepartmentResponse,
    ProgramCreate,
    ProgramResponse,
    SectionCreate,
    SectionResponse,
    SubjectCreate,
    SubjectResponse,
    TimetableCreate,
    TimetableResponse,
    TimetableSlotCreate,
    TimetableSlotResponse,
)
from app.modules.academics.service import AcademicManagementService
from app.modules.auth.dependencies import enforce_csrf, get_current_user, require_permissions
from app.modules.auth.models import User

router = academic_router = APIRouter(prefix="/academics", tags=["Enterprise Academic Management System"])


# ==================== Departments ====================
@academic_router.get("/departments", response_model=List[DepartmentResponse])
async def list_departments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[DepartmentResponse]:
    if not current_user.institute_id:
        return []
    service = AcademicManagementService(db)
    depts = await service.repo.list_departments(current_user.institute_id)
    return [DepartmentResponse.model_validate(d) for d in depts]


@academic_router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_department(
    payload: DepartmentCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> DepartmentResponse:
    service = AcademicManagementService(db)
    dept = await service.create_department(payload)
    return DepartmentResponse.model_validate(dept)


# ==================== Programs & Courses ====================
@academic_router.get("/programs", response_model=List[ProgramResponse])
async def list_programs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[ProgramResponse]:
    if not current_user.institute_id:
        return []
    service = AcademicManagementService(db)
    progs = await service.repo.list_programs(current_user.institute_id)
    return [ProgramResponse.model_validate(p) for p in progs]


@academic_router.post("/programs", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_program(
    payload: ProgramCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> ProgramResponse:
    service = AcademicManagementService(db)
    prog = await service.create_program(payload)
    return ProgramResponse.model_validate(prog)


@academic_router.get("/courses", response_model=List[CourseResponse])
async def list_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[CourseResponse]:
    if not current_user.institute_id:
        return []
    service = AcademicManagementService(db)
    courses = await service.repo.list_courses(current_user.institute_id)
    return [CourseResponse.model_validate(c) for c in courses]


@academic_router.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_course(
    payload: CourseCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> CourseResponse:
    service = AcademicManagementService(db)
    course = await service.create_course(payload)
    return CourseResponse.model_validate(course)


# ==================== Subjects ====================
@academic_router.get("/subjects", response_model=List[SubjectResponse])
async def list_subjects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[SubjectResponse]:
    if not current_user.institute_id:
        return []
    service = AcademicManagementService(db)
    subjects = await service.repo.list_subjects(current_user.institute_id)
    return [SubjectResponse.model_validate(s) for s in subjects]


@academic_router.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_subject(
    payload: SubjectCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> SubjectResponse:
    service = AcademicManagementService(db)
    subject = await service.create_subject(payload)
    return SubjectResponse.model_validate(subject)


# ==================== Batches & Sections ====================
@academic_router.get("/batches", response_model=List[BatchResponse])
async def list_batches(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[BatchResponse]:
    if not current_user.institute_id:
        return []
    service = AcademicManagementService(db)
    batches = await service.repo.list_batches(current_user.institute_id)
    return [BatchResponse.model_validate(b) for b in batches]


@academic_router.post("/batches", response_model=BatchResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_batch(
    payload: BatchCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> BatchResponse:
    service = AcademicManagementService(db)
    batch = await service.create_batch(payload)
    return BatchResponse.model_validate(batch)


# ==================== Timetable ====================
@academic_router.get("/timetable", response_model=Optional[TimetableResponse])
async def get_timetable(
    batch_id: uuid.UUID = Query(...),
    section_id: uuid.UUID = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Optional[TimetableResponse]:
    service = AcademicManagementService(db)
    tt = await service.repo.get_timetable_by_batch_section(batch_id, section_id)
    return TimetableResponse.model_validate(tt) if tt else None


@academic_router.post("/timetable/slots", response_model=TimetableSlotResponse, dependencies=[Depends(enforce_csrf)])
async def add_timetable_slot(
    payload: TimetableSlotCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> TimetableSlotResponse:
    service = AcademicManagementService(db)
    slot = await service.add_timetable_slot(payload)
    return TimetableSlotResponse.model_validate(slot)
