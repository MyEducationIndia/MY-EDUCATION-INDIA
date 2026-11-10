from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.cbt.models import (
    QuestionPool,
    CandidateAnswer,
    CandidateSession,
    CBTSession,
    ExamTemplate,
    QuestionBank,
    QuestionCategory,
    QuestionTopic,
    QuestionTag,
    QuestionVersion,
)


class CBTRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # Question Bank & Topics
    async def create_question_bank(self, qb: QuestionBank) -> QuestionBank:
        self.session.add(qb)
        await self.session.commit()
        await self.session.refresh(qb)
        return qb

    async def get_question_banks(self, institute_id: uuid.UUID) -> List[QuestionBank]:
        stmt = select(QuestionBank).where(QuestionBank.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def save_question(self, q: QuestionVersion) -> QuestionVersion:
        self.session.add(q)
        await self.session.commit()
        await self.session.refresh(q)
        return q

    # Templates & CBT Sessions
    async def create_template(self, t: ExamTemplate) -> ExamTemplate:
        self.session.add(t)
        await self.session.commit()
        await self.session.refresh(t)
        return t

    async def create_cbt_session(self, s: CBTSession) -> CBTSession:
        self.session.add(s)
        await self.session.commit()
        await self.session.refresh(s)
        return s

    async def get_cbt_session_by_id(self, session_id: uuid.UUID) -> Optional[CBTSession]:
        stmt = select(CBTSession).where(CBTSession.id == session_id).options(selectinload(CBTSession.template))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # Candidate Sessions & Answers
    async def get_candidate_session(self, cbt_session_id: uuid.UUID, student_id: uuid.UUID) -> Optional[CandidateSession]:
        stmt = select(CandidateSession).where(
            CandidateSession.cbt_session_id == cbt_session_id,
            CandidateSession.student_id == student_id,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def save_candidate_session(self, cs: CandidateSession) -> CandidateSession:
        self.session.add(cs)
        await self.session.commit()
        await self.session.refresh(cs)
        return cs

    async def save_candidate_answer(self, ans: CandidateAnswer) -> CandidateAnswer:
        self.session.add(ans)
        await self.session.commit()
        await self.session.refresh(ans)
        return ans

    async def get_candidate_answers(self, candidate_session_id: uuid.UUID) -> List[CandidateAnswer]:
        stmt = select(CandidateAnswer).where(CandidateAnswer.candidate_session_id == candidate_session_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # Categories, Topics, and Tags
    async def create_category(self, cat: QuestionCategory) -> QuestionCategory:
        self.session.add(cat)
        await self.session.commit()
        await self.session.refresh(cat)
        return cat

    async def get_categories(self, question_bank_id: uuid.UUID) -> List[QuestionCategory]:
        stmt = select(QuestionCategory).where(QuestionCategory.question_bank_id == question_bank_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_topic(self, topic: QuestionTopic) -> QuestionTopic:
        self.session.add(topic)
        await self.session.commit()
        await self.session.refresh(topic)
        return topic

    async def get_topics(self, category_id: uuid.UUID) -> List[QuestionTopic]:
        stmt = select(QuestionTopic).where(QuestionTopic.category_id == category_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_tag(self, tag: QuestionTag) -> QuestionTag:
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def get_tags(self, institute_id: uuid.UUID) -> List[QuestionTag]:
        stmt = select(QuestionTag).where(QuestionTag.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_questions(
        self,
        topic_id: Optional[uuid.UUID] = None,
        difficulty_level: Optional[str] = None,
        question_type: Optional[str] = None,
        language: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[QuestionVersion]:
        stmt = select(QuestionVersion).where(QuestionVersion.is_active.is_(True))
        if topic_id:
            stmt = stmt.where(QuestionVersion.topic_id == topic_id)
        if difficulty_level:
            stmt = stmt.where(QuestionVersion.difficulty_level == difficulty_level)
        if question_type:
            stmt = stmt.where(QuestionVersion.question_type == question_type)
        if language:
            stmt = stmt.where(QuestionVersion.language == language)
        if search:
            stmt = stmt.where(QuestionVersion.question_text.ilike(f"%{search}%"))
        stmt = stmt.order_by(QuestionVersion.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_question_by_id(self, question_id: uuid.UUID) -> Optional[QuestionVersion]:
        stmt = select(QuestionVersion).where(QuestionVersion.id == question_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_question(self, question_id: uuid.UUID) -> bool:
        q = await self.get_question_by_id(question_id)
        if not q:
            return False
        q.is_active = False
        await self.session.commit()
        return True

    # Exam Templates & Question Pools
    async def get_templates(self, institute_id: uuid.UUID) -> List[ExamTemplate]:
        stmt = select(ExamTemplate).where(ExamTemplate.institute_id == institute_id).order_by(ExamTemplate.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_template_by_id(self, template_id: uuid.UUID) -> Optional[ExamTemplate]:
        stmt = select(ExamTemplate).where(ExamTemplate.id == template_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_template(self, template_id: uuid.UUID, update_fields: dict) -> Optional[ExamTemplate]:
        t = await self.get_template_by_id(template_id)
        if not t:
            return None
        for k, v in update_fields.items():
            if v is not None:
                setattr(t, k, v)
        await self.session.commit()
        await self.session.refresh(t)
        return t

    async def delete_template(self, template_id: uuid.UUID) -> bool:
        t = await self.get_template_by_id(template_id)
        if not t:
            return False
        await self.session.delete(t)
        await self.session.commit()
        return True

    async def create_pool(self, p: QuestionPool) -> QuestionPool:
        self.session.add(p)
        await self.session.commit()
        await self.session.refresh(p)
        return p

    async def get_pools(self, institute_id: uuid.UUID) -> List[QuestionPool]:
        stmt = select(QuestionPool).where(QuestionPool.institute_id == institute_id).order_by(QuestionPool.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_pool_by_id(self, pool_id: uuid.UUID) -> Optional[QuestionPool]:
        stmt = select(QuestionPool).where(QuestionPool.id == pool_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
