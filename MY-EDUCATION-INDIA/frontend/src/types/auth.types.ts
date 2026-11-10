export interface AuthenticatedUser {
  id: string;
  email: string;
  username: string;
  phone_number: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_super_admin: boolean;
  is_verified: boolean;
  mfa_enabled?: boolean;
  institute_id: string | null;
  roles: string[];
  permissions: string[];
  last_login_at: string | null;
}

export interface TokenSessionResponse {
  access_token: string;
  token_type: string;
  expires_at: string;
  csrf_token: string;
  user: AuthenticatedUser;
}

export interface LoginCredentials {
  identifier: string;
  password: string;
  remember_me?: boolean;
}

export interface ActiveSessionItem {
  id: string;
  device_name: string;
  ip_address: string;
  user_agent: string;
  is_current: boolean;
  expires_at: string;
  last_active_at: string;
  created_at: string;
}

export interface LoginHistoryItem {
  id: string;
  email: string;
  ip_address: string;
  user_agent: string;
  device_name: string;
  status: string;
  failure_reason: string | null;
  location: string | null;
  created_at: string;
}

export interface SecurityPolicy {
  policy_name: string;
  min_password_length: number;
  require_uppercase: boolean;
  require_numbers: boolean;
  require_special_chars: boolean;
  password_expiry_days: number;
  max_failed_attempts: number;
  lockout_duration_minutes: number;
  session_timeout_minutes: number;
  enforce_2fa: boolean;
  allow_remember_me: boolean;
  remember_me_days: number;
}

export interface MfaSetupResponse {
  mfa_secret: string;
  totp_uri: string;
  backup_codes: string[];
}
