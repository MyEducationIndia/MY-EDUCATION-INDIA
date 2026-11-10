import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.modules.auth.dependencies import enforce_csrf, get_current_user
from app.modules.auth.models import User
from app.modules.dashboard.notifications import NotificationService
from app.modules.dashboard.schemas import (
    ActivityItemResponse,
    DashboardKPIStatistics,
    GlobalSearchResponse,
    MultiChartAnalyticsResponse,
    NotificationCreateRequest,
    NotificationItemResponse,
    SystemHealthResponse,
    UpdateWidgetsBatchRequest,
    WidgetConfigItem,
)
from app.modules.dashboard.service import DashboardService

dashboard_router = APIRouter(prefix="/dashboard", tags=["Enterprise Admin Dashboard & Control Center"])


@dashboard_router.get("", response_model=Dict[str, Any])
async def get_dashboard_summary(
    granularity: str = Query(default="MONTHLY"),
    institute_id: Optional[uuid.UUID] = Query(default=None),
    branch_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    """Unified high-speed dashboard bootstrap API returning stats, charts, widgets, and timeline in one pass."""
    service = DashboardService(db)
    eff_inst = institute_id or current_user.institute_id

    kpi_stats = await service.get_dashboard_kpis(eff_inst, branch_id)
    charts = await service.get_analytics_charts(granularity, eff_inst)
    widgets = await service.get_user_widgets(current_user)
    activities = await service.get_recent_activities(eff_inst, limit=8)
    notifications = await NotificationService.get_user_notifications(db, current_user.id, eff_inst, unread_only=True, limit=5)
    health = await service.get_system_health()

    return {
        "kpi_stats": kpi_stats.model_dump(),
        "charts": charts.model_dump(),
        "widgets": [w.model_dump() for w in widgets],
        "activities": [a.model_dump() for a in activities],
        "notifications": [NotificationItemResponse.model_validate(n).model_dump() for n in notifications],
        "system_health": health.model_dump(),
    }


@dashboard_router.get("/stats", response_model=DashboardKPIStatistics)
async def get_dashboard_stats(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    branch_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> DashboardKPIStatistics:
    service = DashboardService(db)
    eff_inst = institute_id or current_user.institute_id
    return await service.get_dashboard_kpis(eff_inst, branch_id)


@dashboard_router.get("/charts", response_model=MultiChartAnalyticsResponse)
async def get_dashboard_charts(
    granularity: str = Query(default="MONTHLY", pattern=r"^(DAILY|WEEKLY|MONTHLY|YEARLY|CUSTOM)$"),
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MultiChartAnalyticsResponse:
    service = DashboardService(db)
    eff_inst = institute_id or current_user.institute_id
    return await service.get_analytics_charts(granularity, eff_inst)


@dashboard_router.get("/widgets", response_model=List[WidgetConfigItem])
async def get_dashboard_widgets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[WidgetConfigItem]:
    service = DashboardService(db)
    return await service.get_user_widgets(current_user)


@dashboard_router.put("/widgets", response_model=List[WidgetConfigItem], dependencies=[Depends(enforce_csrf)])
async def update_dashboard_widgets(
    payload: UpdateWidgetsBatchRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[WidgetConfigItem]:
    service = DashboardService(db)
    return await service.update_user_widgets(current_user, payload.widgets)


@dashboard_router.get("/search", response_model=GlobalSearchResponse)
async def global_erp_search(
    q: str = Query(..., min_length=2, max_length=120),
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> GlobalSearchResponse:
    service = DashboardService(db)
    eff_inst = institute_id or current_user.institute_id
    return await service.execute_global_search(q, eff_inst)


@dashboard_router.get("/activities", response_model=List[ActivityItemResponse])
async def get_activity_feed(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[ActivityItemResponse]:
    service = DashboardService(db)
    eff_inst = institute_id or current_user.institute_id
    return await service.get_recent_activities(eff_inst, limit)


@dashboard_router.get("/notifications", response_model=List[NotificationItemResponse])
async def list_notifications(
    unread_only: bool = Query(default=False),
    limit: int = Query(default=30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[NotificationItemResponse]:
    notifications = await NotificationService.get_user_notifications(
        db, current_user.id, current_user.institute_id, unread_only, limit
    )
    return [NotificationItemResponse.model_validate(n) for n in notifications]


@dashboard_router.post("/notifications", response_model=NotificationItemResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_notification(
    payload: NotificationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> NotificationItemResponse:
    notif = await NotificationService.create_notification(db, payload)
    return NotificationItemResponse.model_validate(notif)


@dashboard_router.patch("/notifications/{notification_id}/read", response_model=NotificationItemResponse, dependencies=[Depends(enforce_csrf)])
async def mark_notification_read(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> NotificationItemResponse:
    notif = await NotificationService.mark_as_read(db, notification_id)
    if not notif:
        raise ValueError("Notification not found")
    return NotificationItemResponse.model_validate(notif)


@dashboard_router.post("/notifications/read-all", dependencies=[Depends(enforce_csrf)])
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    count = await NotificationService.mark_all_as_read(db, current_user.id, current_user.institute_id)
    return {"success": True, "marked_count": count}


@dashboard_router.get("/system-health", response_model=SystemHealthResponse)
async def get_system_health(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> SystemHealthResponse:
    service = DashboardService(db)
    return await service.get_system_health()
