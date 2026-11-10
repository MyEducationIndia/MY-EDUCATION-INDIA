export type MediaFileType =
  | "ALL"
  | "IMAGE"
  | "PDF"
  | "VIDEO"
  | "DOCUMENT"
  | "LOGO"
  | "CERTIFICATE";

export interface MediaFolderItem {
  id: string;
  institute_id: string;
  name: string;
  slug: string;
  parent_folder_id: string | null;
  folder_type: string;
  access_level: string;
  allowed_roles: string[];
  icon: string;
  color: string;
  files_count: number;
  sub_folders_count: number;
  created_at: string;
}

export interface CreateFolderPayload {
  name: string;
  parent_folder_id?: string | null;
  folder_type?: string;
  access_level?: string;
  allowed_roles?: string[];
  icon?: string;
  color?: string;
}

export interface MediaFileVersionItem {
  id: string;
  media_file_id: string;
  version_number: number;
  file_url: string;
  file_size_bytes: number;
  changelog_notes: string | null;
  uploaded_by_user_id: string | null;
  is_active_version: boolean;
  created_at: string;
}

export interface MediaFileItem {
  id: string;
  institute_id: string;
  folder_id: string | null;
  file_name: string;
  original_name: string;
  file_type: string;
  mime_type: string;
  file_size_bytes: number;
  compressed_size_bytes: number;
  compression_ratio_pct: number;
  file_url: string;
  thumbnail_url: string | null;
  tags: string[];
  access_level: string;
  allowed_roles: string[];
  current_version: number;
  uploaded_by_user_id: string | null;
  metadata_json: Record<string, unknown>;
  versions: MediaFileVersionItem[];
  created_at: string;
}

export interface UploadFilePayload {
  file_name: string;
  original_name: string;
  folder_id?: string | null;
  file_type?: string;
  mime_type?: string;
  file_size_bytes: number;
  file_url: string;
  thumbnail_url?: string | null;
  tags?: string[];
  access_level?: string;
  allowed_roles?: string[];
  metadata_json?: Record<string, unknown>;
}

export interface AddVersionPayload {
  file_url: string;
  file_size_bytes: number;
  changelog_notes?: string;
}

export interface MediaManagerSummary {
  total_files: number;
  total_folders: number;
  total_storage_bytes: number;
  total_compressed_bytes: number;
  total_saved_bytes: number;
  overall_compression_savings_pct: number;
  type_breakdown: Record<string, number>;
}
