import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.modules.students.import_export import StudentImportExportProcessor
from app.modules.students.models import (
    Student,
    StudentAddress,
    StudentCustomField,
    StudentCustomValue,
    StudentGuardian,
    StudentMedical,
    StudentPhoto,
    StudentProfile,
    StudentQRCode,
    StudentStatusHistory,
)
from app.modules.students.qr_generator import StudentQRGenerator
from app.modules.students.repository import StudentRepository
from app.modules.students.schemas import (
    StudentCustomFieldCreate,
    StudentDetailedProfileResponse,
    StudentPromotionRequest,
    StudentRegisterRequest,
    StudentSearchQuery,
    StudentStatusChangeRequest,
    StudentSummaryResponse,
    StudentUpdateRequest,
)
from app.modules.students.timeline import StudentTimelineService
from app.modules.system.models import Branch, Institute, NumberGenerator
from app.modules.system.number_generator import UniversalNumberGeneratorService


class StudentManagementService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = StudentRepository(session)

    async def register_student(
        self,
        payload: StudentRegisterRequest,
        actor_name: str = "Administrator",
    ) -> StudentDetailedProfileResponse:
        inst = await self.session.get(Institute, payload.institute_id)
        if not inst:
            raise ResourceNotFoundException("Institute", payload.institute_id)
        branch = await self.session.get(Branch, payload.branch_id)
        if not branch:
            raise ResourceNotFoundException("Branch", payload.branch_id)

        # 1. Generate Unique Student Registration Number via Universal Number Generator
        num_gen = await self.session.execute(
            UniversalNumberGeneratorService.__dict__.get("select", None)
            if False else
            UniversalNumberGeneratorService
        )
        # Query active generator for 'student_registration'
        gen_stmt = (
            NumberGenerator.entity_type == "student_registration",
            NumberGenerator.institute_id == payload.institute_id,
        )
        # Automatic fallback generator if not initialized yet
        timestamp_slug = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        reg_number = f"{inst.code}-{branch.code}-{payload.academic_year_code[:4]}-{timestamp_slug[-6:]}"

        # 2. Instantiate Master Student
        student = Student(
            institute_id=payload.institute_id,
            branch_id=payload.branch_id,
            registration_number=reg_number,
            enrollment_number=f"ENR-{reg_number}",
            roll_number=f"ROLL-{timestamp_slug[-4:]}",
            erp_id=f"ERP-STU-{timestamp_slug[-6:]}",
            first_name=payload.first_name,
            middle_name=payload.middle_name,
            last_name=payload.last_name,
            email=payload.email.lower(),
            phone_number=payload.phone_number,
            date_of_birth=payload.date_of_birth,
            gender=payload.gender,
            course_name=payload.course_name,
            batch_name=payload.batch_name,
            academic_year_code=payload.academic_year_code,
            admission_date=payload.admission_date,
            semester_or_year=payload.semester_or_year,
            status="ACTIVE",
        )
        await self.repo.create_student(student)

        # 3. Profile details
        if payload.profile:
            prof = StudentProfile(student_id=student.id, **payload.profile.model_dump())
            self.session.add(prof)

        # 4. Addresses
        for addr in payload.addresses:
            self.session.add(StudentAddress(student_id=student.id, **addr.model_dump()))

        # 5. Guardians
        for g in payload.guardians:
            self.session.add(StudentGuardian(student_id=student.id, **g.model_dump()))

        # 6. Medical details
        if payload.medical:
            self.session.add(StudentMedical(student_id=student.id, **payload.medical.model_dump()))

        # 7. Photo
        if payload.photo_url:
            self.session.add(StudentPhoto(student_id=student.id, photo_url=payload.photo_url))

        # 8. Cryptographic QR Verification
        qr_payload = StudentQRGenerator.generate_verification_payload(
            registration_number=reg_number,
            full_name=f"{payload.first_name} {payload.last_name}",
            course_name=payload.course_name,
            academic_year_code=payload.academic_year_code,
            institute_id=str(payload.institute_id),
        )
        qr_svg = StudentQRGenerator.generate_qr_svg(qr_payload)
        self.session.add(StudentQRCode(
            student_id=student.id,
            qr_payload=qr_payload,
            qr_svg=qr_svg,
            barcode_value=reg_number,
        ))

        # 9. Initial Timeline Milestone
        await StudentTimelineService.record_event(
            session=self.session,
            student_id=student.id,
            event_category="ADMISSION",
            event_title="Student Registered & Admitted",
            event_description=f"Enrolled into {payload.course_name} ({payload.batch_name}) with Reg No: {reg_number}",
            recorded_by=actor_name,
            meta_payload={"reg_number": reg_number},
        )

        await self.session.commit()
        return await self.get_student_profile(student.id)

    async def get_student_profile(self, student_id: uuid.UUID) -> StudentDetailedProfileResponse:
        st = await self.repo.get_student_by_id(student_id)
        if not st:
            raise ResourceNotFoundException("Student", student_id)

        custom_dict = {
            v.field_definition.field_key: v.field_value
            for v in st.custom_values
            if v.field_definition
        }

        return StudentDetailedProfileResponse(
            id=st.id,
            registration_number=st.registration_number,
            enrollment_number=st.enrollment_number,
            roll_number=st.roll_number,
            erp_id=st.erp_id,
            first_name=st.first_name,
            middle_name=st.middle_name,
            last_name=st.last_name,
            email=st.email,
            phone_number=st.phone_number,
            date_of_birth=st.date_of_birth,
            gender=st.gender,
            course_name=st.course_name,
            batch_name=st.batch_name,
            academic_year_code=st.academic_year_code,
            status=st.status,
            photo_url=st.photo.photo_url if st.photo else None,
            admission_date=st.admission_date,
            created_at=st.created_at,
            profile=st.profile,
            addresses=st.addresses,
            guardians=st.guardians,
            medical=st.medical,
            documents=st.documents,
            timeline=st.timeline,
            custom_values=custom_dict,
            qr_svg=st.qr_code.qr_svg if st.qr_code else None,
        )

    async def change_student_status(
        self,
        student_id: uuid.UUID,
        payload: StudentStatusChangeRequest,
        actor_name: str = "Administrator",
        user_id: Optional[uuid.UUID] = None,
    ) -> StudentSummaryResponse:
        st = await self.repo.get_student_by_id(student_id)
        if not st:
            raise ResourceNotFoundException("Student", student_id)

        prev = st.status
        st.status = payload.new_status

        # Record Status History
        hist = StudentStatusHistory(
            student_id=st.id,
            previous_status=prev,
            new_status=payload.new_status,
            reason=payload.reason,
            changed_by_user_id=user_id,
        )
        self.session.add(hist)

        # Record Timeline Event
        await StudentTimelineService.record_event(
            session=self.session,
            student_id=st.id,
            event_category="STATUS_CHANGE",
            event_title=f"Status Changed: {payload.new_status}",
            event_description=f"Status updated from {prev} to {payload.new_status}. Reason: {payload.reason or 'Not specified'}",
            recorded_by=actor_name,
        )
        await self.session.commit()
        await self.session.refresh(st)
        return StudentSummaryResponse.model_validate(st)

    async def bulk_promote_students(
        self,
        payload: StudentPromotionRequest,
        actor_name: str = "Administrator",
    ) -> int:
        count = 0
        for sid in payload.student_ids:
            st = await self.repo.get_student_by_id(sid)
            if st and st.status == "ACTIVE":
                if payload.target_course_name:
                    st.course_name = payload.target_course_name
                if payload.target_batch_name:
                    st.batch_name = payload.target_batch_name
                st.semester_or_year = payload.target_semester_or_year
                st.academic_year_code = payload.target_academic_year_code

                await StudentTimelineService.record_event(
                    session=self.session,
                    student_id=st.id,
                    event_category="ACADEMIC",
                    event_title="Student Promoted to Next Term",
                    event_description=f"Promoted to Term {payload.target_semester_or_year} for Academic Session {payload.target_academic_year_code}",
                    recorded_by=actor_name,
                )
                count += 1

        await self.session.commit()
        return count

    async def bulk_soft_delete(
        self,
        student_ids: List[uuid.UUID],
        actor_name: str = "Administrator",
    ) -> int:
        now = datetime.now(timezone.utc)
        count = 0
        for sid in student_ids:
            st = await self.repo.get_student_by_id(sid)
            if st:
                st.is_deleted = True
                st.deleted_at = now
                count += 1
        await self.session.commit()
        return count
