"""
Re-export AcademicSession from app.modules.examinations.models to avoid duplicate table definition.
"""
from app.modules.examinations.models import AcademicSession  # noqa: F401
