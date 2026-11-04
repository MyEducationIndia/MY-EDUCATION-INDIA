from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_db
from app.db.seed_data import seed
import random

client = TestClient(app)

def test_api():
    print("Initializing clean test database...")
    init_db()
    seed()
    print("Starting automated API integration tests...")

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, res.text
    print("✓ /health passed")

    # 2. Authentication - Admin Login
    res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@1234", "role": "admin"})
    assert res.status_code == 200, res.text
    token = res.json()["access_token"]
    print("✓ /auth/login (Admin) passed")

    # 3. Authentication - Student Login with Roll Number and DOB
    res = client.post("/api/v1/auth/login", json={"username": "STU-2026-1001", "password": "2004-05-15", "role": "student"})
    assert res.status_code == 200, res.text
    print("✓ /auth/login (Student Roll Number + DOB) passed")

    # 4. Master User Accounts
    res = client.get("/api/v1/users")
    assert res.status_code == 200, res.text
    users = res.json()
    assert len(users) >= 8
    print(f"✓ /users passed (retrieved {len(users)} accounts)")

    # 5. Course Catalog
    res = client.get("/api/v1/courses")
    assert res.status_code == 200, res.text
    courses = res.json()
    assert len(courses) >= 6
    print(f"✓ /courses passed ({len(courses)} courses active)")

    # 6. Student Roster & Create Student
    res = client.get("/api/v1/students")
    assert res.status_code == 200, res.text
    students = res.json()
    print(f"✓ /students list passed ({len(students)} students)")

    # Create new student with unique email
    rand_id = random.randint(1000, 9999)
    new_stu = {
        "name": "Aarav Sharma",
        "dob": "2005-08-14",
        "course_id": 3,
        "batch_id": 1,
        "mobile": f"98765{rand_id}",
        "email": f"aarav.sharma.{rand_id}@test.edu",
        "guardian_name": "R. K. Sharma",
        "guardian_mobile": "9876543298",
        "gender": "Male",
        "blood_group": "B+",
        "address": "Vijay Nagar, Indore",
        "total_fee": 9500.0,
        "paid_fee": 4500.0
    }
    res = client.post("/api/v1/students", json=new_stu)
    assert res.status_code == 201, res.text
    new_roll = res.json()["roll_number"]
    print(f"✓ /students POST passed (Created student {new_roll})")

    # 7. Student Login with Newly Created Student
    res = client.post("/api/v1/auth/login", json={"username": new_roll, "password": "2005-08-14", "role": "student"})
    assert res.status_code == 200, res.text
    print(f"✓ /auth/login for newly created student {new_roll} with DOB passed")

    # 8. Fee Collection & Invoice
    res = client.post("/api/v1/fees/pay", json={"student_id": 1, "amount": 2500.0, "payment_mode": "UPI", "remarks": "Installment #3"})
    assert res.status_code == 201, res.text
    inv_no = res.json()["invoice_number"]
    print(f"✓ /fees/pay passed (Generated invoice {inv_no})")

    res = client.get(f"/api/v1/fees/invoice/{inv_no}")
    assert res.status_code == 200, res.text
    print(f"✓ /fees/invoice/{inv_no} passed")

    # 9. Attendance
    att_payload = [
        {"student_id": 1, "batch_id": 1, "date": "2026-11-01", "status": "Present", "remarks": "On Time"},
        {"student_id": 2, "batch_id": 1, "date": "2026-11-01", "status": "Present", "remarks": "On Time"}
    ]
    res = client.post("/api/v1/attendance", json=att_payload)
    assert res.status_code == 200, res.text
    print("✓ /attendance POST passed")

    # 10. Notices
    res = client.get("/api/v1/notices")
    assert res.status_code == 200, res.text
    print(f"✓ /notices passed ({len(res.json())} circulars)")

    # 11. CMS Config
    res = client.get("/api/v1/cms/config")
    assert res.status_code == 200, res.text
    print("✓ /cms/config GET passed")

    # 12. Reports Summary
    res = client.get("/api/v1/reports/summary")
    assert res.status_code == 200, res.text
    summary = res.json()
    assert summary["total_students"] > 0
    print(f"✓ /reports/summary passed (Total Students: {summary['total_students']}, Collected: ₹{summary['total_collected']})")

    # 13. Settings & Backup Snapshot + Full Database Restore
    res = client.get("/api/v1/settings/backup/json")
    assert res.status_code == 200, res.text
    backup_payload = res.json()
    print("✓ /settings/backup/json passed (Snapshot downloaded)")

    res_restore = client.post("/api/v1/settings/restore?mode=overwrite", json=backup_payload)
    assert res_restore.status_code == 200, res_restore.text
    assert res_restore.json()["total_records_restored"] > 0
    print(f"✓ /settings/restore POST passed (Restored {res_restore.json()['total_records_restored']} database records)")

    # 14. Restore Verification
    res = client.post("/api/v1/settings/restore/verify")
    assert res.status_code == 200, res.text
    print("✓ /settings/restore/verify passed")

    print("\n==============================================")
    print("ALL 14 REST API INTEGRATION TESTS 100% PASSED!")
    print("==============================================")

if __name__ == "__main__":
    test_api()
