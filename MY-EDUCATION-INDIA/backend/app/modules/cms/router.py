import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.modules.auth.dependencies import enforce_csrf, get_current_user, require_permissions
from app.modules.auth.models import User
from app.modules.cms.models import Banner, DownloadableResource, Enquiry, Menu, NewsArticle, Page, Testimonial, WebsiteSettings
from app.modules.cms.schemas import (
    BannerCreate,
    BannerResponse,
    DownloadCreate,
    DownloadResponse,
    EnquiryCreate,
    EnquiryResponse,
    MenuResponse,
    NewsCreate,
    NewsResponse,
    PageCreate,
    PageResponse,
    PageUpdate,
    TestimonialCreate,
    TestimonialResponse,
    WebsiteSettingsResponse,
    WebsiteSettingsUpdate,
)
from app.modules.cms.seo import SEOGenerator
from app.modules.cms.service import CMSService

cms_router = APIRouter(prefix="/cms", tags=["Enterprise Website CMS & Page Builder"])


# ==================== Public Public Website Endpoints ====================

@cms_router.get("/pages/slug/{slug}", response_model=PageResponse)
async def get_public_page_by_slug(
    slug: str,
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
) -> PageResponse:
    service = CMSService(db)
    page = await service.repo.get_page_by_slug(slug, institute_id)
    if not page:
        raise ValueError(f"Page '{slug}' not found.")
    page.view_count += 1
    await db.commit()
    return PageResponse.model_validate(page)


@cms_router.get("/pages/homepage", response_model=PageResponse)
async def get_public_homepage(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
) -> PageResponse:
    service = CMSService(db)
    page = await service.repo.get_homepage(institute_id)
    if not page:
        # Fallback to first published page if no explicit home
        pages = await service.repo.list_pages(institute_id)
        if pages:
            page = pages[0]
        else:
            raise ValueError("No published homepage found for this institute.")
    return PageResponse.model_validate(page)


@cms_router.get("/menus/{code}", response_model=MenuResponse)
async def get_public_menu(
    code: str,
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
) -> MenuResponse:
    service = CMSService(db)
    menu = await service.repo.get_menu_by_code(code, institute_id)
    if not menu:
        return MenuResponse(
            id=uuid.uuid4(),
            institute_id=institute_id,
            code=code.upper(),
            name=code.replace("_", " ").title(),
            location="HEADER",
            is_active=True,
            items=[],
        )
    return MenuResponse.model_validate(menu)


@cms_router.get("/banners", response_model=List[BannerResponse])
async def list_public_banners(
    institute_id: uuid.UUID = Query(...),
    banner_type: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db_session),
) -> List[BannerResponse]:
    service = CMSService(db)
    banners = await service.repo.list_banners(institute_id, banner_type)
    return [BannerResponse.model_validate(b) for b in banners]


@cms_router.get("/news", response_model=List[NewsResponse])
async def list_public_news(
    institute_id: uuid.UUID = Query(...),
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db_session),
) -> List[NewsResponse]:
    service = CMSService(db)
    news = await service.repo.list_news(institute_id, limit)
    return [NewsResponse.model_validate(n) for n in news]


@cms_router.get("/testimonials", response_model=List[TestimonialResponse])
async def list_public_testimonials(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
) -> List[TestimonialResponse]:
    service = CMSService(db)
    testimonials = await service.repo.list_testimonials(institute_id)
    return [TestimonialResponse.model_validate(t) for t in testimonials]


@cms_router.get("/downloads", response_model=List[DownloadResponse])
async def list_public_downloads(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
) -> List[DownloadResponse]:
    service = CMSService(db)
    downloads = await service.repo.list_downloads(institute_id)
    return [DownloadResponse.model_validate(d) for d in downloads]


@cms_router.post("/enquiries", response_model=EnquiryResponse, status_code=status.HTTP_201_CREATED)
async def submit_public_enquiry(
    payload: EnquiryCreate,
    db: AsyncSession = Depends(get_db_session),
) -> EnquiryResponse:
    service = CMSService(db)
    enquiry = await service.submit_enquiry(payload)
    return EnquiryResponse.model_validate(enquiry)


@cms_router.get("/settings", response_model=WebsiteSettingsResponse)
async def get_public_website_settings(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
) -> WebsiteSettingsResponse:
    service = CMSService(db)
    settings = await service.get_or_create_settings(institute_id)
    return WebsiteSettingsResponse.model_validate(settings)


@cms_router.get("/sitemap.xml", response_class=Response)
async def get_sitemap_xml(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
) -> Response:
    service = CMSService(db)
    pages = await service.repo.list_pages(institute_id)
    xml_content = SEOGenerator.generate_sitemap_xml(pages)
    return Response(content=xml_content, media_type="application/xml")


@cms_router.get("/robots.txt", response_class=Response)
async def get_robots_txt() -> Response:
    robots_content = SEOGenerator.generate_robots_txt()
    return Response(content=robots_content, media_type="text/plain")


# ==================== Admin CMS Governance Endpoints ====================

@cms_router.get("/admin/pages", response_model=List[PageResponse])
async def list_admin_pages(
    current_user: User = Depends(require_permissions("cms.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> List[PageResponse]:
    service = CMSService(db)
    if not current_user.institute_id:
        return []
    pages = await service.repo.list_pages(current_user.institute_id)
    return [PageResponse.model_validate(p) for p in pages]


@cms_router.post("/admin/pages", response_model=PageResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_page(
    payload: PageCreate,
    current_user: User = Depends(require_permissions("cms.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> PageResponse:
    service = CMSService(db)
    page = await service.create_page(payload)
    return PageResponse.model_validate(page)


@cms_router.patch("/admin/pages/{page_id}", response_model=PageResponse, dependencies=[Depends(enforce_csrf)])
async def update_page(
    page_id: uuid.UUID,
    payload: PageUpdate,
    current_user: User = Depends(require_permissions("cms.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> PageResponse:
    service = CMSService(db)
    page = await service.update_page(page_id, payload)
    return PageResponse.model_validate(page)


@cms_router.put("/admin/settings", response_model=WebsiteSettingsResponse, dependencies=[Depends(enforce_csrf)])
async def update_website_settings(
    payload: WebsiteSettingsUpdate,
    current_user: User = Depends(require_permissions("cms.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> WebsiteSettingsResponse:
    service = CMSService(db)
    if not current_user.institute_id:
        raise ValueError("Institute context required")
    settings = await service.update_settings(current_user.institute_id, payload)
    return WebsiteSettingsResponse.model_validate(settings)


@cms_router.get("/admin/enquiries", response_model=List[EnquiryResponse])
async def list_admin_enquiries(
    current_user: User = Depends(require_permissions("cms.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> List[EnquiryResponse]:
    service = CMSService(db)
    if not current_user.institute_id:
        return []
    enquiries = await service.repo.list_enquiries(current_user.institute_id)
    return [EnquiryResponse.model_validate(e) for e in enquiries]
