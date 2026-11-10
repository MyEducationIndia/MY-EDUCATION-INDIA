"""
Module 15: LXP SQLAlchemy 2.x Async Repository
"""
from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.modules.lxp.models import (
    LearningCourse, LearningModule, LearningLesson,
    CourseEnrollment, LearningProgress, AssignmentSubmission,
    DiscussionTopic, DiscussionPost
)

class LXPRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_course(self, institute_id: str, data: dict) -> LearningCourse:
        cid = str(uuid.uuid4())
        course = LearningCourse(id=cid, institute_id=institute_id, **data)
        self.session.add(course)
        await self.session.commit()
        await self.session.refresh(course)
        return course

    async def list_courses(self, institute_id: str, category: Optional[str] = None) -> List[LearningCourse]:
        stmt = select(LearningCourse).where(LearningCourse.institute_id == institute_id)
        if category:
            stmt = stmt.where(LearningCourse.category == category)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def enroll_student(self, course_id: str, student_id: str, enrollment_type: str = "FREE") -> CourseEnrollment:
        eid = str(uuid.uuid4())
        enrollment = CourseEnrollment(
            id=eid,
            course_id=course_id,
            student_id=student_id,
            enrollment_type=enrollment_type,
            enrollment_status="ACTIVE",
            progress_percentage=0.0
        )
        self.session.add(enrollment)
        await self.session.commit()
        await self.session.refresh(enrollment)
        return enrollment
