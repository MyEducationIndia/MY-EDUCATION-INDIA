"""
CMS Testimonials - Public & Admin CMS Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

public_testimonials_router = APIRouter(prefix="/cms/testimonials", tags=["CMS Testimonials (Public)"])
admin_testimonials_router = APIRouter(prefix="/admin/cms/testimonials", tags=["CMS Testimonials (Admin)"])


@public_testimonials_router.get("")
async def list_public_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List public testimonials items."""
    return []


@public_testimonials_router.get("/health")
async def public_health() -> Dict[str, str]:
    return {"module": "testimonials", "scope": "public", "status": "active"}


@admin_testimonials_router.get("")
async def list_admin_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List admin testimonials items."""
    return []
