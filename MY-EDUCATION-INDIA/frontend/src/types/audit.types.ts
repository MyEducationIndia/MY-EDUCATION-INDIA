export type AuditEventCategory =
  | "ALL"
  | "AUTH_LOGIN"
  | "AUTH_LOGOUT"
  | "CRUD_OPERATION"
  | "SETTINGS_CHANGE"
  | "SECURITY_EVENT"
  | "API_CALL"
  | "PERMISSION_CHANGE"
  | "FILE_UPLOAD";

export type AuditSeverity = "ALL" | "INFO" | "WARNING" | "SECURITY_ALERT" | "CRITICAL";

export interface AuditLogEntry {
  id: string;
  actor_user_id: string | null;
  actor_username: string | null;
  actor_role: string | null;
  institute_id: string | null;
  module_key: string;
  action: string;
  event_category: string;
  severity: string;
  resource_type: string;
  resource_id: string | null;
  http_method: string;
  endpoint_path: string;
  status_code: number;
  duration_ms: number;
  ip_address: string;
  ip_location: string;
  user_agent: string;
  request_id: string;
  changes_payload: Record<string, unknown>;
  payload_checksum: string | null;
  created_at: string;
}

export interface AuditLogSummary {
  total_events: number;
  category_breakdown: Record<string, number>;
  severity_breakdown: Record<string, number>;
  security_alerts_count: number;
  active_audited_modules_count: number;
}
