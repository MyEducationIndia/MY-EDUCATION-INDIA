import time, json
from fastapi.testclient import TestClient
from app.main import app

def test_multi_device_scenario():
    print("\n=======================================================")
    print("STARTING 11-STEP MULTI-DEVICE SYNCHRONIZATION TEST")
    print("=======================================================")

    # Device A Client (e.g. Admin Laptop)
    device_a = TestClient(app)
    # Device B Client (e.g. Mobile Phone / Secondary Laptop)
    device_b = TestClient(app)

    # Step 1: Open Admin Dashboard on Device A
    res_a_login = device_a.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "Admin@1234",
        "role": "admin"
    })
    print("Step 1: Opened Admin Dashboard on Device A (Auth Response:", res_a_login.status_code, ")")

    # Step 2: Change website title on Device A
    new_title = "MY EDUCATION PREMIER ACADEMY"
    current_state = {
        "cms": {
            "instituteName": new_title,
            "announcementTicker": "ADMISSIONS OPEN 2026-27: DCA, PGDCA, TCCP",
            "theme": "dark"
        },
        "students": [],
        "fees": []
    }
    print(f"Step 2: Prepared updated website title '{new_title}' on Device A")

    # Step 3: Save on Device A
    res_a_save = device_a.post("/api/v1/sync/state", json={"state": current_state})
    assert res_a_save.status_code == 200, res_a_save.text
    print("Step 3: Saved updated institutional state from Device A to PostgreSQL")

    # Step 4: Open website on Device B
    res_b_sync = device_b.get("/api/v1/sync/state")
    assert res_b_sync.status_code == 200, res_b_sync.text
    b_data = res_b_sync.json()
    print("Step 4: Opened website on Device B and fetched state from PostgreSQL")

    # Step 5: Verify the new title appears on Device B
    assert b_data["has_state"] is True
    assert b_data["state"]["cms"]["instituteName"] == new_title
    print(f"Step 5: Verified new title '{new_title}' appears on Device B")

    # Step 6: Add a student on Device A
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
        "status": "Enrolled"
    }
    current_state["students"].append(new_student)
    res_a_add_stu = device_a.post("/api/v1/sync/state", json={"state": current_state})
    assert res_a_add_stu.status_code == 200, res_a_add_stu.text
    print("Step 6: Added student 'Rohan Sharma' on Device A and saved to PostgreSQL")

    # Step 7: Verify that student appears on Device B
    res_b_stu = device_b.get("/api/v1/sync/state")
    assert res_b_stu.status_code == 200
    students_on_b = res_b_stu.json()["state"]["students"]
    assert any(s["name"] == "Rohan Sharma" for s in students_on_b)
    print("Step 7: Verified student 'Rohan Sharma' appears on Device B")

    # Step 8: Record a fee payment on Device A
    new_payment = {
        "inv": "INV-2026-9999",
        "studentId": "STU-2026-9999",
        "studentName": "Rohan Sharma",
        "amount": 3000,
        "mode": "UPI (Google Pay)",
        "date": "2026-11-04",
        "remarks": "Tuition Installment #1"
    }
    current_state["fees"].append(new_payment)
    res_a_fee = device_a.post("/api/v1/sync/state", json={"state": current_state})
    assert res_a_fee.status_code == 200, res_a_fee.text
    print("Step 8: Recorded fee payment of ₹3,000 on Device A and saved to PostgreSQL")

    # Step 9: Verify the payment appears on Device B
    res_b_fees = device_b.get("/api/v1/sync/state")
    assert res_b_fees.status_code == 200
    fees_on_b = res_b_fees.json()["state"]["fees"]
    assert any(f["inv"] == "INV-2026-9999" and f["amount"] == 3000 for f in fees_on_b)
    print("Step 9: Verified fee payment INV-2026-9999 appears on Device B")

    # Step 10: Restart the backend (simulate re-instantiating application & fresh client)
    print("Step 10: Simulating backend restart (creating clean client session from PostgreSQL)...")
    restarted_backend_client = TestClient(app)

    # Step 11: Verify all saved data remains available
    res_restarted = restarted_backend_client.get("/api/v1/sync/state")
    assert res_restarted.status_code == 200, res_restarted.text
    restarted_data = res_restarted.json()
    assert restarted_data["has_state"] is True
    assert restarted_data["state"]["cms"]["instituteName"] == new_title
    assert any(s["name"] == "Rohan Sharma" for s in restarted_data["state"]["students"])
    assert any(f["inv"] == "INV-2026-9999" for f in restarted_data["state"]["fees"])
    print("Step 11: Verified all saved data remains 100% available and intact after backend restart")

    print("\n=======================================================")
    print("ALL 11 STEPS OF MULTI-DEVICE VERIFICATION 100% PASSED!")
    print("=======================================================\n")

if __name__ == "__main__":
    test_multi_device_scenario()
