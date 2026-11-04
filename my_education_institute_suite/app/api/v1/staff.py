from fastapi import APIRouter, HTTPException, Query
from app.core.database import get_db
from app.core.security import hash_password
from app.models.schemas import StaffCreate, StaffUpdate, LeaveApplyRequest
from typing import Optional

router = APIRouter(prefix="/staff", tags=["Faculty & Staff Management"])

@router.get("")
def list_staff(department: Optional[str] = None):
    with get_db() as conn:
        cur = conn.cursor()
        query = "SELECT * FROM staff WHERE 1=1"
        params = []
        if department and department != "all":
            query += " AND department = ?"
            params.append(department)
        query += " ORDER BY id ASC"
        cur.execute(query, params)
        staff_list = [dict(row) for row in cur.fetchall()]

        # Attach assigned batches
        for s in staff_list:
            cur.execute("SELECT code, name, timing FROM batches WHERE trainer_id = ?", (s["id"],))
            s["assigned_batches"] = [dict(b) for b in cur.fetchall()]
        return staff_list

@router.post("", status_code=201)
def create_staff(st: StaffCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT count(*) as count FROM staff")
        next_id = cur.fetchone()["count"] + 101
        emp_code = f"STF-{next_id}"
        u_name = f"staff.{st.name.lower().split()[0]}"

        # 1. Create User account
        pwd_hash = hash_password("Staff@1234")
        cur.execute("""
            INSERT INTO users (username, email, password_hash, full_name, role_id, linked_id)
            VALUES (?, ?, ?, ?, 2, ?)
        """, (u_name, st.email, pwd_hash, st.name, emp_code))
        user_id = cur.lastrowid

        # 2. Create Staff record
        cur.execute("""
            INSERT INTO staff (employee_code, user_id, name, designation, department, qualification, salary_amount, phone, email, joining_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
        """, (emp_code, user_id, st.name, st.designation, st.department, st.qualification, st.salary_amount, st.phone, st.email))
        staff_id = cur.lastrowid

        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Staff')", (f"Added faculty member [{emp_code}] {st.name}",))
        return {"status": "success", "staff_id": staff_id, "employee_code": emp_code, "username": u_name}

@router.put("/{staff_id}")
def update_staff(staff_id: int, st: StaffUpdate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM staff WHERE id = ? OR employee_code = ?", (staff_id, str(staff_id)))
        existing = cur.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Staff member not found.")

        updates = []
        params = []
        for field, val in st.dict(exclude_unset=True).items():
            if val is not None:
                updates.append(f"{field} = ?")
                params.append(val)

        if updates:
            params.append(existing["id"])
            cur.execute(f"UPDATE staff SET {', '.join(updates)} WHERE id = ?", params)
            if st.name or st.email:
                cur.execute("UPDATE users SET full_name = COALESCE(?, full_name), email = COALESCE(?, email) WHERE linked_id = ?", (st.name, st.email, existing["employee_code"]))
            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Staff')", (f"Updated faculty profile [{existing['employee_code']}]",))

        return {"status": "success", "message": "Staff details updated successfully."}

@router.delete("/{staff_id}")
def delete_staff(staff_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM staff WHERE id = ? OR employee_code = ?", (staff_id, str(staff_id)))
        s = cur.fetchone()
        if not s:
            raise HTTPException(status_code=404, detail="Staff member not found.")

        cur.execute("DELETE FROM staff WHERE id = ?", (s["id"],))
        cur.execute("DELETE FROM users WHERE linked_id = ?", (s["employee_code"],))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Staff')", (f"Deleted faculty member [{s['employee_code']}] {s['name']}",))
        return {"status": "success", "message": f"Staff member {s['employee_code']} deleted."}

# Leave Management
@router.post("/leave/apply")
def apply_leave(req: LeaveApplyRequest):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO staff_leaves (staff_id, leave_type, start_date, end_date, reason, status)
            VALUES (?, ?, ?, ?, ?, 'Pending')
        """, (req.staff_id, req.leave_type, req.start_date, req.end_date, req.reason))
        leave_id = cur.lastrowid
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('staff', ?, 'Leaves')", (f"Applied for {req.leave_type} leave from {req.start_date} to {req.end_date}",))
        return {"status": "success", "leave_id": leave_id, "message": "Leave application submitted."}

@router.get("/leave")
def list_leaves(staff_id: Optional[int] = None):
    with get_db() as conn:
        cur = conn.cursor()
        query = "SELECT l.*, s.name as staff_name, s.employee_code FROM staff_leaves l JOIN staff s ON l.staff_id = s.id WHERE 1=1"
        params = []
        if staff_id:
            query += " AND l.staff_id = ?"
            params.append(staff_id)
        query += " ORDER BY l.id DESC"
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]
