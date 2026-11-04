from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import Assignment, AssignmentSubmission, Course, Batch, Staff, Student, AuditLog
from app.models.schemas import AssignmentCreate, AssignmentSubmit, AssignmentGrade
from typing import Optional
from datetime import datetime, date

router = APIRouter(prefix="/assignments", tags=["Homework & Assignments"])

@router.get("")
def list_assignments(batch_id: Optional[int] = None, course_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Assignment).join(Course, Assignment.course_id == Course.id).join(Batch, Assignment.batch_id == Batch.id).join(Staff, Assignment.trainer_id == Staff.id)
        if batch_id:
            query = query.filter(Assignment.batch_id == batch_id)
        if course_id:
            query = query.filter(Assignment.course_id == course_id)
        assignments = query.order_by(Assignment.id.desc()).all()

        results = []
        for a in assignments:
            sub_count = db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == a.id).count()
            results.append({
                "id": a.id,
                "title": a.title,
                "course_id": a.course_id,
                "batch_id": a.batch_id,
                "trainer_id": a.trainer_id,
                "due_date": a.due_date.strftime("%Y-%m-%d") if a.due_date else None,
                "instructions": a.instructions,
                "max_marks": a.max_marks,
                "course_title": a.course.title if a.course else None,
                "batch_name": a.batch.name if a.batch else None,
                "trainer_name": a.trainer.name if a.trainer else None,
                "submission_count": sub_count,
                "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S") if a.created_at else None
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve assignments.")

@router.post("", status_code=201)
def create_assignment(a: AssignmentCreate, db: Session = Depends(get_db)):
    try:
        due = datetime.strptime(a.due_date, "%Y-%m-%d").date()
        new_a = Assignment(
            title=a.title,
            course_id=a.course_id,
            batch_id=a.batch_id,
            trainer_id=a.trainer_id,
            due_date=due,
            instructions=a.instructions,
            max_marks=a.max_marks or 20
        )
        db.add(new_a)
        db.flush()
        db.add(AuditLog(actor="faculty", action=f"Published assignment [{new_a.id}] {a.title}", module="Assignments"))
        return {"status": "success", "assignment_id": new_a.id, "title": a.title}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create assignment: {str(e)}")

@router.post("/submit", status_code=201)
def submit_assignment(s: AssignmentSubmit, db: Session = Depends(get_db)):
    try:
        existing = db.query(AssignmentSubmission).filter(
            AssignmentSubmission.assignment_id == s.assignment_id,
            AssignmentSubmission.student_id == s.student_id
        ).first()

        if existing:
            existing.submission_text = s.submission_text
            existing.file_path = s.file_path or ""
            existing.submitted_at = datetime.utcnow()
            existing.status = "Submitted"
        else:
            db.add(AssignmentSubmission(
                assignment_id=s.assignment_id,
                student_id=s.student_id,
                submission_text=s.submission_text,
                file_path=s.file_path or "",
                status="Submitted"
            ))
        return {"status": "success", "message": "Assignment submission recorded."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to submit assignment: {str(e)}")

@router.get("/{assignment_id}/submissions")
def list_submissions(assignment_id: int, db: Session = Depends(get_db)):
    try:
        subs = db.query(AssignmentSubmission).join(Student, AssignmentSubmission.student_id == Student.id).filter(AssignmentSubmission.assignment_id == assignment_id).order_by(AssignmentSubmission.submitted_at.desc()).all()
        return [
            {
                "id": sub.id,
                "assignment_id": sub.assignment_id,
                "student_id": sub.student_id,
                "student_name": sub.student.name if sub.student else None,
                "roll_number": sub.student.roll_number if sub.student else None,
                "submission_text": sub.submission_text,
                "file_path": sub.file_path,
                "grade": sub.grade,
                "marks_obtained": sub.marks_obtained,
                "feedback": sub.feedback,
                "status": sub.status,
                "submitted_at": sub.submitted_at.strftime("%Y-%m-%d %H:%M:%S") if sub.submitted_at else None
            }
            for sub in subs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve submissions.")

@router.post("/submissions/{sub_id}/grade")
def grade_submission(sub_id: int, g: AssignmentGrade, db: Session = Depends(get_db)):
    try:
        sub = db.query(AssignmentSubmission).filter(AssignmentSubmission.id == sub_id).first()
        if not sub:
            raise HTTPException(status_code=404, detail="Submission not found.")
        sub.grade = g.grade
        sub.marks_obtained = g.marks_obtained
        sub.feedback = g.feedback
        sub.status = "Graded"
        return {"status": "success", "message": "Grade recorded."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to grade submission: {str(e)}")

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    try:
        a = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Assignment not found.")
        db.delete(a)
        db.add(AuditLog(actor="admin", action=f"Deleted assignment [{assignment_id}]", module="Assignments"))
        return {"status": "success", "message": "Assignment deleted."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete assignment: {str(e)}")
