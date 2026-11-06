import { httpClient } from "@/api/httpClient";
import { AuditLogEntry } from "@/types/audit.types";
import { PaginatedResponse } from "@/types/common.types";

export const auditService = {
  async listAuditLogs(params: {
    institute_id?: string;
    module_key?: string;
    action?: string;
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
