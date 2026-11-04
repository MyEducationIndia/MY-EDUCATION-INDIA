from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.models.schemas import MaterialCreate
from typing import Optional

router = APIRouter(prefix="/materials", tags=["Study Material & Lecture Notes"])

@router.get("")
def list_materials(course_id: Optional[int] = None):
    with get_db() as conn:
        cur = conn.cursor()
        query = """
            SELECT sm.*, c.title as course_title, c.code as course_code, b.name as batch_name
            FROM study_materials sm
            JOIN courses c ON sm.course_id = c.id
            LEFT JOIN batches b ON sm.batch_id = b.id
            WHERE 1=1
        """
        params = []
        if course_id:
            query += " AND sm.course_id = ?"
            params.append(course_id)
        query += " ORDER BY sm.id DESC"
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

@router.post("", status_code=201)
def upload_material(m: MaterialCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO study_materials (title, course_id, batch_id, file_path, file_type, file_size, author)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (m.title, m.course_id, m.batch_id, m.file_path, m.file_type, m.file_size, m.author))
        mat_id = cur.lastrowid
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('faculty', ?, 'Materials')", (f"Uploaded document [{m.title}]",))
        return {"status": "success", "material_id": mat_id, "title": m.title}

@router.delete("/{material_id}")
def delete_material(material_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM study_materials WHERE id = ?", (material_id,))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Materials')", (f"Deleted material [{material_id}]",))
        return {"status": "success", "message": "Study material removed."}
