export type ReportCategory =
  | "ALL"
  | "ACADEMIC"
  | "FINANCE"
  | "ADMISSIONS"
  | "ATTENDANCE"
  | "EXAMINATION"
  | "HR";

export type ReportFormat = "PDF" | "EXCEL" | "CSV" | "PRINT" | "JSON";

export interface ReportDefinitionItem {
  id: string;
  institute_id: string;
  report_code: string;
  title: string;
  category: string;
  description: string | null;
  supported_formats: ReportFormat[];
  chart_type: string | null;
  filter_schema: Array<{ key: string; label: string }>;
  is_active: boolean;
  created_at: string;
}

export interface ReportExecutionLogItem {
  id: string;
  report_id: string;
  report_title: string;
  export_format: string;
  applied_filters: Record<string, unknown>;
  rows_count: number;
  execution_duration_ms: number;
  file_url: string | null;
  status: string;
  created_at: string;
}

export interface ScheduledReportJobItem {
  id: string;
  report_id: string;
  report_title: string;
  job_title: string;
  frequency: "DAILY" | "WEEKLY" | "MONTHLY" | "QUARTERLY";
  export_format: string;
  recipient_emails: string[];
  filter_parameters: Record<string, unknown>;
  last_run_at: string | null;
  next_run_at: string | null;
  is_active: boolean;
}

export interface GenerateReportPayload {
  report_code: string;
  export_format: ReportFormat;
  filters?: Record<string, unknown>;
}

export interface GeneratedReportData {
  report_code: string;
  title: string;
  category: string;
  export_format: string;
  generated_at: string;
  columns: string[];
  rows: Array<Record<string, unknown>>;
  summary_kpis: Record<string, string | number>;
  chart_data?: {
    labels: string[];
    values: number[];
  } | null;
  file_url?: string | null;
  execution_duration_ms: number;
}

export interface CreateScheduledJobPayload {
  report_code: string;
  job_title: string;
  frequency: "DAILY" | "WEEKLY" | "MONTHLY" | "QUARTERLY";
  export_format: "PDF" | "EXCEL" | "CSV";
  recipient_emails: string[];
  filter_parameters?: Record<string, unknown>;
}

export interface ReportEngineSummary {
  total_reports_available: number;
  total_generated_this_month: number;
  active_scheduled_jobs: number;
  category_distribution: Record<string, number>;
  format_distribution: Record<string, number>;
}
