from fastapi import APIRouter, HTTPException, Query
from app.core.database import get_db
from app.models.schemas import FeePaymentCreate
import time, random

router = APIRouter(prefix="/fees", tags=["Fee Management & Invoices"])

@router.get("")
def list_fees(student_id: int = None):
    with get_db() as conn:
        cur = conn.cursor()
        query = """
            SELECT fp.*, s.name as student_name, s.roll_number, c.title as course_title
            FROM fee_payments fp
            JOIN students s ON fp.student_id = s.id
            JOIN courses c ON s.course_id = c.id
            WHERE 1=1
        """
        params = []
        if student_id:
            query += " AND fp.student_id = ?"
            params.append(student_id)
        query += " ORDER BY fp.id DESC"
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

@router.post("/pay", status_code=201)
def record_payment(p: FeePaymentCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = ? OR roll_number = ?", (p.student_id, str(p.student_id)))
        stu = cur.fetchone()
        if not stu:
            raise HTTPException(status_code=404, detail="Student not found.")

        inv = f"INV-2026-00{random.randint(50, 999)}"
        today = time.strftime("%Y-%m-%d")

        cur.execute("""
            INSERT INTO fee_payments (invoice_number, student_id, amount, payment_mode, payment_date, remarks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (inv, stu["id"], p.amount, p.payment_mode, today, p.remarks))

        # Update student dues
        cur.execute("""
            UPDATE students 
            SET paid_fee = paid_fee + ?, due_fee = MAX(0, due_fee - ?) 
            WHERE id = ?
        """, (p.amount, p.amount, stu["id"]))

        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Finance')", (f"Collected fee ₹{p.amount} from {stu['name']} ({inv})",))
        return {
            "status": "success",
            "invoice_number": inv,
            "student_name": stu["name"],
            "amount": p.amount,
            "payment_date": today,
            "message": f"Payment of ₹{p.amount} recorded successfully."
        }

@router.get("/invoice/{invoice_no}")
def get_invoice(invoice_no: str):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT fp.*, s.name as student_name, s.roll_number, s.dob, s.guardian_name, s.total_fee, s.paid_fee, s.due_fee,
                   c.title as course_title, b.name as batch_name
            FROM fee_payments fp
            JOIN students s ON fp.student_id = s.id
            JOIN courses c ON s.course_id = c.id
            LEFT JOIN batches b ON s.batch_id = b.id
            WHERE fp.invoice_number = ?
        """, (invoice_no,))
        inv = cur.fetchone()
        if not inv:
            raise HTTPException(status_code=404, detail="Invoice receipt not found.")
        return dict(inv)
