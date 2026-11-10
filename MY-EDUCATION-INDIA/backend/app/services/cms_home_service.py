import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.cms_home import (
    CmsFeaturedProgram,
    CmsHeroSlide,
    CmsNewsletterSubscriber,
    CmsQuickLink,
    CmsRecruiterLogo,
    CmsStatCounter,
    CmsTestimonial,
)
from app.models.institute import Institute
from app.schemas.cms_home import (
    CmsFeaturedProgramCreateRequest,
    CmsFeaturedProgramResponse,
    CmsFeaturedProgramUpdateRequest,
    CmsHeroSlideCreateRequest,
    CmsHeroSlideResponse,
    CmsHeroSlideUpdateRequest,
    CmsQuickLinkCreateRequest,
    CmsQuickLinkResponse,
    CmsQuickLinkUpdateRequest,
    CmsRecruiterLogoCreateRequest,
    CmsRecruiterLogoResponse,
    CmsRecruiterLogoUpdateRequest,
    CmsStatCounterCreateRequest,
    CmsStatCounterResponse,
    CmsStatCounterUpdateRequest,
    CmsTestimonialCreateRequest,
    CmsTestimonialResponse,
    CmsTestimonialUpdateRequest,
    PublicHomePageBundle,
)


class CmsHomeService:
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
    # 1. Public Master Home Page Bundle (High-speed single query aggregator)
    # -------------------------------------------------------------------------
    async def get_public_home_bundle(self) -> PublicHomePageBundle:
        inst = await self._get_primary_institute()

        # Hero Slides
        slides_res = await self.session.execute(
            select(CmsHeroSlide)
            .where(CmsHeroSlide.institute_id == inst.id, CmsHeroSlide.is_active.is_(True))
            .order_by(CmsHeroSlide.display_order, CmsHeroSlide.created_at)
        )
        slides = slides_res.scalars().all()

        # Stat Counters
        stats_res = await self.session.execute(
            select(CmsStatCounter)
            .where(CmsStatCounter.institute_id == inst.id, CmsStatCounter.is_active.is_(True))
            .order_by(CmsStatCounter.display_order)
        )
        stats = stats_res.scalars().all()

        # Quick Links
        ql_res = await self.session.execute(
            select(CmsQuickLink)
            .where(CmsQuickLink.institute_id == inst.id, CmsQuickLink.is_active.is_(True))
            .order_by(CmsQuickLink.display_order)
        )
        quick_links = ql_res.scalars().all()

        # Featured Programs
        prog_res = await self.session.execute(
            select(CmsFeaturedProgram)
            .where(CmsFeaturedProgram.institute_id == inst.id, CmsFeaturedProgram.is_active.is_(True))
            .order_by(CmsFeaturedProgram.display_order)
        )
        programs = prog_res.scalars().all()

        # Recruiter Logos
        rec_res = await self.session.execute(
            select(CmsRecruiterLogo)
            .where(CmsRecruiterLogo.institute_id == inst.id, CmsRecruiterLogo.is_active.is_(True))
            .order_by(CmsRecruiterLogo.display_order)
        )
        recruiters = rec_res.scalars().all()

        # Testimonials
        test_res = await self.session.execute(
            select(CmsTestimonial)
            .where(CmsTestimonial.institute_id == inst.id, CmsTestimonial.is_active.is_(True))
            .order_by(CmsTestimonial.display_order)
        )
        testimonials = test_res.scalars().all()

        return PublicHomePageBundle(
            hero_slides=[CmsHeroSlideResponse.model_validate(s) for s in slides],
            stat_counters=[CmsStatCounterResponse.model_validate(c) for c in stats],
            quick_links=[CmsQuickLinkResponse.model_validate(q) for q in quick_links],
            featured_programs=[CmsFeaturedProgramResponse.model_validate(p) for p in programs],
            recruiters=[CmsRecruiterLogoResponse.model_validate(r) for r in recruiters],
            testimonials=[CmsTestimonialResponse.model_validate(t) for t in testimonials],
        )

    # -------------------------------------------------------------------------
    # 2. Public Newsletter Subscription
    # -------------------------------------------------------------------------
    async def subscribe_newsletter(self, email: str) -> None:
        inst = await self._get_primary_institute()
        normalized = email.strip().lower()

        res = await self.session.execute(
            select(CmsNewsletterSubscriber).where(
                CmsNewsletterSubscriber.institute_id == inst.id,
                CmsNewsletterSubscriber.email == normalized,
            )
        )
        existing = res.scalar_one_or_none()
        if not existing:
            sub = CmsNewsletterSubscriber(institute_id=inst.id, email=normalized)
            self.session.add(sub)
            await self.session.commit()

    # -------------------------------------------------------------------------
    # 3. Super Admin Hero Slides CRUD
    # -------------------------------------------------------------------------
    async def list_hero_slides(self) -> List[CmsHeroSlideResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(CmsHeroSlide)
            .where(CmsHeroSlide.institute_id == inst.id)
            .order_by(CmsHeroSlide.display_order)
        )
        return [CmsHeroSlideResponse.model_validate(s) for s in res.scalars().all()]

    async def create_hero_slide(self, payload: CmsHeroSlideCreateRequest) -> CmsHeroSlideResponse:
        inst = await self._get_primary_institute()
        slide = CmsHeroSlide(institute_id=inst.id, **payload.model_dump())
        self.session.add(slide)
        await self.session.commit()
        await self.session.refresh(slide)
        return CmsHeroSlideResponse.model_validate(slide)

    async def update_hero_slide(self, slide_id: uuid.UUID, payload: CmsHeroSlideUpdateRequest) -> CmsHeroSlideResponse:
        res = await self.session.execute(select(CmsHeroSlide).where(CmsHeroSlide.id == slide_id))
        slide = res.scalar_one_or_none()
        if not slide:
            raise NotFoundException(f"Hero slide {slide_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(slide, k, v)

        await self.session.commit()
        await self.session.refresh(slide)
        return CmsHeroSlideResponse.model_validate(slide)

    async def delete_hero_slide(self, slide_id: uuid.UUID) -> None:
        res = await self.session.execute(select(CmsHeroSlide).where(CmsHeroSlide.id == slide_id))
        slide = res.scalar_one_or_none()
        if not slide:
            raise NotFoundException(f"Hero slide {slide_id} not found.")
        await self.session.delete(slide)
        await self.session.commit()

    # -------------------------------------------------------------------------
    # 4. Super Admin Stat Counters CRUD
    # -------------------------------------------------------------------------
    async def list_stat_counters(self) -> List[CmsStatCounterResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(CmsStatCounter)
            .where(CmsStatCounter.institute_id == inst.id)
            .order_by(CmsStatCounter.display_order)
        )
        return [CmsStatCounterResponse.model_validate(c) for c in res.scalars().all()]

    async def create_stat_counter(self, payload: CmsStatCounterCreateRequest) -> CmsStatCounterResponse:
        inst = await self._get_primary_institute()
        counter = CmsStatCounter(institute_id=inst.id, **payload.model_dump())
        self.session.add(counter)
        await self.session.commit()
        await self.session.refresh(counter)
        return CmsStatCounterResponse.model_validate(counter)

    async def update_stat_counter(self, counter_id: uuid.UUID, payload: CmsStatCounterUpdateRequest) -> CmsStatCounterResponse:
        res = await self.session.execute(select(CmsStatCounter).where(CmsStatCounter.id == counter_id))
        counter = res.scalar_one_or_none()
        if not counter:
            raise NotFoundException(f"Stat counter {counter_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(counter, k, v)

        await self.session.commit()
        await self.session.refresh(counter)
        return CmsStatCounterResponse.model_validate(counter)

    async def delete_stat_counter(self, counter_id: uuid.UUID) -> None:
        res = await self.session.execute(select(CmsStatCounter).where(CmsStatCounter.id == counter_id))
        counter = res.scalar_one_or_none()
        if not counter:
            raise NotFoundException(f"Stat counter {counter_id} not found.")
        await self.session.delete(counter)
        await self.session.commit()

    # -------------------------------------------------------------------------
    # 5. Super Admin Featured Programs CRUD
    # -------------------------------------------------------------------------
    async def list_featured_programs(self) -> List[CmsFeaturedProgramResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(CmsFeaturedProgram)
            .where(CmsFeaturedProgram.institute_id == inst.id)
            .order_by(CmsFeaturedProgram.display_order)
        )
        return [CmsFeaturedProgramResponse.model_validate(p) for p in res.scalars().all()]

    async def create_featured_program(self, payload: CmsFeaturedProgramCreateRequest) -> CmsFeaturedProgramResponse:
        inst = await self._get_primary_institute()
        prog = CmsFeaturedProgram(institute_id=inst.id, **payload.model_dump())
        self.session.add(prog)
        await self.session.commit()
        await self.session.refresh(prog)
        return CmsFeaturedProgramResponse.model_validate(prog)

    async def update_featured_program(self, program_id: uuid.UUID, payload: CmsFeaturedProgramUpdateRequest) -> CmsFeaturedProgramResponse:
        res = await self.session.execute(select(CmsFeaturedProgram).where(CmsFeaturedProgram.id == program_id))
        prog = res.scalar_one_or_none()
        if not prog:
            raise NotFoundException(f"Featured program {program_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(prog, k, v)

        await self.session.commit()
        await self.session.refresh(prog)
        return CmsFeaturedProgramResponse.model_validate(prog)

    async def delete_featured_program(self, program_id: uuid.UUID) -> None:
        res = await self.session.execute(select(CmsFeaturedProgram).where(CmsFeaturedProgram.id == program_id))
        prog = res.scalar_one_or_none()
        if not prog:
            raise NotFoundException(f"Featured program {program_id} not found.")
        await self.session.delete(prog)
        await self.session.commit()
