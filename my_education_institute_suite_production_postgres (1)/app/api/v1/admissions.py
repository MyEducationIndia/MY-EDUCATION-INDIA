from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.core.security import hash_password
from app.models.entities import Admission, Course, Student, User, AuditLog
from app.models.schemas import AdmissionApply
import random

router = APIRouter(prefix="/admissions", tags=["Online Admission Queue"])

@router.get("")
def list_admissions(db: Session = Depends(get_db)):
    try:
        admissions = db.query(Admission).join(Course, Admission.course_id == Course.id).order_by(Admission.id.desc()).all()
        return [
            {
                "id": a.id,
                "application_number": a.application_number,
                "applicant_name": a.applicant_name,
                "course_id": a.course_id,
                "course_title": a.course.title if a.course else None,
                "course_code": a.course.code if a.course else None,
                "course_fee": a.course.fee if a.course else 0.0,
                "preferred_timing": a.preferred_timing,
                "prior_qualification": a.prior_qualification,
                "mobile": a.mobile,
                "email": a.email,
                "guardian_name": a.guardian_name,
                "status": a.status,
                "remarks": a.remarks,
                "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S") if a.created_at else None
            }
            for a in admissions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve admissions.")

@router.post("/apply", status_code=201)
def submit_admission(a: AdmissionApply, db: Session = Depends(get_db)):
    try:
        app_no = f"APP-2026-{random.randint(1000, 9999)}"
        new_admission = Admission(
            application_number=app_no,
            applicant_name=a.applicant_name,
            course_id=a.course_id,
            preferred_timing=a.preferred_timing,
            prior_qualification=a.prior_qualification,
            mobile=a.mobile,
            email=a.email,
            guardian_name=a.guardian_name,
            status="Pending Review"
        )
        db.add(new_admission)
        db.flush()
        db.add(AuditLog(actor="public", action=f"Received admission application {app_no} from {a.applicant_name}", module="Admissions"))
        return {
            "status": "success",
            "application_number": app_no,
            "message": "Application received successfully. Present slip at admission counter."
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to submit application: {str(e)}")

@router.post("/{app_id}/approve")
def approve_admission(app_id: int, db: Session = Depends(get_db)):
    try:
        adm = db.query(Admission).filter(or_(Admission.id == app_id, Admission.application_number == str(app_id))).first()
        if not adm:
            raise HTTPException(status_code=404, detail="Application not found.")

        adm.status = "Approved"

        # Auto-enroll student & generate credentials
        count = db.query(Student).count()
        next_num = count + 1001
        roll = f"STU-2026-{next_num}"
        dob = "2004-06-15"
        pwd_hash = hash_password(dob)

        user = User(
            username=roll,
            email=adm.email,
            password_hash=pwd_hash,
            full_name=adm.applicant_name,
            role_id=3,
            linked_id=roll,
            is_active=1
        )
        db.add(user)
        db.flush()

        course_fee = adm.course.fee if adm.course else 9500.0
        student = Student(
            roll_number=roll,
            user_id=user.id,
            name=adm.applicant_name,
            dob=dob,
            course_id=adm.course_id,
            batch_id=1,
            mobile=adm.mobile,
            email=adm.email,
            guardian_name=adm.guardian_name or "Guardian",
            gender="Male",
            blood_group="B+",
            total_fee=course_fee,
            paid_fee=0.0,
            due_fee=course_fee,
            attendance_rate=100.0,
            status="Enrolled"
        )
        db.add(student)
        db.flush()

        db.add(AuditLog(actor="admin", action=f"Approved application {adm.application_number} -> Enrolled {roll} ({adm.applicant_name})", module="Admissions"))
        return {
            "status": "success",
            "message": f"Application approved! Enrolled as Roll Number {roll}",
            "roll_number": roll,
            "default_password": dob
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to approve admission: {str(e)}")

@router.post("/{app_id}/reject")
def reject_admission(app_id: int, db: Session = Depends(get_db)):
    try:
        adm = db.query(Admission).filter(or_(Admission.id == app_id, Admission.application_number == str(app_id))).first()
        if not adm:
            raise HTTPException(status_code=404, detail="Application not found.")
        adm.status = "Rejected"
        return {"status": "success", "message": "Application rejected."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to reject admission: {str(e)}")

@router.delete("/{app_id}")
def delete_admission(app_id: int, db: Session = Depends(get_db)):
    try:
        adm = db.query(Admission).filter(or_(Admission.id == app_id, Admission.application_number == str(app_id))).first()
        if not adm:
            raise HTTPException(status_code=404, detail="Application not found.")
        db.delete(adm)
        return {"status": "success", "message": "Application deleted."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete admission: {str(e)}")
