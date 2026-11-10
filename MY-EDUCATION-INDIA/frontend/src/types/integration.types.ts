export interface ApiProvider {
  id: string;
  institute_id: string;
  provider_key: string;
  display_name: string;
  category: string; // SMS, WHATSAPP, EMAIL, PUSH, PAYMENT, VIDEO, STORAGE, AI, MAPS, OTP, GOV_PORTAL, WEBHOOK
  auth_type: string; // API_KEY, BEARER, OAUTH2, BASIC, JWT, CUSTOM_HEADER, HMAC
  base_url: string;
  is_enabled: boolean;
  is_default: boolean;
  failover_provider_id: string | null;
  rate_limit_per_minute: number;
  timeout_seconds: number;
  retry_max_attempts: number;
  retry_backoff_factor: number;
  circuit_breaker_threshold: number;
  has_credentials: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProviderTemplate {
  provider_key: string;
  display_name: string;
  category: string;
  auth_type: string;
  suggested_base_url: string;
  required_credential_fields: string[];
  doc_url: string;
}

export interface ConnectionTestRequest {
  endpoint_path?: string;
  test_payload?: Record<string, any>;
}

export interface ConnectionTestResponse {
  is_connected: boolean;
  status_code?: number;
  latency_ms: number;
  message: string;
  response_preview?: string;
}

export interface CredentialUpdateRequest {
  credentials: Record<string, string>;
}

export interface ApiExecutionLog {
  id: string;
  provider_id: string;
  endpoint_key: string;
  category: string;
  status_code: number | null;
  is_success: boolean;
  latency_ms: number;
  error_message: string | null;
  retry_count: number;
  circuit_broken: boolean;
  request_timestamp: string;
}

export interface WebhookRegistration {
  id: string;
  institute_id: string;
  direction: string;
  event_type: string;
  target_url: string;
  secret_token: string;
  signature_header: string;
  is_active: boolean;
  retry_count: number;
  created_at: string;
}

export interface IntegrationAnalytics {
  total_api_calls_24h: number;
  overall_success_rate: number;
  average_latency_ms: number;
  circuit_breaker_events: number;
  category_breakdown: Record<string, number>;
}
