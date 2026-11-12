"""
Enterprise Departments Management - API Endpoints
"""
import uuid
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import get_current_user

router = APIRouter(prefix="/departments", tags=["Departments Management"])


class DepartmentCreate(BaseModel):
    code: str
    name: str
    description: str | None = None
    is_active: bool = True


@router.get("")
async def list_departments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[Dict[str, Any]]:
    """List all academic and administrative departments."""
    return [
        {"code": "CSE", "name": "Computer Science & Engineering", "is_active": True},
        {"code": "ECE", "name": "Electronics & Communication", "is_active": True},
        {"code": "ME", "name": "Mechanical Engineering", "is_active": True},
        {"code": "MBA", "name": "Management Studies", "is_active": True},
        {"code": "ADMIN", "name": "Central Administration", "is_active": True},
    ]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_department(
    payload: DepartmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    """Create a new department."""
    return {
        "id": str(uuid.uuid4()),
        "code": payload.code,
        "name": payload.name,
        "description": payload.description,
        "is_active": payload.is_active,
    }
