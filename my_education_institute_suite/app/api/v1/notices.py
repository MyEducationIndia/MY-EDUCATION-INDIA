from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.entities import Notice, AuditLog
from app.models.schemas import NoticeCreate, NoticeUpdate
from typing import Optional

router = APIRouter(prefix="/notices", tags=["Institute Broadcast & Notice Board"])

@router.get("")
def list_notices(target: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Notice)
        if target and target != "All":
            query = query.filter(or_(Notice.target_audience == target, Notice.target_audience == "All"))
        notices = query.order_by(Notice.is_pinned.desc(), Notice.id.desc()).all()
        return [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "target_audience": n.target_audience,
                "category": n.category,
                "is_pinned": n.is_pinned,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S") if n.created_at else None
            }
            for n in notices
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve notices.")

@router.post("", status_code=201)
def create_notice(n: NoticeCreate, db: Session = Depends(get_db)):
    try:
        new_notice = Notice(
            title=n.title,
            content=n.content,
            target_audience=n.target_audience,
            category=n.category,
            is_pinned=n.is_pinned or 0
        )
        db.add(new_notice)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Published notice [{new_notice.id}] {n.title}", module="Notices"))
        return {"status": "success", "notice_id": new_notice.id, "title": n.title}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create notice: {str(e)}")

@router.put("/{notice_id}")
def update_notice(notice_id: int, n: NoticeUpdate, db: Session = Depends(get_db)):
    try:
        notice = db.query(Notice).filter(Notice.id == notice_id).first()
        if not notice:
            raise HTTPException(status_code=404, detail="Notice not found.")

        if n.title is not None: notice.title = n.title
        if n.content is not None: notice.content = n.content
        if n.target_audience is not None: notice.target_audience = n.target_audience
        if n.category is not None: notice.category = n.category
        if n.is_pinned is not None: notice.is_pinned = n.is_pinned

        db.add(AuditLog(actor="admin", action=f"Updated circular [{notice_id}]", module="Notices"))
        return {"status": "success", "message": "Notice updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update notice: {str(e)}")

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
        return {"status": "success", "message": "Notice circular removed."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete notice: {str(e)}")
