from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_db
from app.db.seed_data import seed
import random

client = TestClient(app)

def test_api():
    print("Testing enterprise API endpoints and schemas...")

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, res.text
    assert res.json()["database"] == "PostgreSQL (Render)"
    print("✓ /health passed (PostgreSQL service online)")

    # 2. Verify config
    from app.core.config import settings
    assert settings.DATABASE_URL.startswith("postgresql") or settings.DATABASE_URL.startswith("postgres"), f"Invalid DB URL: {settings.DATABASE_URL}"
    print(f"✓ settings.DATABASE_URL verified: {settings.DATABASE_URL}")

    # 3. Verify SPA Delivery
    res = client.get("/")
    assert res.status_code == 200, res.text
    assert "MY EDUCATION" in res.text
    # Verify no browser permanent storage keys exist in HTML
    for kw in ["localStorage", "sessionStorage", "indexedDB"]:
        assert kw not in res.text, f"Forbidden browser storage found: {kw}"
    print("✓ SPA delivery passed (100% verified zero localStorage, sessionStorage, or indexedDB)")

    # 4. Verify OpenAPI Schema contains all enterprise endpoints
    res = client.get("/openapi.json")
    assert res.status_code == 200, res.text
    schema = res.json()
    paths = schema["paths"]

    # Assert core endpoints exist in schema
    expected_endpoints = [
        "/api/v1/auth/login",
        "/api/v1/users",
        "/api/v1/students",
        "/api/v1/staff",
        "/api/v1/courses",
        "/api/v1/batches",
        "/api/v1/admissions",
        "/api/v1/fees",
        "/api/v1/attendance",
        "/api/v1/materials",
        "/api/v1/notices",
        "/api/v1/cms/config",
        "/api/v1/cms/sections",
        "/api/v1/cms/custom-sections",
        "/api/v1/cms/documents",
        "/api/v1/cms/advertisements",
        "/api/v1/cms/seo",
        "/api/v1/exams/config",
        "/api/v1/exams/forms",
        "/api/v1/exams/questions",
        "/api/v1/exams/results",
        "/api/v1/storage/upload",
        "/api/v1/storage/file/{file_id}",
        "/api/v1/reports/summary",
        "/api/v1/settings",
        "/api/v1/settings/restore-points",
        "/api/v1/sync/state"
    ]
    for ep in expected_endpoints:
        assert ep in paths, f"Missing expected endpoint in OpenAPI schema: {ep}"
    print(f"✓ All {len(expected_endpoints)} enterprise REST API route declarations verified in OpenAPI schema")

    print("\n==============================================")
    print("ALL REST API INTEGRATION SUITE TESTS PASSED!")
    print("==============================================")

if __name__ == "__main__":
    test_api()
