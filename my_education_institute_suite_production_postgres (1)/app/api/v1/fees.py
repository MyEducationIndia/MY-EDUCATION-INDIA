from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.core.database import get_db
from app.models.entities import FeePayment, Student, Course, Batch, AuditLog
from app.models.schemas import FeePaymentCreate, FeePaymentUpdate
from datetime import date, datetime
import random, time

router = APIRouter(prefix="/fees", tags=["Fee Management & Invoices"])

@router.get("")
def list_fees(student_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(FeePayment).join(Student, FeePayment.student_id == Student.id).join(Course, Student.course_id == Course.id)
        if student_id:
            query = query.filter(FeePayment.student_id == student_id)
        fees = query.order_by(FeePayment.id.desc()).all()

        return [
            {
                "id": fp.id,
                "invoice_number": fp.invoice_number,
                "student_id": fp.student_id,
                "student_name": fp.student.name if fp.student else None,
                "roll_number": fp.student.roll_number if fp.student else None,
                "course_title": fp.student.course.title if (fp.student and fp.student.course) else None,
                "amount": fp.amount,
                "payment_mode": fp.payment_mode,
                "payment_date": fp.payment_date.strftime("%Y-%m-%d") if fp.payment_date else None,
                "remarks": fp.remarks,
                "receipt_data": fp.receipt_data,
                "created_at": fp.created_at.strftime("%Y-%m-%d %H:%M:%S") if fp.created_at else None
            }
            for fp in fees
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve fee records.")

@router.post("/pay", status_code=201)
def record_payment(p: FeePaymentCreate, db: Session = Depends(get_db)):
    try:
        stu = db.query(Student).filter(or_(Student.id == p.student_id, Student.roll_number == str(p.student_id))).first()
        if not stu:
            raise HTTPException(status_code=404, detail="Student not found.")

        inv = f"INV-2026-00{random.randint(50, 999)}"
        today = date.today()

        payment = FeePayment(
            invoice_number=inv,
            student_id=stu.id,
            amount=p.amount,
            payment_mode=p.payment_mode,
            payment_date=today,
            remarks=p.remarks
        )
        db.add(payment)

        # Update student dues
        stu.paid_fee += p.amount
        stu.due_fee = max(0.0, stu.due_fee - p.amount)

        db.add(AuditLog(actor="admin", action=f"Collected fee ₹{p.amount} from {stu.name} ({inv})", module="Finance"))
        return {
            "status": "success",
            "invoice_number": inv,
            "student_name": stu.name,
            "amount": p.amount,
            "payment_date": today.strftime("%Y-%m-%d"),
            "message": f"Payment of ₹{p.amount} recorded successfully."
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to record payment: {str(e)}")

@router.get("/invoice/{invoice_no}")
def get_invoice(invoice_no: str, db: Session = Depends(get_db)):
    try:
        fp = db.query(FeePayment).join(Student, FeePayment.student_id == Student.id).filter(FeePayment.invoice_number == invoice_no).first()
        if not fp:
            raise HTTPException(status_code=404, detail="Invoice receipt not found.")

        stu = fp.student
        return {
            "id": fp.id,
            "invoice_number": fp.invoice_number,
            "student_id": fp.student_id,
            "student_name": stu.name if stu else None,
            "roll_number": stu.roll_number if stu else None,
            "dob": stu.dob if stu else None,
            "guardian_name": stu.guardian_name if stu else None,
            "total_fee": stu.total_fee if stu else 0.0,
            "paid_fee": stu.paid_fee if stu else 0.0,
            "due_fee": stu.due_fee if stu else 0.0,
            "course_title": stu.course.title if (stu and stu.course) else None,
            "batch_name": stu.batch.name if (stu and stu.batch) else None,
            "amount": fp.amount,
            "payment_mode": fp.payment_mode,
            "payment_date": fp.payment_date.strftime("%Y-%m-%d") if fp.payment_date else None,
            "remarks": fp.remarks
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve invoice.")

@router.put("/{payment_id}")
def update_payment(payment_id: int, p: FeePaymentUpdate, db: Session = Depends(get_db)):
    try:
        fp = db.query(FeePayment).filter(FeePayment.id == payment_id).first()
        if not fp:
            raise HTTPException(status_code=404, detail="Payment record not found.")

        if p.amount is not None:
            diff = p.amount - fp.amount
            fp.amount = p.amount
            if fp.student:
                fp.student.paid_fee += diff
                fp.student.due_fee = max(0.0, fp.student.due_fee - diff)
        if p.payment_mode is not None:
            fp.payment_mode = p.payment_mode
        if p.remarks is not None:
            fp.remarks = p.remarks

        db.add(AuditLog(actor="admin", action=f"Updated fee payment [{fp.invoice_number}]", module="Finance"))
        return {"status": "success", "message": "Payment updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update payment: {str(e)}")

@router.patch("/{payment_id}")
def patch_payment(payment_id: int, p: FeePaymentUpdate, db: Session = Depends(get_db)):
    return update_payment(payment_id, p, db)

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        fp = db.query(FeePayment).filter(FeePayment.id == payment_id).first()
        if not fp:
            raise HTTPException(status_code=404, detail="Payment record not found.")

        inv = fp.invoice_number
        amount = fp.amount
        if fp.student:
            fp.student.paid_fee = max(0.0, fp.student.paid_fee - amount)
            fp.student.due_fee += amount

        db.delete(fp)
        db.add(AuditLog(actor="admin", action=f"Deleted fee receipt [{inv}] of ₹{amount}", module="Finance"))
        return {"status": "success", "message": f"Payment {inv} deleted."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete payment: {str(e)}")
