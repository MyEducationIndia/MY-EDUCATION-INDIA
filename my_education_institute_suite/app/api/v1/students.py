import csv
import io
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.core.security import hash_password
from app.models.entities import AuditLog, Batch, Course, FeePayment, Student, User
from app.models.schemas import StudentCreate, StudentUpdate

logger = get_logger(__name__)
router = APIRouter(prefix="/students", tags=["Student Management"])


@router.get("")
def list_students(
    course_id: Optional[int] = None,
    batch_id: Optional[int] = None,
    fee_status: Optional[str] = None,
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    try:
        query = (
            db.query(Student)
            .join(Course, Student.course_id == Course.id)
            .outerjoin(Batch, Student.batch_id == Batch.id)
        )
        if course_id:
            query = query.filter(Student.course_id == course_id)
        if batch_id:
            query = query.filter(Student.batch_id == batch_id)
        if fee_status == "paid":
            query = query.filter(Student.due_fee <= 0)
        elif fee_status == "due":
            query = query.filter(Student.due_fee > 0)
        if q:
            term = f"%{q}%"
            query = query.filter(
                or_(
                    Student.name.ilike(term),
                    Student.roll_number.ilike(term),
                    Student.mobile.ilike(term),
                    Student.guardian_name.ilike(term),
                )
            )
        students = query.order_by(Student.id.desc()).offset(skip).limit(limit).all()

        results = []
        for s in students:
            results.append({
                "id": s.id,
                "roll_number": s.roll_number,
                "name": s.name,
                "dob": s.dob,
                "course_id": s.course_id,
                "batch_id": s.batch_id,
                "mobile": s.mobile,
                "email": s.email,
                "guardian_name": s.guardian_name,
                "guardian_mobile": s.guardian_mobile,
                "gender": s.gender,
                "blood_group": s.blood_group,
                "address": s.address,
                "total_fee": s.total_fee,
                "paid_fee": s.paid_fee,
                "due_fee": s.due_fee,
                "attendance_rate": s.attendance_rate,
                "status": s.status,
                "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S") if s.created_at else None,
                "course_title": s.course.title if s.course else None,
                "course_code": s.course.code if s.course else None,
                "batch_name": s.batch.name if s.batch else None,
                "batch_code": s.batch.code if s.batch else None,
                "batch_timing": s.batch.timing if s.batch else None,
            })
        return results
    except Exception as exc:
        logger.error("Failed to list students: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve students.")


@router.post("", status_code=201)
def create_student(s: StudentCreate, db: Session = Depends(get_db)):
    try:
        count = db.query(Student).count()
        next_num = count + 1001
        roll = f"STU-2026-{next_num}"
        due = max(0.0, s.total_fee - s.paid_fee)

        pwd_hash = hash_password(s.dob)
        user = User(
            username=roll,
            email=s.email,
            password_hash=pwd_hash,
            full_name=s.name,
            role_id=3,
            linked_id=roll,
            is_active=1,
        )
        db.add(user)
        db.flush()

        new_student = Student(
            roll_number=roll,
            user_id=user.id,
            name=s.name,
            dob=s.dob,
            course_id=s.course_id,
            batch_id=s.batch_id,
            mobile=s.mobile,
            email=s.email,
            guardian_name=s.guardian_name,
            guardian_mobile=s.guardian_mobile or "",
            gender=s.gender,
            blood_group=s.blood_group or "B+",
            address=s.address or "",
            total_fee=s.total_fee,
            paid_fee=s.paid_fee,
            due_fee=due,
            attendance_rate=100.0,
            status="Enrolled",
        )
        db.add(new_student)
        db.flush()

        if s.paid_fee > 0:
            inv = f"INV-2026-00{next_num - 900}"
            today_date = date.today()
            payment = FeePayment(
                invoice_number=inv,
                student_id=new_student.id,
                amount=s.paid_fee,
                payment_mode="Counter Deposit",
                payment_date=today_date,
                remarks="Admission Enrollment Deposit",
            )
            db.add(payment)

        db.add(
            AuditLog(
                actor="admin",
                action=f"Enrolled student {roll} ({s.name}) with default DOB credentials",
                module="Students",
            )
        )
        db.commit()
        return {
            "status": "success",
            "student_id": new_student.id,
            "roll_number": roll,
            "name": s.name,
            "dob": s.dob,
            "message": f"Student enrolled successfully. Default password is DOB ({s.dob})",
        }
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create student: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create student: {str(exc)}")


@router.get("/export/csv")
def export_students_csv(db: Session = Depends(get_db)):
    try:
        students = (
            db.query(Student)
            .join(Course, Student.course_id == Course.id)
            .outerjoin(Batch, Student.batch_id == Batch.id)
            .order_by(Student.id.asc())
            .all()
        )
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Roll Number",
            "Full Name",
            "DOB",
            "Course",
            "Batch",
            "Mobile",
            "Email",
            "Guardian",
            "Total Fee",
            "Paid Fee",
            "Due Fee",
            "Attendance %",
            "Status",
        ])
        for s in students:
            writer.writerow([
                s.roll_number,
                s.name,
                s.dob,
                s.course.title if s.course else "N/A",
                s.batch.name if s.batch else "N/A",
                s.mobile,
                s.email,
                s.guardian_name,
                s.total_fee,
                s.paid_fee,
                s.due_fee,
                f"{s.attendance_rate}%",
                s.status,
            ])

        response = Response(content=output.getvalue(), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=my_education_erp_students.csv"
        return response
    except Exception as exc:
        logger.error("Failed to export students CSV: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to export students CSV.")


@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    try:
        s = db.query(Student).filter(or_(Student.id == student_id, Student.roll_number == str(student_id))).first()
        if not s:
            raise HTTPException(status_code=404, detail="Student not found.")

        payments = db.query(FeePayment).filter(FeePayment.student_id == s.id).order_by(FeePayment.id.desc()).all()
        fee_history = [
            {
                "id": p.id,
                "invoice_number": p.invoice_number,
                "amount": p.amount,
                "payment_mode": p.payment_mode,
                "payment_date": p.payment_date.strftime("%Y-%m-%d") if p.payment_date else None,
                "remarks": p.remarks,
            }
            for p in payments
        ]

        return {
            "id": s.id,
            "roll_number": s.roll_number,
            "name": s.name,
            "dob": s.dob,
            "course_id": s.course_id,
            "batch_id": s.batch_id,
            "mobile": s.mobile,
            "email": s.email,
            "guardian_name": s.guardian_name,
            "guardian_mobile": s.guardian_mobile,
            "gender": s.gender,
            "blood_group": s.blood_group,
            "address": s.address,
            "total_fee": s.total_fee,
            "paid_fee": s.paid_fee,
            "due_fee": s.due_fee,
            "attendance_rate": s.attendance_rate,
            "status": s.status,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S") if s.created_at else None,
            "course_title": s.course.title if s.course else None,
            "course_duration": s.course.duration if s.course else None,
            "batch_name": s.batch.name if s.batch else None,
            "batch_timing": s.batch.timing if s.batch else None,
            "batch_room": s.batch.room if s.batch else None,
            "fee_history": fee_history,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Failed to fetch student %s: %s", student_id, exc)
        raise HTTPException(status_code=500, detail="Failed to fetch student details.")


@router.put("/{student_id}")
def update_student(student_id: int, s: StudentUpdate, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(or_(Student.id == student_id, Student.roll_number == str(student_id))).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        for field, val in s.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(student, field, val)

        student.due_fee = max(0.0, float(student.total_fee or 0.0) - float(student.paid_fee or 0.0))

        if s.name or s.email:
            usr = db.query(User).filter(User.linked_id == student.roll_number).first()
            if usr:
                if s.name:
                    usr.full_name = s.name
                if s.email:
                    usr.email = s.email

        db.add(
            AuditLog(
                actor="admin",
                action=f"Updated student record [{student.roll_number}] {student.name}",
                module="Students",
            )
        )
        db.commit()
        return {"status": "success", "message": "Student details updated successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update student %s: %s", student_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update student: {str(exc)}")


@router.patch("/{student_id}")
def patch_student(student_id: int, s: StudentUpdate, db: Session = Depends(get_db)):
    return update_student(student_id, s, db)


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(or_(Student.id == student_id, Student.roll_number == str(student_id))).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        roll = student.roll_number
        name = student.name

        usr = db.query(User).filter(User.linked_id == roll).first()
        if usr:
            db.delete(usr)

        db.delete(student)
        db.add(AuditLog(actor="admin", action=f"Deleted student record [{roll}] {name}", module="Students"))
        db.commit()
        return {"status": "success", "message": f"Student {roll} removed from institutional database."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete student %s: %s", student_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete student: {str(exc)}")
