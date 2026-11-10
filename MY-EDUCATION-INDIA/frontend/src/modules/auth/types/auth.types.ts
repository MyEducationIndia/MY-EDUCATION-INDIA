export interface RoleSummary {
  id: string;
  code: string;
  name: string;
  portal_subdomain: string;
  is_system_role: boolean;
}

export interface PermissionSummary {
  id: string;
  code: string;
  name: string;
  module_key: string;
  description?: string | null;
}

export interface UserProfile {
  id: string;
  email: string;
  username: string;
  phone_number: string;
  first_name: string;
  last_name: string;
  registration_number?: string | null;
  enrollment_number?: string | null;
  roll_number?: string | null;
  erp_id?: string | null;
  student_id?: string | null;
  is_active: boolean;
  is_super_admin: boolean;
  is_verified: boolean;
  institute_id?: string | null;
  roles: RoleSummary[];
  permissions: string[];
  last_login_at?: string | null;
}

export interface AuthSessionResponse {
  access_token: string;
  token_type: string;
  expires_at: string;
  csrf_token: string;
  user: UserProfile;
}

export interface ConfigurableLoginPayload {
  identifier: string;
  password: string;
  remember_me: boolean;
  login_criterion?: string;
}

export interface ActiveSession {
  id: string;
  device_info: string;
  ip_address: string;
  user_agent: string;
  created_at: string;
  expires_at: string;
  is_current: boolean;
}

export interface LoginHistoryRecord {
  id: string;
  identifier_used: string;
  login_criterion: string;
  status: "SUCCESS" | "FAILED" | "LOCKED";
  failure_reason?: string | null;
  ip_address: string;
  device_type: string;
  browser: string;
  os: string;
  logged_in_at: string;
  logged_out_at?: string | null;
}

export interface SystemAuthSettings {
  login_criteria: string[];
  allow_remember_me: boolean;
  password_min_length: number;
  password_require_uppercase: boolean;
  password_require_lowercase: boolean;
  password_require_number: boolean;
  password_require_special: boolean;
  session_timeout_minutes: number;
}
