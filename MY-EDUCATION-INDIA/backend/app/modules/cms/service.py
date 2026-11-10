import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.modules.cms.models import (
    Banner,
    DownloadableResource,
    Enquiry,
    Menu,
    MenuItem,
    NewsArticle,
    Page,
    PageSection,
    Testimonial,
    WebsiteSettings,
)
from app.modules.cms.page_builder import PageBuilderCompiler
from app.modules.cms.repository import CMSRepository
from app.modules.cms.schemas import (
    BannerCreate,
    DownloadCreate,
    EnquiryCreate,
    NewsCreate,
    PageCreate,
    PageUpdate,
    TestimonialCreate,
    WebsiteSettingsUpdate,
)


class CMSService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CMSRepository(session)

    # ==================== Page Builder ====================
    async def create_page(self, payload: PageCreate) -> Page:
        existing = await self.repo.get_page_by_slug(payload.slug, payload.institute_id)
        if existing:
            raise ConflictException(f"Page with slug '{payload.slug}' already exists in this institute.")

        page = Page(
            institute_id=payload.institute_id,
            title=payload.title,
            slug=payload.slug.lower(),
            summary=payload.summary,
            featured_image_url=payload.featured_image_url,
            status=payload.status,
            is_homepage=payload.is_homepage,
            template_type=payload.template_type,
            meta_title=payload.meta_title or payload.title,
            meta_description=payload.meta_description or payload.summary,
            meta_keywords=payload.meta_keywords,
            version=1,
        )
        self.session.add(page)
        await self.session.flush()

        for idx, sec in enumerate(payload.sections):
            clean_payload = PageBuilderCompiler.sanitize_block_payload(sec.block_type, sec.content_payload)
            section = PageSection(
                page_id=page.id,
                section_key=sec.section_key,
                block_type=sec.block_type,
                display_order=sec.display_order if sec.display_order is not None else idx,
                is_visible=sec.is_visible,
                container_width=sec.container_width,
                background_color=sec.background_color,
                background_image_url=sec.background_image_url,
                padding_top=sec.padding_top,
                padding_bottom=sec.padding_bottom,
                content_payload=clean_payload,
            )
            self.session.add(section)

        await self.session.commit()
        await self.session.refresh(page)
        return page

    async def update_page(self, page_id: uuid.UUID, payload: PageUpdate) -> Page:
        stmt = await self.session.get(Page, page_id)
        if not stmt:
            raise ResourceNotFoundException("Page", page_id)

        update_dict = payload.model_dump(exclude_unset=True)
        sections_data = update_dict.pop("sections", None)

        for k, v in update_dict.items():
            setattr(stmt, k, v)
        stmt.version += 1

        if sections_data is not None:
            # Delete old sections and replace with updated builder layout
            for old_sec in stmt.sections:
                await self.session.delete(old_sec)
            await self.session.flush()

            for idx, sec in enumerate(sections_data):
                clean_payload = PageBuilderCompiler.sanitize_block_payload(sec.get("block_type", "HERO"), sec.get("content_payload", {}))
                new_sec = PageSection(
                    page_id=stmt.id,
                    section_key=sec.get("section_key", f"section_{idx}"),
                    block_type=sec.get("block_type", "HERO"),
                    display_order=sec.get("display_order", idx),
                    is_visible=sec.get("is_visible", True),
                    container_width=sec.get("container_width", "BOXED"),
                    background_color=sec.get("background_color"),
                    background_image_url=sec.get("background_image_url"),
                    padding_top=sec.get("padding_top", 40),
                    padding_bottom=sec.get("padding_bottom", 40),
                    content_payload=clean_payload,
                )
                self.session.add(new_sec)

        await self.session.commit()
        await self.session.refresh(stmt)
        return stmt

    # ==================== Enquiries ====================
    async def submit_enquiry(self, payload: EnquiryCreate) -> Enquiry:
        enquiry = Enquiry(**payload.model_dump())
        created = await self.repo.create_enquiry(enquiry)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    # ==================== Settings ====================
    async def get_or_create_settings(self, institute_id: uuid.UUID) -> WebsiteSettings:
        settings = await self.repo.get_website_settings(institute_id)
        if not settings:
            settings = WebsiteSettings(
                institute_id=institute_id,
                website_title="MY EDUCATION INDIA",
                tagline="Premier Educational Institute & Assessment Center",
                social_links={"facebook": "https://facebook.com", "linkedin": "https://linkedin.com", "youtube": "https://youtube.com"},
            )
            await self.repo.save_website_settings(settings)
            await self.session.commit()
            await self.session.refresh(settings)
        return settings

    async def update_settings(self, institute_id: uuid.UUID, payload: WebsiteSettingsUpdate) -> WebsiteSettings:
        settings = await self.get_or_create_settings(institute_id)
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(settings, k, v)
        await self.session.commit()
        await self.session.refresh(settings)
        return settings
