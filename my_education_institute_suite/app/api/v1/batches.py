from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import AuditLog, Batch, Course, Staff, Student
from app.models.schemas import BatchCreate, BatchUpdate

logger = get_logger(__name__)
router = APIRouter(prefix="/batches", tags=["Batch Scheduling & Classroom Timings"])


@router.get("")
def list_batches(db: Session = Depends(get_db)):
    try:
        batches = (
            db.query(Batch)
            .join(Course, Batch.course_id == Course.id)
            .outerjoin(Staff, Batch.trainer_id == Staff.id)
            .order_by(Batch.id.asc())
            .all()
        )
        # Single-pass student count aggregation to avoid N+1 queries
        all_students = db.query(Student).all()
        enrolled_counts: Dict[int, int] = {}
        for s in all_students:
            if s.batch_id is not None:
                enrolled_counts[s.batch_id] = enrolled_counts.get(s.batch_id, 0) + 1

        results = []
        for b in batches:
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
                "enrolled_count": enrolled_counts.get(b.id, 0),
                "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S") if b.created_at else None,
            })
        return results
    except Exception as exc:
        logger.error("Failed to list batches: %s", exc)
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
            status="Active",
        )
        db.add(new_batch)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Created batch schedule [{b.code}] {b.name}", module="Batches"))
        db.commit()
        return {"status": "success", "batch_id": new_batch.id, "code": b.code}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create batch: %s", exc)
        raise HTTPException(status_code=400, detail=f"Batch creation failed: {str(exc)}")


@router.put("/{batch_id}")
def update_batch(batch_id: int, b: BatchUpdate, db: Session = Depends(get_db)):
    try:
        batch = db.query(Batch).filter(or_(Batch.id == batch_id, Batch.code == str(batch_id))).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found.")

        for field, val in b.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(batch, field, val)

        db.add(AuditLog(actor="admin", action=f"Updated batch timing [{batch.code}]", module="Batches"))
        db.commit()
        return {"status": "success", "message": "Batch schedule updated successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update batch %s: %s", batch_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update batch: {str(exc)}")


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
        db.commit()
        return {"status": "success", "message": f"Batch {code} deleted."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete batch %s: %s", batch_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete batch: {str(exc)}")
