import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundException
from app.models.institute import Institute
from app.models.website import (
    WebsiteNavigationMenu,
    WebsiteSearchIndex,
    WebsiteSetting,
    WebsiteSocialLink,
    WebsiteTheme,
    WebsiteTickerItem,
)
from app.schemas.website import (
    NavigationMenuCreateRequest,
    NavigationMenuItemResponse,
    NavigationMenuUpdateRequest,
    PublicWebsiteFrameworkBundle,
    SearchResultItem,
    WebsiteSettingsResponse,
    WebsiteSettingsUpdateRequest,
    WebsiteSocialLinkCreateRequest,
    WebsiteSocialLinkResponse,
    WebsiteThemeResponse,
    WebsiteThemeUpdateRequest,
    WebsiteTickerItemCreateRequest,
    WebsiteTickerItemResponse,
    WebsiteTickerItemUpdateRequest,
)


class WebsiteService:
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
    # 1. Public Framework Bundle (Zero-login high-speed aggregator)
    # -------------------------------------------------------------------------
    async def get_public_framework_bundle(self) -> PublicWebsiteFrameworkBundle:
        inst = await self._get_primary_institute()
        now = datetime.now(timezone.utc)

        # Settings
        s_res = await self.session.execute(select(WebsiteSetting).where(WebsiteSetting.institute_id == inst.id))
        settings = s_res.scalar_one_or_none()
        if not settings:
            settings = WebsiteSetting(institute_id=inst.id)
            self.session.add(settings)
            await self.session.flush()

        # Theme
        t_res = await self.session.execute(select(WebsiteTheme).where(WebsiteTheme.institute_id == inst.id))
        theme = t_res.scalar_one_or_none()
        if not theme:
            theme = WebsiteTheme(institute_id=inst.id)
            self.session.add(theme)
            await self.session.flush()

        # Navigation (Header root items with nested children)
        nav_res = await self.session.execute(
            select(WebsiteNavigationMenu)
            .options(selectinload(WebsiteNavigationMenu.children))
            .where(
                WebsiteNavigationMenu.institute_id == inst.id,
                WebsiteNavigationMenu.menu_location == "HEADER_MAIN",
                WebsiteNavigationMenu.parent_id.is_(None),
                WebsiteNavigationMenu.is_active.is_(True),
            )
            .order_by(WebsiteNavigationMenu.display_order)
        )
        nav_items = nav_res.scalars().all()

        # Live Ticker Items (Active, publish_at <= now, expire_at is null or > now)
        ticker_res = await self.session.execute(
            select(WebsiteTickerItem)
            .where(
                WebsiteTickerItem.institute_id == inst.id,
                WebsiteTickerItem.is_active.is_(True),
                WebsiteTickerItem.publish_at <= now,
                or_(WebsiteTickerItem.expire_at.is_(None), WebsiteTickerItem.expire_at > now),
            )
            .order_by(WebsiteTickerItem.priority_level.desc(), WebsiteTickerItem.display_order)
        )
        ticker_items = ticker_res.scalars().all()

        # Social Links
        soc_res = await self.session.execute(
            select(WebsiteSocialLink)
            .where(
                WebsiteSocialLink.institute_id == inst.id,
                WebsiteSocialLink.is_active.is_(True),
            )
            .order_by(WebsiteSocialLink.display_order)
        )
        social_links = soc_res.scalars().all()

        return PublicWebsiteFrameworkBundle(
            settings=WebsiteSettingsResponse.model_validate(settings),
            theme=WebsiteThemeResponse.model_validate(theme),
            header_navigation=[NavigationMenuItemResponse.model_validate(item) for item in nav_items],
            ticker_announcements=[WebsiteTickerItemResponse.model_validate(item) for item in ticker_items],
            social_links=[WebsiteSocialLinkResponse.model_validate(link) for link in social_links],
        )

    # -------------------------------------------------------------------------
    # 2. Global Website Search
    # -------------------------------------------------------------------------
    async def global_search(self, query: str, limit: int = 15) -> Tuple[List[SearchResultItem], int]:
        inst = await self._get_primary_institute()
        normalized = f"%{query.strip().lower()}%"

        stmt = select(WebsiteSearchIndex).where(
            WebsiteSearchIndex.institute_id == inst.id,
            WebsiteSearchIndex.is_published.is_(True),
            or_(
                func.lower(WebsiteSearchIndex.title).like(normalized),
                func.lower(WebsiteSearchIndex.summary).like(normalized),
                func.lower(WebsiteSearchIndex.keywords).like(normalized),
            ),
        ).limit(limit)

        count_stmt = select(func.count(WebsiteSearchIndex.id)).where(
            WebsiteSearchIndex.institute_id == inst.id,
            WebsiteSearchIndex.is_published.is_(True),
            or_(
                func.lower(WebsiteSearchIndex.title).like(normalized),
                func.lower(WebsiteSearchIndex.summary).like(normalized),
                func.lower(WebsiteSearchIndex.keywords).like(normalized),
            ),
        )

        res = await self.session.execute(stmt)
        items = res.scalars().all()

        count_res = await self.session.execute(count_stmt)
        total = count_res.scalar_one()

        return [SearchResultItem.model_validate(i) for i in items], total

    # -------------------------------------------------------------------------
    # 3. Super Admin Settings & Theme Mutators
    # -------------------------------------------------------------------------
    async def update_settings(self, payload: WebsiteSettingsUpdateRequest) -> WebsiteSettingsResponse:
        inst = await self._get_primary_institute()
        res = await self.session.execute(select(WebsiteSetting).where(WebsiteSetting.institute_id == inst.id))
        settings = res.scalar_one_or_none()
        if not settings:
            settings = WebsiteSetting(institute_id=inst.id)
            self.session.add(settings)

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(settings, k, v)

        await self.session.commit()
        await self.session.refresh(settings)
        return WebsiteSettingsResponse.model_validate(settings)

    async def update_theme(self, payload: WebsiteThemeUpdateRequest) -> WebsiteThemeResponse:
        inst = await self._get_primary_institute()
        res = await self.session.execute(select(WebsiteTheme).where(WebsiteTheme.institute_id == inst.id))
        theme = res.scalar_one_or_none()
        if not theme:
            theme = WebsiteTheme(institute_id=inst.id)
            self.session.add(theme)

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(theme, k, v)

        await self.session.commit()
        await self.session.refresh(theme)
        return WebsiteThemeResponse.model_validate(theme)

    # -------------------------------------------------------------------------
    # 4. Ticker Items Admin CRUD
    # -------------------------------------------------------------------------
    async def list_ticker_items(self) -> List[WebsiteTickerItemResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(WebsiteTickerItem)
            .where(WebsiteTickerItem.institute_id == inst.id)
            .order_by(WebsiteTickerItem.display_order, WebsiteTickerItem.created_at.desc())
        )
        return [WebsiteTickerItemResponse.model_validate(i) for i in res.scalars().all()]

    async def create_ticker_item(self, payload: WebsiteTickerItemCreateRequest) -> WebsiteTickerItemResponse:
        inst = await self._get_primary_institute()
        data = payload.model_dump()
        if not data.get("publish_at"):
            data["publish_at"] = datetime.now(timezone.utc)

        item = WebsiteTickerItem(institute_id=inst.id, **data)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return WebsiteTickerItemResponse.model_validate(item)

    async def update_ticker_item(self, item_id: uuid.UUID, payload: WebsiteTickerItemUpdateRequest) -> WebsiteTickerItemResponse:
        res = await self.session.execute(select(WebsiteTickerItem).where(WebsiteTickerItem.id == item_id))
        item = res.scalar_one_or_none()
        if not item:
            raise NotFoundException(f"Ticker announcement {item_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(item, k, v)

        await self.session.commit()
        await self.session.refresh(item)
        return WebsiteTickerItemResponse.model_validate(item)

    async def delete_ticker_item(self, item_id: uuid.UUID) -> None:
        res = await self.session.execute(select(WebsiteTickerItem).where(WebsiteTickerItem.id == item_id))
        item = res.scalar_one_or_none()
        if not item:
            raise NotFoundException(f"Ticker announcement {item_id} not found.")
        await self.session.delete(item)
        await self.session.commit()

    # -------------------------------------------------------------------------
    # 5. Navigation Menus Admin CRUD
    # -------------------------------------------------------------------------
    async def list_navigation_menus(self, menu_location: str = "HEADER_MAIN") -> List[NavigationMenuItemResponse]:
        inst = await self._get_primary_institute()
        res = await self.session.execute(
            select(WebsiteNavigationMenu)
            .options(selectinload(WebsiteNavigationMenu.children))
            .where(
                WebsiteNavigationMenu.institute_id == inst.id,
                WebsiteNavigationMenu.menu_location == menu_location,
                WebsiteNavigationMenu.parent_id.is_(None),
            )
            .order_by(WebsiteNavigationMenu.display_order)
        )
        return [NavigationMenuItemResponse.model_validate(i) for i in res.scalars().all()]

    async def create_navigation_menu(self, payload: NavigationMenuCreateRequest) -> NavigationMenuItemResponse:
        inst = await self._get_primary_institute()
        item = WebsiteNavigationMenu(institute_id=inst.id, **payload.model_dump())
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return NavigationMenuItemResponse.model_validate(item)

    async def update_navigation_menu(self, menu_id: uuid.UUID, payload: NavigationMenuUpdateRequest) -> NavigationMenuItemResponse:
        res = await self.session.execute(
            select(WebsiteNavigationMenu)
            .options(selectinload(WebsiteNavigationMenu.children))
            .where(WebsiteNavigationMenu.id == menu_id)
        )
        item = res.scalar_one_or_none()
        if not item:
            raise NotFoundException(f"Navigation menu {menu_id} not found.")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(item, k, v)

        await self.session.commit()
        await self.session.refresh(item)
        return NavigationMenuItemResponse.model_validate(item)

    async def delete_navigation_menu(self, menu_id: uuid.UUID) -> None:
        res = await self.session.execute(select(WebsiteNavigationMenu).where(WebsiteNavigationMenu.id == menu_id))
        item = res.scalar_one_or_none()
        if not item:
            raise NotFoundException(f"Navigation menu {menu_id} not found.")
        await self.session.delete(item)
        await self.session.commit()
