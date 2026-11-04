from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.entities import ExamConfiguration, ExamForm, QuestionBank, CBTExamResult, AuditLog
from app.models.schemas import ExamConfigUpdate, ExamFormCreate, ExamFormUpdate, QuestionCreate, QuestionUpdate, CBTResultSubmit
from typing import Optional, List, Dict, Any
import json, random

router = APIRouter(prefix="/exams", tags=["Exam Management, Question Bank & CBT Results"])

# Exam Configuration
@router.get("/config")
def get_exam_config(db: Session = Depends(get_db)):
    cfg = db.query(ExamConfiguration).filter(ExamConfiguration.id == 1).first()
    if not cfg:
        return {
            "window_open": True,
            "require_no_dues": True,
            "session_title": "Winter Semester Diploma & Vocational Final Examination — Dec 2026",
            "start_date": "2026-12-10",
            "last_form_date": "2026-11-25",
            "center_name": "MY EDUCATION Main Campus — Lab Complex 1 & 2, Indore"
        }
    return {
        "window_open": bool(cfg.window_open),
        "require_no_dues": bool(cfg.require_no_dues),
        "session_title": cfg.session_title,
        "start_date": cfg.start_date,
        "last_form_date": cfg.last_form_date,
        "center_name": cfg.center_name
    }

@router.put("/config")
def update_exam_config(u: ExamConfigUpdate, db: Session = Depends(get_db)):
    try:
        cfg = db.query(ExamConfiguration).filter(ExamConfiguration.id == 1).first()
        if not cfg:
            cfg = ExamConfiguration(id=1)
            db.add(cfg)

        if u.window_open is not None: cfg.window_open = u.window_open
        if u.require_no_dues is not None: cfg.require_no_dues = u.require_no_dues
        if u.session_title is not None: cfg.session_title = u.session_title
        if u.start_date is not None: cfg.start_date = u.start_date
        if u.last_form_date is not None: cfg.last_form_date = u.last_form_date
        if u.center_name is not None: cfg.center_name = u.center_name

        db.add(AuditLog(actor="admin", action="Updated Exam Portal Configuration", module="Exams"))
        return {"status": "success", "message": "Exam configuration updated."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update exam config: {str(e)}")

# Exam Registration Forms
@router.get("/forms")
def list_exam_forms(student_id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(ExamForm)
        if student_id:
            query = query.filter(ExamForm.student_id == student_id)
        forms = query.order_by(ExamForm.id.desc()).all()
        return [
            {
                "id": f.id,
                "form_no": f.form_no,
                "admit_card_no": f.admit_card_no,
                "student_id": f.student_id,
                "student_name": f.student_name,
                "course": f.course,
                "batch": f.batch,
                "exam_session": f.exam_session,
                "category": f.category,
                "medium": f.medium,
                "papers": json.loads(f.papers) if f.papers else [],
                "no_dues_cert_no": f.no_dues_cert_no,
                "submitted_date": f.submitted_date,
                "status": f.status,
                "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S") if f.created_at else None
            }
            for f in forms
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve exam forms.")

@router.post("/forms", status_code=201)
def submit_exam_form(f: ExamFormCreate, db: Session = Depends(get_db)):
    try:
        f_no = f"EXM-2026-{random.randint(1000, 9999)}"
        adm_card = f"ADM-2026-{random.randint(1000, 9999)}"
        new_form = ExamForm(
            form_no=f_no,
            admit_card_no=adm_card,
            student_id=f.student_id,
            student_name=f.student_name,
            course=f.course,
            batch=f.batch or "",
            exam_session=f.exam_session or "Winter Semester Final Exam — 2026",
            category=f.category or "Regular",
            medium=f.medium or "English",
            papers=json.dumps(f.papers or []),
            no_dues_cert_no=f.no_dues_cert_no or f"NDC-2026-{random.randint(1000, 9999)}",
            submitted_date=f"{random.randint(2026, 2026)}-11-01",
            status="Approved"
        )
        db.add(new_form)
        db.flush()
        db.add(AuditLog(actor=f.student_id, action=f"Submitted exam form [{f_no}]", module="Exams"))
        return {
            "status": "success",
            "form_no": f_no,
            "admit_card_no": adm_card,
            "message": "Exam form approved. Admit card generated."
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to submit exam form: {str(e)}")

@router.put("/forms/{form_id}")
def update_exam_form(form_id: int, u: ExamFormUpdate, db: Session = Depends(get_db)):
    try:
        form = db.query(ExamForm).filter(ExamForm.id == form_id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Exam form not found.")
        if u.status is not None: form.status = u.status
        if u.admit_card_no is not None: form.admit_card_no = u.admit_card_no
        if u.papers is not None: form.papers = json.dumps(u.papers)
        return {"status": "success", "message": "Exam form updated."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update exam form: {str(e)}")

@router.delete("/forms/{form_id}")
def delete_exam_form(form_id: int, db: Session = Depends(get_db)):
    try:
        form = db.query(ExamForm).filter(ExamForm.id == form_id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Exam form not found.")
        db.delete(form)
        return {"status": "success", "message": "Exam form removed."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete exam form: {str(e)}")

# Question Bank
@router.get("/questions")
def list_questions(course_code: Optional[str] = None, paper_code: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(QuestionBank)
        if course_code:
            query = query.filter(QuestionBank.course_code == course_code)
        if paper_code:
            query = query.filter(QuestionBank.paper_code == paper_code)
        questions = query.order_by(QuestionBank.id.asc()).all()
        return [
            {
                "id": q.id,
                "course_code": q.course_code,
                "paper_code": q.paper_code,
                "question_text": q.question_text,
                "options": json.loads(q.options) if q.options else [],
                "correct_option": q.correct_option,
                "explanation": q.explanation,
                "marks": q.marks
            }
            for q in questions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve questions.")

@router.post("/questions", status_code=201)
def add_question(q: QuestionCreate, db: Session = Depends(get_db)):
    try:
        new_q = QuestionBank(
            course_code=q.course_code,
            paper_code=q.paper_code,
            question_text=q.question_text,
            options=json.dumps(q.options),
            correct_option=q.correct_option,
            explanation=q.explanation or "",
            marks=q.marks or 1
        )
        db.add(new_q)
        db.flush()
        return {"status": "success", "id": new_q.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to add question: {str(e)}")

@router.delete("/questions/{id}")
def delete_question(id: int, db: Session = Depends(get_db)):
    try:
        q = db.query(QuestionBank).filter(QuestionBank.id == id).first()
        if not q:
            raise HTTPException(status_code=404, detail="Question not found.")
        db.delete(q)
        return {"status": "success", "message": "Question deleted."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete question: {str(e)}")

# CBT Examination Results
@router.get("/results")
def list_cbt_results(student_id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(CBTExamResult)
        if student_id:
            query = query.filter(or_(CBTExamResult.student_id == student_id, CBTExamResult.roll_number == student_id))
        results = query.order_by(CBTExamResult.id.desc()).all()
        return [
            {
                "id": r.id,
                "student_id": r.student_id,
                "roll_number": r.roll_number,
                "exam_session": r.exam_session,
                "score": r.score,
                "max_score": r.max_score,
                "percentage": r.percentage,
                "status": r.status,
                "submitted_at": r.submitted_at.strftime("%Y-%m-%d %H:%M:%S") if r.submitted_at else None
            }
            for r in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve exam results.")

@router.post("/results", status_code=201)
def submit_cbt_result(res: CBTResultSubmit, db: Session = Depends(get_db)):
    try:
        new_res = CBTExamResult(
            student_id=res.student_id,
            roll_number=res.roll_number,
            exam_session=res.exam_session or "Winter Semester CBT Exam 2026",
            score=res.score,
            max_score=res.max_score,
            percentage=res.percentage,
            status=res.status or "Completed",
            answers_json=json.dumps(res.answers) if res.answers else "{}"
        )
        db.add(new_res)
        db.flush()
        db.add(AuditLog(actor=res.roll_number, action=f"Completed CBT examination ({res.score}/{res.max_score})", module="Exams"))
        return {"status": "success", "result_id": new_res.id, "score": res.score, "percentage": res.percentage}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to submit CBT result: {str(e)}")
