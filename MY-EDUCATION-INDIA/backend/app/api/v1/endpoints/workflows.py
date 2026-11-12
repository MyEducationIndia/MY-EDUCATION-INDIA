"""
Workflows Endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

router = APIRouter(prefix="/workflows", tags=["Workflows"])


@router.get("")
async def list_items(db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """List workflows items."""
    return []


@router.get("/health")
async def module_health() -> Dict[str, str]:
    return {"module": "workflows", "status": "active"}
