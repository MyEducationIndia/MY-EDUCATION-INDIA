export interface UserSummary {
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
  last_login_at: string | null;
  created_at: string;
}

export interface CreateUserPayload {
  email: string;
  username: string;
  phone_number: string;
  first_name: string;
  last_name: string;
  password: string;
  institute_id?: string | null;
  role_ids: string[];
  is_super_admin: boolean;
}
