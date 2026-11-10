export interface QuestionBank {
  id: string;
  institute_id: string;
  code: string;
  name: string;
  description?: string;
  subject_id?: string;
  is_active: boolean;
  created_at: string;
}

export interface QuestionVersion {
  id: string;
  question_code: string;
  question_type: "MCQ" | "MSQ" | "TRUE_FALSE" | "NUMERICAL" | "FILL_BLANKS" | "ESSAY";
  difficulty_level: "EASY" | "MEDIUM" | "HARD" | "EXPERT";
  bloom_level: string;
  question_text: string;
  options_json: Array<{ id: string; text: string }>;
  correct_answers_json: string[];
  explanation?: string;
  default_marks: number;
  negative_marks: number;
  approval_status: "DRAFT" | "PENDING" | "APPROVED" | "REJECTED";
}

export interface ExamTemplate {
  id: string;
  institute_id: string;
  title: string;
  duration_minutes: number;
  total_marks: number;
  passing_marks: number;
  allow_calculator: boolean;
  shuffle_questions: boolean;
  shuffle_options: boolean;
  allow_offline_sync: boolean;
  instructions?: string;
  created_at: string;
}

export interface CBTSession {
  id: string;
  institute_id: string;
  template_id: string;
  exam_subject_id?: string;
  session_code: string;
  start_window: string;
  end_window: string;
  delivery_mode: "ONLINE" | "LAN" | "OFFLINE" | "HYBRID";
  status: "SCHEDULED" | "LIVE" | "COMPLETED" | "RESULTS_SYNCED";
  created_at: string;
}

export interface CandidateSession {
  id: string;
  cbt_session_id: string;
  student_id: string;
  random_seed: number;
  remaining_seconds: number;
  status: "IN_PROGRESS" | "SUBMITTED" | "FORCE_SUBMITTED" | "PAUSED" | "DISQUALIFIED";
  total_score: number;
  marks_synced_to_module11: boolean;
  created_at: string;
}

export interface LiveCandidateStatus {
  candidate_session_id: string;
  student_id: string;
  student_name: string;
  roll_number: string;
  current_question_index: number;
  answered_count: number;
  remaining_seconds: number;
  status: string;
  warnings_count: number;
}

export interface CBTDashboardSummary {
  total_questions_in_bank: number;
  active_cbt_sessions_count: number;
  live_active_candidates_count: number;
  total_exams_delivered_today: number;
  offline_syncs_processed: number;
  average_candidate_score: number;
  recent_sessions: Array<{ code: string; mode: string; candidates: number; status: string }>;
}
