import { httpClient } from "@/api/httpClient";
import { ApiProvider, ProviderTemplate, ConnectionTestResult, ApiExecutionLog, WebhookRegistration } from "../types/integrations.types";

export const integrationService = {
  listProviders: async (category?: string): Promise<ApiProvider[]> => {
    const res = await httpClient.get<ApiProvider[]>("/integrations/providers", { params: { category } });
    return res.data;
  },

  listTemplates: async (): Promise<ProviderTemplate[]> => {
    const res = await httpClient.get<ProviderTemplate[]>("/integrations/templates");
    return res.data;
  },

  testConnection: async (providerId: string, endpointPath?: string): Promise<ConnectionTestResult> => {
    const res = await httpClient.post<ConnectionTestResult>(`/integrations/providers/${providerId}/test`, { endpoint_path: endpointPath });
    return res.data;
  },

  listLogs: async (): Promise<ApiExecutionLog[]> => {
    const res = await httpClient.get<ApiExecutionLog[]>("/integrations/logs");
    return res.data;
  },

  getAnalytics: async () => {
    const res = await httpClient.get("/integrations/analytics");
    return res.data;
  }
};
