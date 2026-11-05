from datetime import datetime
from typing import Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import Assignment, AssignmentSubmission, AuditLog, Batch, Course, Staff, Student
from app.models.schemas import AssignmentCreate, AssignmentGrade, AssignmentSubmit, AssignmentUpdate

logger = get_logger(__name__)
router = APIRouter(prefix="/assignments", tags=["Homework & Assignments"])


@router.get("")
def list_assignments(
    batch_id: Optional[int] = None,
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    try:
        query = (
            db.query(Assignment)
            .join(Course, Assignment.course_id == Course.id)
            .join(Batch, Assignment.batch_id == Batch.id)
            .join(Staff, Assignment.trainer_id == Staff.id)
        )
        if batch_id:
            query = query.filter(Assignment.batch_id == batch_id)
        if course_id:
            query = query.filter(Assignment.course_id == course_id)
        assignments = query.order_by(Assignment.id.desc()).all()

        # Single-pass submission count aggregation to eliminate N+1 queries
        all_subs = db.query(AssignmentSubmission).all()
        sub_counts: Dict[int, int] = {}
        for s in all_subs:
            sub_counts[s.assignment_id] = sub_counts.get(s.assignment_id, 0) + 1

        results = []
        for a in assignments:
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
                "submission_count": sub_counts.get(a.id, 0),
                "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S") if a.created_at else None,
            })
        return results
    except Exception as exc:
        logger.error("Failed to list assignments: %s", exc)
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
            max_marks=a.max_marks or 20,
        )
        db.add(new_a)
        db.flush()
        db.add(AuditLog(actor="faculty", action=f"Published assignment [{new_a.id}] {a.title}", module="Assignments"))
        return {"status": "success", "assignment_id": new_a.id, "title": a.title}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create assignment: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create assignment: {str(exc)}")


@router.put("/{assignment_id}")
def update_assignment(assignment_id: int, a: AssignmentUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Assignment not found.")
        if a.title is not None:
            item.title = a.title
        if a.due_date is not None:
            item.due_date = datetime.strptime(a.due_date, "%Y-%m-%d").date()
        if a.instructions is not None:
            item.instructions = a.instructions
        if a.max_marks is not None:
            item.max_marks = a.max_marks
        db.add(AuditLog(actor="faculty", action=f"Updated assignment [{assignment_id}]", module="Assignments"))
        return {"status": "success", "message": "Assignment updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update assignment %s: %s", assignment_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update assignment: {str(exc)}")


@router.patch("/{assignment_id}")
def patch_assignment(assignment_id: int, a: AssignmentUpdate, db: Session = Depends(get_db)):
    return update_assignment(assignment_id, a, db)


@router.post("/submit", status_code=201)
def submit_assignment(s: AssignmentSubmit, db: Session = Depends(get_db)):
    try:
        existing = (
            db.query(AssignmentSubmission)
            .filter(
                AssignmentSubmission.assignment_id == s.assignment_id,
                AssignmentSubmission.student_id == s.student_id,
            )
            .first()
        )

        if existing:
            existing.submission_text = s.submission_text
            existing.file_path = s.file_path or ""
            existing.submitted_at = datetime.utcnow()
            existing.status = "Submitted"
        else:
            db.add(
                AssignmentSubmission(
                    assignment_id=s.assignment_id,
                    student_id=s.student_id,
                    submission_text=s.submission_text,
                    file_path=s.file_path or "",
                    status="Submitted",
                )
            )
        return {"status": "success", "message": "Assignment submission recorded."}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to submit assignment: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to submit assignment: {str(exc)}")


@router.get("/{assignment_id}/submissions")
def list_submissions(assignment_id: int, db: Session = Depends(get_db)):
    try:
        subs = (
            db.query(AssignmentSubmission)
            .join(Student, AssignmentSubmission.student_id == Student.id)
            .filter(AssignmentSubmission.assignment_id == assignment_id)
            .order_by(AssignmentSubmission.submitted_at.desc())
            .all()
        )
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
                "submitted_at": sub.submitted_at.strftime("%Y-%m-%d %H:%M:%S") if sub.submitted_at else None,
            }
            for sub in subs
        ]
    except Exception as exc:
        logger.error("Failed to list submissions for assignment %s: %s", assignment_id, exc)
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
    except Exception as exc:
        db.rollback()
        logger.error("Failed to grade submission %s: %s", sub_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to grade submission: {str(exc)}")


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
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete assignment %s: %s", assignment_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete assignment: {str(exc)}")
