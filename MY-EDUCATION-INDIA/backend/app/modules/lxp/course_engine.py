"""
Module 15: Course Hierarchy Engine
"""
from typing import List, Dict

class CourseHierarchyEngine:
    @staticmethod
    def calculate_total_course_duration(modules: List[Dict]) -> int:
        total_seconds = 0
        for m in modules:
            for lesson in m.get("lessons", []):
                total_seconds += lesson.get("duration_seconds", 0)
        return total_seconds // 60 # Return in minutes

    @staticmethod
    def sequence_lessons(lessons: List[Dict]) -> List[Dict]:
        return sorted(lessons, key=lambda x: x.get("order_index", 0))
