from fastapi import APIRouter
from app.api.v1.endpoints import (
    audit_logs,
    auth,
    health,
    institutes,
    roles,
    users,
)

api_v1_router = APIRouter()

# Core System & Enterprise Routers
api_v1_router.include_router(health.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(institutes.router)
api_v1_router.include_router(roles.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(audit_logs.router)
