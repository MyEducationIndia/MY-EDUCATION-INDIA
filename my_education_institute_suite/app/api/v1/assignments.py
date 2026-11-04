from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.models.schemas import AssignmentCreate, AssignmentSubmit, AssignmentGrade
from typing import Optional

router = APIRouter(prefix="/assignments", tags=["Homework & Assignments"])

@router.get("")
def list_assignments(batch_id: Optional[int] = None, course_id: Optional[int] = None):
    with get_db() as conn:
        cur = conn.cursor()
        query = """
            SELECT a.*, c.title as course_title, b.name as batch_name, s.name as trainer_name,
                   (SELECT count(*) FROM assignment_submissions sub WHERE sub.assignment_id = a.id) as submission_count
            FROM assignments a
            JOIN courses c ON a.course_id = c.id
            JOIN batches b ON a.batch_id = b.id
            JOIN staff s ON a.trainer_id = s.id
            WHERE 1=1
        """
        params = []
        if batch_id:
            query += " AND a.batch_id = ?"
            params.append(batch_id)
        if course_id:
            query += " AND a.course_id = ?"
            params.append(course_id)
        query += " ORDER BY a.id DESC"
        cur.execute(query, params)
        return [dict(r) for r in cur.fetchall()]

@router.post("", status_code=201)
def create_assignment(a: AssignmentCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO assignments (title, course_id, batch_id, trainer_id, due_date, instructions, max_marks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (a.title, a.course_id, a.batch_id, a.trainer_id, a.due_date, a.instructions, a.max_marks))
        ass_id = cur.lastrowid
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('faculty', ?, 'Assignments')", (f"Published assignment [{ass_id}] {a.title}",))
        return {"status": "success", "assignment_id": ass_id, "title": a.title}

@router.post("/submit", status_code=201)
def submit_assignment(s: AssignmentSubmit):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO assignment_submissions (assignment_id, student_id, submission_text, file_path, status)
            VALUES (?, ?, ?, ?, 'Submitted')
        """, (s.assignment_id, s.student_id, s.submission_text, s.file_path))
        return {"status": "success", "message": "Assignment submission recorded."}

@router.get("/{assignment_id}/submissions")
def list_submissions(assignment_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT sub.*, st.name as student_name, st.roll_number
            FROM assignment_submissions sub
            JOIN students st ON sub.student_id = st.id
            WHERE sub.assignment_id = ?
            ORDER BY sub.submitted_at DESC
        """, (assignment_id,))
        return [dict(r) for r in cur.fetchall()]
