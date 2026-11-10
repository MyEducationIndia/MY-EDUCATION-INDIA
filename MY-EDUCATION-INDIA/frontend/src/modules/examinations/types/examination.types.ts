export interface ExamType {
  id: string;
  institute_id: string;
  code: string;
  name: string;
  category: "INTERNAL" | "EXTERNAL" | "CONTINUOUS_EVALUATION";
  default_weightage_pct: number;
  is_active: boolean;
  created_at: string;
}

export interface ExamSession {
  id: string;
  institute_id: string;
  branch_id?: string;
  academic_year_id: string;
  code: string;
  name: string;
  start_date: string;
  end_date: string;
  status: "SCHEDULED" | "ONGOING" | "COMPLETED" | "RESULTS_PUBLISHED";
  min_attendance_threshold_pct: number;
  requires_fee_clearance: boolean;
  created_at: string;
}

export interface ExamSchedule {
  id: string;
  exam_session_id: string;
  course_id: string;
  semester_id?: string;
  batch_id?: string;
  exam_date: string;
  start_time: string;
  end_time: string;
  created_at: string;
}

export interface ExamSubject {
  id: string;
  schedule_id: string;
  subject_id: string;
  exam_type_id: string;
  max_marks: number;
  pass_marks: number;
  credits: number;
  weightage_internal_pct: number;
  weightage_external_pct: number;
}

export interface HallTicket {
  id: string;
  hall_ticket_number: string;
  schedule_id: string;
  student_id: string;
  seat_number: string;
  qr_verification_token: string;
  barcode_data: string;
  is_eligible: boolean;
  status: "ISSUED" | "WITHHELD" | "CANCELLED";
  created_at: string;
}

export interface MarkEntry {
  id: string;
  exam_subject_id: string;
  student_id: string;
  internal_marks: number;
  external_marks: number;
  practical_marks: number;
  grace_marks: number;
  moderation_adjustment: number;
  total_marks_obtained: number;
  is_absent: boolean;
  is_locked: boolean;
  updated_at: string;
}

export interface Result {
  id: string;
  exam_session_id: string;
  student_id: string;
  total_credits_registered: number;
  total_credits_earned: number;
  total_marks_obtained: number;
  total_max_marks: number;
  percentage: number;
  sgpa: number;
  cgpa: number;
  classification: string;
  status: "PASSED" | "FAILED" | "PROMOTED_WITH_BACKLOG" | "DETAINED";
  backlog_count: number;
  rank_in_batch?: number;
  is_published: boolean;
}

export interface Transcript {
  id: string;
  transcript_number: string;
  student_id: string;
  transcript_type: string;
  final_cgpa: number;
  digital_signature_hash: string;
  issued_date: string;
}

export interface ExamDashboardSummary {
  active_exam_sessions_count: number;
  scheduled_papers_count: number;
  total_students_enrolled: number;
  hall_tickets_generated_count: number;
  results_published_count: number;
  overall_pass_percentage: number;
  grade_distribution: Record<string, number>;
  top_performers: Array<{ name: string; roll: string; cgpa: number; rank: number }>;
}
