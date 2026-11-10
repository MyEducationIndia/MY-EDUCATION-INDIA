export interface PlatformDashboardMetrics {
  system_health: string;
  database_status: string;
  api_status: string;
  storage_used_gb: number;
  storage_quota_gb: number;
  active_background_jobs: number;
  failed_jobs_count: number;
  last_backup_timestamp: string;
  recent_audit_events_count: number;
  connected_integrations_count: number;
  license_status: string;
}

export interface BackupItem {
  id: string;
  job_name: string;
  backup_type: "FULL" | "INCREMENTAL" | "DATABASE_ONLY" | "FILES_ONLY";
  file_path: string;
  file_size_bytes: number;
  file_size_formatted: string;
  status: "COMPLETED" | "RUNNING" | "FAILED";
  checksum_sha256: string;
  storage_destination: "LOCAL" | "AWS_S3" | "CLOUDFLARE_R2";
  created_at: string;
}

export interface CacheStats {
  cache_engine: string;
  status: string;
  hit_ratio_percentage: number;
  total_keys: number;
  used_memory_human: string;
  uptime_days: number;
  connected_clients: number;
  eviction_policy: string;
}

export interface WorkerQueueTelemetry {
  active_workers_count: number;
  worker_nodes: {
    worker_id: string;
    status: string;
    active_tasks: number;
    processed_total: number;
  }[];
  queue_depth: Record<string, number>;
  failed_tasks_count: number;
}

export interface ServerResources {
  server_hostname: string;
  operating_system: string;
  cpu_usage_percentage: number;
  cpu_cores: number;
  ram_used_gb: number;
  ram_total_gb: number;
  ram_usage_percentage: number;
  disk_used_gb: number;
  disk_total_gb: number;
  disk_usage_percentage: number;
  postgresql_connections_active: number;
  postgresql_connections_max: number;
  network_rx_mbps: number;
  network_tx_mbps: number;
}

export interface SecurityPolicy {
  policy_name: string;
  min_password_length: number;
  require_uppercase: boolean;
  require_numbers: boolean;
  require_special_chars: boolean;
  password_expiry_days: number;
  max_failed_attempts: number;
  lockout_duration_minutes: number;
  session_timeout_minutes: number;
  enforce_2fa: boolean;
  allowed_ip_ranges: string[];
}

export interface MaintenanceWindowState {
  is_active: boolean;
  title: string;
  start_time: string;
  end_time: string;
  custom_banner_message: string;
  whitelist_ips: string[];
}

export interface FeatureFlagItem {
  id: string;
  flag_key: string;
  description: string;
  is_enabled: boolean;
  rollout_percentage: number;
  target_roles: string[];
}
