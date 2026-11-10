"""
Universal API Integration Framework - Models
Defines tables for API providers, encrypted credentials, endpoints,
execution logs, webhooks, and rate limits.
"""
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class ApiProvider(Base):
    __tablename__ = "api_providers"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    provider_key = Column(String(60), nullable=False, index=True) # e.g., fast2sms, twilio, sendgrid, razorpay
    display_name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False, index=True) # SMS, WHATSAPP, EMAIL, PUSH, PAYMENT, VIDEO, STORAGE, AI, MAPS, OTP, WEBHOOK
    auth_type = Column(String(50), default="API_KEY", nullable=False) # API_KEY, BEARER, OAUTH2, BASIC, JWT, CUSTOM_HEADER, HMAC
    base_url = Column(String(500), nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    failover_provider_id = Column(String(36), ForeignKey("api_providers.id"), nullable=True)
    rate_limit_per_minute = Column(Integer, default=120, nullable=False)
    timeout_seconds = Column(Integer, default=10, nullable=False)
    retry_max_attempts = Column(Integer, default=3, nullable=False)
    retry_backoff_factor = Column(Float, default=2.0, nullable=False)
    circuit_breaker_threshold = Column(Integer, default=5, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    credentials = relationship("ApiCredential", back_populates="provider", cascade="all, delete-orphan")
    endpoints = relationship("ApiEndpoint", back_populates="provider", cascade="all, delete-orphan")
    logs = relationship("ApiExecutionLog", back_populates="provider", cascade="all, delete-orphan")

class ApiCredential(Base):
    __tablename__ = "api_credentials"
    id = Column(String(36), primary_key=True)
    provider_id = Column(String(36), ForeignKey("api_providers.id"), nullable=False, index=True)
    institute_id = Column(String(36), nullable=False, index=True)
    credential_type = Column(String(50), default="STANDARD", nullable=False)
    encrypted_payload = Column(Text, nullable=False) # Encrypted JSON dictionary
    key_version = Column(Integer, default=1, nullable=False)
    last_rotated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    provider = relationship("ApiProvider", back_populates="credentials")

class ApiEndpoint(Base):
    __tablename__ = "api_endpoints"
    id = Column(String(36), primary_key=True)
    provider_id = Column(String(36), ForeignKey("api_providers.id"), nullable=False, index=True)
    endpoint_key = Column(String(100), nullable=False) # e.g. SEND_SMS, CREATE_ORDER, GENERATE_TEXT
    http_method = Column(String(10), default="POST", nullable=False) # GET, POST, PUT, DELETE
    path_template = Column(String(500), nullable=False)
    default_headers = Column(JSON, nullable=True)
    request_template_json = Column(JSON, nullable=True)
    response_mapping_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    provider = relationship("ApiProvider", back_populates="endpoints")

class ApiExecutionLog(Base):
    __tablename__ = "api_execution_logs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    provider_id = Column(String(36), ForeignKey("api_providers.id"), nullable=False, index=True)
    endpoint_key = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    is_success = Column(Boolean, default=True, nullable=False)
    latency_ms = Column(Float, default=0.0, nullable=False)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    circuit_broken = Column(Boolean, default=False, nullable=False)
    request_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    provider = relationship("ApiProvider", back_populates="logs")

class WebhookRegistration(Base):
    __tablename__ = "webhook_registrations"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    direction = Column(String(20), default="OUTGOING", nullable=False) # INCOMING, OUTGOING
    event_type = Column(String(100), nullable=False, index=True) # e.g. student.created, fee.received, exam.published
    target_url = Column(String(500), nullable=False)
    secret_token = Column(String(255), nullable=False)
    signature_header = Column(String(100), default="X-ERP-Signature", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    retry_count = Column(Integer, default=3, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    delivery_logs = relationship("WebhookDeliveryLog", back_populates="webhook", cascade="all, delete-orphan")

class WebhookDeliveryLog(Base):
    __tablename__ = "webhook_delivery_logs"
    id = Column(String(36), primary_key=True)
    webhook_id = Column(String(36), ForeignKey("webhook_registrations.id"), nullable=False, index=True)
    event_payload_json = Column(JSON, nullable=False)
    status_code = Column(Integer, nullable=True)
    response_body = Column(Text, nullable=True)
    is_success = Column(Boolean, default=False, nullable=False)
    attempt_number = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    webhook = relationship("WebhookRegistration", back_populates="delivery_logs")
