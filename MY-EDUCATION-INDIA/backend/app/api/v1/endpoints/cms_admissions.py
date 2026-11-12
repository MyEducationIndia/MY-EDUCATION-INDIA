"""
CMS Admissions - Public & Admin CMS Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

public_admissions_router = APIRouter(prefix="/cms/admissions", tags=["CMS Admissions (Public)"])
admin_admissions_router = APIRouter(prefix="/admin/cms/admissions", tags=["CMS Admissions (Admin)"])


@public_admissions_router.get("")
async def list_public_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List public admissions items."""
    return []


@public_admissions_router.get("/health")
async def public_health() -> Dict[str, str]:
    return {"module": "admissions", "scope": "public", "status": "active"}


@admin_admissions_router.get("")
async def list_admin_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List admin admissions items."""
    return []
