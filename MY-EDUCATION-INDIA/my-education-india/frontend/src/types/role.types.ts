export interface PermissionItem {
  id: string;
  code: string;
  name: string;
  module_key: string;
  description: string | null;
}

export interface RoleItem {
  id: string;
  code: string;
  name: string;
  description: string | null;
  portal_subdomain: string;
  is_system_role: boolean;
  institute_id: string | null;
  permissions: PermissionItem[];
  created_at: string;
  updated_at: string;
}

export interface CreateRolePayload {
  code: string;
  name: string;
  description?: string;
  portal_subdomain: string;
  permission_codes: string[];
}
