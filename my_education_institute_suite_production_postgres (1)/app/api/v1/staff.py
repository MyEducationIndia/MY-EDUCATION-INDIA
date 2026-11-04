from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.core.security import hash_password
from app.models.entities import Staff, User, Batch, StaffLeave, AuditLog
from app.models.schemas import StaffCreate, StaffUpdate, LeaveApplyRequest
from typing import Optional
from datetime import date, datetime

router = APIRouter(prefix="/staff", tags=["Faculty & Staff Management"])

@router.get("")
def list_staff(department: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Staff)
        if department and department != "all":
            query = query.filter(Staff.department == department)
        staff_list = query.order_by(Staff.id.asc()).all()

        results = []
        for s in staff_list:
            batches = db.query(Batch).filter(Batch.trainer_id == s.id).all()
            results.append({
                "id": s.id,
                "employee_code": s.employee_code,
                "user_id": s.user_id,
                "name": s.name,
                "designation": s.designation,
                "department": s.department,
                "qualification": s.qualification,
                "salary_amount": s.salary_amount,
                "phone": s.phone,
                "email": s.email,
                "joining_date": s.joining_date.strftime("%Y-%m-%d") if s.joining_date else None,
                "status": s.status,
                "assigned_batches": [
                    {"code": b.code, "name": b.name, "timing": b.timing}
                    for b in batches
                ]
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve faculty members.")

@router.post("", status_code=201)
def create_staff(st: StaffCreate, db: Session = Depends(get_db)):
    try:
        count = db.query(Staff).count()
        next_id = count + 101
        emp_code = f"STF-{next_id}"
        first_name = st.name.lower().split()[0]
        u_name = f"staff.{first_name}"

        # Check username uniqueness
        existing_u = db.query(User).filter(User.username == u_name).first()
        if existing_u:
            u_name = f"staff.{first_name}{next_id}"

        # 1. Create User account
        pwd_hash = hash_password("Staff@1234")
        new_user = User(
            username=u_name,
            email=st.email,
            password_hash=pwd_hash,
            full_name=st.name,
            role_id=2,
            linked_id=emp_code,
            is_active=1
        )
        db.add(new_user)
        db.flush()

        # 2. Create Staff record
        new_staff = Staff(
            employee_code=emp_code,
            user_id=new_user.id,
            name=st.name,
            designation=st.designation,
            department=st.department,
            qualification=st.qualification,
            salary_amount=st.salary_amount,
            phone=st.phone,
            email=st.email,
            joining_date=date.today(),
            status="Active"
        )
        db.add(new_staff)
        db.flush()

        db.add(AuditLog(actor="admin", action=f"Added faculty member [{emp_code}] {st.name}", module="Staff"))
        return {"status": "success", "staff_id": new_staff.id, "employee_code": emp_code, "username": u_name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create staff member: {str(e)}")

@router.put("/{staff_id}")
def update_staff(staff_id: int, st: StaffUpdate, db: Session = Depends(get_db)):
    try:
        staff = db.query(Staff).filter(or_(Staff.id == staff_id, Staff.employee_code == str(staff_id))).first()
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found.")

        if st.name is not None: staff.name = st.name
        if st.designation is not None: staff.designation = st.designation
        if st.department is not None: staff.department = st.department
        if st.qualification is not None: staff.qualification = st.qualification
        if st.salary_amount is not None: staff.salary_amount = st.salary_amount
        if st.phone is not None: staff.phone = st.phone
        if st.email is not None: staff.email = st.email

        # Sync user account
        if st.name or st.email:
            usr = db.query(User).filter(User.linked_id == staff.employee_code).first()
            if usr:
                if st.name: usr.full_name = st.name
                if st.email: usr.email = st.email

        db.add(AuditLog(actor="admin", action=f"Updated faculty profile [{staff.employee_code}]", module="Staff"))
        return {"status": "success", "message": "Staff details updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update staff member: {str(e)}")

@router.patch("/{staff_id}")
def patch_staff(staff_id: int, st: StaffUpdate, db: Session = Depends(get_db)):
    return update_staff(staff_id, st, db)

@router.delete("/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    try:
        staff = db.query(Staff).filter(or_(Staff.id == staff_id, Staff.employee_code == str(staff_id))).first()
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found.")

        emp = staff.employee_code
        name = staff.name

        usr = db.query(User).filter(User.linked_id == emp).first()
        if usr:
            db.delete(usr)

        db.delete(staff)
        db.add(AuditLog(actor="admin", action=f"Deleted faculty member [{emp}] {name}", module="Staff"))
        return {"status": "success", "message": f"Staff member {emp} deleted."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete staff member: {str(e)}")

# Leave Management
@router.post("/leave/apply")
def apply_leave(req: LeaveApplyRequest, db: Session = Depends(get_db)):
    try:
        s_date = datetime.strptime(req.start_date, "%Y-%m-%d").date()
        e_date = datetime.strptime(req.end_date, "%Y-%m-%d").date()
        new_leave = StaffLeave(
            staff_id=req.staff_id,
            leave_type=req.leave_type,
            start_date=s_date,
            end_date=e_date,
            reason=req.reason,
            status="Pending"
        )
        db.add(new_leave)
        db.flush()
        db.add(AuditLog(actor="staff", action=f"Applied for {req.leave_type} leave from {req.start_date} to {req.end_date}", module="Leaves"))
        return {"status": "success", "leave_id": new_leave.id, "message": "Leave application submitted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to apply for leave: {str(e)}")

@router.get("/leave")
def list_leaves(staff_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(StaffLeave).join(Staff, StaffLeave.staff_id == Staff.id)
        if staff_id:
            query = query.filter(StaffLeave.staff_id == staff_id)
        leaves = query.order_by(StaffLeave.id.desc()).all()
        return [
            {
                "id": l.id,
                "staff_id": l.staff_id,
                "staff_name": l.staff.name if l.staff else None,
                "employee_code": l.staff.employee_code if l.staff else None,
                "leave_type": l.leave_type,
                "start_date": l.start_date.strftime("%Y-%m-%d") if l.start_date else None,
                "end_date": l.end_date.strftime("%Y-%m-%d") if l.end_date else None,
                "reason": l.reason,
                "status": l.status,
                "approved_by": l.approved_by,
                "created_at": l.created_at.strftime("%Y-%m-%d %H:%M:%S") if l.created_at else None
            }
            for l in leaves
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve leaves.")
