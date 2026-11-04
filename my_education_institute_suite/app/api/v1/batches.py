from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.entities import Batch, Course, Staff, Student, AuditLog
from app.models.schemas import BatchCreate, BatchUpdate

router = APIRouter(prefix="/batches", tags=["Batch Scheduling & Classroom Timings"])

@router.get("")
def list_batches(db: Session = Depends(get_db)):
    try:
        batches = db.query(Batch).join(Course, Batch.course_id == Course.id).outerjoin(Staff, Batch.trainer_id == Staff.id).order_by(Batch.id.asc()).all()
        results = []
        for b in batches:
            enrolled = db.query(Student).filter(Student.batch_id == b.id).count()
            results.append({
                "id": b.id,
                "code": b.code,
                "name": b.name,
                "course_id": b.course_id,
                "trainer_id": b.trainer_id,
                "timing": b.timing,
                "room": b.room,
                "capacity": b.capacity,
                "status": b.status,
                "course_title": b.course.title if b.course else None,
                "course_code": b.course.code if b.course else None,
                "trainer_name": b.trainer.name if b.trainer else None,
                "enrolled_count": enrolled,
                "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S") if b.created_at else None
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve batches.")

@router.post("", status_code=201)
def create_batch(b: BatchCreate, db: Session = Depends(get_db)):
    try:
        new_batch = Batch(
            code=b.code,
            name=b.name,
            course_id=b.course_id,
            trainer_id=b.trainer_id,
            timing=b.timing,
            room=b.room,
            capacity=b.capacity or 30,
            status="Active"
        )
        db.add(new_batch)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Created batch schedule [{b.code}] {b.name}", module="Batches"))
        return {"status": "success", "batch_id": new_batch.id, "code": b.code}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Batch creation failed: {str(e)}")

@router.put("/{batch_id}")
def update_batch(batch_id: int, b: BatchUpdate, db: Session = Depends(get_db)):
    try:
        batch = db.query(Batch).filter(or_(Batch.id == batch_id, Batch.code == str(batch_id))).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found.")

        if b.name is not None: batch.name = b.name
        if b.timing is not None: batch.timing = b.timing
        if b.room is not None: batch.room = b.room
        if b.trainer_id is not None: batch.trainer_id = b.trainer_id
        if b.capacity is not None: batch.capacity = b.capacity

        db.add(AuditLog(actor="admin", action=f"Updated batch timing [{batch.code}]", module="Batches"))
        return {"status": "success", "message": "Batch schedule updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update batch: {str(e)}")

@router.patch("/{batch_id}")
def patch_batch(batch_id: int, b: BatchUpdate, db: Session = Depends(get_db)):
    return update_batch(batch_id, b, db)

@router.delete("/{batch_id}")
def delete_batch(batch_id: int, db: Session = Depends(get_db)):
    try:
        batch = db.query(Batch).filter(or_(Batch.id == batch_id, Batch.code == str(batch_id))).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found.")

        code = batch.code
        db.delete(batch)
        db.add(AuditLog(actor="admin", action=f"Deleted batch schedule [{code}]", module="Batches"))
        return {"status": "success", "message": f"Batch {code} deleted."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete batch: {str(e)}")
