import uuid
from typing import List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.admissions.models import (
    AdmissionFeeReceipt,
    AdmissionTimeline,
    Application,
    ApplicationDocument,
    CounsellingSession,
    Lead,
    LeadFollowup,
    Scholarship,
    SeatManagement,
)


class AdmissionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ==================== Leads ====================
    async def create_lead(self, lead: Lead) -> Lead:
        self.session.add(lead)
        await self.session.flush()
        return lead

    async def list_leads_paginated(
        self,
        institute_id: uuid.UUID,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Lead], int]:
        stmt = select(Lead).where(Lead.institute_id == institute_id)
        count_stmt = select(func.count(Lead.id)).where(Lead.institute_id == institute_id)

        if priority:
            stmt = stmt.where(Lead.priority == priority.upper())
            count_stmt = count_stmt.where(Lead.priority == priority.upper())
        if status:
            stmt = stmt.where(Lead.status == status.upper())
            count_stmt = count_stmt.where(Lead.status == status.upper())
        if search:
            pat = f"%{search.strip()}%"
            filter_expr = or_(
                Lead.full_name.ilike(pat),
                Lead.phone_number.ilike(pat),
                Lead.lead_number.ilike(pat),
                Lead.interested_course.ilike(pat),
            )
            stmt = stmt.where(filter_expr)
            count_stmt = count_stmt.where(filter_expr)

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar_one() or 0)

        stmt = stmt.order_by(Lead.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        res = await self.session.execute(stmt)
        return list(res.scalars().all()), total

    # ==================== Applications ====================
    async def create_application(self, application: Application) -> Application:
        self.session.add(application)
        await self.session.flush()
        return application

    async def get_application_by_id(self, application_id: uuid.UUID) -> Optional[Application]:
        stmt = (
            select(Application)
            .options(
                selectinload(Application.documents),
                selectinload(Application.entrance_result),
                selectinload(Application.scholarship),
                selectinload(Application.fees),
                selectinload(Application.timeline),
            )
            .where(Application.id == application_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_applications_paginated(
        self,
        institute_id: uuid.UUID,
        status: Optional[str] = None,
        course_name: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Application], int]:
        stmt = select(Application).where(Application.institute_id == institute_id)
        count_stmt = select(func.count(Application.id)).where(Application.institute_id == institute_id)

        if status:
            stmt = stmt.where(Application.status == status.upper())
            count_stmt = count_stmt.where(Application.status == status.upper())
        if course_name:
            stmt = stmt.where(Application.course_name.ilike(f"%{course_name.strip()}%"))
            count_stmt = count_stmt.where(Application.course_name.ilike(f"%{course_name.strip()}%"))
        if search:
            pat = f"%{search.strip()}%"
            filter_expr = or_(
                Application.application_number.ilike(pat),
                Application.first_name.ilike(pat),
                Application.last_name.ilike(pat),
                Application.email.ilike(pat),
                Application.phone_number.ilike(pat),
            )
            stmt = stmt.where(filter_expr)
            count_stmt = count_stmt.where(filter_expr)

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar_one() or 0)

        stmt = stmt.order_by(Application.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        res = await self.session.execute(stmt)
        return list(res.scalars().all()), total
