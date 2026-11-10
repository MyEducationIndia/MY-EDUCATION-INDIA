import { httpClient } from "@/services/httpClient";
import {
  ExecutiveDashboardMetrics,
  KpiDefinition,
  ReportDefinition,
  TrendChartsData,
  CohortRetentionData,
  NirfNaacDossierData,
  SystemHealthOverview,
} from "@/types/bi.types";

export const biService = {
  // Executive Dashboard
  async getExecutiveDashboard(): Promise<ExecutiveDashboardMetrics> {
    const res = await httpClient.get<ExecutiveDashboardMetrics>("/bi/dashboard/executive");
    return res.data;
  },

  // KPIs
  async listKpis(): Promise<KpiDefinition[]> {
    const res = await httpClient.get<KpiDefinition[]>("/bi/kpis");
    return res.data;
  },

  async createKpi(payload: Partial<KpiDefinition>): Promise<KpiDefinition> {
    const res = await httpClient.post<KpiDefinition>("/bi/kpis", payload);
    return res.data;
  },

  // Reports
  async listReports(category?: string): Promise<ReportDefinition[]> {
    const res = await httpClient.get<ReportDefinition[]>("/bi/reports", {
      params: category && category !== "ALL" ? { category } : undefined,
    });
    return res.data;
  },

  async createReport(payload: Partial<ReportDefinition>): Promise<ReportDefinition> {
    const res = await httpClient.post<ReportDefinition>("/bi/reports", payload);
    return res.data;
  },

  async deleteReport(id: string): Promise<void> {
    await httpClient.delete(`/bi/reports/${id}`);
  },

  async exportReport(id: string, format: string = "PDF"): Promise<any> {
    const res = await httpClient.post(`/bi/reports/${id}/export`, { format });
    return res.data;
  },

  // Trends & Cohorts
  async getTrendCharts(): Promise<TrendChartsData> {
    const res = await httpClient.get<TrendChartsData>("/bi/charts/trends");
    return res.data;
  },

  async getCohortRetention(): Promise<CohortRetentionData> {
    const res = await httpClient.get<CohortRetentionData>("/bi/cohort-retention");
    return res.data;
  },

  async getNirfNaacDossier(): Promise<NirfNaacDossierData> {
    const res = await httpClient.get<NirfNaacDossierData>("/bi/nirf-naac-dossier");
    return res.data;
  },

  async getSystemHealth(): Promise<SystemHealthOverview> {
    const res = await httpClient.get<SystemHealthOverview>("/bi/system-health");
    return res.data;
  },
};
