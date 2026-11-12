"""
CMS Gallery - Public & Admin CMS Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

public_gallery_router = APIRouter(prefix="/cms/gallery", tags=["CMS Gallery (Public)"])
admin_gallery_router = APIRouter(prefix="/admin/cms/gallery", tags=["CMS Gallery (Admin)"])


@public_gallery_router.get("")
async def list_public_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List public gallery items."""
    return []


@public_gallery_router.get("/health")
async def public_health() -> Dict[str, str]:
    return {"module": "gallery", "scope": "public", "status": "active"}


@admin_gallery_router.get("")
async def list_admin_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List admin gallery items."""
    return []
