from datetime import date
from typing import Any, Dict, List
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.attendance.models import AttendanceSession, StudentAttendance


class AttendanceReportEngine:
    @staticmethod
    async def get_daily_attendance_summary(
        session: AsyncSession,
        institute_id: uuid.UUID,
        target_date: date,
    ) -> Dict[str, Any]:
        stmt = (
            select(
                StudentAttendance.status,
                func.count(StudentAttendance.id),
            )
            .join(AttendanceSession, StudentAttendance.session_id == AttendanceSession.id)
            .where(
                AttendanceSession.institute_id == institute_id,
                AttendanceSession.session_date == target_date,
            )
            .group_by(StudentAttendance.status)
        )
        res = await session.execute(stmt)
        rows = res.all()

        counts = {status: count for status, count in rows}
        total = sum(counts.values())
        present = counts.get("PRESENT", 0) + counts.get("LATE", 0) + counts.get("ON_DUTY", 0)
        pct = (present / total * 100.0) if total > 0 else 0.0

        return {
            "date": str(target_date),
            "institute_id": str(institute_id),
            "total_records": total,
            "present_count": present,
            "absent_count": counts.get("ABSENT", 0),
            "leave_count": counts.get("LEAVE", 0),
            "attendance_percentage": round(pct, 2),
            "status_breakdown": counts,
        }
