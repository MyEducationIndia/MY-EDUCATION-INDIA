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
from app.schemas.cms_about import (
    CmsAccreditationCreateRequest,
    CmsAccreditationResponse,
    CmsAccreditationUpdateRequest,
    CmsCampusInfrastructureCreateRequest,
    CmsCampusInfrastructureResponse,
    CmsCampusInfrastructureUpdateRequest,
    CmsLeadershipMessageCreateRequest,
    CmsLeadershipMessageResponse,
    CmsLeadershipMessageUpdateRequest,
    CmsMilestoneCreateRequest,
    CmsMilestoneResponse,
    CmsMilestoneUpdateRequest,
    PublicAboutInstituteBundle,
)
from app.services.audit_service import AuditService
from app.services.cms_about_service import CmsAboutService

# Public Router (High-speed zero-login aggregator)
public_about_router = APIRouter(prefix="/public/about", tags=["Public About Institute CMS"])

# Admin Router (Protected by RBAC & Audit Trail)
admin_about_router = APIRouter(prefix="/admin/about", tags=["Admin About Institute Management"])


# =============================================================================
# PUBLIC ABOUT INSTITUTE ENDPOINTS
# =============================================================================
@public_about_router.get(
    "/bundle",
    response_model=PublicAboutInstituteBundle,
    status_code=status.HTTP_200_OK,
    summary="Fetch complete public about institute bundle (Milestones, Leadership Messages, Accreditations, Infrastructure)",
)
async def get_public_about_bundle(
    db: AsyncSession = Depends(get_db_session),
) -> PublicAboutInstituteBundle:
    return await CmsAboutService(db).get_public_about_bundle()


# =============================================================================
# ADMIN ABOUT INSTITUTE MANAGEMENT ENDPOINTS
# =============================================================================
# 1. Milestones Timeline Admin
@admin_about_router.get(
    "/milestones",
    response_model=List[CmsMilestoneResponse],
    status_code=status.HTTP_200_OK,
    summary="List all timeline milestones",
)
async def list_milestones(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsMilestoneResponse]:
    return await CmsAboutService(db).list_milestones()


@admin_about_router.post(
    "/milestones",
    response_model=CmsMilestoneResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a new timeline milestone",
)
async def create_milestone(
    payload: CmsMilestoneCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsMilestoneResponse:
    service = CmsAboutService(db)
    created = await service.create_milestone(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_MILESTONE_CREATED",
        resource_type="cms_milestones",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/about/milestones",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_about_router.patch(
    "/milestones/{milestone_id}",
    response_model=CmsMilestoneResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update a timeline milestone",
)
async def update_milestone(
    milestone_id: uuid.UUID,
    payload: CmsMilestoneUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsMilestoneResponse:
    service = CmsAboutService(db)
    updated = await service.update_milestone(milestone_id, payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_MILESTONE_UPDATED",
        resource_type="cms_milestones",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path=f"/api/v1/admin/about/milestones/{milestone_id}",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


@admin_about_router.delete(
    "/milestones/{milestone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete a timeline milestone",
)
async def delete_milestone(
    milestone_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = CmsAboutService(db)
    await service.delete_milestone(milestone_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_MILESTONE_DELETED",
        resource_type="cms_milestones",
        resource_id=str(milestone_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/about/milestones/{milestone_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"milestone_id": str(milestone_id)},
    )


# 2. Leadership Messages Admin
@admin_about_router.get(
    "/leadership",
    response_model=List[CmsLeadershipMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="List all leadership messages",
)
async def list_leadership_messages(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsLeadershipMessageResponse]:
    return await CmsAboutService(db).list_leadership_messages()


@admin_about_router.post(
    "/leadership",
    response_model=CmsLeadershipMessageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a leadership message",
)
async def create_leadership_message(
    payload: CmsLeadershipMessageCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsLeadershipMessageResponse:
    service = CmsAboutService(db)
    created = await service.create_leadership_message(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_LEADERSHIP_MESSAGE_CREATED",
        resource_type="cms_leadership_messages",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/about/leadership",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_about_router.patch(
    "/leadership/{message_id}",
    response_model=CmsLeadershipMessageResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update a leadership message",
)
async def update_leadership_message(
    message_id: uuid.UUID,
    payload: CmsLeadershipMessageUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsLeadershipMessageResponse:
    service = CmsAboutService(db)
    updated = await service.update_leadership_message(message_id, payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_LEADERSHIP_MESSAGE_UPDATED",
        resource_type="cms_leadership_messages",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path=f"/api/v1/admin/about/leadership/{message_id}",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


@admin_about_router.delete(
    "/leadership/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete a leadership message",
)
async def delete_leadership_message(
    message_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = CmsAboutService(db)
    await service.delete_leadership_message(message_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_LEADERSHIP_MESSAGE_DELETED",
        resource_type="cms_leadership_messages",
        resource_id=str(message_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/about/leadership/{message_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"message_id": str(message_id)},
    )


# 3. Accreditations Admin
@admin_about_router.get(
    "/accreditations",
    response_model=List[CmsAccreditationResponse],
    status_code=status.HTTP_200_OK,
    summary="List all accreditations and approvals",
)
async def list_accreditations(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsAccreditationResponse]:
    return await CmsAboutService(db).list_accreditations()


@admin_about_router.post(
    "/accreditations",
    response_model=CmsAccreditationResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a new accreditation or approval record",
)
async def create_accreditation(
    payload: CmsAccreditationCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsAccreditationResponse:
    service = CmsAboutService(db)
    created = await service.create_accreditation(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_ACCREDITATION_CREATED",
        resource_type="cms_accreditations",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/about/accreditations",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_about_router.delete(
    "/accreditations/{acc_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete an accreditation record",
)
async def delete_accreditation(
    acc_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = CmsAboutService(db)
    await service.delete_accreditation(acc_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_ACCREDITATION_DELETED",
        resource_type="cms_accreditations",
        resource_id=str(acc_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/about/accreditations/{acc_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"acc_id": str(acc_id)},
    )


# 4. Campus Infrastructure Admin
@admin_about_router.get(
    "/infrastructure",
    response_model=List[CmsCampusInfrastructureResponse],
    status_code=status.HTTP_200_OK,
    summary="List all campus infrastructure facilities",
)
async def list_infrastructure(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[CmsCampusInfrastructureResponse]:
    return await CmsAboutService(db).list_infrastructure()


@admin_about_router.post(
    "/infrastructure",
    response_model=CmsCampusInfrastructureResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a new campus infrastructure facility record",
)
async def create_infrastructure(
    payload: CmsCampusInfrastructureCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> CmsCampusInfrastructureResponse:
    service = CmsAboutService(db)
    created = await service.create_infrastructure(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_INFRASTRUCTURE_CREATED",
        resource_type="cms_campus_infrastructure",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/about/infrastructure",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_about_router.delete(
    "/infrastructure/{infra_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete a campus infrastructure facility record",
)
async def delete_infrastructure(
    infra_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = CmsAboutService(db)
    await service.delete_infrastructure(infra_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="CMS_INFRASTRUCTURE_DELETED",
        resource_type="cms_campus_infrastructure",
        resource_id=str(infra_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/about/infrastructure/{infra_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"infra_id": str(infra_id)},
    )
