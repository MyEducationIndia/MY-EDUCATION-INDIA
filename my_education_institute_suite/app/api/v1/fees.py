import random
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import AuditLog, Course, Expense, FeeHead, FeePayment, Student
from app.models.schemas import (
    ExpenseCreate,
    FeeHeadCreate,
    FeeHeadUpdate,
    FeePaymentCreate,
    FeePaymentUpdate,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/fees", tags=["Fee Management & Invoices"])


@router.get("")
def list_fees(
    student_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    try:
        query = (
            db.query(FeePayment)
            .join(Student, FeePayment.student_id == Student.id)
            .join(Course, Student.course_id == Course.id)
        )
        if student_id:
            query = query.filter(FeePayment.student_id == student_id)
        fees = query.order_by(FeePayment.id.desc()).offset(skip).limit(limit).all()

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
                "created_at": fp.created_at.strftime("%Y-%m-%d %H:%M:%S") if fp.created_at else None,
            }
            for fp in fees
        ]
    except Exception as exc:
        logger.error("Failed to list fees: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve fee records.")


@router.post("/pay", status_code=201)
def record_payment(p: FeePaymentCreate, db: Session = Depends(get_db)):
    try:
        stu = (
            db.query(Student)
            .filter(or_(Student.id == p.student_id, Student.roll_number == str(p.student_id)))
            .first()
        )
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
            remarks=p.remarks,
            receipt_data=p.receipt_data,
        )
        db.add(payment)

        stu.paid_fee += p.amount
        stu.due_fee = max(0.0, stu.due_fee - p.amount)

        db.add(AuditLog(actor="admin", action=f"Collected fee ₹{p.amount} from {stu.name} ({inv})", module="Finance"))
        return {
            "status": "success",
            "invoice_number": inv,
            "student_name": stu.name,
            "amount": p.amount,
            "payment_date": today.strftime("%Y-%m-%d"),
            "message": f"Payment of ₹{p.amount} recorded successfully.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to record fee payment: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to record payment: {str(exc)}")


@router.get("/invoice/{invoice_no}")
def get_invoice(invoice_no: str, db: Session = Depends(get_db)):
    try:
        fp = (
            db.query(FeePayment)
            .join(Student, FeePayment.student_id == Student.id)
            .filter(FeePayment.invoice_number == invoice_no)
            .first()
        )
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
            "remarks": fp.remarks,
            "receipt_data": fp.receipt_data,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Failed to retrieve invoice %s: %s", invoice_no, exc)
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
        if p.receipt_data is not None:
            fp.receipt_data = p.receipt_data

        db.add(AuditLog(actor="admin", action=f"Updated fee payment [{fp.invoice_number}]", module="Finance"))
        return {"status": "success", "message": "Payment updated successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update payment %s: %s", payment_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update payment: {str(exc)}")


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
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete payment %s: %s", payment_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete payment: {str(exc)}")


# Master Fee Heads Relational CRUD
@router.get("/heads")
def list_fee_heads(db: Session = Depends(get_db)):
    heads = db.query(FeeHead).order_by(FeeHead.id.asc()).all()
    return [
        {
            "id": h.id,
            "code": h.code,
            "title": h.title,
            "category": h.category,
            "course": h.course,
            "defaultAmount": h.default_amount,
            "gst": h.gst,
            "mandatory": bool(h.mandatory),
        }
        for h in heads
    ]


@router.post("/heads", status_code=201)
def create_fee_head(fh: FeeHeadCreate, db: Session = Depends(get_db)):
    try:
        head_id = fh.id or f"FH-{random.randint(200, 999)}"
        new_head = FeeHead(
            id=head_id,
            code=fh.code.upper(),
            title=fh.title,
            category=fh.category,
            course=fh.course,
            default_amount=fh.default_amount,
            gst=fh.gst,
            mandatory=1 if fh.mandatory else 0,
        )
        db.add(new_head)
        db.flush()
        db.add(AuditLog(actor="accounts", action=f"Created Fee Head [{fh.code}] {fh.title}", module="Finance"))
        return {"status": "success", "id": head_id, "code": fh.code}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create fee head: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create fee head: {str(exc)}")


@router.put("/heads/{head_id}")
def update_fee_head(head_id: str, fh: FeeHeadUpdate, db: Session = Depends(get_db)):
    try:
        head = db.query(FeeHead).filter(FeeHead.id == head_id).first()
        if not head:
            raise HTTPException(status_code=404, detail="Fee head not found.")
        if fh.code is not None:
            head.code = fh.code.upper()
        if fh.title is not None:
            head.title = fh.title
        if fh.category is not None:
            head.category = fh.category
        if fh.course is not None:
            head.course = fh.course
        if fh.default_amount is not None:
            head.default_amount = fh.default_amount
        if fh.gst is not None:
            head.gst = fh.gst
        if fh.mandatory is not None:
            head.mandatory = 1 if fh.mandatory else 0
        return {"status": "success", "message": "Fee head updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update fee head %s: %s", head_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update fee head: {str(exc)}")


@router.delete("/heads/{head_id}")
def delete_fee_head(head_id: str, db: Session = Depends(get_db)):
    try:
        head = db.query(FeeHead).filter(FeeHead.id == head_id).first()
        if not head:
            raise HTTPException(status_code=404, detail="Fee head not found.")
        db.delete(head)
        return {"status": "success", "message": "Fee head deleted."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete fee head %s: %s", head_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete fee head: {str(exc)}")


# Institute Expense Vouchers Relational CRUD
@router.get("/expenses")
def list_expenses(db: Session = Depends(get_db)):
    exps = db.query(Expense).order_by(Expense.id.desc()).all()
    return [
        {
            "id": ex.id,
            "category": ex.category,
            "amount": ex.amount,
            "payee": ex.payee,
            "mode": ex.mode,
            "notes": ex.notes,
            "date": ex.expense_date,
        }
        for ex in exps
    ]


@router.post("/expenses", status_code=201)
def create_expense(ex: ExpenseCreate, db: Session = Depends(get_db)):
    try:
        v_id = ex.id or f"VCH-2026-{random.randint(1000, 9999)}"
        exp_date = ex.expense_date or date.today().strftime("%Y-%m-%d")
        new_exp = Expense(
            id=v_id,
            category=ex.category,
            amount=ex.amount,
            payee=ex.payee,
            mode=ex.mode,
            notes=ex.notes or "",
            expense_date=exp_date,
        )
        db.add(new_exp)
        db.flush()
        db.add(AuditLog(actor="accounts", action=f"Recorded expense voucher [{v_id}] ₹{ex.amount}", module="Finance"))
        return {"status": "success", "id": v_id, "amount": ex.amount}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create expense: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create expense voucher: {str(exc)}")


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str, db: Session = Depends(get_db)):
    try:
        ex = db.query(Expense).filter(Expense.id == expense_id).first()
        if not ex:
            raise HTTPException(status_code=404, detail="Expense voucher not found.")
        db.delete(ex)
        return {"status": "success", "message": "Expense voucher deleted."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete expense %s: %s", expense_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete expense: {str(exc)}")
