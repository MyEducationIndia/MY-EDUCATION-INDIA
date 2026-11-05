import json
import random
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import AuditLog, CBTExamResult, ExamConfiguration, ExamForm, QuestionBank
from app.models.schemas import (
    CBTResultSubmit,
    ExamConfigUpdate,
    ExamFormCreate,
    ExamFormUpdate,
    QuestionCreate,
    QuestionUpdate,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/exams", tags=["Exam Management, Question Bank & CBT Results"])


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
            "center_name": "MY EDUCATION Main Campus — Lab Complex 1 & 2, Indore",
        }
    return {
        "window_open": bool(cfg.window_open),
        "require_no_dues": bool(cfg.require_no_dues),
        "session_title": cfg.session_title,
        "start_date": cfg.start_date,
        "last_form_date": cfg.last_form_date,
        "center_name": cfg.center_name,
    }


@router.put("/config")
def update_exam_config(u: ExamConfigUpdate, db: Session = Depends(get_db)):
    try:
        cfg = db.query(ExamConfiguration).filter(ExamConfiguration.id == 1).first()
        if not cfg:
            cfg = ExamConfiguration(id=1)
            db.add(cfg)

        for field, val in u.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(cfg, field, val)

        db.add(AuditLog(actor="admin", action="Updated Exam Portal Configuration", module="Exams"))
        db.commit()
        return {"status": "success", "message": "Exam configuration updated."}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update exam config: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to update exam config: {str(exc)}")


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
                "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S") if f.created_at else None,
            }
            for f in forms
        ]
    except Exception as exc:
        logger.error("Failed to list exam forms: %s", exc)
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
            submitted_date=date.today().strftime("%Y-%m-%d"),
            status="Approved",
        )
        db.add(new_form)
        db.flush()
        db.add(AuditLog(actor=f.student_id, action=f"Submitted exam form [{f_no}]", module="Exams"))
        db.commit()
        return {
            "status": "success",
            "form_no": f_no,
            "admit_card_no": adm_card,
            "message": "Exam form approved. Admit card generated.",
        }
    except Exception as exc:
        db.rollback()
        logger.error("Failed to submit exam form: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to submit exam form: {str(exc)}")


@router.put("/forms/{form_id}")
def update_exam_form(form_id: int, u: ExamFormUpdate, db: Session = Depends(get_db)):
    try:
        form = (
            db.query(ExamForm)
            .filter(or_(ExamForm.id == form_id, ExamForm.form_no == str(form_id)))
            .first()
        )
        if not form:
            raise HTTPException(status_code=404, detail="Exam form not found.")
        if u.status is not None:
            form.status = u.status
        if u.admit_card_no is not None:
            form.admit_card_no = u.admit_card_no
        if u.papers is not None:
            form.papers = json.dumps(u.papers)
        db.commit()
        return {"status": "success", "message": "Exam form updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update exam form %s: %s", form_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update exam form: {str(exc)}")


@router.delete("/forms/{form_id}")
def delete_exam_form(form_id: int, db: Session = Depends(get_db)):
    try:
        form = (
            db.query(ExamForm)
            .filter(or_(ExamForm.id == form_id, ExamForm.form_no == str(form_id)))
            .first()
        )
        if not form:
            raise HTTPException(status_code=404, detail="Exam form not found.")
        db.delete(form)
        db.commit()
        return {"status": "success", "message": "Exam form removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete exam form %s: %s", form_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete exam form: {str(exc)}")


@router.get("/questions")
def list_questions(
    course_code: Optional[str] = None,
    paper_code: Optional[str] = None,
    db: Session = Depends(get_db),
):
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
                "marks": q.marks,
            }
            for q in questions
        ]
    except Exception as exc:
        logger.error("Failed to list questions: %s", exc)
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
            marks=q.marks or 1,
        )
        db.add(new_q)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Added CBT question [{new_q.id}]", module="Exams"))
        db.commit()
        return {"status": "success", "id": new_q.id}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to add question: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to add question: {str(exc)}")


@router.put("/questions/{id}")
def update_question(id: int, q: QuestionUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(QuestionBank).filter(QuestionBank.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Question not found.")
        if q.course_code is not None:
            item.course_code = q.course_code
        if q.paper_code is not None:
            item.paper_code = q.paper_code
        if q.question_text is not None:
            item.question_text = q.question_text
        if q.options is not None:
            item.options = json.dumps(q.options)
        if q.correct_option is not None:
            item.correct_option = q.correct_option
        if q.explanation is not None:
            item.explanation = q.explanation
        if q.marks is not None:
            item.marks = q.marks
        db.commit()
        return {"status": "success", "message": "Question updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update question %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update question: {str(exc)}")


@router.patch("/questions/{id}")
def patch_question(id: int, q: QuestionUpdate, db: Session = Depends(get_db)):
    return update_question(id, q, db)


@router.delete("/questions/{id}")
def delete_question(id: int, db: Session = Depends(get_db)):
    try:
        q = db.query(QuestionBank).filter(QuestionBank.id == id).first()
        if not q:
            raise HTTPException(status_code=404, detail="Question not found.")
        db.delete(q)
        db.commit()
        return {"status": "success", "message": "Question deleted."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete question %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete question: {str(exc)}")


@router.get("/results")
def list_cbt_results(student_id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(CBTExamResult)
        if student_id:
            query = query.filter(
                or_(CBTExamResult.student_id == student_id, CBTExamResult.roll_number == student_id)
            )
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
                "submitted_at": r.submitted_at.strftime("%Y-%m-%d %H:%M:%S") if r.submitted_at else None,
            }
            for r in results
        ]
    except Exception as exc:
        logger.error("Failed to list CBT results: %s", exc)
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
            answers_json=json.dumps(res.answers) if res.answers else "{}",
        )
        db.add(new_res)
        db.flush()
        db.add(
            AuditLog(
                actor=res.roll_number,
                action=f"Completed CBT examination ({res.score}/{res.max_score})",
                module="Exams",
            )
        )
        db.commit()
        return {
            "status": "success",
            "result_id": new_res.id,
            "score": res.score,
            "percentage": res.percentage,
        }
    except Exception as exc:
        db.rollback()
        logger.error("Failed to submit CBT result: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to submit CBT result: {str(exc)}")


@router.delete("/results/{id}")
def delete_cbt_result(id: int, db: Session = Depends(get_db)):
    try:
        r = db.query(CBTExamResult).filter(CBTExamResult.id == id).first()
        if not r:
            raise HTTPException(status_code=404, detail="CBT result not found.")
        db.delete(r)
        db.commit()
        return {"status": "success", "message": "CBT result deleted."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete CBT result %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete CBT result: {str(exc)}")
