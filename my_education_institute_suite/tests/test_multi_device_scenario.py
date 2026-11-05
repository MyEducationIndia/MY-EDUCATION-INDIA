import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from app.main import app
from app.core.logging_config import get_logger, setup_logging
from app.db.init_db import init_db
from app.db.seed_data import seed

setup_logging()
logger = get_logger("test_multi_device")


def test_multi_device_scenario() -> None:
    logger.info("STARTING 11-STEP MULTI-DEVICE POSTGRESQL SYNCHRONIZATION TEST")
    init_db(fresh=True)
    seed()

    device_a = TestClient(app)
    device_b = TestClient(app)

    # Step 1: Open Admin Dashboard on Device A
    res_a_login = device_a.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@1234", "role": "admin"},
    )
    assert res_a_login.status_code == 200, res_a_login.text
    logger.info("Step 1: Authenticated Admin on Device A (Status: %d)", res_a_login.status_code)

    # Step 2: Change website title on Device A
    new_title = "MY EDUCATION PREMIER ACADEMY"
    current_state = {
        "cms": {
            "instituteName": new_title,
            "announcementTicker": "ADMISSIONS OPEN 2026-27: DCA, PGDCA, TCCP",
            "theme": "dark",
        },
        "students": [],
        "fees": [],
    }

    # Step 3: Save on Device A
    res_a_save = device_a.post("/api/v1/sync/state", json={"state": current_state})
    assert res_a_save.status_code == 200, res_a_save.text
    logger.info("Step 3: Saved updated institutional state from Device A to PostgreSQL")

    # Step 4 & 5: Open website on Device B and verify new title
    res_b_sync = device_b.get("/api/v1/sync/state")
    assert res_b_sync.status_code == 200, res_b_sync.text
    b_data = res_b_sync.json()
    assert b_data["has_state"] is True
    assert b_data["state"]["cms"]["instituteName"] == new_title
    logger.info("Step 5: Verified new title '%s' immediately appears on Device B", new_title)

    # Step 6 & 7: Add a student on Device A and verify on Device B
    new_student = {
        "id": "STU-2026-9999",
        "name": "Rohan Sharma",
        "dob": "2004-11-20",
        "course": "D.C.A",
        "mobile": "9876543299",
        "email": "rohan.sharma@myeducation.edu.in",
        "totalFee": 9500,
        "paidFee": 3000,
        "dueFee": 6500,
        "status": "Enrolled",
    }
    current_state["students"].append(new_student)
    res_a_add_stu = device_a.post("/api/v1/sync/state", json={"state": current_state})
    assert res_a_add_stu.status_code == 200, res_a_add_stu.text

    res_b_stu = device_b.get("/api/v1/sync/state")
    assert res_b_stu.status_code == 200
    students_on_b = res_b_stu.json()["state"]["students"]
    assert any(s["name"] == "Rohan Sharma" for s in students_on_b)
    logger.info("Step 7: Verified student 'Rohan Sharma' immediately appears on Device B")

    # Step 8 & 9: Record a fee payment on Device A and verify on Device B
    new_payment = {
        "inv": "INV-2026-9999",
        "studentId": "STU-2026-9999",
        "studentName": "Rohan Sharma",
        "amount": 3000,
        "mode": "UPI (Google Pay)",
        "date": "2026-11-04",
        "remarks": "Tuition Installment #1",
    }
    current_state["fees"].append(new_payment)
    res_a_fee = device_a.post("/api/v1/sync/state", json={"state": current_state})
    assert res_a_fee.status_code == 200, res_a_fee.text

    res_b_fees = device_b.get("/api/v1/sync/state")
    assert res_b_fees.status_code == 200
    fees_on_b = res_b_fees.json()["state"]["fees"]
    assert any(f["inv"] == "INV-2026-9999" and f["amount"] == 3000 for f in fees_on_b)
    logger.info("Step 9: Verified fee payment INV-2026-9999 immediately appears on Device B")

    # Step 10 & 11: Simulate backend restart and verify persistence
    restarted_backend_client = TestClient(app)
    res_restarted = restarted_backend_client.get("/api/v1/sync/state")
    assert res_restarted.status_code == 200, res_restarted.text
    restarted_data = res_restarted.json()
    assert restarted_data["has_state"] is True
    assert restarted_data["state"]["cms"]["instituteName"] == new_title
    assert any(s["name"] == "Rohan Sharma" for s in restarted_data["state"]["students"])
    assert any(f["inv"] == "INV-2026-9999" for f in restarted_data["state"]["fees"])
    logger.info("Step 11: Verified all saved data remains intact after backend restart")


if __name__ == "__main__":
    test_multi_device_scenario()
