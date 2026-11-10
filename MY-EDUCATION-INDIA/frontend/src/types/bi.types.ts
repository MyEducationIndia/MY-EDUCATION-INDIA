export interface ExecutiveDashboardMetrics {
  admissions_count: number;
  total_revenue_inr: number;
  pending_fees_inr: number;
  fee_collection_rate_percentage: number;
  average_attendance_percentage: number;
  exam_pass_percentage: number;
  active_course_enrollments: number;
  lead_conversion_rate_percentage: number;
  institute_health_score: number;
}

export interface KpiDefinition {
  id: string;
  institute_id: string;
  kpi_key: string;
  kpi_name: string;
  category: string;
  calculation_formula: string;
  target_value: number;
  current_value: number;
  warning_threshold: number;
  critical_threshold: number;
  unit: string;
  trend_direction: "UP" | "DOWN" | "STABLE";
}

export interface ReportDefinition {
  id: string;
  institute_id: string;
  report_code: string;
  report_name: string;
  category: string;
  description?: string | null;
  source_tables: string[];
  is_system_report: boolean;
  is_active: boolean;
  created_at: string;
}

export interface TrendChartsData {
  monthly_revenue: {
    month: string;
    revenue: number;
    collections: number;
  }[];
  attendance_distribution: {
    range: string;
    percentage: number;
  }[];
  placement_package_distribution: {
    tier: string;
    count: number;
  }[];
}

export interface CohortRetentionData {
  academic_cohort: string;
  initial_intake: number;
  year_1_retention: number;
  year_2_retention: number;
  year_3_retention: number;
  year_4_on_track: number;
  dropout_rate: number;
  lateral_entry_additions: number;
  remedial_support_sessions: number;
}

export interface NirfNaacDossierData {
  naac_grade: string;
  cgpa: number;
  nirf_score_breakdown: {
    TLR_Teaching_Learning_Resources: number;
    RP_Research_Professional_Practice: number;
    GO_Graduation_Outcomes: number;
    OI_Outreach_Inclusivity: number;
    PR_Perception: number;
  };
  faculty_phd_percentage: number;
  scopus_wos_papers_indexed: number;
  annual_research_grant_inr: number;
  median_salary_inr: number;
  highest_package_inr: number;
}

export interface SystemHealthOverview {
  overall_status: string;
  healthy_services_count: number;
  total_services_count: number;
  cluster_latency_ms: number;
  uptime_percentage_30d: number;
  services: {
    name: string;
    status: "HEALTHY" | "DEGRADED" | "DOWN";
    latency_ms: number;
  }[];
}
