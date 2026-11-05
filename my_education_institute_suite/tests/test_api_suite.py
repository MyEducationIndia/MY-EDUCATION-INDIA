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
    logger.info("Starting comprehensive enterprise API & subsystem verification...")
    init_db(fresh=True)
    seed()

    # 1. Health check & Security Headers
    res = client.get("/health")
    assert res.status_code == 200, res.text
    health_data = res.json()
    assert health_data["status"] == "healthy"
    assert health_data["database"] == "PostgreSQL (Render)"
    assert res.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert res.headers.get("X-Content-Type-Options") == "nosniff"
    logger.info("PASS: /health & security headers verified")

    # 2. Verify Pydantic V2 Settings Configuration
    assert settings.DATABASE_URL.startswith(("postgresql", "postgres"))
    assert hasattr(settings, "model_config")
    import inspect
    cfg_src = inspect.getsource(settings.__class__)
    assert "class Config:" not in cfg_src and "os.getenv" not in cfg_src
    logger.info("PASS: Pydantic V2 BaseSettings configuration verified")

    # 3. Verify SPA Delivery & Zero Browser Storage
    res = client.get("/")
    assert res.status_code == 200, res.text
    assert "MY EDUCATION" in res.text
    for kw in ["localStorage", "sessionStorage", "indexedDB"]:
        assert kw not in res.text, f"Forbidden browser storage found: {kw}"
    logger.info("PASS: SPA delivery verified (zero localStorage/sessionStorage/indexedDB)")

    # 4. Verify Structured Error Handling
    err_res = client.get("/api/v1/students/999999")
    assert err_res.status_code == 404
    err_json = err_res.json()
    assert err_json.get("success") is False
    assert "message" in err_json
    logger.info("PASS: Structured JSON error handler verified: %s", err_json)

    # 5. Authentication: Login, Refresh, /me, Logout Revocation
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
    assert "access_token" in ref_res.json()

    logout_res = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert logout_res.status_code == 200
    revoked_check = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert revoked_check.status_code == 401
    logger.info("PASS: Authentication (JWT, Refresh, /me, Logout Revocation) verified")

    # 6. Courses & Batches CRUD
    crs_list = client.get("/api/v1/courses")
    assert crs_list.status_code == 200
    assert len(crs_list.json()) >= 8

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

    # 7. Staff & Leave CRUD
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

    lv_apply = client.post(
        "/api/v1/staff/leave/apply",
        json={
            "staff_id": staff_id,
            "leave_type": "Casual Leave",
            "start_date": "2026-11-10",
            "end_date": "2026-11-12",
            "reason": "Academic seminar",
        },
    )
    assert lv_apply.status_code == 201, lv_apply.text
    leave_id = lv_apply.json()["leave_id"]
    lv_approve = client.put(f"/api/v1/staff/leave/{leave_id}", json={"status": "Approved"})
    assert lv_approve.status_code == 200
    logger.info("PASS: Courses, Batches, Staff, and Leave Management CRUD verified")

    # 8. Students, Admissions, Fees, Fee Heads & Expenses CRUD
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

    csv_res = client.get("/api/v1/students/export/csv")
    assert csv_res.status_code == 200
    assert "Aarav Verma" in csv_res.text

    adm_apply = client.post(
        "/api/v1/admissions/apply",
        json={
            "applicant_name": "Priya Nair",
            "course_id": 4,
            "prior_qualification": "B.Sc CS",
            "mobile": "9876500002",
            "email": "priya.nair@myeducation.edu.in",
        },
    )
    assert adm_apply.status_code == 201, adm_apply.text

    fee_pay = client.post(
        "/api/v1/fees/pay",
        json={"student_id": student_id, "amount": 2000.0, "payment_mode": "UPI", "remarks": "Installment 2"},
    )
    assert fee_pay.status_code == 201, fee_pay.text
    inv_no = fee_pay.json()["invoice_number"]

    inv_res = client.get(f"/api/v1/fees/invoice/{inv_no}")
    assert inv_res.status_code == 200
    assert inv_res.json()["amount"] == 2000.0

    fh_res = client.get("/api/v1/fees/heads")
    assert fh_res.status_code == 200 and len(fh_res.json()) >= 7

    exp_res = client.post(
        "/api/v1/fees/expenses",
        json={"category": "Gigabit Internet", "amount": 2500.0, "payee": "Airtel Fiber", "mode": "NEFT"},
    )
    assert exp_res.status_code == 201
    logger.info("PASS: Students, Admissions, Fees, Fee Heads & Expenses CRUD verified")

    # 9. Attendance, Assignments, Materials & Notices CRUD
    att_res = client.post(
        "/api/v1/attendance",
        json=[{"student_id": student_id, "batch_id": batch_id, "date": "2026-11-04", "status": "Present"}],
    )
    assert att_res.status_code == 200

    ass_res = client.post(
        "/api/v1/assignments",
        json={
            "title": "SQL Normalization Lab",
            "course_id": 3,
            "batch_id": batch_id,
            "trainer_id": staff_id,
            "due_date": "2026-11-20",
            "instructions": "Design 3NF schema",
            "max_marks": 20,
        },
    )
    assert ass_res.status_code == 201
    ass_id = ass_res.json()["assignment_id"]

    sub_res = client.post(
        "/api/v1/assignments/submit",
        json={"assignment_id": ass_id, "student_id": student_id, "submission_text": "Completed 3NF SQL DDL"},
    )
    assert sub_res.status_code == 201

    mat_res = client.post(
        "/api/v1/materials",
        json={"title": "RDBMS Lecture Notes", "course_id": 3, "batch_id": batch_id, "file_path": "/api/v1/storage/file/demo"},
    )
    assert mat_res.status_code == 201

    not_res = client.post(
        "/api/v1/notices",
        json={"title": "Semester Exam Schedule", "content": "Exams start Dec 10", "target_audience": "All"},
    )
    assert not_res.status_code == 201
    logger.info("PASS: Attendance, Assignments, Materials & Notices verified")

    # 10. Website CMS, Custom Sections, Public Documents, Advertisements & SEO
    cms_cfg = client.put("/api/v1/cms/config", json={"settings": {"instituteName": "MY EDUCATION INSTITUTE"}})
    assert cms_cfg.status_code == 200

    cust_sec = client.post(
        "/api/v1/cms/custom-sections",
        json={"title": "Scholarship Drive 2026", "subtitle": "Up to 50% Merit Waiver", "visible": True},
    )
    assert cust_sec.status_code == 201, cust_sec.text
    sec_id = cust_sec.json()["id"]
    cust_upd = client.put(f"/api/v1/cms/custom-sections/{sec_id}", json={"title": "Updated Scholarship Drive 2026"})
    assert cust_upd.status_code == 200

    doc_res = client.post("/api/v1/cms/documents", json={"title": "Academic Prospectus 2026", "category": "Prospectus"})
    assert doc_res.status_code == 201
    logger.info("PASS: CMS Config, Custom Sections, and Public Documents verified")

    # 11. Exam Management, Question Bank & CBT Engine
    q_list = client.get("/api/v1/exams/questions")
    assert q_list.status_code == 200 and len(q_list.json()) >= 5

    q_add = client.post(
        "/api/v1/exams/questions",
        json={
            "course_code": "D.C.A",
            "paper_code": "DCA-102",
            "question_text": "Which protocol secures HTTP traffic using TLS?",
            "options": ["FTP", "HTTPS", "SMTP", "SNMP"],
            "correct_option": 1,
            "marks": 1,
        },
    )
    assert q_add.status_code == 201

    cbt_sub = client.post(
        "/api/v1/exams/results",
        json={
            "student_id": "STU-2026-1001",
            "roll_number": "STU-2026-1001",
            "exam_session": "Winter Semester CBT 2026",
            "score": 14.0,
            "max_score": 15.0,
            "percentage": 93.3,
            "status": "Passed",
            "answers": {"0": 1, "1": 1},
        },
    )
    assert cbt_sub.status_code == 201
    logger.info("PASS: Exam Management, Question Bank & CBT Engine verified")

    # 12. Persistent Object / Binary Storage
    upload_res = client.post(
        "/api/v1/storage/upload",
        files={"file": ("syllabus.pdf", b"%PDF-1.4 test syllabus binary", "application/pdf")},
        data={"category": "syllabus"},
    )
    assert upload_res.status_code == 200, upload_res.text
    fid = upload_res.json()["file_id"]

    stream_res = client.get(f"/api/v1/storage/file/{fid}")
    assert stream_res.status_code == 200
    assert stream_res.content == b"%PDF-1.4 test syllabus binary"
    logger.info("PASS: Persistent Binary / Object Storage verified")

    # 13. Reports, Backup, Restore & Integrity Verification
    rep_res = client.get("/api/v1/reports/summary")
    assert rep_res.status_code == 200
    assert rep_res.json()["total_students"] >= 1

    ver_res = client.post("/api/v1/settings/restore/verify")
    assert ver_res.status_code == 200
    assert ver_res.json()["tables_registered"] == 37
    logger.info("PASS: Reports & 37-table PostgreSQL schema integrity verified")

    logger.info("ALL ENTERPRISE REST API & SUBSYSTEM INTEGRATION TESTS PASSED!")


if __name__ == "__main__":
    test_api()
