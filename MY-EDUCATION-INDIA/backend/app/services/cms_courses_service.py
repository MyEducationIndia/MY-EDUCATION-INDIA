import uuid
from typing import List, Optional
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ConflictException, NotFoundException
from app.models.cms_courses import (
    CmsCourse,
    CmsCourseCategory,
    CmsCourseCurriculum,
    CmsCourseFaculty,
)
from app.models.institute import Institute
from app.schemas.cms_courses import (
    CmsCourseCategoryCreateRequest,
    CmsCourseCategoryResponse,
    CmsCourseCategoryUpdateRequest,
    CmsCourseCreateRequest,
    CmsCourseCurriculumCreateRequest,
    CmsCourseCurriculumResponse,
    CmsCourseDetailResponse,
    CmsCourseFacultyCreateRequest,
    CmsCourseFacultyResponse,
    CmsCourseSummaryResponse,
    CmsCourseUpdateRequest,
    PublicCoursesBundle,
)


class CmsCoursesService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_primary_institute(self) -> Institute:
        res = await self.session.execute(select(Institute).where(Institute.code == "MEI-HQ"))
        inst = res.scalar_one_or_none()
        if not inst:
            res_any = await self.session.execute(select(Institute).limit(1))
            inst = res_any.scalar_one_or_none()
        if not inst:
            raise NotFoundException("Primary Institute baseline not found in database.")
        return inst

    # =========================================================================
    # 1. PUBLIC ENDPOINTS (Zero-Login Public Aggregator)
    # =========================================================================
    async def get_public_courses_bundle(
        self,
        category_slug: Optional[str] = None,
        degree_level: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> PublicCoursesBundle:
        inst = await self._get_primary_institute()

        # 1. Categories
        cat_stmt = (
            select(CmsCourseCategory)
            .where(
                CmsCourseCategory.institute_id == inst.id,
                CmsCourseCategory.is_active == True,
            )
            .order_by(CmsCourseCategory.display_order.asc(), CmsCourseCategory.name.asc())
        )
        cat_res = await self.session.execute(cat_stmt)
        categories = list(cat_res.scalars().all())

        # 2. Courses
        course_stmt = (
            select(CmsCourse)
            .where(
                CmsCourse.institute_id == inst.id,
                CmsCourse.is_active == True,
            )
        )

        if category_slug:
            # Join with category to filter by slug
            course_stmt = course_stmt.join(CmsCourse.category).where(CmsCourseCategory.slug == category_slug)

        if degree_level:
            course_stmt = course_stmt.where(CmsCourse.degree_level == degree_level.upper())

        if search_query:
            q = f"%{search_query.strip()}%"
            course_stmt = course_stmt.where(
                or_(
                    CmsCourse.title.ilike(q),
                    CmsCourse.code.ilike(q),
                    CmsCourse.short_name.ilike(q),
                    CmsCourse.summary.ilike(q),
                )
            )

        course_stmt = course_stmt.order_by(CmsCourse.display_order.asc(), CmsCourse.title.asc())
        course_res = await self.session.execute(course_stmt)
        courses = list(course_res.scalars().all())

        # Featured Courses
        featured_courses = [c for c in courses if c.is_featured]

        return PublicCoursesBundle(
            categories=[CmsCourseCategoryResponse.model_validate(c) for c in categories],
            courses=[CmsCourseSummaryResponse.model_validate(c) for c in courses],
            featured_courses=[CmsCourseSummaryResponse.model_validate(c) for c in featured_courses],
            total_courses=len(courses),
        )

    async def get_course_by_slug(self, slug: str) -> CmsCourseDetailResponse:
        inst = await self._get_primary_institute()

        stmt = (
            select(CmsCourse)
            .where(
                CmsCourse.institute_id == inst.id,
                CmsCourse.slug == slug,
                CmsCourse.is_active == True,
            )
            .options(
                selectinload(CmsCourse.category),
                selectinload(CmsCourse.curricula),
                selectinload(CmsCourse.faculty_members),
            )
        )
        res = await self.session.execute(stmt)
        course = res.scalar_one_or_none()

        if not course:
            raise NotFoundException(f"Degree course with slug '{slug}' not found.")

        return CmsCourseDetailResponse.model_validate(course)

    # =========================================================================
    # 2. ADMIN COURSE CATEGORIES
    # =========================================================================
    async def list_admin_categories(self) -> List[CmsCourseCategoryResponse]:
        inst = await self._get_primary_institute()
        stmt = (
            select(CmsCourseCategory)
            .where(CmsCourseCategory.institute_id == inst.id)
            .order_by(CmsCourseCategory.display_order.asc(), CmsCourseCategory.name.asc())
        )
        res = await self.session.execute(stmt)
        return [CmsCourseCategoryResponse.model_validate(c) for c in res.scalars().all()]

    async def create_category(self, payload: CmsCourseCategoryCreateRequest) -> CmsCourseCategoryResponse:
        inst = await self._get_primary_institute()

        # Check duplicate slug
        existing = await self.session.execute(
            select(CmsCourseCategory).where(
                CmsCourseCategory.institute_id == inst.id,
                CmsCourseCategory.slug == payload.slug,
            )
        )
        if existing.scalar_one_or_none():
            raise ConflictException(f"Course category with slug '{payload.slug}' already exists.")

        cat = CmsCourseCategory(
            institute_id=inst.id,
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            icon_name=payload.icon_name,
            display_order=payload.display_order,
            is_active=payload.is_active,
        )
        self.session.add(cat)
        await self.session.commit()
        await self.session.refresh(cat)
        return CmsCourseCategoryResponse.model_validate(cat)

    async def update_category(self, cat_id: uuid.UUID, payload: CmsCourseCategoryUpdateRequest) -> CmsCourseCategoryResponse:
        stmt = select(CmsCourseCategory).where(CmsCourseCategory.id == cat_id)
        res = await self.session.execute(stmt)
        cat = res.scalar_one_or_none()
        if not cat:
            raise NotFoundException("Course category not found.")

        for field, val in payload.model_dump(exclude_unset=True).items():
            setattr(cat, field, val)

        await self.session.commit()
        await self.session.refresh(cat)
        return CmsCourseCategoryResponse.model_validate(cat)

    async def delete_category(self, cat_id: uuid.UUID) -> None:
        stmt = select(CmsCourseCategory).where(CmsCourseCategory.id == cat_id)
        res = await self.session.execute(stmt)
        cat = res.scalar_one_or_none()
        if not cat:
            raise NotFoundException("Course category not found.")

        await self.session.delete(cat)
        await self.session.commit()

    # =========================================================================
    # 3. ADMIN COURSES
    # =========================================================================
    async def list_admin_courses(self, category_id: Optional[uuid.UUID] = None) -> List[CmsCourseSummaryResponse]:
        inst = await self._get_primary_institute()
        stmt = select(CmsCourse).where(CmsCourse.institute_id == inst.id)
        if category_id:
            stmt = stmt.where(CmsCourse.category_id == category_id)

        stmt = stmt.order_by(CmsCourse.display_order.asc(), CmsCourse.title.asc())
        res = await self.session.execute(stmt)
        return [CmsCourseSummaryResponse.model_validate(c) for c in res.scalars().all()]

    async def get_admin_course_detail(self, course_id: uuid.UUID) -> CmsCourseDetailResponse:
        stmt = (
            select(CmsCourse)
            .where(CmsCourse.id == course_id)
            .options(
                selectinload(CmsCourse.category),
                selectinload(CmsCourse.curricula),
                selectinload(CmsCourse.faculty_members),
            )
        )
        res = await self.session.execute(stmt)
        course = res.scalar_one_or_none()
        if not course:
            raise NotFoundException("Degree course not found.")
        return CmsCourseDetailResponse.model_validate(course)

    async def create_course(self, payload: CmsCourseCreateRequest) -> CmsCourseDetailResponse:
        inst = await self._get_primary_institute()

        # Check category existence
        cat_res = await self.session.execute(
            select(CmsCourseCategory).where(
                CmsCourseCategory.id == payload.category_id,
                CmsCourseCategory.institute_id == inst.id,
            )
        )
        if not cat_res.scalar_one_or_none():
            raise NotFoundException("Specified course category not found.")

        # Check duplicate code or slug
        existing = await self.session.execute(
            select(CmsCourse).where(
                CmsCourse.institute_id == inst.id,
                or_(CmsCourse.code == payload.code, CmsCourse.slug == payload.slug),
            )
        )
        if existing.scalar_one_or_none():
            raise ConflictException(f"A course with code '{payload.code}' or slug '{payload.slug}' already exists.")

        course = CmsCourse(
            institute_id=inst.id,
            **payload.model_dump(),
        )
        self.session.add(course)
        await self.session.commit()
        return await self.get_admin_course_detail(course.id)

    async def update_course(self, course_id: uuid.UUID, payload: CmsCourseUpdateRequest) -> CmsCourseDetailResponse:
        stmt = select(CmsCourse).where(CmsCourse.id == course_id)
        res = await self.session.execute(stmt)
        course = res.scalar_one_or_none()
        if not course:
            raise NotFoundException("Degree course not found.")

        for field, val in payload.model_dump(exclude_unset=True).items():
            setattr(course, field, val)

        await self.session.commit()
        return await self.get_admin_course_detail(course.id)

    async def delete_course(self, course_id: uuid.UUID) -> None:
        stmt = select(CmsCourse).where(CmsCourse.id == course_id)
        res = await self.session.execute(stmt)
        course = res.scalar_one_or_none()
        if not course:
            raise NotFoundException("Degree course not found.")

        await self.session.delete(course)
        await self.session.commit()

    # =========================================================================
    # 4. CURRICULUM & FACULTY MANAGEMENT
    # =========================================================================
    async def add_curriculum_semester(
        self, course_id: uuid.UUID, payload: CmsCourseCurriculumCreateRequest
    ) -> CmsCourseCurriculumResponse:
        course_res = await self.session.execute(select(CmsCourse).where(CmsCourse.id == course_id))
        if not course_res.scalar_one_or_none():
            raise NotFoundException("Course not found.")

        curr = CmsCourseCurriculum(
            course_id=course_id,
            semester_number=payload.semester_number,
            semester_title=payload.semester_title,
            credits=payload.credits,
            subjects=payload.subjects,
            display_order=payload.display_order,
        )
        self.session.add(curr)
        await self.session.commit()
        await self.session.refresh(curr)
        return CmsCourseCurriculumResponse.model_validate(curr)

    async def delete_curriculum_semester(self, curriculum_id: uuid.UUID) -> None:
        stmt = select(CmsCourseCurriculum).where(CmsCourseCurriculum.id == curriculum_id)
        res = await self.session.execute(stmt)
        curr = res.scalar_one_or_none()
        if not curr:
            raise NotFoundException("Curriculum semester not found.")

        await self.session.delete(curr)
        await self.session.commit()

    async def add_course_faculty(
        self, course_id: uuid.UUID, payload: CmsCourseFacultyCreateRequest
    ) -> CmsCourseFacultyResponse:
        course_res = await self.session.execute(select(CmsCourse).where(CmsCourse.id == course_id))
        if not course_res.scalar_one_or_none():
            raise NotFoundException("Course not found.")

        fac = CmsCourseFaculty(
            course_id=course_id,
            faculty_name=payload.faculty_name,
            designation=payload.designation,
            qualifications=payload.qualifications,
            specialization=payload.specialization,
            avatar_url=payload.avatar_url,
            display_order=payload.display_order,
        )
        self.session.add(fac)
        await self.session.commit()
        await self.session.refresh(fac)
        return CmsCourseFacultyResponse.model_validate(fac)

    async def delete_course_faculty(self, faculty_id: uuid.UUID) -> None:
        stmt = select(CmsCourseFaculty).where(CmsCourseFaculty.id == faculty_id)
        res = await self.session.execute(stmt)
        fac = res.scalar_one_or_none()
        if not fac:
            raise NotFoundException("Course faculty member not found.")

        await self.session.delete(fac)
        await self.session.commit()
