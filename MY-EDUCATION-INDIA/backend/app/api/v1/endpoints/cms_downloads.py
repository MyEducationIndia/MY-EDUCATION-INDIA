"""
CMS Downloads & Forms - Public & Admin CMS Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

router = APIRouter(prefix="/cms/downloads", tags=["CMS Downloads & Forms"])


@router.get("")
async def list_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List public downloads items."""
    return []


@router.get("/health")
async def module_health() -> Dict[str, str]:
    return {"module": "downloads", "status": "active"}
