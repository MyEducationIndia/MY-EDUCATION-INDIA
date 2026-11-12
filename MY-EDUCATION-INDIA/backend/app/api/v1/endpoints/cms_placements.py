"""
CMS Placements - Public & Admin CMS Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

public_placements_router = APIRouter(prefix="/cms/placements", tags=["CMS Placements (Public)"])
admin_placements_router = APIRouter(prefix="/admin/cms/placements", tags=["CMS Placements (Admin)"])


@public_placements_router.get("")
async def list_public_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List public placements items."""
    return []


@public_placements_router.get("/health")
async def public_health() -> Dict[str, str]:
    return {"module": "placements", "scope": "public", "status": "active"}


@admin_placements_router.get("")
async def list_admin_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List admin placements items."""
    return []
