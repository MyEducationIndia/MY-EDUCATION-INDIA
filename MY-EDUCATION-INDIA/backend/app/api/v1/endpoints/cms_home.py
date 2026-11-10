import uuid
from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    require_permissions,
)
from app.schemas.cms_home import (
    CmsFeaturedProgramCreateRequest,
    CmsFeaturedProgramResponse,
    CmsFeaturedProgramUpdateRequest,
    CmsHeroSlideCreateRequest,
    CmsHeroSlideResponse,
    CmsHeroSlideUpdateRequest,
    CmsNewsletterResponse,
    CmsNewsletterSubscribeRequest,
    CmsQuickLinkResponse,
    CmsRecruiterLogoResponse,
    CmsStatCounterCreateRequest,
    CmsStatCounterResponse,
    CmsStatCounterUpdateRequest,
    CmsTestimonialResponse,
    PublicHomePageBundle,
)
from app.services.audit_service import AuditService
from app.services.cms_home_service import CmsHomeService

# Public Router (High-speed zero-login aggregator)
public_home_router = APIRouter(prefix="/public/home", tags=["Public Home Page CMS"])

# Admin Router (Protected by RBAC & Audit Trail)
admin_home_router = APIRouter(prefix="/admin/home", tags=["Admin Home Page Management"])


# =============================================================================
# PUBLIC HOME PAGE ENDPOINTS
# =============================================================================
@public_home_router.get(
    "/bundle",
    response_model=PublicHomePageBundle,
    status_code=status.HTTP_200_OK,
    summary="Fetch complete public home page bundle (Hero slides, Stats, Quick Links, Featured Programs, Recruiters, Testimonials)",
)
async def get_public_home_bundle(
    db: AsyncSession = Depends(get_db_session),
) -> PublicHomePageBundle:
    return await CmsHomeService(db).get_public_home_bundle()


@public_home_router.post(
    "/newsletter/subscribe",
    response_model=CmsNewsletterResponse,
    status_code=status.HTTP_200_OK,
    summary="Public visitor newsletter email subscription",
)
async def subscribe_newsletter(
    payload: CmsNewsletterSubscribeRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CmsNewsletterResponse:
    await CmsHomeService(db).subscribe_newsletter(email=payload.email)
    return CmsNewsletterResponse(
        success=True,
        message="Thank you for subscribing to MY EDUCATION INDIA announcements.",
    )


# =============================================================================
# ADMIN HOME PAGE MANAGEMENT ENDPOINTS
# =============================================================================
# 1. Hero Slides Admin
@admin_home_router.get(
    "/slides",
    response_model=List[CmsHeroSlideResponse],
    status_code=status.HTTP_200_OK,
    summary="List all hero slides",
)
async def list_hero_slides(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsHeroSlideResponse]:
    return await CmsHomeService(db).list_hero_slides()


@admin_home_router.post(
    "/slides",
    response_model=CmsHeroSlideResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a new hero slide",
)
async def create_hero_slide(
    payload: CmsHeroSlideCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsHeroSlideResponse:
    service = CmsHomeService(db)
    created = await service.create_hero_slide(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_HERO_SLIDE_CREATED",
        resource_type="cms_hero_slides",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/home/slides",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_home_router.patch(
    "/slides/{slide_id}",
    response_model=CmsHeroSlideResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update a hero slide",
)
async def update_hero_slide(
    slide_id: uuid.UUID,
    payload: CmsHeroSlideUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsHeroSlideResponse:
    service = CmsHomeService(db)
    updated = await service.update_hero_slide(slide_id, payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_HERO_SLIDE_UPDATED",
        resource_type="cms_hero_slides",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path=f"/api/v1/admin/home/slides/{slide_id}",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


@admin_home_router.delete(
    "/slides/{slide_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete a hero slide",
)
async def delete_hero_slide(
    slide_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = CmsHomeService(db)
    await service.delete_hero_slide(slide_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_HERO_SLIDE_DELETED",
        resource_type="cms_hero_slides",
        resource_id=str(slide_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/home/slides/{slide_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"slide_id": str(slide_id)},
    )


# 2. Stat Counters Admin
@admin_home_router.get(
    "/counters",
    response_model=List[CmsStatCounterResponse],
    status_code=status.HTTP_200_OK,
    summary="List all stats counters",
)
async def list_stat_counters(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsStatCounterResponse]:
    return await CmsHomeService(db).list_stat_counters()


@admin_home_router.post(
    "/counters",
    response_model=CmsStatCounterResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a new stat counter",
)
async def create_stat_counter(
    payload: CmsStatCounterCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsStatCounterResponse:
    service = CmsHomeService(db)
    created = await service.create_stat_counter(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_STAT_COUNTER_CREATED",
        resource_type="cms_stat_counters",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/home/counters",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_home_router.patch(
    "/counters/{counter_id}",
    response_model=CmsStatCounterResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update a stat counter",
)
async def update_stat_counter(
    counter_id: uuid.UUID,
    payload: CmsStatCounterUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsStatCounterResponse:
    service = CmsHomeService(db)
    updated = await service.update_stat_counter(counter_id, payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_STAT_COUNTER_UPDATED",
        resource_type="cms_stat_counters",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path=f"/api/v1/admin/home/counters/{counter_id}",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


@admin_home_router.delete(
    "/counters/{counter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete a stat counter",
)
async def delete_stat_counter(
    counter_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = CmsHomeService(db)
    await service.delete_stat_counter(counter_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_STAT_COUNTER_DELETED",
        resource_type="cms_stat_counters",
        resource_id=str(counter_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/home/counters/{counter_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"counter_id": str(counter_id)},
    )


# 3. Featured Programs Admin
@admin_home_router.get(
    "/programs",
    response_model=List[CmsFeaturedProgramResponse],
    status_code=status.HTTP_200_OK,
    summary="List all featured programs",
)
async def list_featured_programs(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsFeaturedProgramResponse]:
    return await CmsHomeService(db).list_featured_programs()


@admin_home_router.post(
    "/programs",
    response_model=CmsFeaturedProgramResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a new featured program",
)
async def create_featured_program(
    payload: CmsFeaturedProgramCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsFeaturedProgramResponse:
    service = CmsHomeService(db)
    created = await service.create_featured_program(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_FEATURED_PROGRAM_CREATED",
        resource_type="cms_featured_programs",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/home/programs",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_home_router.patch(
    "/programs/{program_id}",
    response_model=CmsFeaturedProgramResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update a featured program",
)
async def update_featured_program(
    program_id: uuid.UUID,
    payload: CmsFeaturedProgramUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsFeaturedProgramResponse:
    service = CmsHomeService(db)
    updated = await service.update_featured_program(program_id, payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_FEATURED_PROGRAM_UPDATED",
        resource_type="cms_featured_programs",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path=f"/api/v1/admin/home/programs/{program_id}",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


@admin_home_router.delete(
    "/programs/{program_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete a featured program",
)
async def delete_featured_program(
    program_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = CmsHomeService(db)
    await service.delete_featured_program(program_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_FEATURED_PROGRAM_DELETED",
        resource_type="cms_featured_programs",
        resource_id=str(program_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/home/programs/{program_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"program_id": str(program_id)},
    )
