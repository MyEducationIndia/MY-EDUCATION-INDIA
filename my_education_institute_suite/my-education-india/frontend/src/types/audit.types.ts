export interface AuditLogEntry {
  id: string;
  actor_user_id: string | null;
  institute_id: string | null;
  module_key: string;
  action: string;
  resource_type: string;
  resource_id: string | null;
  http_method: string;
  endpoint_path: string;
  status_code: number;
  ip_address: string;
  user_agent: string;
  request_id: string;
  changes_payload: Record<string, unknown>;
  created_at: string;
}
