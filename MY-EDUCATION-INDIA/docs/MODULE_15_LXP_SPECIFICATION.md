# MY EDUCATION INDIA ERP V2 — MODULE 15 SPECIFICATION
## ENTERPRISE LEARNING EXPERIENCE PLATFORM (LXP)

### 1. Executive Summary & Architectural Overview
Module 15 transforms MY EDUCATION INDIA ERP V2 from a conventional administrative system into an adaptive, cloud-native **Learning Experience Platform (LXP)**. Going beyond traditional Learning Management Systems (LMS), the platform supports synchronous and asynchronous pedagogy across online, offline, and hybrid delivery modes.

The architecture emphasizes:
- **Zero Mock Policy**: Production-ready data models, business logic engines, and API endpoints.
- **Client-Side Storage Prohibition**: Strictly zero usage of `localStorage`, `sessionStorage`, or `indexedDB`. All authentication state and session telemetry reside in secure HTTP-only cookies and in-memory TanStack Query caches.
- **Full ERP Ecosystem Integration**:
  - **Module 6 (SIMS)**: Student demographics, enrolled program profiles, and batch cohorts.
  - **Module 8 (Academics)**: Academic curricula, syllabus mapping, and department alignments.
  - **Module 9 (Fee & Finance)**: Automated prerequisite fee clearance checks before allowing paid course enrollment.
  - **Module 10 (Attendance)**: Synchronized lecture attendance logging for live/hybrid sessions.
  - **Module 11 (Examinations)**: Syllabus alignment for formative homework and summative assessments.
  - **Module 12 (CBT Platform)**: Seamless embedding of CBT practice tests and topic-wise question bank drills.
  - **Module 13 (Certificates & Verification)**: Automated generation of verifiable digital course completion certificates upon reaching 100% progress.
  - **Module 14 (Library & Digital Knowledge)**: Cross-referencing eBooks, peer-reviewed journals, and study materials inside lesson resources.

---

### 2. Database Schema (17 Enterprise Relational Tables)
Provisioned via Alembic revision `0015_lxp_platform`:
1. `learning_courses`: Course metadata, codes, descriptions, difficulty ranks, duration, instructors, fee configuration, certificate linkages, and visibility flags.
2. `learning_modules`: Curriculum units, chapters, prerequisites, ordering indexes, and module durations.
3. `learning_lessons`: Multi-format lesson units (Video, PDF, Presentation, Article, HTML, Embed, Audio, Assignment, Quiz, Practice Test, CBT Session).
4. `lesson_resources`: Downloadable laboratory datasets, code files, slide decks, and version histories.
5. `video_library`: Video master ledger supporting HLS/DASH streaming URLs, multi-resolution encodes (360p to 1080p), captions, and thumbnails.
6. `course_enrollments`: Student enrollment state (Free, Paid, Batch-assigned), progress percent, and fee-clearance verification.
7. `learning_progress`: Granular lesson telemetry, watch time in seconds, last playback resume timestamp, and quiz scores.
8. `assignment_submissions`: Student submission texts, file attachments, submission timestamps, and late submission flags.
9. `assignment_feedback`: Faculty grading, rubric-based score breakdowns, and constructive feedback remarks.
10. `discussion_topics`: Course- and lesson-specific discussion threads, pinned topics, and upvote counters.
11. `discussion_posts`: Peer replies, nested commentary, code snippets, and faculty endorsements.
12. `course_announcements`: Targeted broadcasts for institute, course, batch, or individual student cohorts.
13. `bookmarks`: Student personal bookmarks, timestamp-anchored video notes, and revision flags.
14. `learning_badges`: Gamification definitions, criteria types, badge icons, and XP reward values.
15. `learning_achievements`: Student earned badges, award timestamps, and accumulated XP tallies.
16. `learning_reports`: Saved audit snapshots, batch-wise gradebooks, and learner compliance records.
17. `learning_analytics`: Daily telemetry on active learners, average watch minutes, completion velocity, and discussion volume.

---

### 3. Business Logic Engines
- **Course Hierarchy Engine (`course_engine.py`)**:
  - Dynamically calculates total course duration from module lessons.
  - Enforces prerequisite sequencing and order index normalization.
- **Learning Progress & Gamification Engine (`progress_engine.py`)**:
  - Course Progress Formula:
    $$Progress\% = \left(rac{	ext{Completed Mandatory Lessons}}{	ext{Total Mandatory Lessons}}ight) 	imes 100$$
  - Awards XP points for lesson completions (+10 XP), assignment submissions (+25 XP), perfect quizzes (+50 XP), and course completions (+200 XP).
  - Automatically triggers Module 13 certificate issuance eligibility when progress reaches 100%.
- **Video Streaming & Telemetry Service (`video_service.py`)**:
  - Generates secure, time-limited signed streaming URLs with HMAC SHA-256 tokens.
  - Computes watch-time ratios to mark lessons as completed once 90% watch ratio is achieved.
- **Assignment & Rubric Engine (`assignment_engine.py`)**:
  - Detects late submissions against due dates and calculates adjusted grades based on late penalty rules.
  - Computes weighted rubric totals across custom evaluation criteria.

---

### 4. Frontend & Navigation Structure
- **Path**: `frontend/src/modules/lxp/`
- **15 Submodules Delivered**:
  - `dashboard/LearningDashboardPage.tsx`: Student & Instructor overview (My Courses, Streaks, XP Leaderboard, Study Time).
  - `courses/CoursesCatalogPage.tsx`: Searchable public and enrolled course catalog.
  - `course-builder/CourseBuilderPage.tsx`: Course creation studio with curriculum tree builder.
  - `modules/CourseModulesPage.tsx`: Module organization, sequencing, and prerequisite mapping.
  - `lessons/LessonViewerPage.tsx`: Interactive multi-format lesson viewer with video player and notes.
  - `videos/VideoLibraryPage.tsx`: Transcoding queue and video asset management.
  - `assignments/AssignmentsHubPage.tsx`: Submission portal and rubric evaluation terminal.
  - `practice/PracticeTestsHubPage.tsx`: CBT question bank practice tests and instant solution reviews.
  - `forum/DiscussionForumPage.tsx`: Peer discussion threads, upvoting, and instructor endorsements.
  - `progress/StudentProgressPage.tsx`: Visual progress telemetry, learning streaks, and certificates.
  - `reports/LXPReportsPage.tsx`: Batch progress exports, gradebooks, and audit trails.
  - `analytics/LXPAnalyticsPage.tsx`: Retention curves, drop-off analysis, and faculty performance.
  - `settings/LXPSettingsPage.tsx`: Gamification XP rules, video CDN parameters, and access controls.
  - `types/lxp.types.ts` & `services/lxpService.ts`: TypeScript contracts and HTTP API client.
- **Routing**: Mounted under `/admin/lxp/*` in `AppRoutes.tsx` with sidebar navigation under `GraduationCap` icon.

---

### 5. Verification & Testing
- Unit test suite `tests/unit/test_module15_backend_lxp.py` executed with 100% pass rate:
  - Clean AST syntax across all 13 Python source files in `backend/app/modules/lxp/`.
  - Pydantic schema serialization for courses, modules, lessons, and enrollments.
  - Course code format regex validation and lesson type white-listing.
  - Course Hierarchy Engine total duration computation.
  - Progress Engine percentage calculations and certificate eligibility thresholds.
  - Video Streaming Service signed token generation and watch ratio algorithms.
  - Assignment Engine late submission penalty factor computation and rubric grading.
  - Zero browser storage audit: 0 instances of `localStorage`, `sessionStorage`, or `indexedDB` found.
