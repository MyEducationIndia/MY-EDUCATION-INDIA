from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.entities import Course, AuditLog
from app.models.schemas import CourseCreate, CourseUpdate
from typing import Optional

router = APIRouter(prefix="/courses", tags=["Course & Curriculum Management"])

@router.get("")
def list_courses(category: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Course)
        if category and category != "all":
            query = query.filter(Course.category == category)
        courses = query.order_by(Course.is_popular.desc(), Course.id.asc()).all()
        return [
            {
                "id": c.id,
                "code": c.code,
                "title": c.title,
                "category": c.category,
                "duration": c.duration,
                "fee": c.fee,
                "eligibility": c.eligibility,
                "highlights": c.highlights,
                "syllabus_modules": c.syllabus_modules,
                "badge": c.badge,
                "is_popular": c.is_popular,
                "is_active": c.is_active,
                "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None
            }
            for c in courses
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve courses.")

@router.post("", status_code=201)
def create_course(c: CourseCreate, db: Session = Depends(get_db)):
    try:
        new_course = Course(
            code=c.code,
            title=c.title,
            category=c.category,
            duration=c.duration,
            fee=c.fee,
            eligibility=c.eligibility,
            highlights=c.highlights,
            badge=c.badge or "Standard",
            is_active=1
        )
        db.add(new_course)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Published new course catalog item [{c.code}] {c.title}", module="Courses"))
        return {"status": "success", "course_id": new_course.id, "code": c.code, "title": c.title}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Course creation failed: {str(e)}")

@router.put("/{course_id}")
def update_course(course_id: int, c: CourseUpdate, db: Session = Depends(get_db)):
    try:
        course = db.query(Course).filter(or_(Course.id == course_id, Course.code == str(course_id))).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found.")

        if c.title is not None: course.title = c.title
        if c.duration is not None: course.duration = c.duration
        if c.fee is not None: course.fee = c.fee
        if c.eligibility is not None: course.eligibility = c.eligibility
        if c.highlights is not None: course.highlights = c.highlights
        if c.is_active is not None: course.is_active = c.is_active

        db.add(AuditLog(actor="admin", action=f"Updated parameters for course [{course.code}]", module="Courses"))
        return {"status": "success", "message": "Course parameters updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update course: {str(e)}")

@router.patch("/{course_id}")
def patch_course(course_id: int, c: CourseUpdate, db: Session = Depends(get_db)):
    return update_course(course_id, c, db)

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        course = db.query(Course).filter(or_(Course.id == course_id, Course.code == str(course_id))).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found.")

        code = course.code
        title = course.title
        db.delete(course)
        db.add(AuditLog(actor="admin", action=f"Deleted course [{code}] {title}", module="Courses"))
        return {"status": "success", "message": f"Course {code} deleted."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete course: {str(e)}")
