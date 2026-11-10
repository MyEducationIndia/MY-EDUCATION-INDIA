export type UserCategory =
  | "ALL"
  | "STUDENT"
  | "FACULTY"
  | "STAFF"
  | "PARENT"
  | "RECEPTION"
  | "LIBRARIAN"
  | "ACCOUNTANT"
  | "EXAM_CELL"
  | "CBT_STAFF"
  | "LMS_STAFF"
  | "SUPER_ADMIN";

export interface UserDocument {
  id: string;
  user_id: string;
  document_type: string;
  document_title: string;
  document_url: string;
  file_size_bytes: number;
  mime_type: string;
  verification_status: string;
  verified_by_user_id: string | null;
  verified_at: string | null;
  remarks: string | null;
  created_at: string;
}

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
  user_category: string;
  department: string | null;
  designation: string | null;
  admission_or_emp_id: string | null;
  photo_url: string | null;
  identity_verification_status: string;
  is_archived: boolean;
  institute_id: string | null;
  last_login_at: string | null;
  created_at: string;
}

export interface UserDetail extends UserSummary {
  dob: string | null;
  gender: string | null;
  blood_group: string | null;
  digital_signature_url: string | null;
  verification_id_type: string | null;
  verification_id_number: string | null;
  archived_at: string | null;
  metadata_json: Record<string, unknown>;
  roles: Array<{ id: string; code: string; name: string }>;
  documents: UserDocument[];
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
  user_category: string;
  department?: string | null;
  designation?: string | null;
  admission_or_emp_id?: string | null;
  dob?: string | null;
  gender?: string | null;
  blood_group?: string | null;
  photo_url?: string | null;
  digital_signature_url?: string | null;
  verification_id_type?: string | null;
  verification_id_number?: string | null;
}

export interface UpdateUserPayload {
  first_name?: string;
  last_name?: string;
  phone_number?: string;
  user_category?: string;
  department?: string | null;
  designation?: string | null;
  admission_or_emp_id?: string | null;
  dob?: string | null;
  gender?: string | null;
  blood_group?: string | null;
  photo_url?: string | null;
  digital_signature_url?: string | null;
  identity_verification_status?: string;
  verification_id_type?: string | null;
  verification_id_number?: string | null;
  role_ids?: string[];
  is_active?: boolean;
}

export interface UserBulkActionPayload {
  user_ids: string[];
  action: "ACTIVATE" | "DEACTIVATE" | "ARCHIVE" | "RESTORE" | "ASSIGN_ROLE";
  role_id?: string;
}

export interface UserBulkImportItem {
  email: string;
  username: string;
  phone_number: string;
  first_name: string;
  last_name: string;
  user_category?: string;
  department?: string;
  designation?: string;
  admission_or_emp_id?: string;
  gender?: string;
}

export interface UserBulkImportPayload {
  users: UserBulkImportItem[];
  default_password?: string;
}
