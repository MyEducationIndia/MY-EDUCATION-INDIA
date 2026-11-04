from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.models.schemas import BatchCreate, BatchUpdate
from typing import Optional

router = APIRouter(prefix="/batches", tags=["Batch Scheduling & Classroom Timings"])

@router.get("")
def list_batches():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT b.*, c.title as course_title, c.code as course_code, 
                   st.name as trainer_name,
                   (SELECT count(*) FROM students s WHERE s.batch_id = b.id) as enrolled_count
            FROM batches b
            JOIN courses c ON b.course_id = c.id
            LEFT JOIN staff st ON b.trainer_id = st.id
            ORDER BY b.id ASC
        """)
        return [dict(row) for row in cur.fetchall()]

@router.post("", status_code=201)
def create_batch(b: BatchCreate):
    with get_db() as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO batches (code, name, course_id, trainer_id, timing, room, capacity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (b.code, b.name, b.course_id, b.trainer_id, b.timing, b.room, b.capacity))
            batch_id = cur.lastrowid
            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Batches')", (f"Created batch schedule [{b.code}] {b.name}",))
            return {"status": "success", "batch_id": batch_id, "code": b.code}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Batch creation failed: {str(e)}")

@router.put("/{batch_id}")
def update_batch(batch_id: int, b: BatchUpdate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM batches WHERE id = ? OR code = ?", (batch_id, str(batch_id)))
        existing = cur.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Batch not found.")

        updates = []
        params = []
        for field, val in b.dict(exclude_unset=True).items():
            if val is not None:
                updates.append(f"{field} = ?")
                params.append(val)

        if updates:
            params.append(existing["id"])
            cur.execute(f"UPDATE batches SET {', '.join(updates)} WHERE id = ?", params)
            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Batches')", (f"Updated batch timing [{existing['code']}]",))

        return {"status": "success", "message": "Batch schedule updated successfully."}

@router.delete("/{batch_id}")
def delete_batch(batch_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM batches WHERE id = ? OR code = ?", (batch_id, str(batch_id)))
        b = cur.fetchone()
        if not b:
            raise HTTPException(status_code=404, detail="Batch not found.")

        cur.execute("DELETE FROM batches WHERE id = ?", (b["id"],))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Batches')", (f"Deleted batch schedule [{b['code']}]",))
        return {"status": "success", "message": f"Batch {b['code']} deleted."}
