import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    require_permissions,
)
from app.schemas.cms_courses import (
    CmsCourseCategoryCreateRequest,
    CmsCourseCategoryResponse,
    CmsCourseCategoryUpdateRequest,
    CmsCourseCreateRequest,
    CmsCourseCurriculumCreateRequest,
    CmsCourseCurriculumResponse,
    CmsCourseDetailResponse,
    CmsCourseFacultyCreateRequest,
    CmsCourseFacultyResponse,
    CmsCourseSummaryResponse,
    CmsCourseUpdateRequest,
    PublicCoursesBundle,
)
from app.services.audit_service import AuditService
from app.services.cms_courses_service import CmsCoursesService

# Public Router (Zero-Login High-Speed Aggregator)
public_courses_router = APIRouter(prefix="/public/courses", tags=["Public Courses CMS"])

# Admin Router (Protected by RBAC & Audit Trails)
admin_courses_router = APIRouter(prefix="/admin/courses", tags=["Admin Course Management"])


# =============================================================================
# PUBLIC COURSES ENDPOINTS
# =============================================================================
@public_courses_router.get(
    "/bundle",
    response_model=PublicCoursesBundle,
    status_code=status.HTTP_200_OK,
    summary="Fetch public course catalog bundle with optional filters (category, degree, search)",
)
async def get_public_courses_bundle(
    category_slug: Optional[str] = Query(None, description="Filter by category slug"),
    degree_level: Optional[str] = Query(None, description="Filter by degree level (e.g. UNDERGRADUATE, POSTGRADUATE)"),
    q: Optional[str] = Query(None, description="Free text course search query"),
    db: AsyncSession = Depends(get_db_session),
) -> PublicCoursesBundle:
    return await CmsCoursesService(db).get_public_courses_bundle(
        category_slug=category_slug,
        degree_level=degree_level,
        search_query=q,
    )


@public_courses_router.get(
    "/detail/{slug}",
    response_model=CmsCourseDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch comprehensive course profile by URL slug (Overview, Curricula, Faculty)",
)
async def get_public_course_detail(
    slug: str,
    db: AsyncSession = Depends(get_db_session),
) -> CmsCourseDetailResponse:
    return await CmsCoursesService(db).get_course_by_slug(slug)


# =============================================================================
# ADMIN COURSE CATEGORIES ENDPOINTS
# =============================================================================
@admin_courses_router.get(
    "/categories",
    response_model=List[CmsCourseCategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="List all course categories",
    dependencies=[Depends(require_permissions(["institutes:read", "modules:toggle"]))],
)
async def list_admin_categories(
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsCourseCategoryResponse]:
    return await CmsCoursesService(db).list_admin_categories()


@admin_courses_router.post(
    "/categories",
    response_model=CmsCourseCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new course category",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def create_admin_category(
    payload: CmsCourseCategoryCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions(["institutes:write"])),
    db: AsyncSession = Depends(get_db_session),
) -> CmsCourseCategoryResponse:
    created = await CmsCoursesService(db).create_category(payload)
    await AuditService(db).log_action(
        user=current_user,
        action="CMS_COURSE_CATEGORY_CREATED",
        entity_name="cms_course_categories",
        entity_id=created.id,
        new_values=payload.model_dump(),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return created


@admin_courses_router.patch(
    "/categories/{category_id}",
    response_model=CmsCourseCategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing course category",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def update_admin_category(
    category_id: uuid.UUID,
    payload: CmsCourseCategoryUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions(["institutes:write"])),
    db: AsyncSession = Depends(get_db_session),
) -> CmsCourseCategoryResponse:
    updated = await CmsCoursesService(db).update_category(category_id, payload)
    await AuditService(db).log_action(
        user=current_user,
        action="CMS_COURSE_CATEGORY_UPDATED",
        entity_name="cms_course_categories",
        entity_id=category_id,
        new_values=payload.model_dump(exclude_unset=True),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return updated


@admin_courses_router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a course category",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def delete_admin_category(
    category_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions(["institutes:write"])),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    await CmsCoursesService(db).delete_category(category_id)
    await AuditService(db).log_action(
        user=current_user,
        action="CMS_COURSE_CATEGORY_DELETED",
        entity_name="cms_course_categories",
        entity_id=category_id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )


# =============================================================================
# ADMIN COURSES ENDPOINTS
# =============================================================================
@admin_courses_router.get(
    "/",
    response_model=List[CmsCourseSummaryResponse],
    status_code=status.HTTP_200_OK,
    summary="List all degree courses",
    dependencies=[Depends(require_permissions(["institutes:read", "modules:toggle"]))],
)
async def list_admin_courses(
    category_id: Optional[uuid.UUID] = Query(None, description="Optional category filter"),
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsCourseSummaryResponse]:
    return await CmsCoursesService(db).list_admin_courses(category_id=category_id)


@admin_courses_router.get(
    "/{course_id}",
    response_model=CmsCourseDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get course detail by ID",
    dependencies=[Depends(require_permissions(["institutes:read"]))],
)
async def get_admin_course_detail(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> CmsCourseDetailResponse:
    return await CmsCoursesService(db).get_admin_course_detail(course_id)


@admin_courses_router.post(
    "/",
    response_model=CmsCourseDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new degree course",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def create_admin_course(
    payload: CmsCourseCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions(["institutes:write"])),
    db: AsyncSession = Depends(get_db_session),
) -> CmsCourseDetailResponse:
    created = await CmsCoursesService(db).create_course(payload)
    await AuditService(db).log_action(
        user=current_user,
        action="CMS_COURSE_CREATED",
        entity_name="cms_courses",
        entity_id=created.id,
        new_values=payload.model_dump(mode="json"),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return created


@admin_courses_router.patch(
    "/{course_id}",
    response_model=CmsCourseDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing course",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def update_admin_course(
    course_id: uuid.UUID,
    payload: CmsCourseUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions(["institutes:write"])),
    db: AsyncSession = Depends(get_db_session),
) -> CmsCourseDetailResponse:
    updated = await CmsCoursesService(db).update_course(course_id, payload)
    await AuditService(db).log_action(
        user=current_user,
        action="CMS_COURSE_UPDATED",
        entity_name="cms_courses",
        entity_id=course_id,
        new_values=payload.model_dump(exclude_unset=True, mode="json"),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return updated


@admin_courses_router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a course",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def delete_admin_course(
    course_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions(["institutes:write"])),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    await CmsCoursesService(db).delete_course(course_id)
    await AuditService(db).log_action(
        user=current_user,
        action="CMS_COURSE_DELETED",
        entity_name="cms_courses",
        entity_id=course_id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )


# =============================================================================
# CURRICULUM & FACULTY SUB-ENDPOINTS
# =============================================================================
@admin_courses_router.post(
    "/{course_id}/curricula",
    response_model=CmsCourseCurriculumResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add curriculum semester to course",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def add_course_curriculum(
    course_id: uuid.UUID,
    payload: CmsCourseCurriculumCreateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CmsCourseCurriculumResponse:
    return await CmsCoursesService(db).add_curriculum_semester(course_id, payload)


@admin_courses_router.delete(
    "/curricula/{curriculum_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete curriculum semester",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def delete_course_curriculum(
    curriculum_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    await CmsCoursesService(db).delete_curriculum_semester(curriculum_id)


@admin_courses_router.post(
    "/{course_id}/faculty",
    response_model=CmsCourseFacultyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add faculty member to course",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def add_course_faculty(
    course_id: uuid.UUID,
    payload: CmsCourseFacultyCreateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CmsCourseFacultyResponse:
    return await CmsCoursesService(db).add_course_faculty(course_id, payload)


@admin_courses_router.delete(
    "/faculty/{faculty_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete faculty member from course",
    dependencies=[
        Depends(require_permissions(["institutes:write"])),
        Depends(enforce_csrf_protection),
    ],
)
async def delete_course_faculty(
    faculty_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    await CmsCoursesService(db).delete_course_faculty(faculty_id)
