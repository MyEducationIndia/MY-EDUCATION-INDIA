export type DashboardRoleKey =
  | "SUPER_ADMIN"
  | "ADMIN"
  | "PRINCIPAL"
  | "FACULTY"
  | "STUDENT"
  | "PARENT"
  | "RECEPTION"
  | "ACCOUNTANT"
  | "LIBRARY"
  | "CBT"
  | "LMS"
  | "EXAMINATION_CELL";

export interface DashboardKPICard {
  key: string;
  label: string;
  value: string;
  delta: string;
  is_positive: boolean;
  icon: string;
  trend: string;
}

export interface DashboardWidget {
  widget_key: string;
  title: string;
  widget_type: string;
  grid_width: number;
  data: Record<string, unknown>;
}

export interface DashboardChartDataset {
  label: string;
  data: number[];
  color?: string;
}

export interface DashboardChart {
  chart_key: string;
  title: string;
  chart_type: "bar" | "line" | "donut" | "area";
  labels: string[];
  datasets: DashboardChartDataset[];
}

export interface DashboardNotification {
  id: string;
  title: string;
  message: string;
  category: string;
  priority: string;
  created_at: string;
  is_read: boolean;
}

export interface DashboardTask {
  id: string;
  institute_id: string;
  user_id?: string | null;
  role_target: string;
  title: string;
  description?: string | null;
  due_date?: string | null;
  priority: string;
  status: string;
  action_url?: string | null;
  created_at: string;
}

export interface DashboardCalendarEvent {
  id: string;
  title: string;
  event_date: string;
  time_slot: string;
  category: string;
}

export interface DashboardQuickAction {
  label: string;
  action_key: string;
  route: string;
  icon: string;
  is_primary: boolean;
}

export interface RoleDashboardBundle {
  role_key: string;
  role_title: string;
  kpis: DashboardKPICard[];
  widgets: DashboardWidget[];
  charts: DashboardChart[];
  notifications: DashboardNotification[];
  tasks: DashboardTask[];
  calendar_events: DashboardCalendarEvent[];
  quick_actions: DashboardQuickAction[];
  system_status: Record<string, unknown>;
}
