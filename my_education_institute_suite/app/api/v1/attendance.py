from fastapi import APIRouter, HTTPException, Query
from app.core.database import get_db
from app.models.schemas import AttendanceRecord
from typing import List, Optional
import time

router = APIRouter(prefix="/attendance", tags=["Attendance Register"])

@router.post("")
def record_attendance(records: List[AttendanceRecord]):
    with get_db() as conn:
        cur = conn.cursor()
        for r in records:
            cur.execute("""
                INSERT OR REPLACE INTO attendance (student_id, batch_id, date, status, remarks)
                VALUES (?, ?, ?, ?, ?)
            """, (r.student_id, r.batch_id, r.date, r.status, r.remarks))
            
            # Recalculate student attendance percentage
            cur.execute("SELECT count(*) as total, sum(case when status='Present' then 1 else 0 end) as present FROM attendance WHERE student_id = ?", (r.student_id,))
            stat = cur.fetchone()
            if stat and stat["total"] > 0:
                pct = round((stat["present"] / stat["total"]) * 100, 1)
                cur.execute("UPDATE students SET attendance_rate = ? WHERE id = ?", (pct, r.student_id))

        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('staff', ?, 'Attendance')", (f"Submitted daily attendance register for {len(records)} students",))
        return {"status": "success", "count": len(records), "message": "Attendance records saved."}

@router.get("/batch/{batch_id}")
def get_batch_attendance(batch_id: int, date: Optional[str] = None):
    with get_db() as conn:
        cur = conn.cursor()
        target_date = date or time.strftime("%Y-%m-%d")
        cur.execute("""
            SELECT s.id as student_id, s.roll_number, s.name, s.attendance_rate,
                   COALESCE(a.status, 'Present') as status, COALESCE(a.remarks, '') as remarks
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
            WHERE s.batch_id = ?
            ORDER BY s.roll_number ASC
        """, (target_date, batch_id))
        return [dict(row) for row in cur.fetchall()]

@router.get("/student/{student_id}")
def get_student_attendance(student_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.*, b.name as batch_name
            FROM attendance a
            JOIN batches b ON a.batch_id = b.id
            WHERE a.student_id = ?
            ORDER BY a.date DESC
        """, (student_id,))
        return [dict(row) for row in cur.fetchall()]
