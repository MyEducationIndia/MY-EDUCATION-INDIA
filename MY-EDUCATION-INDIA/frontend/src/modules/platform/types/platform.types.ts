export interface PlatformDashboardMetrics {
  systemHealth: "HEALTHY" | "DEGRADED" | "DOWN";
  databaseStatus: string;
  apiStatus: string;
  storageUsedGb: number;
  storageQuotaGb: number;
  activeBackgroundJobs: number;
  failedJobsCount: number;
  lastBackupTimestamp?: string;
  recentAuditEventsCount: number;
  connectedIntegrationsCount: number;
  licenseStatus: string;
}

export interface SecurityPolicy {
  policyName: string;
  minPasswordLength: number;
  requireUppercase: boolean;
  requireNumbers: boolean;
  requireSpecialChars: boolean;
  passwordExpiryDays: number;
  maxFailedAttempts: number;
  lockoutDurationMinutes: number;
  sessionTimeoutMinutes: number;
  allowedIpRanges?: string[];
  enforce2fa: boolean;
}

export interface BackupRecord {
  id: string;
  jobName: string;
  backupType: "FULL" | "INCREMENTAL" | "DATABASE_ONLY" | "FILES_ONLY" | "CONFIG_ONLY";
  filePath: string;
  fileSizeBytes: number;
  status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED";
  checksumSha256: string;
  createdAt: string;
}

export interface FeatureFlag {
  id: string;
  flagKey: string;
  description?: string;
  isEnabled: boolean;
  rolloutPercentage: number;
  targetRoles?: string[];
  targetBranches?: string[];
}
