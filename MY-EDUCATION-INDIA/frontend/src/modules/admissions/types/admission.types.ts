export interface LeadRecord {
  id: string;
  lead_number: string;
  full_name: string;
  phone_number: string;
  email?: string | null;
  city?: string | null;
  state?: string | null;
  source_channel: string;
  interested_course?: string | null;
  priority: "HOT" | "WARM" | "COLD";
  status: string;
  score: number;
  assigned_counsellor_id?: string | null;
  next_followup_at?: string | null;
  remarks?: string | null;
  created_at: string;
}

export interface ApplicationRecord {
  id: string;
  application_number: string;
  application_mode: string;
  first_name: string;
  middle_name?: string | null;
  last_name: string;
  email: string;
  phone_number: string;
  date_of_birth: string;
  gender: string;
  category: string;
  course_name: string;
  batch_preference: string;
  academic_year_code: string;
  guardian_name: string;
  status: string;
  is_locked: boolean;
  student_id?: string | null;
  created_at: string;
}

export interface AdmissionMetrics {
  today_enquiries: number;
  admissions_today: number;
  pending_applications: number;
  verification_pending: number;
  waiting_list: number;
  total_leads: number;
  conversions_count: number;
  conversion_rate_pct: number;
  total_revenue_collected: number;
}
