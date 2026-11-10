import { httpClient } from "@/services/httpClient";
import {
  PlatformDashboardMetrics,
  BackupItem,
  CacheStats,
  WorkerQueueTelemetry,
  ServerResources,
  SecurityPolicy,
  MaintenanceWindowState,
  FeatureFlagItem,
} from "@/types/platform.types";

export const platformService = {
  // Dashboard & Health
  async getDashboard(): Promise<PlatformDashboardMetrics> {
    const res = await httpClient.get<PlatformDashboardMetrics>("/platform/dashboard");
    return res.data;
  },

  // Backups & Restores
  async listBackups(): Promise<BackupItem[]> {
    const res = await httpClient.get<BackupItem[]>("/platform/backups");
    return res.data;
  },

  async triggerBackup(payload: { job_name?: string; backup_type?: string; storage_destination?: string }): Promise<BackupItem> {
    const res = await httpClient.post<BackupItem>("/platform/backups", payload);
    return res.data;
  },

  async deleteBackup(id: string): Promise<void> {
    await httpClient.delete(`/platform/backups/${id}`);
  },

  async dryRunRestore(backupId: string, scope: string = "ENTIRE_SYSTEM"): Promise<any> {
    const res = await httpClient.post("/platform/restores/dry-run", {
      backup_id: backupId,
      restore_scope: scope,
    });
    return res.data;
  },

  // Cache Engine
  async getCacheStats(): Promise<CacheStats> {
    const res = await httpClient.get<CacheStats>("/platform/cache/stats");
    return res.data;
  },

  async flushCache(pattern: string = "*"): Promise<any> {
    const res = await httpClient.post("/platform/cache/flush", { pattern });
    return res.data;
  },

  // Worker Queue
  async getWorkerQueue(): Promise<WorkerQueueTelemetry> {
    const res = await httpClient.get<WorkerQueueTelemetry>("/platform/workers/queue");
    return res.data;
  },

  async retryFailedTasks(): Promise<any> {
    const res = await httpClient.post("/platform/workers/retry-failed");
    return res.data;
  },

  // Server Resources
  async getServerResources(): Promise<ServerResources> {
    const res = await httpClient.get<ServerResources>("/platform/server/resources");
    return res.data;
  },

  // Security Policy
  async getSecurityPolicy(): Promise<SecurityPolicy> {
    const res = await httpClient.get<SecurityPolicy>("/platform/security/policy");
    return res.data;
  },

  async updateSecurityPolicy(payload: Partial<SecurityPolicy>): Promise<SecurityPolicy> {
    const res = await httpClient.patch<SecurityPolicy>("/platform/security/policy", payload);
    return res.data;
  },

  // Maintenance Windows
  async getMaintenanceWindow(): Promise<MaintenanceWindowState> {
    const res = await httpClient.get<MaintenanceWindowState>("/platform/maintenance");
    return res.data;
  },

  async toggleMaintenanceWindow(payload: Partial<MaintenanceWindowState>): Promise<MaintenanceWindowState> {
    const res = await httpClient.post<MaintenanceWindowState>("/platform/maintenance", payload);
    return res.data;
  },

  // Feature Flags
  async listFeatureFlags(): Promise<FeatureFlagItem[]> {
    const res = await httpClient.get<FeatureFlagItem[]>("/platform/feature-flags");
    return res.data;
  },

  async createFeatureFlag(payload: Partial<FeatureFlagItem>): Promise<FeatureFlagItem> {
    const res = await httpClient.post<FeatureFlagItem>("/platform/feature-flags", payload);
    return res.data;
  },

  async toggleFeatureFlag(id: string, is_enabled: boolean): Promise<FeatureFlagItem> {
    const res = await httpClient.patch<FeatureFlagItem>(`/platform/feature-flags/${id}`, { is_enabled });
    return res.data;
  },
};
