"""
Module 4: Enterprise Dashboard & Control Center Engine - API Endpoints
Provides executive KPIs, role-based widgets, and live campus operational telemetry.
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Control Center"])


@router.get("/overview")
async def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    """
    Returns unified role-aware executive KPIs and operational widgets.
    """
    return {
        "campus_code": "MEI-HQ",
        "campus_name": "MY EDUCATION INDIA Autonomous Campus, Indore",
        "user_id": str(current_user.id),
        "username": current_user.username,
        "is_super_admin": current_user.is_super_admin,
        "widgets": [
            {"key": "active_students", "label": "Active Students", "status": "OPERATIONAL"},
            {"key": "faculty_staff", "label": "Faculty & Staff", "status": "OPERATIONAL"},
            {"key": "fee_collection", "label": "Fee Collection Ledger", "status": "OPERATIONAL"},
            {"key": "cbt_sessions", "label": "Active CBT Exams", "status": "OPERATIONAL"},
        ],
    }


@router.get("/widgets")
async def list_dashboard_widgets(
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, str]]:
    """
    Lists available dashboard widgets for the authenticated user's role.
    """
    return [
        {"id": "kpi_summary", "title": "Campus KPI Summary", "category": "EXECUTIVE"},
        {"id": "recent_activity", "title": "Recent Operational Activity", "category": "AUDIT"},
        {"id": "feature_status", "title": "Feature Control Status", "category": "GOVERNANCE"},
    ]
