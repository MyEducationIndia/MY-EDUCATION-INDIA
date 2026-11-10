export interface CrmLead {
  id: string;
  institute_id: string;
  lead_code: string;
  full_name: string;
  mobile: string;
  email?: string | null;
  guardian_name?: string | null;
  course_interested_id: string;
  source_id?: string | null;
  priority: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
  assigned_counsellor_id?: string | null;
  stage: "NEW_LEAD" | "CONTACTED" | "COUNSELLING" | "FEE_DISCUSSION" | "ADMISSION_CONFIRMED" | "LOST";
  status: "ACTIVE" | "CONVERTED" | "DROPPED";
  score: number;
  remarks?: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CrmFollowup {
  id: string;
  lead_id: string;
  counsellor_name: string;
  channel: "CALL" | "WHATSAPP" | "SMS" | "EMAIL" | "MEETING";
  scheduled_at: string;
  notes?: string | null;
  outcome?: string | null;
  next_followup_date?: string | null;
}

export interface CrmCampaign {
  id: string;
  institute_id: string;
  campaign_name: string;
  channel: string;
  start_date: string;
  end_date?: string | null;
  allocated_budget: number;
  actual_spent: number;
  status: "DRAFT" | "ACTIVE" | "PAUSED" | "COMPLETED";
  utm_source?: string | null;
  utm_campaign?: string | null;
  leads_generated: number;
  conversions: number;
  created_at: string;
}

export interface FranchiseCenter {
  id: string;
  institute_id: string;
  center_code: string;
  center_name: string;
  city: string;
  state: string;
  contact_email: string;
  contact_phone: string;
  royalty_percentage: number;
  active_students: number;
  revenue_generated: number;
  status: "ACTIVE" | "SUSPENDED" | "PENDING";
  created_at: string;
}

export interface CrmPipelineStage {
  stage_key: string;
  stage_name: string;
  order_index: number;
  probability: number;
}

export interface CrmDashboardMetrics {
  total_new_leads: number;
  todays_followups_count: number;
  admissions_this_month: number;
  conversion_rate_percentage: number;
  revenue_forecast: number;
  top_counsellor: string;
  active_campaigns_count: number;
  pending_tasks_count: number;
}
