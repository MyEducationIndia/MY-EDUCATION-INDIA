import uuid
from typing import List, Optional
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.cms.models import (
    Banner,
    BlogPost,
    DownloadableResource,
    Enquiry,
    GalleryAlbum,
    GalleryItem,
    MediaAsset,
    Menu,
    MenuItem,
    NewsArticle,
    Page,
    PageSection,
    Testimonial,
    WebsiteSettings,
)


class CMSRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ==================== Pages ====================
    async def get_page_by_slug(self, slug: str, institute_id: uuid.UUID) -> Optional[Page]:
        stmt = (
            select(Page)
            .options(selectinload(Page.sections))
            .where(Page.slug == slug.strip().lower(), Page.institute_id == institute_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_homepage(self, institute_id: uuid.UUID) -> Optional[Page]:
        stmt = (
            select(Page)
            .options(selectinload(Page.sections))
            .where(Page.is_homepage.is_(True), Page.institute_id == institute_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_pages(self, institute_id: uuid.UUID) -> List[Page]:
        stmt = select(Page).options(selectinload(Page.sections)).where(Page.institute_id == institute_id).order_by(Page.title.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def save_page(self, page: Page) -> Page:
        self.session.add(page)
        await self.session.flush()
        return page

    # ==================== Menus ====================
    async def get_menu_by_code(self, code: str, institute_id: uuid.UUID) -> Optional[Menu]:
        stmt = (
            select(Menu)
            .options(selectinload(Menu.items).selectinload(MenuItem.children))
            .where(Menu.code == code.upper(), Menu.institute_id == institute_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_menus(self, institute_id: uuid.UUID) -> List[Menu]:
        stmt = select(Menu).options(selectinload(Menu.items)).where(Menu.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Banners ====================
    async def list_banners(self, institute_id: uuid.UUID, banner_type: Optional[str] = None) -> List[Banner]:
        stmt = select(Banner).where(Banner.institute_id == institute_id, Banner.is_active.is_(True))
        if banner_type:
            stmt = stmt.where(Banner.banner_type == banner_type.upper())
        stmt = stmt.order_by(Banner.display_order.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== News & Blogs ====================
    async def list_news(self, institute_id: uuid.UUID, limit: int = 10) -> List[NewsArticle]:
        stmt = select(NewsArticle).where(NewsArticle.institute_id == institute_id).order_by(NewsArticle.published_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Testimonials ====================
    async def list_testimonials(self, institute_id: uuid.UUID) -> List[Testimonial]:
        stmt = select(Testimonial).where(Testimonial.institute_id == institute_id, Testimonial.is_approved.is_(True)).order_by(Testimonial.display_order.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Downloads ====================
    async def list_downloads(self, institute_id: uuid.UUID) -> List[DownloadableResource]:
        stmt = select(DownloadableResource).where(DownloadableResource.institute_id == institute_id, DownloadableResource.is_active.is_(True)).order_by(DownloadableResource.title.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Enquiries ====================
    async def create_enquiry(self, enquiry: Enquiry) -> Enquiry:
        self.session.add(enquiry)
        await self.session.flush()
        return enquiry

    async def list_enquiries(self, institute_id: uuid.UUID, limit: int = 25) -> List[Enquiry]:
        stmt = select(Enquiry).where(Enquiry.institute_id == institute_id).order_by(Enquiry.created_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Settings ====================
    async def get_website_settings(self, institute_id: uuid.UUID) -> Optional[WebsiteSettings]:
        stmt = select(WebsiteSettings).where(WebsiteSettings.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def save_website_settings(self, settings: WebsiteSettings) -> WebsiteSettings:
        self.session.add(settings)
        await self.session.flush()
        return settings
