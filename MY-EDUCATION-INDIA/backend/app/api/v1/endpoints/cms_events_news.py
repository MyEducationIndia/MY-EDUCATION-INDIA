"""
CMS Events & News - Public & Admin CMS Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

public_events_news_router = APIRouter(prefix="/cms/events-news", tags=["CMS Events & News (Public)"])
admin_events_news_router = APIRouter(prefix="/admin/cms/events-news", tags=["CMS Events & News (Admin)"])


@public_events_news_router.get("")
async def list_public_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List public events_news items."""
    return []


@public_events_news_router.get("/health")
async def public_health() -> Dict[str, str]:
    return {"module": "events_news", "scope": "public", "status": "active"}


@admin_events_news_router.get("")
async def list_admin_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List admin events_news items."""
    return []
