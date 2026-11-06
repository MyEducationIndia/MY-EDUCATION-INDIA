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
}
