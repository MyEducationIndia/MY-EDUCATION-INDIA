export type ApiCategory = 
  | "SMS" | "WHATSAPP" | "EMAIL" | "PUSH" | "PAYMENT"
  | "VIDEO" | "STORAGE" | "AI" | "MAPS" | "OTP" | "WEBHOOK";

export type AuthType = "API_KEY" | "BEARER" | "OAUTH2" | "BASIC" | "JWT" | "CUSTOM_HEADER" | "HMAC";

export interface ApiProvider {
  id: string;
  instituteId: string;
  providerKey: string;
  displayName: string;
  category: ApiCategory;
  authType: AuthType;
  baseUrl: string;
  isEnabled: boolean;
  isDefault: boolean;
  failoverProviderId?: string;
  rateLimitPerMinute: number;
  timeoutSeconds: number;
  retryMaxAttempts: number;
  circuitBreakerThreshold: number;
  hasCredentials: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface ProviderTemplate {
  providerKey: string;
  displayName: string;
  category: ApiCategory;
  authType: AuthType;
  suggestedBaseUrl: string;
  requiredCredentialFields: string[];
  docUrl: string;
}

export interface ConnectionTestResult {
  isConnected: boolean;
  statusCode?: number;
  latencyMs: number;
  message: string;
  responsePreview?: string;
}

export interface ApiExecutionLog {
  id: string;
  providerId: string;
  endpointKey: string;
  category: ApiCategory;
  statusCode?: number;
  isSuccess: boolean;
  latencyMs: number;
  errorMessage?: string;
  retryCount: number;
  circuitBroken: boolean;
  requestTimestamp: string;
}

export interface WebhookRegistration {
  id: string;
  direction: "INCOMING" | "OUTGOING";
  eventType: string;
  targetUrl: string;
  signatureHeader: string;
  isActive: boolean;
  retryCount: number;
  createdAt: string;
}
