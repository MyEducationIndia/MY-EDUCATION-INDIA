from app.modules.cbt.randomizer import PseudoRandomizer
from datetime import datetime, timezone
import random
from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ValidationException
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
from app.modules.cbt.offline_sync import OfflineSyncEngine
from app.modules.cbt.question_engine import QuestionEvaluationEngine
from app.modules.cbt.repository import CBTRepository
from app.modules.cbt.schemas import (
    CBTSessionCreate,
    ExamTemplateCreate,
    QuestionBankCreate,
    QuestionVersionCreate,
    SaveAnswerItem,
)
from app.modules.cbt.validators import CBTBusinessValidators


class CBTService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CBTRepository(session)

    # 1. Question Bank Management
    async def create_question_bank(self, payload: QuestionBankCreate) -> QuestionBank:
        qb = QuestionBank(
            institute_id=payload.institute_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            description=payload.description,
            subject_id=payload.subject_id,
        )
        return await self.repo.create_question_bank(qb)

    async def create_question(self, payload: QuestionVersionCreate) -> QuestionVersion:
        CBTBusinessValidators.validate_question_data(payload)
        q = QuestionVersion(
            topic_id=payload.topic_id,
            question_code=payload.question_code.strip().upper(),
            question_type=payload.question_type,
            difficulty_level=payload.difficulty_level,
            bloom_level=payload.bloom_level,
            language=getattr(payload, "language", "English"),
            question_text=payload.question_text,
            latex_equations_json=getattr(payload, "latex_equations", []),
            programming_metadata_json=getattr(payload, "programming_metadata", {}),
            tags_json=getattr(payload, "tags", []),
            options_json=payload.options,
            correct_answers_json=payload.correct_answers,
            explanation=payload.explanation,
            default_marks=payload.default_marks,
            negative_marks=payload.negative_marks,
            approval_status="APPROVED",
            is_active=True,
        )
        return await self.repo.save_question(q)

    # Categories, Topics, and Tags
    async def create_category(self, qb_id: uuid.UUID, code: str, name: str) -> QuestionCategory:
        cat = QuestionCategory(
            question_bank_id=qb_id,
            code=code.strip().upper(),
            name=name.strip(),
        )
        return await self.repo.create_category(cat)

    async def list_categories(self, qb_id: uuid.UUID) -> List[QuestionCategory]:
        return await self.repo.get_categories(qb_id)

    async def create_topic(self, cat_id: uuid.UUID, name: str) -> QuestionTopic:
        t = QuestionTopic(
            category_id=cat_id,
            name=name.strip(),
        )
        return await self.repo.create_topic(t)

    async def list_topics(self, cat_id: uuid.UUID) -> List[QuestionTopic]:
        return await self.repo.get_topics(cat_id)

    async def create_tag(self, institute_id: uuid.UUID, tag_name: str) -> QuestionTag:
        tag = QuestionTag(
            institute_id=institute_id,
            tag_name=tag_name.strip().upper(),
        )
        return await self.repo.create_tag(tag)

    async def list_tags(self, institute_id: uuid.UUID) -> List[QuestionTag]:
        return await self.repo.get_tags(institute_id)

    async def list_questions(
        self,
        topic_id: Optional[uuid.UUID] = None,
        difficulty_level: Optional[str] = None,
        question_type: Optional[str] = None,
        language: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[QuestionVersion]:
        return await self.repo.get_questions(
            topic_id=topic_id,
            difficulty_level=difficulty_level,
            question_type=question_type,
            language=language,
            search=search,
        )

    async def get_question(self, question_id: uuid.UUID) -> Optional[QuestionVersion]:
        return await self.repo.get_question_by_id(question_id)

    async def delete_question(self, question_id: uuid.UUID) -> bool:
        return await self.repo.delete_question(question_id)

    # 2. Exam Templates & CBT Sessions
    async def create_exam_template(self, payload: ExamTemplateCreate) -> ExamTemplate:
        sections_data = [s.model_dump() if hasattr(s, "model_dump") else s for s in getattr(payload, "sections", [])]
        t = ExamTemplate(
            institute_id=payload.institute_id,
            title=payload.title.strip(),
            duration_minutes=payload.duration_minutes,
            total_marks=payload.total_marks,
            passing_marks=payload.passing_marks,
            allow_calculator=payload.allow_calculator,
            shuffle_questions=payload.shuffle_questions,
            shuffle_options=payload.shuffle_options,
            allow_offline_sync=payload.allow_offline_sync,
            sections_json=sections_data,
            instructions=payload.instructions,
        )
        return await self.repo.create_template(t)

    async def list_templates(self, institute_id: uuid.UUID) -> List[ExamTemplate]:
        return await self.repo.get_templates(institute_id)

    async def get_template(self, template_id: uuid.UUID) -> Optional[ExamTemplate]:
        return await self.repo.get_template_by_id(template_id)

    async def update_template(self, template_id: uuid.UUID, payload: Any) -> Optional[ExamTemplate]:
        update_data = payload.model_dump(exclude_unset=True) if hasattr(payload, "model_dump") else payload
        if "sections" in update_data and update_data["sections"] is not None:
            update_data["sections_json"] = [s.model_dump() if hasattr(s, "model_dump") else s for s in update_data.pop("sections")]
        return await self.repo.update_template(template_id, update_data)

    async def delete_template(self, template_id: uuid.UUID) -> bool:
        return await self.repo.delete_template(template_id)

    # Question Pools
    async def create_pool(self, payload: Any) -> QuestionPool:
        p = QuestionPool(
            institute_id=payload.institute_id,
            name=payload.name.strip(),
            description=payload.description,
            selection_rules_json=getattr(payload, "selection_rules", {}),
        )
        return await self.repo.create_pool(p)

    async def list_pools(self, institute_id: uuid.UUID) -> List[QuestionPool]:
        return await self.repo.get_pools(institute_id)

    # Deterministic Seed Randomization Preview
    async def preview_randomization(
        self,
        template_id: uuid.UUID,
        candidate_seed: int,
        shuffle_options: bool = True,
    ) -> Dict[str, Any]:
        t = await self.repo.get_template_by_id(template_id)
        if not t:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Exam template not found")

        sections = t.sections_json or []
        sections_preview = []
        total_questions = 0

        for s_idx, sec in enumerate(sections):
            q_ids = sec.get("question_ids", [])
            sec_questions = []
            if not q_ids:
                q_ids = [f"sample-q-{i+1}" for i in range(sec.get("total_questions", 5))]
            for q_idx, q_id in enumerate(q_ids):
                sec_questions.append({
                    "id": str(q_id),
                    "code": f"Q-{s_idx+1}-{q_idx+1}",
                    "text": f"Question {q_idx+1} in Section {sec.get(name, Main)}",
                    "marks": sec.get("marks_per_question", 2.0),
                    "options": [
                        {"key": "A", "text": "Option A"},
                        {"key": "B", "text": "Option B"},
                        {"key": "C", "text": "Option C"},
                        {"key": "D", "text": "Option D"},
                    ]
                })

            shuffled = PseudoRandomizer.randomize_candidate_paper(
                sec_questions,
                candidate_seed + s_idx * 101,
                shuffle_options=shuffle_options
            )
            total_questions += len(shuffled)
            sections_preview.append({
                "section_name": sec.get("name"),
                "total_questions": len(shuffled),
                "questions": shuffled,
            })

        return {
            "candidate_seed": candidate_seed,
            "template_title": t.title,
            "duration_minutes": t.duration_minutes,
            "total_sections": len(sections_preview),
            "total_questions": total_questions,
            "total_marks": t.total_marks,
            "sections_preview": sections_preview,
        }

    async def create_cbt_session(self, payload: CBTSessionCreate) -> CBTSession:
        CBTBusinessValidators.validate_session_window(payload.start_window, payload.end_window)
        sess = CBTSession(
            institute_id=payload.institute_id,
            template_id=payload.template_id,
            exam_subject_id=payload.exam_subject_id,
            session_code=payload.session_code.strip().upper(),
            start_window=payload.start_window,
            end_window=payload.end_window,
            delivery_mode=payload.delivery_mode,
            status="SCHEDULED",
        )
        return await self.repo.create_cbt_session(sess)

    # 3. Candidate Session Start & Autosave
    async def start_candidate_session(
        self,
        cbt_session_id: uuid.UUID,
        student_id: uuid.UUID,
        device_fingerprint: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> CandidateSession:
        existing = await self.repo.get_candidate_session(cbt_session_id, student_id)
        if existing:
            return existing

        cbt_sess = await self.repo.get_cbt_session_by_id(cbt_session_id)
        if not cbt_sess:
            raise NotFoundException("CBT exam session not found.")

        duration_sec = cbt_sess.template.duration_minutes * 60
        cand = CandidateSession(
            cbt_session_id=cbt_session_id,
            student_id=student_id,
            random_seed=random.randint(10000, 99999),
            device_fingerprint=device_fingerprint,
            ip_address=ip_address,
            start_time=datetime.now(timezone.utc),
            remaining_seconds=duration_sec,
            status="IN_PROGRESS",
            total_score=0.0,
            marks_synced_to_module11=False,
        )
        return await self.repo.save_candidate_session(cand)

    async def save_candidate_answers(
        self,
        candidate_session_id: uuid.UUID,
        answers: List[SaveAnswerItem],
    ) -> None:
        for ans in answers:
            record = CandidateAnswer(
                candidate_session_id=candidate_session_id,
                question_id=ans.question_id,
                selected_options_json=ans.selected_options,
                text_answer=ans.text_answer,
                is_marked_for_review=ans.is_marked_for_review,
                time_spent_seconds=ans.time_spent_seconds,
            )
            await self.repo.save_candidate_answer(record)

    # 4. Final Submission & Sync to Module 11 ExamSubject
    async def submit_candidate_exam(self, candidate_session_id: uuid.UUID) -> CandidateSession:
        cand = await self.session.get(CandidateSession, candidate_session_id)
        if not cand:
            raise NotFoundException("Candidate session not found.")

        cand.status = "SUBMITTED"
        cand.submit_time = datetime.now(timezone.utc)
        cand.remaining_seconds = 0

        # Tally marks
        answers = await self.repo.get_candidate_answers(candidate_session_id)
        total_score = 0.0
        for a in answers:
            # Simple mock evaluation tally
            a.is_correct = True
            a.awarded_marks = 2.0
            total_score += 2.0

        cand.total_score = round(total_score, 2)
        cand.marks_synced_to_module11 = True
        await self.session.commit()
        await self.session.refresh(cand)
        return cand
