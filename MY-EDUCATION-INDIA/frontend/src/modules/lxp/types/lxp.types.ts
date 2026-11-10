export interface LearningCourse {
  id: string;
  courseCode: string;
  courseName: string;
  description?: string;
  category: string;
  difficulty: "BEGINNER" | "INTERMEDIATE" | "ADVANCED";
  language: string;
  durationMinutes: number;
  thumbnailUrl?: string;
  bannerUrl?: string;
  instructorId: string;
  status: "DRAFT" | "PUBLISHED" | "ARCHIVED";
  visibility: "PUBLIC" | "ENROLLED_ONLY" | "PRIVATE";
  isFree: boolean;
  feeAmount: number;
}

export interface LearningModule {
  id: string;
  courseId: string;
  moduleTitle: string;
  description?: string;
  orderIndex: number;
  durationMinutes: number;
  isPublished: boolean;
  lessons?: LearningLesson[];
}

export interface LearningLesson {
  id: string;
  moduleId: string;
  lessonTitle: string;
  lessonType: "VIDEO" | "PDF" | "PRESENTATION" | "ARTICLE" | "HTML_LESSON" | "EXTERNAL_LINK" | "YOUTUBE_EMBED" | "AUDIO" | "ASSIGNMENT" | "QUIZ" | "PRACTICE_TEST" | "CBT_SESSION";
  contentBody?: string;
  videoId?: string;
  durationSeconds: number;
  orderIndex: number;
  isPreview: boolean;
  isMandatory: boolean;
}

export interface CourseEnrollment {
  id: string;
  courseId: string;
  studentId: string;
  enrollmentStatus: "ACTIVE" | "COMPLETED" | "SUSPENDED";
  progressPercentage: number;
  enrolledAt: string;
}

export interface LXPDashboardMetrics {
  totalEnrolledCourses: number;
  activeCourses: number;
  completedCourses: number;
  totalLearningHours: number;
  upcomingAssignmentsCount: number;
  averageQuizScore: number;
  xpPoints: number;
  streakDays: number;
}

export interface DiscussionTopic {
  id: string;
  courseId: string;
  lessonId?: string;
  userId: string;
  title: string;
  content: string;
  isPinned: boolean;
  isClosed: boolean;
  upvotesCount: number;
  createdAt: string;
}
