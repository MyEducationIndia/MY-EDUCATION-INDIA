"""
CMS Faculty - Public & Admin CMS Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

public_faculty_router = APIRouter(prefix="/cms/faculty", tags=["CMS Faculty (Public)"])
admin_faculty_router = APIRouter(prefix="/admin/cms/faculty", tags=["CMS Faculty (Admin)"])


@public_faculty_router.get("")
async def list_public_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List public faculty items."""
    return []


@public_faculty_router.get("/health")
async def public_health() -> Dict[str, str]:
    return {"module": "faculty", "scope": "public", "status": "active"}


@admin_faculty_router.get("")
async def list_admin_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List admin faculty items."""
    return []
