"""
CMS Contact - Public & Admin CMS Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

public_contact_router = APIRouter(prefix="/cms/contact", tags=["CMS Contact (Public)"])
admin_contact_router = APIRouter(prefix="/admin/cms/contact", tags=["CMS Contact (Admin)"])


@public_contact_router.get("")
async def list_public_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List public contact items."""
    return []


@public_contact_router.get("/health")
async def public_health() -> Dict[str, str]:
    return {"module": "contact", "scope": "public", "status": "active"}


@admin_contact_router.get("")
async def list_admin_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List admin contact items."""
    return []
