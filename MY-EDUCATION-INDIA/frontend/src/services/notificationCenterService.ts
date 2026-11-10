import { httpClient } from "@/api/httpClient";
import {
  CreateDispatchPayload,
  CreateTemplatePayload,
  NotificationCenterSummary,
  NotificationDeliveryReportItem,
  NotificationDispatchItem,
  NotificationTemplateItem,
  UpdateTemplatePayload,
} from "@/types/notificationCenter.types";

export const notificationCenterService = {
  async getSummary(): Promise<NotificationCenterSummary> {
    const response = await httpClient.get<NotificationCenterSummary>(
      "/notification-center/summary"
    );
    return response.data;
  },

  async listTemplates(category?: string): Promise<NotificationTemplateItem[]> {
    const response = await httpClient.get<NotificationTemplateItem[]>(
      "/notification-center/templates",
      {
        params: category ? { category } : undefined,
      }
    );
    return response.data;
  },

  async createTemplate(
    payload: CreateTemplatePayload
  ): Promise<NotificationTemplateItem> {
    const response = await httpClient.post<NotificationTemplateItem>(
      "/notification-center/templates",
      payload
    );
    return response.data;
  },

  async updateTemplate(
    templateId: string,
    payload: UpdateTemplatePayload
  ): Promise<NotificationTemplateItem> {
    const response = await httpClient.patch<NotificationTemplateItem>(
      `/notification-center/templates/${templateId}`,
      payload
    );
    return response.data;
  },

  async deleteTemplate(
    templateId: string
  ): Promise<{ status: string; message: string }> {
    const response = await httpClient.delete<{ status: string; message: string }>(
      `/notification-center/templates/${templateId}`
    );
    return response.data;
  },

  async createDispatch(
    payload: CreateDispatchPayload
  ): Promise<NotificationDispatchItem> {
    const response = await httpClient.post<NotificationDispatchItem>(
      "/notification-center/dispatches",
      payload
    );
    return response.data;
  },

  async listDispatches(limit?: number): Promise<NotificationDispatchItem[]> {
    const response = await httpClient.get<NotificationDispatchItem[]>(
      "/notification-center/dispatches",
      {
        params: limit ? { limit } : undefined,
      }
    );
    return response.data;
  },

  async listDeliveryReports(
    dispatchId: string
  ): Promise<NotificationDeliveryReportItem[]> {
    const response = await httpClient.get<NotificationDeliveryReportItem[]>(
      `/notification-center/dispatches/${dispatchId}/delivery-reports`
    );
    return response.data;
  },
};
