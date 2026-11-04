from fastapi import APIRouter, HTTPException, Query
from app.core.database import get_db
from app.models.schemas import CourseCreate, CourseUpdate
from typing import Optional

router = APIRouter(prefix="/courses", tags=["Course & Curriculum Management"])

@router.get("")
def list_courses(category: Optional[str] = None):
    with get_db() as conn:
        cur = conn.cursor()
        query = "SELECT * FROM courses WHERE 1=1"
        params = []
        if category and category != "all":
            query += " AND category = ?"
            params.append(category)
        query += " ORDER BY is_popular DESC, id ASC"
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

@router.post("", status_code=201)
def create_course(c: CourseCreate):
    with get_db() as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO courses (code, title, category, duration, fee, eligibility, highlights, badge)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (c.code, c.title, c.category, c.duration, c.fee, c.eligibility, c.highlights, c.badge))
            course_id = cur.lastrowid
            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Courses')", (f"Published new course catalog item [{c.code}] {c.title}",))
            return {"status": "success", "course_id": course_id, "code": c.code, "title": c.title}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Course creation failed: {str(e)}")

@router.put("/{course_id}")
def update_course(course_id: int, c: CourseUpdate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses WHERE id = ? OR code = ?", (course_id, str(course_id)))
        existing = cur.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Course not found.")

        updates = []
        params = []
        for field, val in c.dict(exclude_unset=True).items():
            if val is not None:
                updates.append(f"{field} = ?")
                params.append(val)

        if updates:
            params.append(existing["id"])
            cur.execute(f"UPDATE courses SET {', '.join(updates)} WHERE id = ?", params)
            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Courses')", (f"Updated parameters for course [{existing['code']}]",))

        return {"status": "success", "message": "Course parameters updated successfully."}

@router.delete("/{course_id}")
def delete_course(course_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses WHERE id = ? OR code = ?", (course_id, str(course_id)))
        c = cur.fetchone()
        if not c:
            raise HTTPException(status_code=404, detail="Course not found.")

        cur.execute("DELETE FROM courses WHERE id = ?", (c["id"],))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Courses')", (f"Deleted course [{c['code']}] {c['title']}",))
        return {"status": "success", "message": f"Course {c['code']} deleted."}
