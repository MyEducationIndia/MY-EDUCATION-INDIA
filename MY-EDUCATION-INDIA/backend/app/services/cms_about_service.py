import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.cms_about import (
    CmsAccreditation,
    CmsCampusInfrastructure,
    CmsLeadershipMessage,
    CmsMilestone,
)
from app.models.institute import Institute
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


class CmsAboutService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_primary_institute(self) -> Institute:
        res = await self.session.execute(select(Institute).where(Institute.code == "MEI-HQ"))
        inst = res.scalar_one_or_none()
        if not inst:
            res_any = await self.session.execute(select(Institute).limit(1))
            inst = res_any.scalar_one_or_none()
        if not inst:
            raise NotFoundException("Primary Institute baseline not found in database.")
        return inst

    # -------------------------------------------------------------------------
    # 1. Public About Bundle Aggregator (Zero-login high-speed query)
    # -------------------------------------------------------------------------
    async def get_public_about_bundle(self) -> PublicAboutInstituteBundle:
        inst = await self._get_primary_institute()

        # Milestones
        ms_res = await self.session.execute(
            select(CmsMilestone)
            .where(CmsMilestone.institute_id == inst.id, CmsMilestone.is_active.is_(True))
            .order_by(CmsMilestone.display_order, CmsMilestone.year)
        )
        milestones = ms_res.scalars().all()

        # Leadership Messages
        lm_res = await self.session.execute(
            select(CmsLeadershipMessage)
            .where(CmsLeadershipMessage.institute_id == inst.id, CmsLeadershipMessage.is_active.is_(True))
            .order_by(CmsLeadershipMessage.display_order)
        )
        leaders = lm_res.scalars().all()

        # Accreditations
        acc_res = await self.session.execute(
            select(CmsAccreditation)
            .where(CmsAccreditation.institute_id == inst.id, CmsAccreditation.is_active.is_(True))
            .order_by(CmsAccreditation.display_order)
        )
        accreditations = acc_res.scalars().all()

        # Campus Infrastructure
        inf_res = await self.session.execute(
            select(CmsCampusInfrastructure)
            .where(CmsCampusInfrastructure.institute_id == inst.id, CmsCampusInfrastructure.is_active.is_(True))
            .order_by(CmsCampusInfrastructure.display_order)
        )
        infrastructure = inf_res.scalars().all()

        return PublicAboutInstituteBundle(
            milestones=[CmsMilestoneResponse.model_validate(m) for m in milestones],
            leadership_messages=[CmsLeadershipMessageResponse.model_validate(l) for l in leaders],
            accreditations=[CmsAccreditationResponse.model_validate(a) for a in accreditations],
            infrastructure=[CmsCampusInfrastructureResponse.model_validate(i) for i in infrastructure],
        )

    # -------------------------------------------------------------------------
    # 2. Super Admin Milestones CRUD
    # -------------------------------------------------------------------------
    async def list_milestones(self) -> List[CmsMilestoneResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(CmsMilestone)
            .where(CmsMilestone.institute_id == inst.id)
            .order_by(CmsMilestone.display_order)
        )
        return [CmsMilestoneResponse.model_validate(m) for m in res.scalars().all()]

    async def create_milestone(self, payload: CmsMilestoneCreateRequest) -> CmsMilestoneResponse:
        inst = await self._get_primary_institute()
        milestone = CmsMilestone(institute_id=inst.id, **payload.model_dump())
        self.session.add(milestone)
        await self.session.commit()
        await self.session.refresh(milestone)
        return CmsMilestoneResponse.model_validate(milestone)

    async def update_milestone(self, milestone_id: uuid.UUID, payload: CmsMilestoneUpdateRequest) -> CmsMilestoneResponse:
        res = await self.session.execute(select(CmsMilestone).where(CmsMilestone.id == milestone_id))
        milestone = res.scalar_one_or_none()
        if not milestone:
            raise NotFoundException(f"Milestone {milestone_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(milestone, k, v)

        await self.session.commit()
        await self.session.refresh(milestone)
        return CmsMilestoneResponse.model_validate(milestone)

    async def delete_milestone(self, milestone_id: uuid.UUID) -> None:
        res = await self.session.execute(select(CmsMilestone).where(CmsMilestone.id == milestone_id))
        milestone = res.scalar_one_or_none()
        if not milestone:
            raise NotFoundException(f"Milestone {milestone_id} not found.")
        await self.session.delete(milestone)
        await self.session.commit()

    # -------------------------------------------------------------------------
    # 3. Super Admin Leadership Messages CRUD
    # -------------------------------------------------------------------------
    async def list_leadership_messages(self) -> List[CmsLeadershipMessageResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(CmsLeadershipMessage)
            .where(CmsLeadershipMessage.institute_id == inst.id)
            .order_by(CmsLeadershipMessage.display_order)
        )
        return [CmsLeadershipMessageResponse.model_validate(l) for l in res.scalars().all()]

    async def create_leadership_message(self, payload: CmsLeadershipMessageCreateRequest) -> CmsLeadershipMessageResponse:
        inst = await self._get_primary_institute()
        msg = CmsLeadershipMessage(institute_id=inst.id, **payload.model_dump())
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return CmsLeadershipMessageResponse.model_validate(msg)

    async def update_leadership_message(self, message_id: uuid.UUID, payload: CmsLeadershipMessageUpdateRequest) -> CmsLeadershipMessageResponse:
        res = await self.session.execute(select(CmsLeadershipMessage).where(CmsLeadershipMessage.id == message_id))
        msg = res.scalar_one_or_none()
        if not msg:
            raise NotFoundException(f"Leadership message {message_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(msg, k, v)

        await self.session.commit()
        await self.session.refresh(msg)
        return CmsLeadershipMessageResponse.model_validate(msg)

    async def delete_leadership_message(self, message_id: uuid.UUID) -> None:
        res = await self.session.execute(select(CmsLeadershipMessage).where(CmsLeadershipMessage.id == message_id))
        msg = res.scalar_one_or_none()
        if not msg:
            raise NotFoundException(f"Leadership message {message_id} not found.")
        await self.session.delete(msg)
        await self.session.commit()

    # -------------------------------------------------------------------------
    # 4. Super Admin Accreditations CRUD
    # -------------------------------------------------------------------------
    async def list_accreditations(self) -> List[CmsAccreditationResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(CmsAccreditation)
            .where(CmsAccreditation.institute_id == inst.id)
            .order_by(CmsAccreditation.display_order)
        )
        return [CmsAccreditationResponse.model_validate(a) for a in res.scalars().all()]

    async def create_accreditation(self, payload: CmsAccreditationCreateRequest) -> CmsAccreditationResponse:
        inst = await self._get_primary_institute()
        acc = CmsAccreditation(institute_id=inst.id, **payload.model_dump())
        self.session.add(acc)
        await self.session.commit()
        await self.session.refresh(acc)
        return CmsAccreditationResponse.model_validate(acc)

    async def update_accreditation(self, acc_id: uuid.UUID, payload: CmsAccreditationUpdateRequest) -> CmsAccreditationResponse:
        res = await self.session.execute(select(CmsAccreditation).where(CmsAccreditation.id == acc_id))
        acc = res.scalar_one_or_none()
        if not acc:
            raise NotFoundException(f"Accreditation {acc_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(acc, k, v)

        await self.session.commit()
        await self.session.refresh(acc)
        return CmsAccreditationResponse.model_validate(acc)

    async def delete_accreditation(self, acc_id: uuid.UUID) -> None:
        res = await self.session.execute(select(CmsAccreditation).where(CmsAccreditation.id == acc_id))
        acc = res.scalar_one_or_none()
        if not acc:
            raise NotFoundException(f"Accreditation {acc_id} not found.")
        await self.session.delete(acc)
        await self.session.commit()

    # -------------------------------------------------------------------------
    # 5. Super Admin Campus Infrastructure CRUD
    # -------------------------------------------------------------------------
    async def list_infrastructure(self) -> List[CmsCampusInfrastructureResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(CmsCampusInfrastructure)
            .where(CmsCampusInfrastructure.institute_id == inst.id)
            .order_by(CmsCampusInfrastructure.display_order)
        )
        return [CmsCampusInfrastructureResponse.model_validate(i) for i in res.scalars().all()]

    async def create_infrastructure(self, payload: CmsCampusInfrastructureCreateRequest) -> CmsCampusInfrastructureResponse:
        inst = await self._get_primary_institute()
        infra = CmsCampusInfrastructure(institute_id=inst.id, **payload.model_dump())
        self.session.add(infra)
        await self.session.commit()
        await self.session.refresh(infra)
        return CmsCampusInfrastructureResponse.model_validate(infra)

    async def update_infrastructure(self, infra_id: uuid.UUID, payload: CmsCampusInfrastructureUpdateRequest) -> CmsCampusInfrastructureResponse:
        res = await self.session.execute(select(CmsCampusInfrastructure).where(CmsCampusInfrastructure.id == infra_id))
        infra = res.scalar_one_or_none()
        if not infra:
            raise NotFoundException(f"Facility {infra_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(infra, k, v)

        await self.session.commit()
        await self.session.refresh(infra)
        return CmsCampusInfrastructureResponse.model_validate(infra)

    async def delete_infrastructure(self, infra_id: uuid.UUID) -> None:
        res = await self.session.execute(select(CmsCampusInfrastructure).where(CmsCampusInfrastructure.id == infra_id))
        infra = res.scalar_one_or_none()
        if not infra:
            raise NotFoundException(f"Facility {infra_id} not found.")
        await self.session.delete(infra)
        await self.session.commit()
