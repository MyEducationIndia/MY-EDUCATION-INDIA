import { httpClient } from "@/services/httpClient";
import {
  ApiProvider,
  ProviderTemplate,
  ConnectionTestRequest,
  ConnectionTestResponse,
  CredentialUpdateRequest,
  ApiExecutionLog,
  WebhookRegistration,
  IntegrationAnalytics,
} from "@/types/integration.types";

export const integrationService = {
  // Health & Catalog
  async getHealth(): Promise<{ status: string; framework: string; supported_categories: string[] }> {
    const res = await httpClient.get("/integrations/health");
    return res.data;
  },

  async getTemplates(): Promise<ProviderTemplate[]> {
    const res = await httpClient.get<ProviderTemplate[]>("/integrations/templates");
    return res.data;
  },

  // Providers Management
  async listProviders(category?: string): Promise<ApiProvider[]> {
    const res = await httpClient.get<ApiProvider[]>("/integrations/providers", {
      params: category && category !== "ALL" ? { category } : undefined,
    });
    return res.data;
  },

  async createProvider(payload: Partial<ApiProvider> & { credentials_payload?: Record<string, string> }): Promise<ApiProvider> {
    const res = await httpClient.post<ApiProvider>("/integrations/providers", payload);
    return res.data;
  },

  async updateProvider(id: string, payload: Partial<ApiProvider>): Promise<ApiProvider> {
    const res = await httpClient.patch<ApiProvider>(`/integrations/providers/${id}`, payload);
    return res.data;
  },

  async deleteProvider(id: string): Promise<void> {
    await httpClient.delete(`/integrations/providers/${id}`);
  },

  // Connection Handshake Test
  async testProviderConnection(
    id: string,
    payload: ConnectionTestRequest = {}
  ): Promise<ConnectionTestResponse> {
    const res = await httpClient.post<ConnectionTestResponse>(
      `/integrations/providers/${id}/test`,
      payload
    );
    return res.data;
  },

  // Encrypted Credential Vault
  async updateCredentials(
    id: string,
    credentials: Record<string, string>
  ): Promise<{ status: string; message: string }> {
    const res = await httpClient.post<{ status: string; message: string }>(
      `/integrations/providers/${id}/credentials`,
      { credentials }
    );
    return res.data;
  },

  // Webhooks
  async listWebhooks(): Promise<WebhookRegistration[]> {
    const res = await httpClient.get<WebhookRegistration[]>("/integrations/webhooks");
    return res.data;
  },

  async createWebhook(payload: Partial<WebhookRegistration>): Promise<WebhookRegistration> {
    const res = await httpClient.post<WebhookRegistration>("/integrations/webhooks", payload);
    return res.data;
  },

  async deleteWebhook(id: string): Promise<void> {
    await httpClient.delete(`/integrations/webhooks/${id}`);
  },

  async testWebhook(id: string): Promise<any> {
    const res = await httpClient.post(`/integrations/webhooks/${id}/test`);
    return res.data;
  },

  // Telemetry & Logs
  async listLogs(limit: number = 50): Promise<ApiExecutionLog[]> {
    const res = await httpClient.get<ApiExecutionLog[]>("/integrations/logs", {
      params: { limit },
    });
    return res.data;
  },

  // Analytics
  async getAnalytics(): Promise<IntegrationAnalytics> {
    const res = await httpClient.get<IntegrationAnalytics>("/integrations/analytics");
    return res.data;
  },
};
