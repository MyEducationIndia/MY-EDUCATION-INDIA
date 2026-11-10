import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.models import LoginHistory, Role, User
from app.modules.dashboard.models import DashboardActivity, DashboardWidget, UserPinnedModule
from app.modules.system.models import AcademicYear, Branch, FinancialYear, Institute, NumberGenerator


class DashboardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ==================== Dashboard Activities ====================
    async def record_activity(self, activity: DashboardActivity) -> DashboardActivity:
        self.session.add(activity)
        await self.session.flush()
        return activity

    async def list_recent_activities(
        self,
        institute_id: Optional[uuid.UUID],
        limit: int = 15,
    ) -> List[DashboardActivity]:
        stmt = select(DashboardActivity)
        if institute_id:
            stmt = stmt.where((DashboardActivity.institute_id == institute_id) | (DashboardActivity.institute_id.is_(None)))
        stmt = stmt.order_by(DashboardActivity.occurred_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Dashboard Widgets ====================
    async def get_user_widgets(self, user_id: uuid.UUID) -> List[DashboardWidget]:
        stmt = (
            select(DashboardWidget)
            .where(DashboardWidget.user_id == user_id)
            .order_by(DashboardWidget.grid_position.asc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def save_user_widget(self, widget: DashboardWidget) -> DashboardWidget:
        self.session.add(widget)
        await self.session.flush()
        return widget

    # ==================== Recent Logins ====================
    async def list_recent_logins(
        self,
        institute_id: Optional[uuid.UUID],
        limit: int = 10,
    ) -> List[LoginHistory]:
        stmt = select(LoginHistory)
        if institute_id:
            stmt = stmt.where((LoginHistory.institute_id == institute_id) | (LoginHistory.institute_id.is_(None)))
        stmt = stmt.order_by(LoginHistory.logged_in_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Global Multi-Entity Search ====================
    async def search_users(self, query: str, institute_id: Optional[uuid.UUID], limit: int = 5) -> List[User]:
        pat = f"%{query.strip()}%"
        stmt = select(User).where(
            or_(
                User.first_name.ilike(pat),
                User.last_name.ilike(pat),
                User.email.ilike(pat),
                User.username.ilike(pat),
                User.roll_number.ilike(pat),
                User.erp_id.ilike(pat),
            )
        )
        if institute_id:
            stmt = stmt.where(User.institute_id == institute_id)
        stmt = stmt.limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def search_branches(self, query: str, institute_id: Optional[uuid.UUID], limit: int = 5) -> List[Branch]:
        pat = f"%{query.strip()}%"
        stmt = select(Branch).where(
            or_(
                Branch.name.ilike(pat),
                Branch.code.ilike(pat),
                Branch.city.ilike(pat),
            )
        )
        if institute_id:
            stmt = stmt.where(Branch.institute_id == institute_id)
        stmt = stmt.limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def search_number_generators(self, query: str, institute_id: Optional[uuid.UUID], limit: int = 5) -> List[NumberGenerator]:
        pat = f"%{query.strip()}%"
        stmt = select(NumberGenerator).where(
            or_(
                NumberGenerator.name.ilike(pat),
                NumberGenerator.entity_type.ilike(pat),
                NumberGenerator.prefix.ilike(pat),
            )
        )
        if institute_id:
            stmt = stmt.where(NumberGenerator.institute_id == institute_id)
        stmt = stmt.limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
