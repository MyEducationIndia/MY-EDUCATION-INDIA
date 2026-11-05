from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import AuditLog, Notice
from app.models.schemas import NoticeCreate, NoticeUpdate

logger = get_logger(__name__)
router = APIRouter(prefix="/notices", tags=["Institute Broadcast & Notice Board"])


@router.get("")
def list_notices(
    target: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Notice)
        if target and target != "All":
            query = query.filter(or_(Notice.target_audience == target, Notice.target_audience == "All"))
        notices = query.order_by(Notice.is_pinned.desc(), Notice.id.desc()).offset(skip).limit(limit).all()
        return [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "target_audience": n.target_audience,
                "category": n.category,
                "is_pinned": n.is_pinned,
                "created_at": (n.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(n.created_at, "strftime") else str(n.created_at)) if n.created_at else None,
            }
            for n in notices
        ]
    except Exception as exc:
        logger.error("Failed to list notices: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve notices.")


@router.post("", status_code=201)
def create_notice(n: NoticeCreate, db: Session = Depends(get_db)):
    try:
        new_notice = Notice(
            title=n.title,
            content=n.content,
            target_audience=n.target_audience,
            category=n.category,
            is_pinned=n.is_pinned or 0,
        )
        db.add(new_notice)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Published notice [{new_notice.id}] {n.title}", module="Notices"))
        db.commit()
        return {"status": "success", "notice_id": new_notice.id, "title": n.title}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create notice: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create notice: {str(exc)}")


@router.put("/{notice_id}")
def update_notice(notice_id: int, n: NoticeUpdate, db: Session = Depends(get_db)):
    try:
        notice = db.query(Notice).filter(Notice.id == notice_id).first()
        if not notice:
            raise HTTPException(status_code=404, detail="Notice not found.")

        for field, val in n.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(notice, field, val)

        db.add(AuditLog(actor="admin", action=f"Updated circular [{notice_id}]", module="Notices"))
        db.commit()
        return {"status": "success", "message": "Notice updated successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update notice %s: %s", notice_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update notice: {str(exc)}")


@router.patch("/{notice_id}")
def patch_notice(notice_id: int, n: NoticeUpdate, db: Session = Depends(get_db)):
    return update_notice(notice_id, n, db)


@router.delete("/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    try:
        notice = db.query(Notice).filter(Notice.id == notice_id).first()
        if not notice:
            raise HTTPException(status_code=404, detail="Notice not found.")

        db.delete(notice)
        db.add(AuditLog(actor="admin", action=f"Deleted circular [{notice_id}]", module="Notices"))
        db.commit()
        return {"status": "success", "message": "Notice circular removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete notice %s: %s", notice_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete notice: {str(exc)}")
