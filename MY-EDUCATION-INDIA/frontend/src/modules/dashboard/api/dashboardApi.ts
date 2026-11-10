import { httpClient } from "@/api/httpClient";
import {
  DashboardActivityItem,
  DashboardBootstrapPayload,
  DashboardKPIStats,
  GlobalSearchData,
  MultiChartData,
  NotificationItem,
  SystemHealthData,
  WidgetConfig,
} from "../types/dashboard.types";

export const dashboardApi = {
  async getDashboardSummary(params?: {
    granularity?: string;
    instituteId?: string;
    branchId?: string;
  }): Promise<DashboardBootstrapPayload> {
    const res = await httpClient.get<DashboardBootstrapPayload>("/dashboard", {
      params: {
        granularity: params?.granularity || "MONTHLY",
        institute_id: params?.instituteId,
        branch_id: params?.branchId,
      },
    });
    return res.data;
  },

  async getKPIStats(params?: { instituteId?: string; branchId?: string }): Promise<DashboardKPIStats> {
    const res = await httpClient.get<DashboardKPIStats>("/dashboard/stats", {
      params: { institute_id: params?.instituteId, branch_id: params?.branchId },
    });
    return res.data;
  },

  async getCharts(granularity: string = "MONTHLY", instituteId?: string): Promise<MultiChartData> {
    const res = await httpClient.get<MultiChartData>("/dashboard/charts", {
      params: { granularity, institute_id: instituteId },
    });
    return res.data;
  },

  async searchGlobal(q: string, instituteId?: string): Promise<GlobalSearchData> {
    const res = await httpClient.get<GlobalSearchData>("/dashboard/search", {
      params: { q, institute_id: instituteId },
    });
    return res.data;
  },

  async getActivities(instituteId?: string, limit: number = 15): Promise<DashboardActivityItem[]> {
    const res = await httpClient.get<DashboardActivityItem[]>("/dashboard/activities", {
      params: { institute_id: instituteId, limit },
    });
    return res.data;
  },

  async listNotifications(unreadOnly: boolean = false): Promise<NotificationItem[]> {
    const res = await httpClient.get<NotificationItem[]>("/dashboard/notifications", {
      params: { unread_only: unreadOnly },
    });
    return res.data;
  },

  async markNotificationRead(id: string): Promise<NotificationItem> {
    const res = await httpClient.patch<NotificationItem>(`/dashboard/notifications/${id}/read`, {});
    return res.data;
  },

  async markAllNotificationsRead(): Promise<void> {
    await httpClient.post("/dashboard/notifications/read-all", {});
  },

  async getSystemHealth(): Promise<SystemHealthData> {
    const res = await httpClient.get<SystemHealthData>("/dashboard/system-health");
    return res.data;
  },

  async updateWidgets(widgets: WidgetConfig[]): Promise<WidgetConfig[]> {
    const res = await httpClient.put<WidgetConfig[]>("/dashboard/widgets", { widgets });
    return res.data;
  },
};
