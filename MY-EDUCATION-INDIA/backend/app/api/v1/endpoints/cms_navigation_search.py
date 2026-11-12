"""
CMS Navigation & Search - Public & Admin Endpoints
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

public_navigation_router = APIRouter(prefix="/cms/navigation", tags=["CMS Navigation (Public)"])
public_search_router = APIRouter(prefix="/cms/search", tags=["CMS Search (Public)"])
public_sitemap_router = APIRouter(prefix="/cms/sitemap", tags=["CMS Sitemap (Public)"])
admin_navigation_router = APIRouter(prefix="/admin/cms/navigation", tags=["CMS Navigation (Admin)"])


@public_navigation_router.get("")
async def get_navigation(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """Get public navigation menu items."""
    return []


@public_search_router.get("")
async def search_content(
    q: Optional[str] = Query(default=None, description="Search query"),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    """Search public CMS content."""
    return {"query": q or "", "results": []}


@public_sitemap_router.get("")
async def get_sitemap(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """Get public CMS sitemap entries."""
    return []


@admin_navigation_router.get("")
async def list_admin_navigation(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List admin navigation items."""
    return []
