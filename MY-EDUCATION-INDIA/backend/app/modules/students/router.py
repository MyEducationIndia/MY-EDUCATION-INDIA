import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.modules.auth.dependencies import enforce_csrf, get_current_user, require_permissions
from app.modules.auth.models import User
from app.modules.students.import_export import StudentImportExportProcessor
from app.modules.students.schemas import (
    StudentBulkDeleteRequest,
    StudentCustomFieldCreate,
    StudentCustomFieldResponse,
    StudentDetailedProfileResponse,
    StudentPromotionRequest,
    StudentRegisterRequest,
    StudentSearchQuery,
    StudentStatusChangeRequest,
    StudentSummaryResponse,
    StudentUpdateRequest,
)
from app.modules.students.service import StudentManagementService

student_router = APIRouter(prefix="/students", tags=["Enterprise Student Information Management System (SIMS)"])


@student_router.get("", response_model=Dict[str, Any])
async def search_students(
    query: Optional[str] = Query(default=None),
    course_name: Optional[str] = Query(default=None),
    batch_name: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    branch_id: Optional[uuid.UUID] = Query(default=None),
    academic_year_code: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(require_permissions("student.view")),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    if not current_user.institute_id:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}

    service = StudentManagementService(db)
    items, total = await service.repo.search_students_paginated(
        institute_id=current_user.institute_id,
        query=query,
        course_name=course_name,
        batch_name=batch_name,
        status=status,
        branch_id=branch_id,
        academic_year_code=academic_year_code,
        page=page,
        page_size=page_size,
    )
    return {
        "items": [StudentSummaryResponse.model_validate(s).model_dump() for s in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@student_router.post("", response_model=StudentDetailedProfileResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def register_student(
    payload: StudentRegisterRequest,
    current_user: User = Depends(require_permissions("student.create")),
    db: AsyncSession = Depends(get_db_session),
) -> StudentDetailedProfileResponse:
    service = StudentManagementService(db)
    actor_label = f"{current_user.first_name} {current_user.last_name}"
    return await service.register_student(payload, actor_name=actor_label)


@student_router.get("/{student_id}", response_model=StudentDetailedProfileResponse)
async def get_student_profile(
    student_id: uuid.UUID,
    current_user: User = Depends(require_permissions("student.view")),
    db: AsyncSession = Depends(get_db_session),
) -> StudentDetailedProfileResponse:
    service = StudentManagementService(db)
    return await service.get_student_profile(student_id)


@student_router.patch("/{student_id}/status", response_model=StudentSummaryResponse, dependencies=[Depends(enforce_csrf)])
async def change_student_status(
    student_id: uuid.UUID,
    payload: StudentStatusChangeRequest,
    current_user: User = Depends(require_permissions("student.edit")),
    db: AsyncSession = Depends(get_db_session),
) -> StudentSummaryResponse:
    service = StudentManagementService(db)
    actor_label = f"{current_user.first_name} {current_user.last_name}"
    return await service.change_student_status(student_id, payload, actor_name=actor_label, user_id=current_user.id)


@student_router.post("/promote", dependencies=[Depends(enforce_csrf)])
async def bulk_promote_students(
    payload: StudentPromotionRequest,
    current_user: User = Depends(require_permissions("student.edit")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = StudentManagementService(db)
    actor_label = f"{current_user.first_name} {current_user.last_name}"
    promoted_count = await service.bulk_promote_students(payload, actor_name=actor_label)
    return {"success": True, "promoted_count": promoted_count}


@student_router.post("/bulk-delete", dependencies=[Depends(enforce_csrf)])
async def bulk_delete_students(
    payload: StudentBulkDeleteRequest,
    current_user: User = Depends(require_permissions("student.delete")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = StudentManagementService(db)
    actor_label = f"{current_user.first_name} {current_user.last_name}"
    deleted_count = await service.bulk_soft_delete(payload.student_ids, actor_name=actor_label)
    return {"success": True, "deleted_count": deleted_count}


@student_router.get("/template/csv", response_class=Response)
async def download_import_template() -> Response:
    csv_text = StudentImportExportProcessor.generate_csv_template()
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="students_import_template.csv"'},
    )


@student_router.get("/custom-fields", response_model=List[StudentCustomFieldResponse])
async def list_custom_fields(
    current_user: User = Depends(require_permissions("student.view")),
    db: AsyncSession = Depends(get_db_session),
) -> List[StudentCustomFieldResponse]:
    service = StudentManagementService(db)
    if not current_user.institute_id:
        return []
    fields = await service.repo.list_custom_fields(current_user.institute_id)
    return [StudentCustomFieldResponse.model_validate(f) for f in fields]


@student_router.post("/custom-fields", response_model=StudentCustomFieldResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_custom_field(
    payload: StudentCustomFieldCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> StudentCustomFieldResponse:
    service = StudentManagementService(db)
    field = await service.repo.save_custom_field(StudentCustomField(**payload.model_dump()))
    await db.commit()
    await db.refresh(field)
    return StudentCustomFieldResponse.model_validate(field)
