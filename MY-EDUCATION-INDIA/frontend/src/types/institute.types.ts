export interface SystemModuleConfig {
  id: string;
  institute_id: string;
  module_key: string;
  display_name: string;
  category: string;
  subdomain: string;
  description: string;
  is_enabled: boolean;
  is_core_locked: boolean;
  configuration: Record<string, unknown>;
  updated_at: string;
}

export interface AcademicSessionItem {
  id: string;
  institute_id: string;
  session_code: string;
  session_name: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
  is_admission_open: boolean;
  term_structure: string;
  terms_count: number;
  status: string;
  metadata_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface AcademicSessionCreatePayload {
  session_code: string;
  session_name: string;
  start_date: string;
  end_date: string;
  is_current?: boolean;
  is_admission_open?: boolean;
  term_structure?: string;
  terms_count?: number;
  status?: string;
  metadata_json?: Record<string, unknown>;
}

export interface AcademicSessionUpdatePayload {
  session_name?: string;
  start_date?: string;
  end_date?: string;
  is_current?: boolean;
  is_admission_open?: boolean;
  term_structure?: string;
  terms_count?: number;
  status?: string;
  metadata_json?: Record<string, unknown>;
}

export interface Institute {
  id: string;
  code: string;
  name: string;
  tagline: string | null;
  affiliation_number: string | null;
  official_email: string;
  official_phone: string;
  website_domain: string | null;
  address_line1: string;
  address_line2: string | null;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  logo_url: string | null;
  favicon_url: string | null;
  primary_color_hex: string;
  secondary_color_hex: string;
  time_zone: string;
  default_language: string;
  currency_code: string;
  currency_symbol: string;
  current_academic_year: string;
  custom_domain: string | null;
  custom_domain_status: string;
  google_maps_embed_url: string | null;
  google_maps_latitude: number | null;
  google_maps_longitude: number | null;
  social_media_links: Record<string, string>;
  smtp_config: Record<string, unknown>;
  sms_gateway_config: Record<string, unknown>;
  whatsapp_gateway_config: Record<string, unknown>;
  payment_gateway_config: Record<string, unknown>;
  theme_config: Record<string, unknown>;
  seo_metadata: Record<string, unknown>;
  is_active: boolean;
  module_configs: SystemModuleConfig[];
  academic_sessions: AcademicSessionItem[];
  created_at: string;
  updated_at: string;
}

export interface InstituteBrandingUpdatePayload {
  name?: string;
  tagline?: string;
  official_email?: string;
  official_phone?: string;
  logo_url?: string;
  favicon_url?: string;
  primary_color_hex?: string;
  secondary_color_hex?: string;
}

export interface InstituteProfileUpdatePayload {
  name?: string;
  tagline?: string;
  affiliation_number?: string;
  official_email?: string;
  official_phone?: string;
  website_domain?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  time_zone?: string;
  default_language?: string;
  currency_code?: string;
  currency_symbol?: string;
  current_academic_year?: string;
  custom_domain?: string;
  custom_domain_status?: string;
  google_maps_embed_url?: string;
  google_maps_latitude?: number;
  google_maps_longitude?: number;
}

export interface InstituteIntegrationsUpdatePayload {
  smtp_config?: Record<string, unknown>;
  sms_gateway_config?: Record<string, unknown>;
  whatsapp_gateway_config?: Record<string, unknown>;
  payment_gateway_config?: Record<string, unknown>;
  social_media_links?: Record<string, string>;
  theme_config?: Record<string, unknown>;
}

export interface InstituteSetupBundle {
  institute: Institute;
  current_session: AcademicSessionItem | null;
  all_sessions: AcademicSessionItem[];
  module_configs: SystemModuleConfig[];
  system_status: Record<string, boolean | number | string>;
}
