from datetime import date, datetime
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import Attendance, AuditLog, Batch, Student
from app.models.schemas import AttendanceRecord

logger = get_logger(__name__)
router = APIRouter(prefix="/attendance", tags=["Attendance Register"])


@router.post("")
def record_attendance(records: List[AttendanceRecord], db: Session = Depends(get_db)):
    try:
        updated_student_ids = set()
        for r in records:
            att_date = datetime.strptime(r.date, "%Y-%m-%d").date()
            existing = (
                db.query(Attendance)
                .filter(
                    Attendance.student_id == r.student_id,
                    Attendance.batch_id == r.batch_id,
                    Attendance.date == att_date,
                )
                .first()
            )

            if existing:
                existing.status = r.status
                existing.remarks = r.remarks or ""
            else:
                db.add(
                    Attendance(
                        student_id=r.student_id,
                        batch_id=r.batch_id,
                        date=att_date,
                        status=r.status,
                        remarks=r.remarks or "",
                    )
                )
            updated_student_ids.add(r.student_id)

        db.flush()

        for stu_id in updated_student_ids:
            stu_records = db.query(Attendance).filter(Attendance.student_id == stu_id).all()
            total_count = len(stu_records)
            if total_count > 0:
                present_count = sum(1 for a in stu_records if a.status == "Present")
                pct = round((present_count / total_count) * 100.0, 1)
                stu = db.query(Student).filter(Student.id == stu_id).first()
                if stu:
                    stu.attendance_rate = pct

        db.add(
            AuditLog(
                actor="staff",
                action=f"Submitted daily attendance register for {len(records)} students",
                module="Attendance",
            )
        )
        db.commit()
        return {"status": "success", "count": len(records), "message": "Attendance records saved."}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to record attendance: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to record attendance: {str(exc)}")


@router.get("/batch/{batch_id}")
def get_batch_attendance(
    batch_id: int,
    date_str: Optional[str] = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
        students = db.query(Student).filter(Student.batch_id == batch_id).order_by(Student.roll_number.asc()).all()

        # Batch fetch attendance for target_date to eliminate N+1 queries
        att_rows = (
            db.query(Attendance)
            .filter(Attendance.batch_id == batch_id, Attendance.date == target_date)
            .all()
        )
        att_by_student: Dict[int, Attendance] = {a.student_id: a for a in att_rows}

        results = []
        for s in students:
            att = att_by_student.get(s.id)
            results.append({
                "student_id": s.id,
                "roll_number": s.roll_number,
                "name": s.name,
                "attendance_rate": s.attendance_rate,
                "status": att.status if att else "Present",
                "remarks": att.remarks if att else "",
            })
        return results
    except Exception as exc:
        logger.error("Failed to get batch attendance for batch %s: %s", batch_id, exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve batch attendance.")


@router.get("/student/{student_id}")
def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    try:
        records = (
            db.query(Attendance)
            .join(Batch, Attendance.batch_id == Batch.id)
            .filter(Attendance.student_id == student_id)
            .order_by(Attendance.date.desc())
            .all()
        )
        return [
            {
                "id": a.id,
                "student_id": a.student_id,
                "batch_id": a.batch_id,
                "batch_name": a.batch.name if a.batch else None,
                "date": (a.date.strftime("%Y-%m-%d") if hasattr(a.date, "strftime") else str(a.date)) if a.date else None,
                "status": a.status,
                "remarks": a.remarks,
            }
            for a in records
        ]
    except Exception as exc:
        logger.error("Failed to get student attendance for %s: %s", student_id, exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve student attendance.")
