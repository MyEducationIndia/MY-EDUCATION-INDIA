export interface DesignationItem {
  id: string;
  institute_id: string;
  department_id: string | null;
  code: string;
  title: string;
  cadre: string;
  level: number;
  reports_to_designation_id: string | null;
  description: string | null;
  is_active: boolean;
  created_at: string;
}

export interface DepartmentSummary {
  id: string;
  institute_id: string;
  code: string;
  name: string;
  department_type: string;
  parent_department_id: string | null;
  head_user_id: string | null;
  head_name: string | null;
  head_designation: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  location_room: string | null;
  workflow_assignments: string[];
  is_active: boolean;
  display_order: number;
  sub_departments_count: number;
  designations_count: number;
  created_at: string;
}

export interface DepartmentDetail extends DepartmentSummary {
  sub_departments: DepartmentSummary[];
  designations: DesignationItem[];
  metadata_json: Record<string, unknown>;
}

export interface CreateDepartmentPayload {
  code: string;
  name: string;
  department_type?: string;
  parent_department_id?: string | null;
  head_user_id?: string | null;
  head_designation?: string | null;
  contact_email?: string | null;
  contact_phone?: string | null;
  location_room?: string | null;
  workflow_assignments?: string[];
  display_order?: number;
}

export interface UpdateDepartmentPayload {
  name?: string;
  department_type?: string;
  parent_department_id?: string | null;
  head_user_id?: string | null;
  head_designation?: string | null;
  contact_email?: string | null;
  contact_phone?: string | null;
  location_room?: string | null;
  workflow_assignments?: string[];
  is_active?: boolean;
  display_order?: number;
}

export interface CreateDesignationPayload {
  code: string;
  title: string;
  department_id?: string | null;
  cadre?: string;
  level?: number;
  reports_to_designation_id?: string | null;
  description?: string | null;
}

export interface UpdateDesignationPayload {
  title?: string;
  department_id?: string | null;
  cadre?: string;
  level?: number;
  reports_to_designation_id?: string | null;
  description?: string | null;
  is_active?: boolean;
}
