"""
Module 19: Platform Admin & DevOps Schemas (Pydantic v2 / v1 compatible)
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field

class PlatformSettingBase(BaseModel):
    setting_key: str = Field(..., max_length=100)
    setting_value: str
    category: str = "GENERAL"
    is_system: bool = False

class PlatformSettingCreate(PlatformSettingBase):
    pass

class PlatformSettingResponse(PlatformSettingBase):
    id: str
    institute_id: str
    updated_at: datetime

    class Config:
        orm_mode = True

class SecurityPolicyCreate(BaseModel):
    policy_name: str = Field(..., max_length=100)
    min_password_length: int = 10
    require_uppercase: bool = True
    require_numbers: bool = True
    require_special_chars: bool = True
    password_expiry_days: int = 90
    max_failed_attempts: int = 5
    lockout_duration_minutes: int = 30
    session_timeout_minutes: int = 60
    allowed_ip_ranges: Optional[List[str]] = None
    enforce_2fa: bool = False

class SecurityPolicyResponse(SecurityPolicyCreate):
    id: str
    institute_id: str
    updated_at: datetime

    class Config:
        orm_mode = True

class BackupJobCreate(BaseModel):
    job_name: str = Field(..., max_length=150)
    backup_type: str = "FULL" # FULL, INCREMENTAL, DATABASE_ONLY, FILES_ONLY, CONFIG_ONLY
    schedule_cron: str = "0 2 * * *"
    storage_destination: str = "LOCAL" # LOCAL, AWS_S3, CLOUDFLARE_R2
    is_encrypted: bool = True
    compression_algorithm: str = "GZIP"
    retention_days: int = 30
    is_active: bool = True

class BackupJobResponse(BackupJobCreate):
    id: str
    institute_id: str
    last_run_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        orm_mode = True

class TriggerRestoreRequest(BaseModel):
    backup_id: str
    restore_scope: str = "ENTIRE_SYSTEM" # ENTIRE_SYSTEM, DATABASE_ONLY, FILES_ONLY, MODULE_ONLY
    dry_run: bool = True

class FeatureFlagCreate(BaseModel):
    flag_key: str = Field(..., max_length=100)
    description: Optional[str] = None
    is_enabled: bool = False
    rollout_percentage: float = 100.0
    target_roles: Optional[List[str]] = None
    target_branches: Optional[List[str]] = None

class FeatureFlagResponse(FeatureFlagCreate):
    id: str
    institute_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LicenseSettingResponse(BaseModel):
    license_key: str
    plan_name: str
    max_students: int
    max_branches: int
    max_storage_gb: int
    features_allowed: Optional[List[str]] = None
    valid_until: Optional[date] = None
    is_active: bool

class MaintenanceWindowCreate(BaseModel):
    title: str = Field(..., max_length=200)
    start_time: datetime
    end_time: datetime
    whitelist_user_ids: Optional[List[str]] = None
    custom_banner_message: Optional[str] = None

class PlatformDashboardMetrics(BaseModel):
    system_health: str # HEALTHY, DEGRADED, DOWN
    database_status: str
    api_status: str
    storage_used_gb: float
    storage_quota_gb: float
    active_background_jobs: int
    failed_jobs_count: int
    last_backup_timestamp: Optional[datetime] = None
    recent_audit_events_count: int
    connected_integrations_count: int
    license_status: str
