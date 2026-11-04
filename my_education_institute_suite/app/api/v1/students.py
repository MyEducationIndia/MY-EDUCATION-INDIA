from fastapi import APIRouter, HTTPException, Query, Response
from app.core.database import get_db
from app.core.security import hash_password
from app.models.schemas import StudentCreate, StudentUpdate
from typing import Optional
import csv, io

router = APIRouter(prefix="/students", tags=["Student Management"])

@router.get("")
def list_students(
    course_id: Optional[int] = None, 
    batch_id: Optional[int] = None, 
    fee_status: Optional[str] = None,
    q: Optional[str] = None
):
    with get_db() as conn:
        cur = conn.cursor()
        query = """
            SELECT s.*, c.title as course_title, c.code as course_code, 
                   b.name as batch_name, b.code as batch_code, b.timing as batch_timing
            FROM students s
            JOIN courses c ON s.course_id = c.id
            LEFT JOIN batches b ON s.batch_id = b.id
            WHERE 1=1
        """
        params = []
        if course_id:
            query += " AND s.course_id = ?"
            params.append(course_id)
        if batch_id:
            query += " AND s.batch_id = ?"
            params.append(batch_id)
        if fee_status == "paid":
            query += " AND s.due_fee <= 0"
        elif fee_status == "due":
            query += " AND s.due_fee > 0"
        if q:
            query += " AND (s.name LIKE ? OR s.roll_number LIKE ? OR s.mobile LIKE ? OR s.guardian_name LIKE ?)"
            params.extend([f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"])
            
        query += " ORDER BY s.id DESC"
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

@router.post("", status_code=201)
def create_student(s: StudentCreate):
    with get_db() as conn:
        cur = conn.cursor()
        # Next sequential Roll Number
        cur.execute("SELECT count(*) as count FROM students")
        next_num = cur.fetchone()["count"] + 1001
        roll = f"STU-2026-{next_num}"
        due = max(0.0, s.total_fee - s.paid_fee)

        # 1. Create User Account with password = DOB
        pwd_hash = hash_password(s.dob)
        cur.execute("""
            INSERT INTO users (username, email, password_hash, full_name, role_id, linked_id)
            VALUES (?, ?, ?, ?, 3, ?)
        """, (roll, s.email, pwd_hash, s.name, roll))
        user_id = cur.lastrowid

        # 2. Create Student Record
        cur.execute("""
            INSERT INTO students (
                roll_number, user_id, name, dob, course_id, batch_id, mobile, email, 
                guardian_name, guardian_mobile, gender, blood_group, address, total_fee, paid_fee, due_fee
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            roll, user_id, s.name, s.dob, s.course_id, s.batch_id, s.mobile, s.email,
            s.guardian_name, s.guardian_mobile, s.gender, s.blood_group, s.address, s.total_fee, s.paid_fee, due
        ))
        stu_id = cur.lastrowid

        # 3. If initial fee was paid, record receipt
        if s.paid_fee > 0:
            inv = f"INV-2026-00{next_num - 900}"
            import time
            cur.execute("""
                INSERT INTO fee_payments (invoice_number, student_id, amount, payment_mode, payment_date, remarks)
                VALUES (?, ?, ?, 'Counter Deposit', ?, 'Admission Enrollment Deposit')
            """, (inv, stu_id, s.paid_fee, time.strftime("%Y-%m-%d")))

        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Students')", (f"Enrolled student {roll} ({s.name}) with default DOB credentials",))
        return {
            "status": "success",
            "student_id": stu_id,
            "roll_number": roll,
            "name": s.name,
            "dob": s.dob,
            "message": f"Student enrolled successfully. Default password is DOB ({s.dob})"
        }

@router.get("/export/csv")
def export_students_csv():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.roll_number, s.name, s.dob, c.title as course, b.name as batch, 
                   s.mobile, s.email, s.guardian_name, s.total_fee, s.paid_fee, s.due_fee, 
                   s.attendance_rate, s.status
            FROM students s
            JOIN courses c ON s.course_id = c.id
            LEFT JOIN batches b ON s.batch_id = b.id
            ORDER BY s.id ASC
        """)
        rows = cur.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Roll Number", "Full Name", "DOB", "Course", "Batch", "Mobile", "Email", "Guardian", "Total Fee", "Paid Fee", "Due Fee", "Attendance %", "Status"])
        for r in rows:
            writer.writerow([r["roll_number"], r["name"], r["dob"], r["course"], r["batch"] or "N/A", r["mobile"], r["email"], r["guardian_name"], r["total_fee"], r["paid_fee"], r["due_fee"], f"{r['attendance_rate']}%", r["status"]])

        response = Response(content=output.getvalue(), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=my_education_erp_students.csv"
        return response

@router.get("/{student_id}")
def get_student(student_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.*, c.title as course_title, c.duration as course_duration, 
                   b.name as batch_name, b.timing as batch_timing, b.room as batch_room
            FROM students s
            JOIN courses c ON s.course_id = c.id
            LEFT JOIN batches b ON s.batch_id = b.id
            WHERE s.id = ? OR s.roll_number = ?
        """, (student_id, str(student_id)))
        stu = cur.fetchone()
        if not stu:
            raise HTTPException(status_code=404, detail="Student not found.")
        
        stu_dict = dict(stu)
        # Fetch fee history
        cur.execute("SELECT * FROM fee_payments WHERE student_id = ? ORDER BY id DESC", (stu_dict["id"],))
        stu_dict["fee_history"] = [dict(row) for row in cur.fetchall()]
        return stu_dict

@router.put("/{student_id}")
def update_student(student_id: int, s: StudentUpdate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = ? OR roll_number = ?", (student_id, str(student_id)))
        existing = cur.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Student not found.")

        updates = []
        params = []
        for field, val in s.dict(exclude_unset=True).items():
            if val is not None:
                updates.append(f"{field} = ?")
                params.append(val)

        if updates:
            # Recompute due_fee if total_fee or paid_fee changed
            if s.total_fee is not None or s.paid_fee is not None:
                new_tot = s.total_fee if s.total_fee is not None else existing["total_fee"]
                new_pd = s.paid_fee if s.paid_fee is not None else existing["paid_fee"]
                updates.append("due_fee = ?")
                params.append(max(0.0, new_tot - new_pd))

            params.append(existing["id"])
            query = f"UPDATE students SET {', '.join(updates)} WHERE id = ?"
            cur.execute(query, params)

            # Sync user account if name or email changed
            if s.name or s.email:
                cur.execute("UPDATE users SET full_name = COALESCE(?, full_name), email = COALESCE(?, email) WHERE linked_id = ?", (s.name, s.email, existing["roll_number"]))

            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Students')", (f"Updated student record [{existing['roll_number']}] {existing['name']}",))

        return {"status": "success", "message": "Student details updated successfully."}

@router.delete("/{student_id}")
def delete_student(student_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = ? OR roll_number = ?", (student_id, str(student_id)))
        s = cur.fetchone()
        if not s:
            raise HTTPException(status_code=404, detail="Student not found.")

        # Delete student record (and linked user account)
        cur.execute("DELETE FROM students WHERE id = ?", (s["id"],))
        cur.execute("DELETE FROM users WHERE linked_id = ?", (s["roll_number"],))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Students')", (f"Deleted student record [{s['roll_number']}] {s['name']}",))
        return {"status": "success", "message": f"Student {s['roll_number']} removed from institutional database."}
