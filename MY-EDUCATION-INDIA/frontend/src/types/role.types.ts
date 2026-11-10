export interface PermissionItem {
  id: string;
  code: string;
  name: string;
  module_key: string;
  group_key: string;
  action_type: string;
  description: string | null;
}

export interface PermissionGroupItem {
  id: string;
  group_key: string;
  group_name: string;
  category: string;
  description: string | null;
  display_order: number;
}

export interface RoleTemplateItem {
  id: string;
  template_key: string;
  name: string;
  department: string;
  description: string | null;
  default_permissions: string[];
  default_data_scope: string;
  default_subdomain: string;
}

export interface RoleItem {
  id: string;
  code: string;
  name: string;
  description: string | null;
  portal_subdomain: string;
  is_system_role: boolean;
  is_custom_role: boolean;
  department_name: string | null;
  data_scope: string;
  field_permissions_json: Record<string, boolean | string> | null;
  menu_permissions_json: string[] | null;
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
  is_custom_role?: boolean;
  department_name?: string;
  data_scope?: string;
  field_permissions_json?: Record<string, boolean | string>;
  menu_permissions_json?: string[];
  permission_codes: string[];
}

export interface InstantiateTemplatePayload {
  role_code: string;
  role_name: string;
  department_name?: string;
}

export interface UpdateRolePayload {
  name?: string;
  description?: string;
  department_name?: string;
  data_scope?: string;
  field_permissions_json?: Record<string, boolean | string>;
  menu_permissions_json?: string[];
  permission_codes?: string[];
}
