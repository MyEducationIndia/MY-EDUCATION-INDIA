import json
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import (
    Admission,
    Batch,
    Course,
    Expense,
    FeePayment,
    SharedInstitutionalState,
    Staff,
    Student,
    User,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/reports", tags=["Operational Reports & Analytics"])


@router.get("/summary")
def get_reports_summary(db: Session = Depends(get_db)):
    total_students = db.query(func.count(Student.id)).scalar() or 0
    total_collected = float(db.query(func.coalesce(func.sum(Student.paid_fee), 0.0)).scalar() or 0.0)
    total_dues = float(db.query(func.coalesce(func.sum(Student.due_fee), 0.0)).scalar() or 0.0)
    total_expenses = float(db.query(func.coalesce(func.sum(Expense.amount), 0.0)).scalar() or 0.0)
    active_staff = db.query(func.count(Staff.id)).filter(Staff.status == "Active").scalar() or 0
    total_courses = db.query(func.count(Course.id)).filter(Course.is_active == 1).scalar() or 0
    pending_admissions = (
        db.query(func.count(Admission.id)).filter(Admission.status == "Pending Review").scalar() or 0
    )
    active_batches = db.query(func.count(Batch.id)).filter(Batch.status == "Active").scalar() or 0
    total_users = db.query(func.count(User.id)).filter(User.is_active == 1).scalar() or 0

    # Reconcile with SharedInstitutionalState if records were added via unified state sync
    shared_row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
    if shared_row and shared_row.state_json:
        try:
            st = json.loads(shared_row.state_json)
            st_students = st.get("students") if isinstance(st.get("students"), list) else []
            st_staff = st.get("staff") if isinstance(st.get("staff"), list) else []
            st_admissions = st.get("admissions") if isinstance(st.get("admissions"), list) else []
            st_courses = st.get("courses") if isinstance(st.get("courses"), list) else []
            st_expenses = st.get("expenses") if isinstance(st.get("expenses"), list) else []

            if len(st_students) > total_students:
                total_students = len(st_students)
                total_collected = sum(float(s.get("paidFee", 0) or 0) for s in st_students if isinstance(s, dict))
                total_dues = sum(
                    max(0.0, float(s.get("totalFee", 0) or 0) - float(s.get("paidFee", 0) or 0))
                    for s in st_students
                    if isinstance(s, dict)
                )
            if len(st_staff) > active_staff:
                active_staff = len(st_staff)
            if len(st_courses) > total_courses:
                total_courses = len(st_courses)
            st_pending_adm = sum(1 for a in st_admissions if isinstance(a, dict) and a.get("status") == "Pending")
            if st_pending_adm > pending_admissions:
                pending_admissions = st_pending_adm
            st_exp_sum = sum(float(e.get("amount", 0) or 0) for e in st_expenses if isinstance(e, dict))
            if st_exp_sum > total_expenses:
                total_expenses = st_exp_sum
        except Exception:
            pass

    course_counts = (
        db.query(Course.title, Course.code, func.count(Student.id).label("student_count"))
        .outerjoin(Student, Course.id == Student.course_id)
        .group_by(Course.id, Course.title, Course.code)
        .order_by(func.count(Student.id).desc())
        .all()
    )

    return {
        "total_students": total_students,
        "total_collected": float(total_collected),
        "total_dues": float(total_dues),
        "total_expenses": float(total_expenses),
        "net_surplus": float(total_collected) - float(total_expenses),
        "active_staff": active_staff,
        "total_courses": total_courses,
        "pending_admissions": pending_admissions,
        "active_batches": active_batches,
        "total_users": total_users,
        "course_breakdown": [
            {"title": cc[0], "code": cc[1], "student_count": cc[2]}
            for cc in course_counts
        ],
    }


@router.get("/admissions-trend")
def get_admissions_trend(db: Session = Depends(get_db)):
    try:
        month_expr = func.to_char(Admission.created_at, "YYYY-MM")
        results = (
            db.query(month_expr.label("month"), func.count(Admission.id).label("count"))
            .group_by(month_expr)
            .order_by(month_expr.desc())
            .limit(6)
            .all()
        )
        return [{"month": r[0], "count": r[1]} for r in results]
    except Exception as exc:
        logger.debug("Admissions trend aggregation fallback: %s", exc)
        return []


@router.get("/fees-trend")
def get_fees_trend(db: Session = Depends(get_db)):
    try:
        month_expr = func.to_char(FeePayment.payment_date, "YYYY-MM")
        results = (
            db.query(month_expr.label("month"), func.sum(FeePayment.amount).label("total_amount"))
            .group_by(month_expr)
            .order_by(month_expr.desc())
            .limit(6)
            .all()
        )
        return [{"month": r[0], "total_amount": float(r[1]) if r[1] else 0.0} for r in results]
    except Exception as exc:
        logger.debug("Fees trend aggregation fallback: %s", exc)
        return []
