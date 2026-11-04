from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.entities import Student, Staff, Course, Admission, Batch, User, FeePayment

router = APIRouter(prefix="/reports", tags=["Operational Reports & Analytics"])

@router.get("/summary")
def get_reports_summary(db: Session = Depends(get_db)):
    total_students = db.query(func.count(Student.id)).scalar() or 0
    total_collected = db.query(func.coalesce(func.sum(Student.paid_fee), 0.0)).scalar() or 0.0
    total_dues = db.query(func.coalesce(func.sum(Student.due_fee), 0.0)).scalar() or 0.0
    active_staff = db.query(func.count(Staff.id)).filter(Staff.status == "Active").scalar() or 0
    total_courses = db.query(func.count(Course.id)).filter(Course.is_active == 1).scalar() or 0
    pending_admissions = db.query(func.count(Admission.id)).filter(Admission.status == "Pending Review").scalar() or 0
    active_batches = db.query(func.count(Batch.id)).filter(Batch.status == "Active").scalar() or 0
    total_users = db.query(func.count(User.id)).filter(User.is_active == 1).scalar() or 0

    # Course breakdown
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
        "active_staff": active_staff,
        "total_courses": total_courses,
        "pending_admissions": pending_admissions,
        "active_batches": active_batches,
        "total_users": total_users,
        "course_breakdown": [
            {"title": cc[0], "code": cc[1], "student_count": cc[2]}
            for cc in course_counts
        ]
    }

@router.get("/admissions-trend")
def get_admissions_trend(db: Session = Depends(get_db)):
    try:
        month_expr = func.to_char(Admission.created_at, 'YYYY-MM')
        results = (
            db.query(month_expr.label("month"), func.count(Admission.id).label("count"))
            .group_by(month_expr)
            .order_by(month_expr.desc())
            .limit(6)
            .all()
        )
        return [{"month": r[0], "count": r[1]} for r in results]
    except Exception:
        return []

@router.get("/fees-trend")
def get_fees_trend(db: Session = Depends(get_db)):
    try:
        month_expr = func.to_char(FeePayment.payment_date, 'YYYY-MM')
        results = (
            db.query(month_expr.label("month"), func.sum(FeePayment.amount).label("total_amount"))
            .group_by(month_expr)
            .order_by(month_expr.desc())
            .limit(6)
            .all()
        )
        return [{"month": r[0], "total_amount": float(r[1]) if r[1] else 0.0} for r in results]
    except Exception:
        return []
