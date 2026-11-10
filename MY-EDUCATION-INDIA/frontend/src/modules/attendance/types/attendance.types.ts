export interface AttendanceSession {
  id: string;
  institute_id: string;
  branch_id?: string;
  course_id?: string;
  batch_id?: string;
  section_id?: string;
  subject_id?: string;
  session_date: string;
  session_type: "DAILY" | "PERIOD_WISE" | "LAB" | "PRACTICAL" | "SEMINAR";
  period_number?: number;
  start_time?: string;
  end_time?: string;
  taken_by_user_id: string;
  is_locked: boolean;
  created_at: string;
}

export interface StudentAttendanceRecord {
  id: string;
  session_id: string;
  student_id: string;
  status: "PRESENT" | "ABSENT" | "LATE" | "HALF_DAY" | "LEAVE" | "ON_DUTY";
  check_in_time?: string;
  attendance_method: "MANUAL" | "QR_CODE" | "BARCODE" | "RFID" | "BIOMETRIC";
  remarks?: string;
  created_at: string;
}

export interface FacultyAttendanceRecord {
  id: string;
  faculty_user_id: string;
  attendance_date: string;
  status: "PRESENT" | "ABSENT" | "LATE" | "HALF_DAY" | "ON_DUTY" | "LEAVE";
  clock_in_time?: string;
  clock_out_time?: string;
  total_working_hours: number;
  attendance_method: string;
}

export interface StaffAttendanceRecord {
  id: string;
  staff_user_id: string;
  attendance_date: string;
  status: "PRESENT" | "ABSENT" | "LATE" | "HALF_DAY" | "LEAVE";
  clock_in_time?: string;
  clock_out_time?: string;
  total_working_hours: number;
  attendance_method: string;
}

export interface LeaveType {
  id: string;
  code: string;
  name: string;
  applicable_to: "STUDENT" | "FACULTY" | "STAFF" | "ALL";
  annual_quota_days: number;
  requires_attachment: boolean;
  is_carry_forward: boolean;
  is_active: boolean;
}

export interface LeaveRequest {
  id: string;
  institute_id: string;
  user_id: string;
  user_type: "STUDENT" | "FACULTY" | "STAFF";
  leave_type_id: string;
  start_date: string;
  end_date: string;
  total_days: number;
  reason: string;
  attachment_url?: string;
  status: "PENDING" | "APPROVED" | "REJECTED" | "CANCELLED";
  applied_at: string;
}

export interface AttendanceRule {
  id: string;
  institute_id: string;
  minimum_attendance_pct: number;
  grace_time_minutes: number;
  half_day_threshold_hours: number;
  consecutive_absent_alert_days: number;
  lock_attendance_after_days: number;
  auto_notify_parents_on_absence: boolean;
  exam_eligibility_threshold_pct: number;
  is_active: boolean;
}

export interface AttendanceDashboardSummary {
  today_date: string;
  total_students_enrolled: number;
  students_present_count: number;
  students_absent_count: number;
  students_late_count: number;
  overall_attendance_pct: number;
  faculty_present_pct: number;
  staff_present_pct: number;
  pending_leaves_count: number;
  low_attendance_alert_count: number;
  weekly_trend: Array<{ day: string; attendance_pct: number }>;
}
