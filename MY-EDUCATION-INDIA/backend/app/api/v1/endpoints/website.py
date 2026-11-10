import uuid
from typing import List
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    require_permissions,
)
from app.schemas.website import (
    NavigationMenuCreateRequest,
    NavigationMenuItemResponse,
    NavigationMenuUpdateRequest,
    PublicWebsiteFrameworkBundle,
    SearchResponse,
    WebsiteSettingsResponse,
    WebsiteSettingsUpdateRequest,
    WebsiteThemeResponse,
    WebsiteThemeUpdateRequest,
    WebsiteTickerItemCreateRequest,
    WebsiteTickerItemResponse,
    WebsiteTickerItemUpdateRequest,
)
from app.services.audit_service import AuditService
from app.services.website_service import WebsiteService

# Public Router (Zero Authentication - High Speed CDN Cacheable)
public_website_router = APIRouter(prefix="/public/website", tags=["Public Website Framework"])

# Admin Router (Protected by RBAC & Audit Trail)
admin_website_router = APIRouter(prefix="/admin/website", tags=["Admin Website Governance"])


# =============================================================================
# PUBLIC WEBSITE ENDPOINTS
# =============================================================================
@public_website_router.get(
    "/framework-bundle",
    response_model=PublicWebsiteFrameworkBundle,
    status_code=status.HTTP_200_OK,
    summary="Fetch complete public framework (Settings, Theme, Header Nav, Sticky Ticker, Social Links)",
)
async def get_framework_bundle(
    db: AsyncSession = Depends(get_db_session),
) -> PublicWebsiteFrameworkBundle:
    return await WebsiteService(db).get_public_framework_bundle()


@public_website_router.get(
    "/search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Global public website search across Courses, Notices, News, Events, and Faculty",
)
async def public_global_search(
    q: str = Query(..., min_length=2, max_length=100, description="Search query keyword"),
    limit: int = Query(default=15, ge=1, le=50),
    db: AsyncSession = Depends(get_db_session),
) -> SearchResponse:
    results, total = await WebsiteService(db).global_search(query=q, limit=limit)
    return SearchResponse(query=q, total_results=total, results=results)


# =============================================================================
# ADMIN WEBSITE GOVERNANCE ENDPOINTS
# =============================================================================
@admin_website_router.get(
    "/settings",
    response_model=WebsiteSettingsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current website operational settings",
)
async def get_website_settings(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> WebsiteSettingsResponse:
    bundle = await WebsiteService(db).get_public_framework_bundle()
    return bundle.settings


@admin_website_router.patch(
    "/settings",
    response_model=WebsiteSettingsResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update website operational settings, header toggles, single login button text, and SEO",
)
async def update_website_settings(
    payload: WebsiteSettingsUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> WebsiteSettingsResponse:
    service = WebsiteService(db)
    updated = await service.update_settings(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="WEBSITE_SETTINGS_UPDATED",
        resource_type="website_settings",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path="/api/v1/admin/website/settings",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


@admin_website_router.get(
    "/theme",
    response_model=WebsiteThemeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get website theme configuration",
)
async def get_website_theme(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> WebsiteThemeResponse:
    bundle = await WebsiteService(db).get_public_framework_bundle()
    return bundle.theme


@admin_website_router.patch(
    "/theme",
    response_model=WebsiteThemeResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update website colors, typography, border radius, and shadow styles",
)
async def update_website_theme(
    payload: WebsiteThemeUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> WebsiteThemeResponse:
    service = WebsiteService(db)
    updated = await service.update_theme(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="WEBSITE_THEME_UPDATED",
        resource_type="website_themes",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path="/api/v1/admin/website/theme",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


# -----------------------------------------------------------------------------
# Ticker Admin Endpoints
# -----------------------------------------------------------------------------
@admin_website_router.get(
    "/ticker",
    response_model=List[WebsiteTickerItemResponse],
    status_code=status.HTTP_200_OK,
    summary="List all live ticker announcements",
)
async def list_ticker_announcements(
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[WebsiteTickerItemResponse]:
    return await WebsiteService(db).list_ticker_items()


@admin_website_router.post(
    "/ticker",
    response_model=WebsiteTickerItemResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a new sticky live ticker announcement",
)
async def create_ticker_announcement(
    payload: WebsiteTickerItemCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> WebsiteTickerItemResponse:
    service = WebsiteService(db)
    created = await service.create_ticker_item(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="WEBSITE_TICKER_CREATED",
        resource_type="website_ticker_items",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/website/ticker",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_website_router.patch(
    "/ticker/{item_id}",
    response_model=WebsiteTickerItemResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update a live ticker announcement",
)
async def update_ticker_announcement(
    item_id: uuid.UUID,
    payload: WebsiteTickerItemUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> WebsiteTickerItemResponse:
    service = WebsiteService(db)
    updated = await service.update_ticker_item(item_id, payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="WEBSITE_TICKER_UPDATED",
        resource_type="website_ticker_items",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path=f"/api/v1/admin/website/ticker/{item_id}",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


@admin_website_router.delete(
    "/ticker/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete a live ticker announcement",
)
async def delete_ticker_announcement(
    item_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = WebsiteService(db)
    await service.delete_ticker_item(item_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="WEBSITE_TICKER_DELETED",
        resource_type="website_ticker_items",
        resource_id=str(item_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/website/ticker/{item_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"item_id": str(item_id)},
    )


# -----------------------------------------------------------------------------
# Navigation Menus Admin Endpoints
# -----------------------------------------------------------------------------
@admin_website_router.get(
    "/menus",
    response_model=List[NavigationMenuItemResponse],
    status_code=status.HTTP_200_OK,
    summary="List navigation tree by menu location (HEADER_MAIN, FOOTER_COL_1, etc.)",
)
async def list_navigation_menus(
    location: str = Query(default="HEADER_MAIN"),
    current_user: User = Depends(require_permissions("website:read", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> List[NavigationMenuItemResponse]:
    return await WebsiteService(db).list_navigation_menus(menu_location=location)


@admin_website_router.post(
    "/menus",
    response_model=NavigationMenuItemResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Create a navigation menu node (parent or nested child)",
)
async def create_navigation_menu(
    payload: NavigationMenuCreateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> NavigationMenuItemResponse:
    service = WebsiteService(db)
    created = await service.create_navigation_menu(payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="WEBSITE_MENU_CREATED",
        resource_type="website_navigation_menus",
        resource_id=str(created.id),
        http_method="POST",
        endpoint_path="/api/v1/admin/website/menus",
        status_code=201,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(),
    )
    return created


@admin_website_router.patch(
    "/menus/{menu_id}",
    response_model=NavigationMenuItemResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Update a navigation menu node",
)
async def update_navigation_menu(
    menu_id: uuid.UUID,
    payload: NavigationMenuUpdateRequest,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> NavigationMenuItemResponse:
    service = WebsiteService(db)
    updated = await service.update_navigation_menu(menu_id, payload)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="WEBSITE_MENU_UPDATED",
        resource_type="website_navigation_menus",
        resource_id=str(updated.id),
        http_method="PATCH",
        endpoint_path=f"/api/v1/admin/website/menus/{menu_id}",
        status_code=200,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload=payload.model_dump(exclude_unset=True),
    )
    return updated


@admin_website_router.delete(
    "/menus/{menu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(enforce_csrf_protection)],
    summary="Delete a navigation menu node",
)
async def delete_navigation_menu(
    menu_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("website:write", module_key="website_cms")),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = WebsiteService(db)
    await service.delete_navigation_menu(menu_id)
    await AuditService(db).record_event(
        actor_user_id=current_user.id,
        institute_id=current_user.institute_id,
        module_key="website_cms",
        action="WEBSITE_MENU_DELETED",
        resource_type="website_navigation_menus",
        resource_id=str(menu_id),
        http_method="DELETE",
        endpoint_path=f"/api/v1/admin/website/menus/{menu_id}",
        status_code=204,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
        changes_payload={"menu_id": str(menu_id)},
    )
