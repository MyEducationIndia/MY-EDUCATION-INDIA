export type NotificationChannel = "EMAIL" | "SMS" | "WHATSAPP" | "PUSH" | "IN_APP";

export interface NotificationTemplateItem {
  id: string;
  institute_id: string;
  template_code: string;
  template_name: string;
  category: string;
  channels: NotificationChannel[];
  subject_template: string | null;
  body_template: string;
  sms_dlt_template_id: string | null;
  whatsapp_template_name: string | null;
  variables_schema: string[];
  is_active: boolean;
  created_at: string;
}

export interface CreateTemplatePayload {
  template_code: string;
  template_name: string;
  category?: string;
  channels: NotificationChannel[];
  subject_template?: string | null;
  body_template: string;
  sms_dlt_template_id?: string | null;
  whatsapp_template_name?: string | null;
  variables_schema?: string[];
}

export interface UpdateTemplatePayload {
  template_name?: string;
  category?: string;
  channels?: NotificationChannel[];
  subject_template?: string | null;
  body_template?: string;
  sms_dlt_template_id?: string | null;
  whatsapp_template_name?: string | null;
  variables_schema?: string[];
  is_active?: boolean;
}

export interface NotificationDeliveryReportItem {
  id: string;
  dispatch_id: string;
  recipient_contact: string;
  channel: string;
  status: string;
  delivered_at: string | null;
  error_message: string | null;
  created_at: string;
}

export interface NotificationDispatchItem {
  id: string;
  institute_id: string;
  template_id: string | null;
  title: string;
  content: string;
  channels: NotificationChannel[];
  target_audience: string;
  target_roles: string[];
  scheduled_at: string | null;
  is_scheduled: boolean;
  dispatch_status: string;
  total_recipients: number;
  successful_deliveries: number;
  failed_deliveries: number;
  delivery_reports: NotificationDeliveryReportItem[];
  created_at: string;
}

export interface CreateDispatchPayload {
  template_code?: string;
  title: string;
  content: string;
  channels: NotificationChannel[];
  target_audience?: string;
  target_roles?: string[];
  scheduled_at?: string | null;
  template_variables?: Record<string, string | number>;
}

export interface NotificationCenterSummary {
  total_dispatches: number;
  total_delivered: number;
  delivery_success_rate: number;
  channel_stats: Record<string, number>;
  templates_count: number;
  active_scheduled_count: number;
}
