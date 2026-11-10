"""
Module 18: BI SQLAlchemy 2.x Async Repository
"""
from typing import List, Optional
from datetime import datetime, date
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.modules.bi.models import (
    ReportDefinition, ReportTemplate, ReportSchedule,
    DashboardWidget, DashboardLayout, KpiDefinition,
    SystemHealthLog, ExportHistory, ChartDefinition
)

class BiRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_report_definition(self, institute_id: str, data: dict) -> ReportDefinition:
        rid = str(uuid.uuid4())
        report = ReportDefinition(id=rid, institute_id=institute_id, **data)
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def list_reports(self, institute_id: str, category: Optional[str] = None) -> List[ReportDefinition]:
        stmt = select(ReportDefinition).where(ReportDefinition.institute_id == institute_id)
        if category:
            stmt = stmt.where(ReportDefinition.category == category)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_kpi(self, institute_id: str, data: dict) -> KpiDefinition:
        kid = str(uuid.uuid4())
        kpi = KpiDefinition(id=kid, institute_id=institute_id, **data)
        self.session.add(kpi)
        await self.session.commit()
        await self.session.refresh(kpi)
        return kpi

    async def list_kpis(self, institute_id: str) -> List[KpiDefinition]:
        res = await self.session.execute(
            select(KpiDefinition).where(KpiDefinition.institute_id == institute_id)
        )
        return list(res.scalars().all())
