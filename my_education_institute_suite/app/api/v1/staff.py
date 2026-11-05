from datetime import date, datetime
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.core.security import hash_password
from app.models.entities import AuditLog, Batch, Staff, StaffLeave, User
from app.models.schemas import LeaveApplyRequest, LeaveStatusUpdate, StaffCreate, StaffUpdate

logger = get_logger(__name__)
router = APIRouter(prefix="/staff", tags=["Faculty & Staff Management"])


@router.get("")
def list_staff(
    department: Optional[str] = None,
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Staff)
        if department and department != "all":
            query = query.filter(Staff.department == department)
        if q:
            term = f"%{q}%"
            query = query.filter(
                or_(
                    Staff.name.ilike(term),
                    Staff.employee_code.ilike(term),
                    Staff.designation.ilike(term),
                    Staff.email.ilike(term),
                )
            )
        staff_list = query.order_by(Staff.id.asc()).offset(skip).limit(limit).all()

        # Prefetch all batches in one query to eliminate N+1 queries
        all_batches = db.query(Batch).all()
        batches_by_trainer: Dict[int, List[Dict[str, str]]] = {}
        for b in all_batches:
            if b.trainer_id is not None:
                batches_by_trainer.setdefault(b.trainer_id, []).append(
                    {"code": b.code, "name": b.name, "timing": b.timing}
                )

        results = []
        for s in staff_list:
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
                "assigned_batches": batches_by_trainer.get(s.id, []),
            })
        return results
    except Exception as exc:
        logger.error("Failed to list staff: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve faculty members.")


@router.post("", status_code=201)
def create_staff(st: StaffCreate, db: Session = Depends(get_db)):
    try:
        count = db.query(Staff).count()
        next_id = count + 101
        emp_code = f"STF-{next_id}"
        first_name = st.name.lower().split()[0] if st.name.strip() else "faculty"
        u_name = f"staff.{first_name}"

        existing_u = db.query(User).filter(User.username == u_name).first()
        if existing_u:
            u_name = f"staff.{first_name}{next_id}"

        pwd_hash = hash_password("Staff@1234")
        new_user = User(
            username=u_name,
            email=st.email,
            password_hash=pwd_hash,
            full_name=st.name,
            role_id=2,
            linked_id=emp_code,
            is_active=1,
        )
        db.add(new_user)
        db.flush()

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
            status="Active",
        )
        db.add(new_staff)
        db.flush()

        db.add(AuditLog(actor="admin", action=f"Added faculty member [{emp_code}] {st.name}", module="Staff"))
        db.commit()
        return {"status": "success", "staff_id": new_staff.id, "employee_code": emp_code, "username": u_name}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create staff: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create staff member: {str(exc)}")


@router.put("/{staff_id}")
def update_staff(staff_id: int, st: StaffUpdate, db: Session = Depends(get_db)):
    try:
        staff = db.query(Staff).filter(or_(Staff.id == staff_id, Staff.employee_code == str(staff_id))).first()
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found.")

        for field, val in st.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(staff, field, val)

        if st.name or st.email:
            usr = db.query(User).filter(User.linked_id == staff.employee_code).first()
            if usr:
                if st.name:
                    usr.full_name = st.name
                if st.email:
                    usr.email = st.email

        db.add(AuditLog(actor="admin", action=f"Updated faculty profile [{staff.employee_code}]", module="Staff"))
        db.commit()
        return {"status": "success", "message": "Staff details updated successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update staff %s: %s", staff_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update staff member: {str(exc)}")


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
        db.commit()
        return {"status": "success", "message": f"Staff member {emp} deleted."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete staff %s: %s", staff_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete staff member: {str(exc)}")


@router.post("/leave/apply", status_code=201)
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
            status="Pending",
        )
        db.add(new_leave)
        db.flush()
        db.add(
            AuditLog(
                actor="staff",
                action=f"Applied for {req.leave_type} leave from {req.start_date} to {req.end_date}",
                module="Leaves",
            )
        )
        db.commit()
        return {"status": "success", "leave_id": new_leave.id, "message": "Leave application submitted."}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to apply leave: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to apply for leave: {str(exc)}")


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
                "created_at": l.created_at.strftime("%Y-%m-%d %H:%M:%S") if l.created_at else None,
            }
            for l in leaves
        ]
    except Exception as exc:
        logger.error("Failed to list leaves: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve leaves.")


@router.put("/leave/{leave_id}")
def update_leave_status(leave_id: int, req: LeaveStatusUpdate, db: Session = Depends(get_db)):
    try:
        lv = db.query(StaffLeave).filter(StaffLeave.id == leave_id).first()
        if not lv:
            raise HTTPException(status_code=404, detail="Leave application not found.")
        lv.status = req.status
        lv.approved_by = req.approved_by or "Administrator"
        db.add(AuditLog(actor="admin", action=f"Updated leave [{leave_id}] status to {req.status}", module="Leaves"))
        db.commit()
        return {"status": "success", "message": f"Leave status updated to {req.status}."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update leave %s: %s", leave_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update leave: {str(exc)}")


@router.delete("/leave/{leave_id}")
def delete_leave(leave_id: int, db: Session = Depends(get_db)):
    try:
        lv = db.query(StaffLeave).filter(StaffLeave.id == leave_id).first()
        if not lv:
            raise HTTPException(status_code=404, detail="Leave application not found.")
        db.delete(lv)
        db.commit()
        return {"status": "success", "message": "Leave application removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete leave %s: %s", leave_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete leave: {str(exc)}")
