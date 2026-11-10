from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.modules.admissions.models import (
    AdmissionFeeReceipt,
    AdmissionTimeline,
    Application,
    ApplicationDocument,
    SeatManagement,
)
from app.modules.students.models import Student
from app.modules.students.schemas import StudentRegisterRequest
from app.modules.students.service import StudentManagementService


class AdmissionWorkflowEngine:
    """Handles complete admission lifecycle and converts approved applications into SIMS students."""

    @staticmethod
    async def record_timeline(
        session: AsyncSession,
        application_id: uuid.UUID,
        stage: str,
        title: str,
        description: str,
        actor_name: str = "System",
        metadata_payload: Optional[Dict[str, Any]] = None,
    ) -> AdmissionTimeline:
        timeline_entry = AdmissionTimeline(
            application_id=application_id,
            stage=stage.upper(),
            title=title,
            description=description,
            actor_name=actor_name,
            occurred_at=datetime.now(timezone.utc),
            metadata_payload=metadata_payload or {},
        )
        session.add(timeline_entry)
        await session.flush()
        return timeline_entry

    @staticmethod
    async def convert_application_to_student(
        session: AsyncSession,
        application: Application,
        allocated_batch: str,
        actor_name: str = "Admission Committee",
    ) -> Student:
        if application.student_id:
            raise ConflictException(f"Application {application.application_number} has already been converted to a student.")

        # Instantiate Student Registration Request for Module 6 SIMS
        sims_service = StudentManagementService(session)
        register_payload = StudentRegisterRequest(
            institute_id=application.institute_id,
            branch_id=application.branch_id,
            first_name=application.first_name,
            middle_name=application.middle_name,
            last_name=application.last_name,
            email=application.email,
            phone_number=application.phone_number,
            date_of_birth=application.date_of_birth,
            gender=application.gender,
            course_name=application.course_name,
            batch_name=allocated_batch,
            academic_year_code=application.academic_year_code,
            admission_date=datetime.now(timezone.utc).date(),
            semester_or_year=1,
            profile={
                "caste_category": application.category,
                "previous_school": application.previous_institution,
                "previous_marks_percentage": application.previous_marks_percentage,
            },
            addresses=[
                {
                    "address_type": "PERMANENT",
                    "address_line1": application.address_line1,
                    "city": application.city,
                    "district": application.city,
                    "state": application.state,
                    "postal_code": application.postal_code,
                    "country": "India",
                    "is_primary": True,
                }
            ],
            guardians=[
                {
                    "relationship_type": application.guardian_relation,
                    "full_name": application.guardian_name,
                    "mobile_number": application.guardian_phone,
                    "is_emergency_contact": True,
                }
            ],
            custom_fields={"converted_from_app": application.application_number},
        )

        student_profile = await sims_service.register_student(register_payload, actor_name=actor_name)
        student_id = student_profile.id

        # Update application state
        application.student_id = student_id
        application.status = "CONVERTED"
        application.is_locked = True
        application.approved_at = datetime.now(timezone.utc)

        await AdmissionWorkflowEngine.record_timeline(
            session=session,
            application_id=application.id,
            stage="SIMS_CONVERSION",
            title="Application Converted to Student",
            description=f"Master Student Record created in SIMS (Reg No: {student_profile.registration_number}) in batch {allocated_batch}.",
            actor_name=actor_name,
            metadata_payload={"registration_number": student_profile.registration_number, "student_id": str(student_id)},
        )

        await session.commit()
        created_student = await session.get(Student, student_id)
        return created_student
