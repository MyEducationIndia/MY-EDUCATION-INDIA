import { httpClient } from "@/api/httpClient";
import { PlatformDashboardMetrics, SecurityPolicy, BackupRecord, FeatureFlag } from "../types/platform.types";

export const platformService = {
  getDashboardMetrics: async (): Promise<PlatformDashboardMetrics> => {
    const res = await httpClient.get<PlatformDashboardMetrics>("/platform/dashboard");
    return res.data;
  },

  getSecurityPolicy: async (): Promise<SecurityPolicy> => {
    const res = await httpClient.get<SecurityPolicy>("/platform/security/policy");
    return res.data;
  },

  listBackups: async (): Promise<BackupRecord[]> => {
    const res = await httpClient.get<BackupRecord[]>("/platform/backups");
    return res.data;
  },

  listFeatureFlags: async (): Promise<FeatureFlag[]> => {
    const res = await httpClient.get<FeatureFlag[]>("/platform/feature-flags");
    return res.data;
  },

  dryRunRestore: async (backupId: string, scope: string = "ENTIRE_SYSTEM") => {
    const res = await httpClient.post("/platform/restores/dry-run", {
      backup_id: backupId,
      restore_scope: scope,
      dry_run: true
    });
    return res.data;
  }
};
