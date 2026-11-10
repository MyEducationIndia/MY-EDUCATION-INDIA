"""
Module 15: LXP Service Layer
"""
from app.modules.lxp.repository import LXPRepository
from app.modules.lxp.validators import LXPBusinessValidators
from app.modules.lxp.progress_engine import LearningProgressEngine
from app.modules.lxp.video_service import VideoStreamingService

class LearningExperiencePlatformService:
    def __init__(self, repo: LXPRepository):
        self.repo = repo

    async def create_new_course(self, institute_id: str, data: dict):
        if not LXPBusinessValidators.validate_course_code(data.get("course_code", "")):
            raise ValueError("Invalid course code format")
        return await self.repo.create_course(institute_id, data)

    def calculate_progress(self, total: int, completed: int) -> float:
        return LearningProgressEngine.calculate_course_progress(total, completed)

    def get_secure_video_stream(self, raw_url: str, user_id: str) -> str:
        return VideoStreamingService.generate_signed_streaming_url(raw_url, user_id)
