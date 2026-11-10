"""
API Integration Framework - Pydantic Schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ApiProviderBase(BaseModel):
    provider_key: str = Field(..., max_length=60)
    display_name: str = Field(..., max_length=150)
    category: str = Field(..., max_length=50) # SMS, WHATSAPP, EMAIL, PUSH, PAYMENT, VIDEO, STORAGE, AI, MAPS, OTP, WEBHOOK
    auth_type: str = "API_KEY" # API_KEY, BEARER, OAUTH2, BASIC, JWT, CUSTOM_HEADER, HMAC
    base_url: str = Field(..., max_length=500)
    is_enabled: bool = True
    is_default: bool = False
    failover_provider_id: Optional[str] = None
    rate_limit_per_minute: int = 120
    timeout_seconds: int = 10
    retry_max_attempts: int = 3
    retry_backoff_factor: float = 2.0
    circuit_breaker_threshold: int = 5

class ApiProviderCreate(ApiProviderBase):
    credentials_payload: Optional[Dict[str, str]] = None

class ApiProviderUpdate(BaseModel):
    display_name: Optional[str] = None
    auth_type: Optional[str] = None
    base_url: Optional[str] = None
    is_enabled: Optional[bool] = None
    is_default: Optional[bool] = None
    failover_provider_id: Optional[str] = None
    rate_limit_per_minute: Optional[int] = None
    timeout_seconds: Optional[int] = None
    retry_max_attempts: Optional[int] = None
    circuit_breaker_threshold: Optional[int] = None

class ApiProviderResponse(ApiProviderBase):
    id: str
    institute_id: str
    created_at: datetime
    updated_at: datetime
    has_credentials: bool = False

    class Config:
        orm_mode = True

class CredentialUpdateRequest(BaseModel):
    credentials: Dict[str, str]

class ConnectionTestRequest(BaseModel):
    endpoint_path: Optional[str] = None
    test_payload: Optional[Dict[str, Any]] = None

class ConnectionTestResponse(BaseModel):
    is_connected: bool
    status_code: Optional[int] = None
    latency_ms: float
    message: str
    response_preview: Optional[str] = None

class ApiExecutionLogResponse(BaseModel):
    id: str
    provider_id: str
    endpoint_key: str
    category: str
    status_code: Optional[int] = None
    is_success: bool
    latency_ms: float
    error_message: Optional[str] = None
    retry_count: int
    circuit_broken: bool
    request_timestamp: datetime

    class Config:
        orm_mode = True

class WebhookRegistrationCreate(BaseModel):
    direction: str = "OUTGOING"
    event_type: str = Field(..., max_length=100)
    target_url: str = Field(..., max_length=500)
    secret_token: Optional[str] = None
    signature_header: str = "X-ERP-Signature"
    is_active: bool = True
    retry_count: int = 3

class WebhookRegistrationResponse(WebhookRegistrationCreate):
    id: str
    institute_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class ProviderTemplate(BaseModel):
    provider_key: str
    display_name: str
    category: str
    auth_type: str
    suggested_base_url: str
    required_credential_fields: List[str]
    doc_url: str
