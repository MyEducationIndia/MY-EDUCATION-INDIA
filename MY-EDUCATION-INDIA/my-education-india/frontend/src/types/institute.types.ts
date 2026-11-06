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
  seo_metadata: Record<string, unknown>;
  is_active: boolean;
  module_configs: SystemModuleConfig[];
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
