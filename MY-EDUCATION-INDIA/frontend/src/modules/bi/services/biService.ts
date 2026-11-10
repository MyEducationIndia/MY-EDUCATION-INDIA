import { httpClient } from "@/api/httpClient";
import { ReportDefinition, KpiDefinition, ExecutiveDashboardMetrics, SystemHealthOverview } from "../types/bi.types";

export const biService = {
  getExecutiveDashboard: async (): Promise<ExecutiveDashboardMetrics> => {
    const res = await httpClient.get<ExecutiveDashboardMetrics>("/bi/dashboard/executive");
    return res.data;
  },

  listReports: async (category?: string): Promise<ReportDefinition[]> => {
    const res = await httpClient.get<ReportDefinition[]>("/bi/reports", { params: { category } });
    return res.data;
  },

  listKpis: async (): Promise<KpiDefinition[]> => {
    const res = await httpClient.get<KpiDefinition[]>("/bi/kpis");
    return res.data;
  },

  getSystemHealth: async (): Promise<SystemHealthOverview> => {
    const res = await httpClient.get<SystemHealthOverview>("/bi/system-health");
    return res.data;
  }
};
