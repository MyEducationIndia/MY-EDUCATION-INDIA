import { httpClient } from "@/api/httpClient";
import { AuditLogEntry, AuditLogSummary } from "@/types/audit.types";
import { PaginatedResponse } from "@/types/common.types";

export const auditService = {
  async getSummary(instituteId?: string): Promise<AuditLogSummary> {
    const response = await httpClient.get<AuditLogSummary>("/audit-logs/summary", {
      params: instituteId ? { institute_id: instituteId } : undefined,
    });
    return response.data;
  },

  async listAuditLogs(params: {
    institute_id?: string;
    event_category?: string;
    severity?: string;
    module_key?: string;
    actor_username?: string;
    search?: string;
    page: number;
    page_size: number;
  }): Promise<PaginatedResponse<AuditLogEntry>> {
    const response = await httpClient.get<PaginatedResponse<AuditLogEntry>>(
      "/audit-logs",
      { params }
    );
    return response.data;
  },
};
