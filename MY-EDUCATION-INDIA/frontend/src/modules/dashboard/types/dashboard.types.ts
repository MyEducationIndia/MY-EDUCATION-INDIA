export interface DashboardKPIStats {
  total_students: number;
  active_students: number;
  admissions_today: number;
  admissions_this_month: number;
  total_faculty: number;
  total_courses: number;
  total_batches: number;
  total_branches: number;
  fee_collection_today: number;
  fee_collection_this_month: number;
  pending_fees_total: number;
  overall_attendance_pct: number;
  examinations_conducted: number;
  certificates_issued: number;
  website_visitors_today: number;
  unread_notifications_count: number;
  sms_sent_count: number;
  whatsapp_sent_count: number;
  emails_sent_count: number;
  database_status: string;
  server_status: string;
  api_status: string;
  storage_usage_mb: number;
  last_backup_at?: string | null;
}

export interface TimeSeriesPoint {
  timestamp: string;
  label: string;
  value: number;
  secondary_value?: number | null;
  category?: string | null;
}

export interface CategoryDistribution {
  name: string;
  count: number;
  percentage: number;
  color_hex?: string | null;
}

export interface MultiChartData {
  admission_trends: TimeSeriesPoint[];
  fee_collection: TimeSeriesPoint[];
  attendance_trends: TimeSeriesPoint[];
  student_growth: TimeSeriesPoint[];
  course_popularity: CategoryDistribution[];
  channel_statistics: Record<string, number>;
  branch_comparison: CategoryDistribution[];
}

export interface SearchResultItem {
  entity_type: string;
  title: string;
  subtitle?: string | null;
  identifier: string;
  target_url: string;
  status_badge?: string | null;
  created_at?: string | null;
}

export interface GlobalSearchData {
  query: string;
  total_results: number;
  grouped_results: Record<string, SearchResultItem[]>;
}

export interface DashboardActivityItem {
  id: string;
  actor_name: string;
  action_type: string;
  entity_type: string;
  entity_id?: string | null;
  summary: string;
  detail_payload: Record<string, unknown>;
  occurred_at: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  category: string;
  priority: string;
  action_url?: string | null;
  is_read: boolean;
  read_at?: string | null;
  created_at: string;
}

export interface WidgetConfig {
  widget_key: string;
  title: string;
  category: string;
  grid_position: number;
  grid_width: number;
  grid_height: number;
  is_visible: boolean;
  is_pinned: boolean;
  configuration: Record<string, unknown>;
}

export interface SystemHealthData {
  database_status: string;
  database_version: string;
  api_status: string;
  server_time: string;
  uptime_seconds: number;
  memory_usage_mb: number;
  total_memory_mb: number;
  cpu_percent: number;
  storage_usage_mb: number;
  active_db_connections: number;
  last_backup_time?: string | null;
  app_version: string;
  environment: string;
}

export interface DashboardBootstrapPayload {
  kpi_stats: DashboardKPIStats;
  charts: MultiChartData;
  widgets: WidgetConfig[];
  activities: DashboardActivityItem[];
  notifications: NotificationItem[];
  system_health: SystemHealthData;
}
