"""
Module 17: CRM SQLAlchemy 2.x Async Repository
"""
from typing import List, Optional
from datetime import datetime, date
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.modules.crm.models import (
    CrmLead, CrmEnquiry, CrmFollowup, CrmPipeline,
    CrmCampaign, CrmCampaignResult, CrmReferral, CrmTask,
    CrmOpportunity, FranchiseCenter
)

class CrmRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_lead(self, institute_id: str, data: dict) -> CrmLead:
        lid = str(uuid.uuid4())
        lead_code = f"LEAD-{lid[:6].upper()}"
        lead = CrmLead(id=lid, institute_id=institute_id, lead_code=lead_code, **data)
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)
        return lead

    async def list_leads(self, institute_id: str, stage: Optional[str] = None) -> List[CrmLead]:
        stmt = select(CrmLead).where(CrmLead.institute_id == institute_id)
        if stage:
            stmt = stmt.where(CrmLead.stage == stage)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_enquiry(self, institute_id: str, data: dict) -> CrmEnquiry:
        eid = str(uuid.uuid4())
        enquiry_code = f"ENQ-{eid[:6].upper()}"
        enq = CrmEnquiry(id=eid, institute_id=institute_id, enquiry_code=enquiry_code, **data)
        self.session.add(enq)
        await self.session.commit()
        await self.session.refresh(enq)
        return enq

    async def list_enquiries(self, institute_id: str) -> List[CrmEnquiry]:
        res = await self.session.execute(
            select(CrmEnquiry).where(CrmEnquiry.institute_id == institute_id)
        )
        return list(res.scalars().all())

    async def create_followup(self, institute_id: str, data: dict) -> CrmFollowup:
        fid = str(uuid.uuid4())
        fup = CrmFollowup(id=fid, institute_id=institute_id, **data)
        self.session.add(fup)
        await self.session.commit()
        await self.session.refresh(fup)
        return fup

    async def list_campaigns(self, institute_id: str) -> List[CrmCampaign]:
        res = await self.session.execute(
            select(CrmCampaign).where(CrmCampaign.institute_id == institute_id)
        )
        return list(res.scalars().all())

    async def create_franchise_center(self, institute_id: str, data: dict) -> FranchiseCenter:
        cid = str(uuid.uuid4())
        center = FranchiseCenter(id=cid, institute_id=institute_id, **data)
        self.session.add(center)
        await self.session.commit()
        await self.session.refresh(center)
        return center
