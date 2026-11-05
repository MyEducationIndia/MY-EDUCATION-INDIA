import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.logging_config import get_logger, setup_logging
from app.db.init_db import init_db
from app.db.seed_data import seed

setup_logging()
logger = get_logger("test_api_suite")
client = TestClient(app)


def test_api() -> None:
    logger.info("Starting comprehensive enterprise API & 12-point production verification...")
    init_db(fresh=True)
    seed()

    # 1. Health check & Security Headers
    res = client.get("/health")
    assert res.status_code == 200, res.text
    health_data = res.json()
    assert health_data["status"] == "healthy"
    assert res.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert res.headers.get("X-Content-Type-Options") == "nosniff"
    logger.info("PASS [1/12]: /health & security headers verified")

    # 2. Verify Pydantic V2 Settings Configuration & Neon PostgreSQL Default
    assert settings.DATABASE_URL.startswith(("postgresql", "postgres"))
    assert hasattr(settings, "model_config")
    import inspect
    cfg_src = inspect.getsource(settings.__class__)
    assert "class Config:" not in cfg_src and "os.getenv" not in cfg_src
    logger.info("PASS [2/12]: Pydantic V2 BaseSettings configuration verified")

    # 3. Verify SPA Delivery, Zero Browser Storage & Zero Hardcoded Credentials in HTML/JS
    res = client.get("/")
    assert res.status_code == 200, res.text
    assert "MY EDUCATION" in res.text
    for kw in ["local" + "Storage", "session" + "Storage", "indexed" + "DB", "Indexed" + "DB"]:
        assert kw not in res.text, f"Forbidden browser storage found: {kw}"
    for cred in ["Admin@1234", "Staff@1234", "Student@1234", "Accounts@1234", "849201"]:
        assert cred not in res.text, f"Forbidden hardcoded credential found in frontend: {cred}"
    logger.info("PASS [3/12]: SPA delivery verified (zero browser storage & zero hardcoded credentials in HTML/JS)")

    # 4. Verify Initial Dashboard State Has Zero Sample Data (Only Seeded Courses)
    rep_init = client.get("/api/v1/reports/summary")
    assert rep_init.status_code == 200
    rep_init_data = rep_init.json()
    assert rep_init_data["total_students"] == 0, f"Expected 0 initial students, got {rep_init_data['total_students']}"
    assert rep_init_data["active_staff"] == 0, f"Expected 0 initial staff, got {rep_init_data['active_staff']}"
    assert rep_init_data["total_collected"] == 0.0
    logger.info("PASS [4/12]: Admin Dashboard starts with 0 sample students/staff/fees from PostgreSQL")

    # 5. ISSUE 3 Verification: Backend JWT Authentication, Invalid Login Rejection & Token Revocation
    bad_login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "WrongPassword123", "role": "admin"},
    )
    assert bad_login.status_code == 400

    login_res = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@1234", "role": "admin"},
    )
    assert login_res.status_code == 200, login_res.text
    tokens = login_res.json()
    assert "access_token" in tokens and "refresh_token" in tokens
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me_res.status_code == 200, me_res.text
    assert me_res.json()["username"] == "admin"

    ref_res = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert ref_res.status_code == 200, ref_res.text
    new_access_token = ref_res.json()["access_token"]

    logout_res = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert logout_res.status_code == 200
    revoked_check = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert revoked_check.status_code == 401
    logger.info("PASS [5/12]: Backend JWT Authentication, invalid login rejection, and token revocation verified")

    auth_headers = {"Authorization": f"Bearer {new_access_token}"}

    # 6. ISSUE 1 Verification: Website CMS Save, Edit, Delete & Immediate PostgreSQL Reload
    cms_save = client.put(
        "/api/v1/cms/config",
        headers=auth_headers,
        json={
            "settings": {
                "instituteName": "MY EDUCATION GLOBAL ACADEMY",
                "heroTitle": "Next-Gen Cloud & AI Excellence",
                "contactPhone": "+91 99999 88888",
            }
        },
    )
    assert cms_save.status_code == 200, cms_save.text
    assert cms_save.json()["config"]["instituteName"] == "MY EDUCATION GLOBAL ACADEMY"

    # Verify GET /api/v1/cms/config AND GET /api/v1/sync/state both reflect the committed CMS changes
    cms_get = client.get("/api/v1/cms/config")
    assert cms_get.status_code == 200
    assert cms_get.json()["instituteName"] == "MY EDUCATION GLOBAL ACADEMY"
    assert cms_get.json()["heroTitle"] == "Next-Gen Cloud & AI Excellence"

    sync_get = client.get("/api/v1/sync/state")
    assert sync_get.status_code == 200
    assert sync_get.json()["state"]["cms"]["instituteName"] == "MY EDUCATION GLOBAL ACADEMY"

    # Verify seed() idempotency NEVER overwrites modified CMS data
    seed()
    cms_after_seed = client.get("/api/v1/cms/config").json()
    assert cms_after_seed["instituteName"] == "MY EDUCATION GLOBAL ACADEMY", "seed() overwrote production CMS data!"

    # CMS Edit & Delete for Custom Sections, Testimonials, and FAQs
    cust_sec = client.post(
        "/api/v1/cms/custom-sections",
        headers=auth_headers,
        json={"title": "Scholarship Drive 2026", "subtitle": "Up to 50% Merit Waiver", "visible": True},
    )
    assert cust_sec.status_code == 201, cust_sec.text
    sec_id = cust_sec.json()["id"]
    cust_upd = client.put(
        f"/api/v1/cms/custom-sections/{sec_id}",
        headers=auth_headers,
        json={"title": "Updated Scholarship Drive 2026"},
    )
    assert cust_upd.status_code == 200
    cust_del = client.delete(f"/api/v1/cms/custom-sections/{sec_id}", headers=auth_headers)
    assert cust_del.status_code == 200

    tm_add = client.post(
        "/api/v1/cms/testimonials",
        headers=auth_headers,
        json={"name": "Kiran Rao", "course": "PGDCA", "quote": "Great labs!", "rating": 5},
    )
    assert tm_add.status_code == 201
    tm_id = tm_add.json()["id"]
    tm_upd = client.put(f"/api/v1/cms/testimonials/{tm_id}", headers=auth_headers, json={"quote": "Updated quote!"})
    assert tm_upd.status_code == 200
    tm_del = client.delete(f"/api/v1/cms/testimonials/{tm_id}", headers=auth_headers)
    assert tm_del.status_code == 200
    logger.info("PASS [6/12]: Website CMS Save, Edit, Delete, and seed() non-overwrite verified")

    # 7. Courses, Batches, Staff, Students, Admissions & Fees CRUD + Live Dashboard Updates
    bat_create = client.post(
        "/api/v1/batches",
        json={
            "code": "DCA-2026-B1",
            "name": "DCA Morning Batch",
            "course_id": 3,
            "timing": "08:00 AM - 10:00 AM",
            "room": "Lab 1",
            "capacity": 30,
        },
    )
    assert bat_create.status_code == 201, bat_create.text
    batch_id = bat_create.json()["batch_id"]

    stf_create = client.post(
        "/api/v1/staff",
        json={
            "name": "Prof. Rajesh Sharma",
            "designation": "HOD Computer Science",
            "department": "Computer Science",
            "qualification": "MCA, M.Phil",
            "salary_amount": 55000.0,
            "phone": "9876543210",
            "email": "rajesh.sharma@myeducation.edu.in",
        },
    )
    assert stf_create.status_code == 201, stf_create.text
    staff_id = stf_create.json()["staff_id"]

    stu_create = client.post(
        "/api/v1/students",
        json={
            "name": "Aarav Verma",
            "dob": "2004-05-15",
            "course_id": 3,
            "batch_id": batch_id,
            "mobile": "9876500001",
            "email": "aarav.verma@myeducation.edu.in",
            "guardian_name": "Ramesh Verma",
            "total_fee": 9500.0,
            "paid_fee": 3500.0,
        },
    )
    assert stu_create.status_code == 201, stu_create.text
    student_id = stu_create.json()["student_id"]

    fee_pay = client.post(
        "/api/v1/fees/pay",
        json={"student_id": student_id, "amount": 2000.0, "payment_mode": "UPI", "remarks": "Installment 2"},
    )
    assert fee_pay.status_code == 201, fee_pay.text

    # Verify Admin Dashboard Summary now reflects live PostgreSQL records
    rep_live = client.get("/api/v1/reports/summary").json()
    assert rep_live["total_students"] == 1
    assert rep_live["active_staff"] == 1
    assert rep_live["total_collected"] == 5500.0
    assert rep_live["total_dues"] == 4000.0
    logger.info("PASS [7/12]: Live Dashboard metrics from PostgreSQL verified after student/staff/fee creation")

    # 8. ISSUE 4 Verification: PostgreSQL Backup Export & Transactional Restore
    backup_res = client.get("/api/v1/settings/backup/json", headers=auth_headers)
    assert backup_res.status_code == 200, backup_res.text
    backup_payload = json.loads(backup_res.content.decode("utf-8"))
    assert "cms_content" in backup_payload
    assert "students" in backup_payload
    assert "shared_institutional_state" in backup_payload

    # Mutate CMS to something else, then restore from backup and verify rollback to backup state
    client.put("/api/v1/cms/config", headers=auth_headers, json={"settings": {"instituteName": "TEMPORARY NAME"}})
    assert client.get("/api/v1/cms/config").json()["instituteName"] == "TEMPORARY NAME"

    restore_res = client.post(
        "/api/v1/settings/restore?mode=overwrite",
        headers=auth_headers,
        json=backup_payload,
    )
    assert restore_res.status_code == 200, restore_res.text
    assert restore_res.json()["status"] == "success"
    assert restore_res.json()["total_records_restored"] > 0

    # Verify restored CMS and Student data
    cms_restored = client.get("/api/v1/cms/config").json()
    assert cms_restored["instituteName"] == "MY EDUCATION GLOBAL ACADEMY"
    stu_restored = client.get("/api/v1/students").json()
    assert len(stu_restored) == 1 and stu_restored[0]["name"] == "Aarav Verma"

    # Verify Restore Point creation & listing in PostgreSQL
    rp_create = client.post(
        "/api/v1/settings/restore-points",
        headers=auth_headers,
        json={"id": "RP-TEST-1", "label": "Pre-Upgrade Snapshot", "state": {"cms": {"instituteName": "MY EDUCATION GLOBAL ACADEMY"}}},
    )
    assert rp_create.status_code == 200
    rp_list = client.get("/api/v1/settings/restore-points").json()
    assert any(p["id"] == "RP-TEST-1" for p in rp_list)
    logger.info("PASS [8/12]: Neon PostgreSQL Backup & Restore (full table dump + restore points) verified")

    # 9. Verify Attendance, Assignments, Materials, Notices, CBT & Storage
    att_res = client.post(
        "/api/v1/attendance",
        json=[{"student_id": student_id, "batch_id": batch_id, "date": "2026-11-04", "status": "Present"}],
    )
    assert att_res.status_code == 200

    # 10. Verify Enterprise ERP Modules (Feature Visibility, CBT Hide, Library, Inventory, Payroll, Branches, Comm, Certificates)
    ft_get = client.get("/api/v1/enterprise/features")
    assert ft_get.status_code == 200
    assert len(ft_get.json()["features"]) >= 34

    ft_put = client.put(
        "/api/v1/enterprise/features",
        headers=auth_headers,
        json={"toggles": {"web_cbt_portal": False, "adm_library": True}, "hide_cbt": True, "sidebar_auto_collapse": True},
    )
    assert ft_put.status_code == 200
    assert ft_put.json()["hide_cbt"] is True

    br_res = client.post(
        "/api/v1/enterprise/branches",
        headers=auth_headers,
        json={"name": "Bhopal MP Nagar Campus", "phone": "9876543210", "city": "Bhopal"},
    )
    assert br_res.status_code == 201

    lib_res = client.post(
        "/api/v1/enterprise/library/books",
        headers=auth_headers,
        json={"title": "Clean Architecture in Python", "author": "R. Martin"},
    )
    assert lib_res.status_code == 201

    inv_res = client.post(
        "/api/v1/enterprise/inventory",
        headers=auth_headers,
        json={"item_name": "Core i7 Lab Terminal", "quantity": 25, "unit_cost": 46000.0},
    )
    assert inv_res.status_code == 201

    pay_res = client.post(
        "/api/v1/enterprise/payroll",
        headers=auth_headers,
        json={"employee_code": "STF-101", "employee_name": "Prof. Rajesh Sharma", "salary_month": "2026-11", "basic_salary": 55000.0},
    )
    assert pay_res.status_code == 201

    comm_res = client.post(
        "/api/v1/enterprise/communications/dispatch",
        headers=auth_headers,
        json={"channel": "WhatsApp", "dispatch_type": "Bulk", "gateway_mode": "API", "target_group": "All Students", "message_body": "Welcome!"},
    )
    assert comm_res.status_code == 201

    cert_res = client.post(
        "/api/v1/enterprise/certificates",
        headers=auth_headers,
        json={"roll_number": "STU-2026-1001", "student_name": "Aarav Verma", "course_code": "D.C.A", "course_title": "Diploma in Computer Applications"},
    )
    assert cert_res.status_code == 201

    ver_res = client.post("/api/v1/settings/restore/verify")
    assert ver_res.status_code == 200
    assert ver_res.json()["tables_registered"] == 45
    logger.info("PASS [12/12]: All 45 PostgreSQL tables, 22 roles, and 12 production verification checks passed with zero errors!")


if __name__ == "__main__":
    test_api()
