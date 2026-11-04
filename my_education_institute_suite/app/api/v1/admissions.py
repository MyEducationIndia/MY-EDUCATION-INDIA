from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.core.security import hash_password
from app.models.schemas import AdmissionApply
import random

router = APIRouter(prefix="/admissions", tags=["Online Admission Queue"])

@router.get("")
def list_admissions():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.*, c.title as course_title, c.code as course_code, c.fee as course_fee
            FROM admissions a
            JOIN courses c ON a.course_id = c.id
            ORDER BY a.id DESC
        """)
        return [dict(row) for row in cur.fetchall()]

@router.post("/apply", status_code=201)
def submit_admission(a: AdmissionApply):
    with get_db() as conn:
        cur = conn.cursor()
        app_no = f"APP-2026-{random.randint(1000, 9999)}"
        cur.execute("""
            INSERT INTO admissions (application_number, applicant_name, course_id, preferred_timing, prior_qualification, mobile, email, guardian_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (app_no, a.applicant_name, a.course_id, a.preferred_timing, a.prior_qualification, a.mobile, a.email, a.guardian_name))
        
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('public', ?, 'Admissions')", (f"Received admission application {app_no} from {a.applicant_name}",))
        return {
            "status": "success",
            "application_number": app_no,
            "message": "Application received successfully. Present slip at admission counter."
        }

@router.post("/{app_id}/approve")
def approve_admission(app_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT a.*, c.fee as course_fee FROM admissions a JOIN courses c ON a.course_id = c.id WHERE a.id = ? OR a.application_number = ?", (app_id, str(app_id)))
        adm = cur.fetchone()
        if not adm:
            raise HTTPException(status_code=404, detail="Application not found.")

        # Update status
        cur.execute("UPDATE admissions SET status = 'Approved' WHERE id = ?", (adm["id"],))

        # Auto-enroll student & generate credentials
        cur.execute("SELECT count(*) as count FROM students")
        next_num = cur.fetchone()["count"] + 1001
        roll = f"STU-2026-{next_num}"
        dob = "2004-06-15" # Default DOB if not given in basic inquiry
        pwd_hash = hash_password(dob)

        cur.execute("""
            INSERT INTO users (username, email, password_hash, full_name, role_id, linked_id)
            VALUES (?, ?, ?, ?, 3, ?)
        """, (roll, adm["email"], pwd_hash, adm["applicant_name"], roll))
        user_id = cur.lastrowid

        cur.execute("""
            INSERT INTO students (roll_number, user_id, name, dob, course_id, batch_id, mobile, email, guardian_name, gender, blood_group, total_fee, paid_fee, due_fee, attendance_rate, status)
            VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, 'Male', 'B+', ?, 0, ?, 100.0, 'Enrolled')
        """, (roll, user_id, adm["applicant_name"], dob, adm["course_id"], adm["mobile"], adm["email"], adm["guardian_name"] or "Guardian", adm["course_fee"], adm["course_fee"]))
        
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Admissions')", (f"Approved application {adm['application_number']} -> Enrolled {roll} ({adm['applicant_name']})",))
        return {
            "status": "success",
            "message": f"Application approved! Enrolled as Roll Number {roll}",
            "roll_number": roll,
            "default_password": dob
        }

@router.post("/{app_id}/reject")
def reject_admission(app_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE admissions SET status = 'Rejected' WHERE id = ? OR application_number = ?", (app_id, str(app_id)))
        return {"status": "success", "message": "Application rejected."}

@router.delete("/{app_id}")
def delete_admission(app_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM admissions WHERE id = ? OR application_number = ?", (app_id, str(app_id)))
        return {"status": "success", "message": "Application deleted."}
