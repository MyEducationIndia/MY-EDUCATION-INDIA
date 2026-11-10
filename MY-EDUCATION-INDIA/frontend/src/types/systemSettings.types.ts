export interface MasterDataEntry {
  id: string;
  institute_id: string;
  category_key: string;
  item_code: string;
  item_label: string;
  item_value?: string;
  display_order: number;
  is_active: boolean;
  extra_metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface MasterDataCategorySummary {
  category_key: string;
  category_label: string;
  item_count: number;
  active_count: number;
  items: MasterDataEntry[];
}

export interface CampusHoliday {
  id: string;
  institute_id: string;
  academic_session_id?: string;
  name: string;
  holiday_date: string;
  holiday_type: 'GAZETTED' | 'RESTRICTED' | 'ACADEMIC_BREAK' | 'INSTITUTIONAL';
  description?: string;
  is_optional: boolean;
  created_at: string;
  updated_at: string;
}

export interface WorkingDaysConfig {
  id: string;
  institute_id: string;
  day_of_week: number;
  day_name: string;
  is_working_day: boolean;
  start_time: string;
  end_time: string;
  periods_count: number;
  lunch_break_start?: string;
  lunch_break_end?: string;
  created_at: string;
  updated_at: string;
}

export interface NumberingRule {
  id: string;
  institute_id: string;
  entity_type: 'STUDENT_ROLL' | 'EMPLOYEE_ID' | 'INVOICE_RECEIPT' | 'ADMISSION_APP' | 'CERTIFICATE_NO';
  entity_title: string;
  prefix: string;
  suffix: string;
  digits_padding: number;
  current_sequence: number;
  reset_frequency: 'ANNUAL' | 'ACADEMIC_SESSION' | 'NEVER';
  format_pattern: string;
  sample_preview?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface DocumentTemplate {
  id: string;
  institute_id: string;
  template_code: 'TRANSFER_CERTIFICATE' | 'BONAFIDE_CERTIFICATE' | 'CHARACTER_CERTIFICATE' | 'STUDENT_ID_CARD' | string;
  title: string;
  content_html: string;
  header_image_url?: string;
  footer_html?: string;
  paper_size: 'A4' | 'LETTER' | 'ID_CARD';
  orientation: 'PORTRAIT' | 'LANDSCAPE';
  available_placeholders?: Record<string, string>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SystemSettingsSummary {
  institute_id: string;
  master_data_categories_count: number;
  master_data_items_count: number;
  holidays_count: number;
  working_days_count: number;
  numbering_rules_count: number;
  document_templates_count: number;
  active_academic_session?: string;
  timezone: string;
  locale: string;
}

export interface NumberingSequenceGenerateResponse {
  entity_type: string;
  generated_number: string;
  sequence_number: number;
  rule_id: string;
}

export interface DocumentRenderResponse {
  template_code: string;
  title: string;
  rendered_html: string;
  paper_size: string;
  orientation: string;
}
