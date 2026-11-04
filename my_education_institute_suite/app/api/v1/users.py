from fastapi import APIRouter, HTTPException, Query
from app.core.database import get_db
from app.core.security import hash_password
from app.models.schemas import UserCreate, UserUpdate
from typing import Optional

router = APIRouter(prefix="/users", tags=["Master User Accounts & Credentials"])

@router.get("")
def list_users(role: Optional[str] = None, q: Optional[str] = None):
    with get_db() as conn:
        cur = conn.cursor()
        query = """
            SELECT u.id, u.username, u.email, u.full_name, u.role_id, r.name as role, 
                   u.linked_id, u.is_active, u.created_at, u.last_login
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE 1=1
        """
        params = []
        if role and role != "all":
            query += " AND r.name = ?"
            params.append(role)
        if q:
            query += " AND (u.username LIKE ? OR u.full_name LIKE ? OR u.email LIKE ? OR u.linked_id LIKE ?)"
            params.extend([f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"])
        query += " ORDER BY u.id ASC"
        cur.execute(query, params)
        users = [dict(row) for row in cur.fetchall()]
        
        # Attach DOB if student
        for u in users:
            if u["role"] == "student" and u["linked_id"]:
                cur.execute("SELECT dob FROM students WHERE roll_number = ?", (u["linked_id"],))
                st = cur.fetchone()
                if st:
                    u["dob"] = st["dob"]
        return users

@router.post("", status_code=201)
def create_user(u: UserCreate):
    with get_db() as conn:
        cur = conn.cursor()
        # Default password if not provided
        pwd = u.password or "User@1234"
        pwd_hash = hash_password(pwd)
        try:
            cur.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role_id, linked_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (u.username, u.email, pwd_hash, u.full_name, u.role_id, u.linked_id))
            user_id = cur.lastrowid
            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Users')", (f"Created user account [{u.username}]",))
            return {"status": "success", "user_id": user_id, "username": u.username}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create user: {str(e)}")

@router.put("/{user_id}")
def update_user(user_id: int, u: UserUpdate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        existing = cur.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="User account not found.")

        updates = []
        params = []
        if u.full_name is not None:
            updates.append("full_name = ?")
            params.append(u.full_name)
        if u.username is not None:
            updates.append("username = ?")
            params.append(u.username)
        if u.email is not None:
            updates.append("email = ?")
            params.append(u.email)
        if u.password is not None and len(u.password.strip()) > 0:
            updates.append("password_hash = ?")
            params.append(hash_password(u.password.strip()))
        if u.is_active is not None:
            updates.append("is_active = ?")
            params.append(u.is_active)

        if updates:
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            cur.execute(query, params)

            # Sync full_name and email to student or staff record if linked
            if existing["linked_id"]:
                if u.full_name or u.email:
                    cur.execute("UPDATE students SET name = COALESCE(?, name), email = COALESCE(?, email) WHERE roll_number = ?", (u.full_name, u.email, existing["linked_id"]))
                    cur.execute("UPDATE staff SET name = COALESCE(?, name), email = COALESCE(?, email) WHERE employee_code = ?", (u.full_name, u.email, existing["linked_id"]))

            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Users')", (f"Updated credentials for user [{existing['username']}]",))

        return {"status": "success", "message": "User credentials updated successfully."}

@router.post("/{user_id}/reset-dob")
def reset_user_to_dob(user_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT u.*, r.name as role FROM users u JOIN roles r ON u.role_id = r.id WHERE u.id = ?", (user_id,))
        u = cur.fetchone()
        if not u or u["role"] != "student" or not u["linked_id"]:
            raise HTTPException(status_code=400, detail="User is not a student or has no linked Roll Number.")

        cur.execute("SELECT dob FROM students WHERE roll_number = ?", (u["linked_id"],))
        stu = cur.fetchone()
        if not stu or not stu["dob"]:
            raise HTTPException(status_code=404, detail="Student date of birth not found in database.")

        dob = stu["dob"]
        new_hash = hash_password(dob)
        cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Users')", (f"Reset password of student [{u['username']}] to DOB ({dob})",))

        return {"status": "success", "message": f"Password reset to official DOB: {dob}", "dob": dob}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        u = cur.fetchone()
        if not u:
            raise HTTPException(status_code=404, detail="User not found.")
        if u["role_id"] == 1 and u["username"] == "admin":
            raise HTTPException(status_code=400, detail="Cannot delete root Super Administrator account.")

        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Users')", (f"Deleted user account [{u['username']}]",))
        return {"status": "success", "message": "User account removed."}
