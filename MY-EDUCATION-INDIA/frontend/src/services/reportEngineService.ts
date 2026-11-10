import { httpClient } from "@/api/httpClient";
import {
  CreateScheduledJobPayload,
  GeneratedReportData,
  GenerateReportPayload,
  ReportDefinitionItem,
  ReportEngineSummary,
  ReportExecutionLogItem,
  ScheduledReportJobItem,
} from "@/types/reportEngine.types";

export const reportEngineService = {
  async getSummary(): Promise<ReportEngineSummary> {
    const response = await httpClient.get<ReportEngineSummary>("/reports/summary");
    return response.data;
  },

  async listDefinitions(category?: string): Promise<ReportDefinitionItem[]> {
    const response = await httpClient.get<ReportDefinitionItem[]>("/reports/definitions", {
      params: category ? { category } : undefined,
    });
    return response.data;
  },

  async generateReport(payload: GenerateReportPayload): Promise<GeneratedReportData> {
    const response = await httpClient.post<GeneratedReportData>("/reports/generate", payload);
    return response.data;
  },

  async listExecutions(limit?: number): Promise<ReportExecutionLogItem[]> {
    const response = await httpClient.get<ReportExecutionLogItem[]>("/reports/executions", {
      params: limit ? { limit } : undefined,
    });
    return response.data;
  },

  async listScheduledJobs(): Promise<ScheduledReportJobItem[]> {
    const response = await httpClient.get<ScheduledReportJobItem[]>("/reports/scheduled-jobs");
    return response.data;
  },

  async createScheduledJob(payload: CreateScheduledJobPayload): Promise<ScheduledReportJobItem> {
    const response = await httpClient.post<ScheduledReportJobItem>(
      "/reports/scheduled-jobs",
      payload
    );
    return response.data;
  },
};
