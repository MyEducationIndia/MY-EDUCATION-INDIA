from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

router = APIRouter(prefix="/health", tags=["System Health"])


@router.get("", summary="Verify API and Neon PostgreSQL connectivity")
async def health_check(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    db_Result = await db.execute(text("SELECT version()"))
    pg_version = db_Result.scalar_one()
    return {
        "status": "healthy",
        "service": "MY EDUCATION INDIA Enterprise API",
        "subdomain_context": getattr(request.state, "subdomain", "api"),
        "database_engine": "PostgreSQL",
        "database_version": pg_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
