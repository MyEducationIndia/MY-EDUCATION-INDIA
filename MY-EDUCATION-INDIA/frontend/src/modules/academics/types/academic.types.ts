export interface DepartmentRecord {
  id: string;
  code: string;
  name: string;
  description?: string | null;
  hod_name?: string | null;
  is_active: boolean;
  created_at: string;
}

export interface ProgramRecord {
  id: string;
  code: string;
  name: string;
  level: string;
  duration_years: number;
  total_credits: number;
  is_active: boolean;
  created_at: string;
}

export interface CourseRecord {
  id: string;
  code: string;
  name: string;
  duration_months: number;
  academic_pattern: string;
  total_semesters_or_years: number;
  min_intake_capacity: number;
  max_intake_capacity: number;
  department_id: string;
  program_id: string;
  is_active: boolean;
  created_at: string;
}

export interface SubjectRecord {
  id: string;
  code: string;
  name: string;
  subject_type: string;
  credits: number;
  theory_hours_per_week: number;
  practical_hours_per_week: number;
  internal_max_marks: number;
  external_max_marks: number;
  passing_percentage: number;
  is_lab_required: boolean;
  is_active: boolean;
  created_at: string;
}

export interface SectionRecord {
  id: string;
  batch_id: string;
  name: string;
  capacity: number;
  classroom_number?: string | null;
  class_teacher_name?: string | null;
  created_at: string;
}

export interface BatchRecord {
  id: string;
  code: string;
  name: string;
  academic_year_code: string;
  start_date: string;
  end_date: string;
  intake_capacity: number;
  current_strength: number;
  course_id: string;
  is_active: boolean;
  sections?: SectionRecord[];
  created_at: string;
}

export interface TimetableSlotRecord {
  id: string;
  timetable_id: string;
  subject_id: string;
  faculty_user_id?: string | null;
  classroom_id?: string | null;
  day_of_week: number;
  start_time: string;
  end_time: string;
  slot_type: string;
  subject?: SubjectRecord;
}

export interface TimetableRecord {
  id: string;
  batch_id: string;
  section_id: string;
  academic_year_code: string;
  is_active: boolean;
  slots: TimetableSlotRecord[];
}
