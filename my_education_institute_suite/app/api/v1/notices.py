from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.models.schemas import NoticeCreate, NoticeUpdate
from typing import Optional

router = APIRouter(prefix="/notices", tags=["Institute Broadcast & Notice Board"])

@router.get("")
def list_notices(target: Optional[str] = None):
    with get_db() as conn:
        cur = conn.cursor()
        query = "SELECT * FROM notices WHERE 1=1"
        params = []
        if target and target != "All":
            query += " AND (target_audience = ? OR target_audience = 'All')"
            params.append(target)
        query += " ORDER BY is_pinned DESC, id DESC"
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

@router.post("", status_code=201)
def create_notice(n: NoticeCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO notices (title, content, target_audience, category, is_pinned)
            VALUES (?, ?, ?, ?, ?)
        """, (n.title, n.content, n.target_audience, n.category, n.is_pinned))
        notice_id = cur.lastrowid
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Notices')", (f"Published notice [{notice_id}] {n.title}",))
        return {"status": "success", "notice_id": notice_id, "title": n.title}

@router.put("/{notice_id}")
def update_notice(notice_id: int, n: NoticeUpdate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM notices WHERE id = ?", (notice_id,))
        existing = cur.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Notice not found.")

        updates = []
        params = []
        for field, val in n.dict(exclude_unset=True).items():
            if val is not None:
                updates.append(f"{field} = ?")
                params.append(val)

        if updates:
            params.append(notice_id)
            cur.execute(f"UPDATE notices SET {', '.join(updates)} WHERE id = ?", params)
            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Notices')", (f"Updated circular [{notice_id}]",))

        return {"status": "success", "message": "Notice updated successfully."}

@router.delete("/{notice_id}")
def delete_notice(notice_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM notices WHERE id = ?", (notice_id,))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Notices')", (f"Deleted circular [{notice_id}]",))
        return {"status": "success", "message": "Notice circular removed."}
