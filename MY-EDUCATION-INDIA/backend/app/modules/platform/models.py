"""
Module 19: Enterprise Platform Administration, Security, Backup & DevOps - Models
Provisions 17 enterprise tables for system settings, security policies,
backup & disaster recovery, audit events, API keys, feature flags, storage,
caching, cluster health, licenses, and maintenance windows.
"""
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON, Index
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class PlatformSetting(Base):
    __tablename__ = "platform_settings"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    setting_key = Column(String(100), nullable=False, index=True)
    setting_value = Column(Text, nullable=False)
    category = Column(String(50), default="GENERAL", nullable=False) # BRANDING, LOCALIZATION, DATE_TIME, SECURITY, STORAGE, MAINTENANCE
    is_system = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SecurityPolicy(Base):
    __tablename__ = "security_policies"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    policy_name = Column(String(100), nullable=False)
    min_password_length = Column(Integer, default=10, nullable=False)
    require_uppercase = Column(Boolean, default=True, nullable=False)
    require_numbers = Column(Boolean, default=True, nullable=False)
    require_special_chars = Column(Boolean, default=True, nullable=False)
    password_expiry_days = Column(Integer, default=90, nullable=False)
    max_failed_attempts = Column(Integer, default=5, nullable=False)
    lockout_duration_minutes = Column(Integer, default=30, nullable=False)
    session_timeout_minutes = Column(Integer, default=60, nullable=False)
    allowed_ip_ranges = Column(JSON, nullable=True) # ["192.168.1.0/24", "10.0.0.0/8"]
    enforce_2fa = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class BackupJob(Base):
    __tablename__ = "backup_jobs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    job_name = Column(String(150), nullable=False)
    backup_type = Column(String(50), default="FULL", nullable=False) # FULL, INCREMENTAL, DATABASE_ONLY, FILES_ONLY, CONFIG_ONLY
    schedule_cron = Column(String(50), default="0 2 * * *", nullable=False)
    storage_destination = Column(String(50), default="LOCAL", nullable=False) # LOCAL, AWS_S3, CLOUDFLARE_R2
    is_encrypted = Column(Boolean, default=True, nullable=False)
    compression_algorithm = Column(String(20), default="GZIP", nullable=False) # GZIP, ZSTD
    retention_days = Column(Integer, default=30, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    history = relationship("BackupHistory", back_populates="job", cascade="all, delete-orphan")

class BackupHistory(Base):
    __tablename__ = "backup_history"
    id = Column(String(36), primary_key=True)
    job_id = Column(String(36), ForeignKey("backup_jobs.id"), nullable=True, index=True)
    institute_id = Column(String(36), nullable=False, index=True)
    backup_type = Column(String(50), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, default=0, nullable=False)
    checksum_sha256 = Column(String(64), nullable=False)
    status = Column(String(30), default="COMPLETED", nullable=False) # PENDING, RUNNING, COMPLETED, FAILED
    duration_seconds = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    job = relationship("BackupJob", back_populates="history")
    restores = relationship("RestoreHistory", back_populates="backup", cascade="all, delete-orphan")

class RestoreHistory(Base):
    __tablename__ = "restore_history"
    id = Column(String(36), primary_key=True)
    backup_id = Column(String(36), ForeignKey("backup_history.id"), nullable=False, index=True)
    institute_id = Column(String(36), nullable=False, index=True)
    restored_by_user_id = Column(String(36), nullable=False)
    restore_scope = Column(String(50), default="ENTIRE_SYSTEM", nullable=False) # ENTIRE_SYSTEM, DATABASE_ONLY, FILES_ONLY, MODULE_ONLY
    status = Column(String(30), default="COMPLETED", nullable=False) # PENDING, IN_PROGRESS, COMPLETED, FAILED
    dry_run = Column(Boolean, default=False, nullable=False)
    logs_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    backup = relationship("BackupHistory", back_populates="restores")

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True) # LOGIN, CONFIG_CHANGE, FINANCIAL, DATA_EXPORT, CERTIFICATE, PERMISSION_CHANGE
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100), nullable=True)
    old_values_json = Column(JSON, nullable=True)
    new_values_json = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class SystemLog(Base):
    __tablename__ = "system_logs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    log_level = Column(String(20), default="INFO", nullable=False) # DEBUG, INFO, WARN, ERROR, CRITICAL
    subsystem = Column(String(50), nullable=False, index=True) # BACKEND, WORKER, DATABASE, STORAGE, INTEGRATION
    message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    key_name = Column(String(100), nullable=False)
    key_prefix = Column(String(16), nullable=False, index=True) # first 8 chars for lookup
    hashed_secret = Column(String(128), nullable=False)
    scopes = Column(JSON, nullable=False) # ["students:read", "fees:write", "attendance:read"]
    rate_limit_rpm = Column(Integer, default=120, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class ApiUsageLog(Base):
    __tablename__ = "api_usage_logs"
    id = Column(String(36), primary_key=True)
    api_key_id = Column(String(36), ForeignKey("api_keys.id"), nullable=False, index=True)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    latency_ms = Column(Float, default=0.0, nullable=False)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class IntegrationConfig(Base):
    __tablename__ = "integration_configs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    service_type = Column(String(50), nullable=False) # SMS, WHATSAPP, EMAIL, PAYMENT, VIDEO, STORAGE, AI
    provider_name = Column(String(100), nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    config_payload = Column(JSON, nullable=True)
    status = Column(String(30), default="CONNECTED", nullable=False) # CONNECTED, ERROR, UNTESTED
    last_tested_at = Column(DateTime, nullable=True)

class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    flag_key = Column(String(100), nullable=False, index=True) # e.g. BETA_NEW_CBT_UI, ADMISSION_ONLINE_PAYMENT
    description = Column(Text, nullable=True)
    is_enabled = Column(Boolean, default=False, nullable=False)
    rollout_percentage = Column(Float, default=100.0, nullable=False)
    target_roles = Column(JSON, nullable=True) # ["SUPER_ADMIN", "STUDENT"]
    target_branches = Column(JSON, nullable=True) # ["branch_01", "branch_02"]
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class StorageConfig(Base):
    __tablename__ = "storage_configs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    storage_provider = Column(String(50), default="LOCAL", nullable=False) # LOCAL, AWS_S3, CLOUDFLARE_R2, MINIO
    bucket_name = Column(String(150), nullable=True)
    region = Column(String(50), nullable=True)
    endpoint_url = Column(String(255), nullable=True)
    quota_bytes = Column(Integer, default=107374182400, nullable=False) # 100 GB default
    used_bytes = Column(Integer, default=0, nullable=False)
    cleanup_rules_json = Column(JSON, nullable=True)
    is_default = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class CacheLog(Base):
    __tablename__ = "cache_logs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    operation = Column(String(30), nullable=False) # CLEAR, WARM, EVICT
    cache_key_pattern = Column(String(255), nullable=False)
    affected_keys_count = Column(Integer, default=0, nullable=False)
    triggered_by_user_id = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    component_name = Column(String(50), nullable=False, index=True)
    status = Column(String(20), default="HEALTHY", nullable=False)
    latency_ms = Column(Float, default=0.0, nullable=False)
    details_json = Column(JSON, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LicenseSetting(Base):
    __tablename__ = "license_settings"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    license_key = Column(String(255), nullable=False)
    plan_name = Column(String(100), default="ENTERPRISE_LIFETIME", nullable=False)
    max_students = Column(Integer, default=10000, nullable=False)
    max_branches = Column(Integer, default=25, nullable=False)
    max_storage_gb = Column(Integer, default=500, nullable=False)
    features_allowed = Column(JSON, nullable=True)
    valid_until = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

class MaintenanceWindow(Base):
    __tablename__ = "maintenance_windows"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    whitelist_user_ids = Column(JSON, nullable=True)
    custom_banner_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class PlatformReport(Base):
    __tablename__ = "platform_reports"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_name = Column(String(150), nullable=False)
    report_type = Column(String(50), nullable=False) # BACKUP_AUDIT, SECURITY_SUMMARY, STORAGE_USAGE, API_ANALYTICS
    filters = Column(JSON, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
