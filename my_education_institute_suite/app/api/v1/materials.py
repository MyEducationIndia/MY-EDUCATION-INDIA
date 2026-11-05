from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import AuditLog, Batch, Course, StudyMaterial
from app.models.schemas import MaterialCreate, MaterialUpdate

logger = get_logger(__name__)
router = APIRouter(prefix="/materials", tags=["Study Material & Lecture Notes"])


@router.get("")
def list_materials(
    course_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    try:
        query = (
            db.query(StudyMaterial)
            .join(Course, StudyMaterial.course_id == Course.id)
            .outerjoin(Batch, StudyMaterial.batch_id == Batch.id)
        )
        if course_id:
            query = query.filter(StudyMaterial.course_id == course_id)
        materials = query.order_by(StudyMaterial.id.desc()).offset(skip).limit(limit).all()

        return [
            {
                "id": sm.id,
                "title": sm.title,
                "course_id": sm.course_id,
                "batch_id": sm.batch_id,
                "file_path": sm.file_path,
                "file_type": sm.file_type,
                "file_size": sm.file_size,
                "author": sm.author,
                "course_title": sm.course.title if sm.course else None,
                "course_code": sm.course.code if sm.course else None,
                "batch_name": sm.batch.name if sm.batch else None,
                "uploaded_at": sm.uploaded_at.strftime("%Y-%m-%d %H:%M:%S") if sm.uploaded_at else None,
            }
            for sm in materials
        ]
    except Exception as exc:
        logger.error("Failed to list materials: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve materials.")


@router.post("", status_code=201)
def upload_material(m: MaterialCreate, db: Session = Depends(get_db)):
    try:
        new_mat = StudyMaterial(
            title=m.title,
            course_id=m.course_id,
            batch_id=m.batch_id,
            file_path=m.file_path,
            file_type=m.file_type,
            file_size=m.file_size,
            author=m.author or "Faculty Desk",
        )
        db.add(new_mat)
        db.flush()
        db.add(AuditLog(actor="faculty", action=f"Uploaded document [{m.title}]", module="Materials"))
        db.commit()
        return {"status": "success", "material_id": new_mat.id, "title": m.title}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to upload material: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to upload material: {str(exc)}")


@router.put("/{material_id}")
def update_material(material_id: int, m: MaterialUpdate, db: Session = Depends(get_db)):
    try:
        mat = db.query(StudyMaterial).filter(StudyMaterial.id == material_id).first()
        if not mat:
            raise HTTPException(status_code=404, detail="Material not found.")
        for field, val in m.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(mat, field, val)
        db.add(AuditLog(actor="admin", action=f"Updated study material [{material_id}]", module="Materials"))
        db.commit()
        return {"status": "success", "message": "Study material updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update material %s: %s", material_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update material: {str(exc)}")


@router.patch("/{material_id}")
def patch_material(material_id: int, m: MaterialUpdate, db: Session = Depends(get_db)):
    return update_material(material_id, m, db)


@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    try:
        mat = db.query(StudyMaterial).filter(StudyMaterial.id == material_id).first()
        if not mat:
            raise HTTPException(status_code=404, detail="Material not found.")
        db.delete(mat)
        db.add(AuditLog(actor="admin", action=f"Deleted material [{material_id}]", module="Materials"))
        db.commit()
        return {"status": "success", "message": "Study material removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete material %s: %s", material_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete material: {str(exc)}")
