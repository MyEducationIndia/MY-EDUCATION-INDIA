from fastapi import APIRouter
from app.core.database import get_db

router = APIRouter(prefix="/reports", tags=["Operational Reports & Analytics"])

@router.get("/summary")
def get_reports_summary():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT count(*) as total_students, COALESCE(SUM(paid_fee), 0) as total_collected, COALESCE(SUM(due_fee), 0) as total_dues FROM students")
        row = dict(cur.fetchone())
        
        cur.execute("SELECT count(*) as active_staff FROM staff WHERE status = 'Active'")
        row["active_staff"] = cur.fetchone()["active_staff"]
        
        cur.execute("SELECT count(*) as total_courses FROM courses WHERE is_active = 1")
        row["total_courses"] = cur.fetchone()["total_courses"]

        cur.execute("SELECT count(*) as pending_admissions FROM admissions WHERE status = 'Pending Review'")
        row["pending_admissions"] = cur.fetchone()["pending_admissions"]

        cur.execute("SELECT count(*) as active_batches FROM batches WHERE status = 'Active'")
        row["active_batches"] = cur.fetchone()["active_batches"]

        cur.execute("SELECT count(*) as total_users FROM users WHERE is_active = 1")
        row["total_users"] = cur.fetchone()["total_users"]

        # Course breakdown
        cur.execute("""
            SELECT c.title, c.code, count(s.id) as student_count
            FROM courses c
            LEFT JOIN students s ON c.id = s.course_id
            GROUP BY c.id
            ORDER BY student_count DESC
        """)
        row["course_breakdown"] = [dict(r) for r in cur.fetchall()]
        return row

@router.get("/admissions-trend")
def get_admissions_trend():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT strftime('%Y-%m', created_at) as month, count(*) as count 
            FROM admissions 
            GROUP BY month 
            ORDER BY month DESC 
            LIMIT 6
        """)
        return [dict(r) for r in cur.fetchall()]

@router.get("/fees-trend")
def get_fees_trend():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT strftime('%Y-%m', payment_date) as month, SUM(amount) as total_amount 
            FROM fee_payments 
            GROUP BY month 
            ORDER BY month DESC 
            LIMIT 6
        """)
        return [dict(r) for r in cur.fetchall()]
