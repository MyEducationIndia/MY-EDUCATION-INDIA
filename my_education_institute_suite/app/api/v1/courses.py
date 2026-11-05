from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import AuditLog, Course
from app.models.schemas import CourseCreate, CourseUpdate

logger = get_logger(__name__)
router = APIRouter(prefix="/courses", tags=["Course & Curriculum Management"])


@router.get("")
def list_courses(
    category: Optional[str] = None,
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Course)
        if category and category != "all":
            query = query.filter(Course.category == category)
        if q:
            term = f"%{q}%"
            query = query.filter(or_(Course.title.ilike(term), Course.code.ilike(term)))
        courses = query.order_by(Course.is_popular.desc(), Course.id.asc()).offset(skip).limit(limit).all()
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
                "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None,
            }
            for c in courses
        ]
    except Exception as exc:
        logger.error("Failed to list courses: %s", exc)
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
            syllabus_modules=c.syllabus_modules,
            badge=c.badge or "Standard",
            is_popular=c.is_popular or 0,
            is_active=1,
        )
        db.add(new_course)
        db.flush()
        db.add(
            AuditLog(
                actor="admin",
                action=f"Published new course catalog item [{c.code}] {c.title}",
                module="Courses",
            )
        )
        return {"status": "success", "course_id": new_course.id, "code": c.code, "title": c.title}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create course: %s", exc)
        raise HTTPException(status_code=400, detail=f"Course creation failed: {str(exc)}")


@router.put("/{course_id}")
def update_course(course_id: int, c: CourseUpdate, db: Session = Depends(get_db)):
    try:
        course = db.query(Course).filter(or_(Course.id == course_id, Course.code == str(course_id))).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found.")

        for field, val in c.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(course, field, val)

        db.add(AuditLog(actor="admin", action=f"Updated parameters for course [{course.code}]", module="Courses"))
        return {"status": "success", "message": "Course parameters updated successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update course %s: %s", course_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update course: {str(exc)}")


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
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete course %s: %s", course_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete course: {str(exc)}")
