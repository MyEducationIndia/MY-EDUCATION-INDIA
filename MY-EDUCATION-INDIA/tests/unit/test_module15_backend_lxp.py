import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import ast
import re
from datetime import datetime, timedelta

from app.modules.lxp.schemas import (
    LearningCourseCreate,
    LearningModuleCreate,
    LearningLessonCreate,
    CourseEnrollmentRequest,
    LessonProgressUpdate
)
from app.modules.lxp.validators import LXPBusinessValidators
from app.modules.lxp.course_engine import CourseHierarchyEngine
from app.modules.lxp.progress_engine import LearningProgressEngine
from app.modules.lxp.video_service import VideoStreamingService
from app.modules.lxp.assignment_engine import AssignmentEngine

class TestModule15LXPBackend(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.lxp_backend_dir = os.path.join(self.base_dir, "backend/app/modules/lxp")
        self.lxp_frontend_dir = os.path.join(self.base_dir, "frontend/src/modules/lxp")

    def test_lxp_models_and_modules_ast(self):
        """Verify all Module 15 Python source files compile cleanly without syntax errors."""
        self.assertTrue(os.path.exists(self.lxp_backend_dir), "LXP backend directory missing")
        py_files = [f for f in os.listdir(self.lxp_backend_dir) if f.endswith(".py")]
        self.assertGreaterEqual(len(py_files), 12, "Expected at least 12 Python files in LXP module")
        for py_file in py_files:
            file_path = os.path.join(self.lxp_backend_dir, py_file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                ast.parse(content, filename=py_file)
            except SyntaxError as e:
                self.fail(f"SyntaxError in {py_file}: {e}")

    def test_lxp_schemas(self):
        """Test Pydantic schemas for course, module, and lesson creation."""
        course = LearningCourseCreate(
            course_code="CS-301",
            course_name="Distributed Systems & Cloud Architecture",
            category="Computer Science",
            difficulty="ADVANCED",
            instructor_id="usr_inst_01",
            duration_minutes=2400,
            is_free=True
        )
        self.assertEqual(course.course_code, "CS-301")
        self.assertEqual(course.difficulty, "ADVANCED")

        module = LearningModuleCreate(
            course_id="crs_123",
            module_title="Module 1: Consensus Protocols",
            order_index=1,
            duration_minutes=180
        )
        self.assertEqual(module.order_index, 1)

        lesson = LearningLessonCreate(
            module_id="mod_123",
            lesson_title="Raft Algorithm Deep Dive",
            lesson_type="VIDEO",
            duration_seconds=1800,
            order_index=1
        )
        self.assertEqual(lesson.lesson_type, "VIDEO")

    def test_lxp_business_validators(self):
        """Test course code, lesson type, and enrollment eligibility validators."""
        self.assertTrue(LXPBusinessValidators.validate_course_code("CS-101"))
        self.assertTrue(LXPBusinessValidators.validate_course_code("MATH_202"))
        self.assertFalse(LXPBusinessValidators.validate_course_code("c"))
        self.assertFalse(LXPBusinessValidators.validate_course_code("invalid space code"))

        self.assertTrue(LXPBusinessValidators.validate_lesson_type("VIDEO"))
        self.assertTrue(LXPBusinessValidators.validate_lesson_type("CBT_SESSION"))
        self.assertTrue(LXPBusinessValidators.validate_lesson_type("ASSIGNMENT"))
        self.assertFalse(LXPBusinessValidators.validate_lesson_type("UNKNOWN_TYPE"))

        # Enrollment eligibility
        self.assertTrue(LXPBusinessValidators.validate_enrollment_eligibility(is_free=True, fee_cleared=False))
        self.assertTrue(LXPBusinessValidators.validate_enrollment_eligibility(is_free=False, fee_cleared=True))
        self.assertFalse(LXPBusinessValidators.validate_enrollment_eligibility(is_free=False, fee_cleared=False))

    def test_course_engine(self):
        """Test total duration and lesson sequencing in course hierarchy."""
        modules = [
            {
                "module_title": "M1",
                "lessons": [
                    {"duration_seconds": 600, "order_index": 2},
                    {"duration_seconds": 1200, "order_index": 1}
                ]
            },
            {
                "module_title": "M2",
                "lessons": [
                    {"duration_seconds": 1800, "order_index": 1}
                ]
            }
        ]
        total_mins = CourseHierarchyEngine.calculate_total_course_duration(modules)
        self.assertEqual(total_mins, 60) # (600+1200+1800) / 60 = 60 minutes

        sequenced = CourseHierarchyEngine.sequence_lessons(modules[0]["lessons"])
        self.assertEqual(sequenced[0]["order_index"], 1)
        self.assertEqual(sequenced[1]["order_index"], 2)

    def test_progress_engine(self):
        """Test progress calculation, XP rewards, and certificate eligibility."""
        progress = LearningProgressEngine.calculate_course_progress(10, 7)
        self.assertEqual(progress, 70.0)

        progress_complete = LearningProgressEngine.calculate_course_progress(10, 10)
        self.assertEqual(progress_complete, 100.0)

        # Certificate eligibility
        self.assertTrue(LearningProgressEngine.check_certificate_eligibility(100.0))
        self.assertFalse(LearningProgressEngine.check_certificate_eligibility(99.0))

        # XP calculation
        xp = LearningProgressEngine.calculate_xp_earned("COURSE_COMPLETED", 100)
        self.assertEqual(xp, 300)

    def test_video_service(self):
        """Test signed URL generation and watch ratio calculation."""
        raw_url = "https://cdn.myeducation.in/videos/cs101_m1.m3u8"
        signed = VideoStreamingService.generate_signed_streaming_url(raw_url, "std_42", ttl_seconds=1800)
        self.assertTrue(signed.startswith(raw_url))
        self.assertIn("token=", signed)
        self.assertIn("expires=", signed)

        ratio = VideoStreamingService.calculate_watch_ratio(900, 1800)
        self.assertEqual(ratio, 50.0)

    def test_assignment_engine(self):
        """Test assignment late submission rules and rubric scoring."""
        due = datetime(2026, 11, 10, 23, 59, 59)
        on_time = datetime(2026, 11, 10, 20, 0, 0)
        late = datetime(2026, 11, 11, 10, 0, 0)

        res_on_time = AssignmentEngine.evaluate_late_submission(on_time, due)
        self.assertFalse(res_on_time["is_late"])
        self.assertEqual(res_on_time["penalty_factor"], 1.0)

        res_late = AssignmentEngine.evaluate_late_submission(late, due, late_penalty_percent=15.0)
        self.assertTrue(res_late["is_late"])
        self.assertEqual(res_late["penalty_factor"], 0.85)

        # Rubric scoring
        rubric = {"clarity": 25.0, "accuracy": 40.0, "code_quality": 30.0}
        total = AssignmentEngine.compute_rubric_grade(rubric, max_marks=100.0)
        self.assertEqual(total, 95.0)

    def test_zero_browser_storage_lxp(self):
        """Strictly enforce zero usage of localStorage, sessionStorage, or indexedDB in frontend."""
        storage_pattern = re.compile(r'\b(localStorage|sessionStorage|indexedDB)\b')
        violations = []
        for root, _, files in os.walk(self.lxp_frontend_dir):
            for file in files:
                if file.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        for line_idx, line in enumerate(f, 1):
                            if storage_pattern.search(line):
                                violations.append(f"{file}:{line_idx}")
        self.assertEqual(violations, [], f"Found forbidden browser storage usage: {violations}")

if __name__ == "__main__":
    unittest.main()
