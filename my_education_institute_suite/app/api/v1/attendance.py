from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.entities import Attendance, Student, Batch, AuditLog
from app.models.schemas import AttendanceRecord
from typing import List, Optional
from datetime import datetime, date

router = APIRouter(prefix="/attendance", tags=["Attendance Register"])

@router.post("")
def record_attendance(records: List[AttendanceRecord], db: Session = Depends(get_db)):
    try:
        updated_student_ids = set()
        for r in records:
            att_date = datetime.strptime(r.date, "%Y-%m-%d").date()
            existing = db.query(Attendance).filter(
                Attendance.student_id == r.student_id,
                Attendance.batch_id == r.batch_id,
                Attendance.date == att_date
            ).first()

            if existing:
                existing.status = r.status
                existing.remarks = r.remarks or ""
            else:
                db.add(Attendance(
                    student_id=r.student_id,
                    batch_id=r.batch_id,
                    date=att_date,
                    status=r.status,
                    remarks=r.remarks or ""
                ))
            updated_student_ids.add(r.student_id)

        db.flush()

        # Recalculate attendance rates
        for stu_id in updated_student_ids:
            total_count = db.query(Attendance).filter(Attendance.student_id == stu_id).count()
            present_count = db.query(Attendance).filter(Attendance.student_id == stu_id, Attendance.status == "Present").count()
            if total_count > 0:
                pct = round((present_count / total_count) * 100.0, 1)
                stu = db.query(Student).filter(Student.id == stu_id).first()
                if stu:
                    stu.attendance_rate = pct

        db.add(AuditLog(actor="staff", action=f"Submitted daily attendance register for {len(records)} students", module="Attendance"))
        return {"status": "success", "count": len(records), "message": "Attendance records saved."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to record attendance: {str(e)}")

@router.get("/batch/{batch_id}")
def get_batch_attendance(batch_id: int, date_str: Optional[str] = Query(None, alias="date"), db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
        students = db.query(Student).filter(Student.batch_id == batch_id).order_by(Student.roll_number.asc()).all()

        results = []
        for s in students:
            att = db.query(Attendance).filter(Attendance.student_id == s.id, Attendance.date == target_date).first()
            results.append({
                "student_id": s.id,
                "roll_number": s.roll_number,
                "name": s.name,
                "attendance_rate": s.attendance_rate,
                "status": att.status if att else "Present",
                "remarks": att.remarks if att else ""
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve batch attendance.")

@router.get("/student/{student_id}")
def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    try:
        records = db.query(Attendance).join(Batch, Attendance.batch_id == Batch.id).filter(Attendance.student_id == student_id).order_by(Attendance.date.desc()).all()
        return [
            {
                "id": a.id,
                "student_id": a.student_id,
                "batch_id": a.batch_id,
                "batch_name": a.batch.name if a.batch else None,
                "date": a.date.strftime("%Y-%m-%d") if a.date else None,
                "status": a.status,
                "remarks": a.remarks
            }
            for a in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve student attendance.")
