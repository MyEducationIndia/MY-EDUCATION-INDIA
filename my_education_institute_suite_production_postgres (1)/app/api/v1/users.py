from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.core.security import hash_password
from app.models.entities import User, Role, Student, Staff, AuditLog, RolePermission
from app.models.schemas import UserCreate, UserUpdate, RolePermissionUpdate
from typing import Optional, Dict

router = APIRouter(prefix="/users", tags=["Master User Accounts & Credentials"])

@router.get("")
def list_users(
    role: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(User).join(Role, User.role_id == Role.id)
        if role and role != "all":
            query = query.filter(Role.name == role)
        if q:
            term = f"%{q}%"
            query = query.filter(
                or_(
                    User.username.ilike(term),
                    User.full_name.ilike(term),
                    User.email.ilike(term),
                    User.linked_id.ilike(term),
                )
            )
        users = query.order_by(User.id.asc()).all()

        results = []
        for u in users:
            item = {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "full_name": u.full_name,
                "role_id": u.role_id,
                "role": u.role.name if u.role else "student",
                "linked_id": u.linked_id,
                "is_active": u.is_active,
                "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else None,
                "last_login": u.last_login.strftime("%Y-%m-%d %H:%M:%S") if u.last_login else None,
            }
            if item["role"] == "student" and u.linked_id:
                st = db.query(Student).filter(Student.roll_number == u.linked_id).first()
                if st and st.dob:
                    item["dob"] = st.dob
            results.append(item)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve users.")

@router.post("", status_code=201)
def create_user(u: UserCreate, db: Session = Depends(get_db)):
    pwd = u.password or "User@1234"
    pwd_hash = hash_password(pwd)
    try:
        new_user = User(
            username=u.username,
            email=u.email,
            password_hash=pwd_hash,
            full_name=u.full_name,
            role_id=u.role_id,
            linked_id=u.linked_id,
            is_active=1
        )
        db.add(new_user)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Created user account [{u.username}]", module="Users"))
        return {"status": "success", "user_id": new_user.id, "username": u.username}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create user: {str(e)}")

@router.put("/{user_id}")
def update_user(user_id: int, u: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User account not found.")

        if u.full_name is not None:
            user.full_name = u.full_name
        if u.username is not None:
            user.username = u.username
        if u.email is not None:
            user.email = u.email
        if u.password is not None and len(u.password.strip()) > 0:
            user.password_hash = hash_password(u.password.strip())
        if u.is_active is not None:
            user.is_active = u.is_active

        # Sync full_name and email to student or staff record if linked
        if user.linked_id:
            if u.full_name or u.email:
                stu = db.query(Student).filter(Student.roll_number == user.linked_id).first()
                if stu:
                    if u.full_name: stu.name = u.full_name
                    if u.email: stu.email = u.email
                stf = db.query(Staff).filter(Staff.employee_code == user.linked_id).first()
                if stf:
                    if u.full_name: stf.name = u.full_name
                    if u.email: stf.email = u.email

        db.add(AuditLog(actor="admin", action=f"Updated credentials for user [{user.username}]", module="Users"))
        return {"status": "success", "message": "User credentials updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update user: {str(e)}")

@router.patch("/{user_id}")
def patch_user(user_id: int, u: UserUpdate, db: Session = Depends(get_db)):
    return update_user(user_id, u, db)

@router.post("/{user_id}/reset-dob")
def reset_user_to_dob(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.role or user.role.name != "student" or not user.linked_id:
            raise HTTPException(status_code=400, detail="User is not a student or has no linked Roll Number.")

        stu = db.query(Student).filter(Student.roll_number == user.linked_id).first()
        if not stu or not stu.dob:
            raise HTTPException(status_code=404, detail="Student date of birth not found in database.")

        dob = stu.dob
        user.password_hash = hash_password(dob)
        db.add(AuditLog(actor="admin", action=f"Reset password of student [{user.username}] to DOB ({dob})", module="Users"))
        return {"status": "success", "message": f"Password reset to official DOB: {dob}", "dob": dob}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to reset password to DOB.")

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        if user.role_id == 1 and user.username == "admin":
            raise HTTPException(status_code=400, detail="Cannot delete root Super Administrator account.")

        db.delete(user)
        db.add(AuditLog(actor="admin", action=f"Deleted user account [{user.username}]", module="Users"))
        return {"status": "success", "message": "User account removed."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete user: {str(e)}")

# Roles Management
@router.get("/roles")
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).order_by(Role.id.asc()).all()
    return [{"id": r.id, "name": r.name, "description": r.description} for r in roles]

# Permissions Management
@router.get("/permissions")
def get_role_permissions(db: Session = Depends(get_db)):
    perms = db.query(RolePermission).order_by(RolePermission.role_name.asc(), RolePermission.id.asc()).all()
    result = {}
    for p in perms:
        if p.role_name not in result:
            result[p.role_name] = {}
        result[p.role_name][p.module_key] = {
            "label": p.label,
            "enabled": bool(p.enabled)
        }
    return result

@router.put("/permissions")
def update_role_permissions(req: RolePermissionUpdate, db: Session = Depends(get_db)):
    try:
        for mod_key, is_enabled in req.permissions.items():
            perm = db.query(RolePermission).filter(
                RolePermission.role_name == req.role_name,
                RolePermission.module_key == mod_key
            ).first()
            if perm:
                perm.enabled = 1 if is_enabled else 0
            else:
                db.add(RolePermission(
                    role_name=req.role_name,
                    module_key=mod_key,
                    label=mod_key.capitalize(),
                    enabled=1 if is_enabled else 0
                ))
        db.add(AuditLog(actor="admin", action=f"Updated role permissions for [{req.role_name}]", module="Permissions"))
        return {"status": "success", "message": f"Permissions updated for role {req.role_name}."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update permissions: {str(e)}")
