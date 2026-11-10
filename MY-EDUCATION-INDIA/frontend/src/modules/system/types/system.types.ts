export interface InstituteItem {
  id: string;
  code: string;
  name: string;
  tagline?: string | null;
  official_email: string;
  official_phone: string;
  website_domain?: string | null;
  address_line1: string;
  address_line2?: string | null;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  primary_color_hex: string;
  secondary_color_hex: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface BranchItem {
  id: string;
  institute_id: string;
  code: string;
  name: string;
  address_line1: string;
  address_line2?: string | null;
  city: string;
  state: string;
  postal_code: string;
  phone: string;
  email: string;
  principal_name?: string | null;
  logo_url?: string | null;
  opening_time?: string | null;
  closing_time?: string | null;
  is_main_branch: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AcademicYearItem {
  id: string;
  institute_id: string;
  code: string;
  name: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
  is_locked: boolean;
  created_at: string;
  updated_at: string;
}

export interface FinancialYearItem {
  id: string;
  institute_id: string;
  code: string;
  name: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
  is_closed: boolean;
  gstin?: string | null;
  created_at: string;
  updated_at: string;
}

export interface NumberGeneratorItem {
  id: string;
  institute_id: string;
  entity_type: string;
  name: string;
  prefix?: string | null;
  suffix?: string | null;
  format_template: string;
  separator: string;
  padding_length: number;
  reset_rule: "NEVER" | "YEARLY" | "ACADEMIC_YEAR" | "FINANCIAL_YEAR" | "MONTHLY" | "BRANCH";
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface OrganizationSettings {
  id: string;
  institute_id: string;
  default_currency: string;
  default_language: string;
  default_timezone: string;
  date_format: string;
  time_format: string;
  fiscal_year_start_month: number;
  academic_year_start_month: number;
  sidebar_style: string;
}

export interface SystemSettingRecord {
  id: string;
  category: string;
  key: string;
  value: Record<string, unknown>;
  description?: string | null;
  is_public: boolean;
  institute_id?: string | null;
  updated_at: string;
}
