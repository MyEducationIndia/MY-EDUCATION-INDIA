# MY EDUCATION INDIA ERP V2 — FUTURE API INTEGRATION FRAMEWORK
## UNIVERSAL PROVIDER INTEGRATION FRAMEWORK & CREDENTIAL VAULT

### 1. Executive Summary & Architectural Philosophy
The **Universal API Integration Framework** transforms MY EDUCATION INDIA ERP V2 into an **API-first, vendor-agnostic institution platform**. Rather than hardcoding communication gateways or third-party cloud services directly into business logic, all external outbound and inbound API traffic is decoupled through a **Universal Provider Integration Framework**.

Administrators can dynamically register, reconfigure, swap, enable/disable, and rotate credentials for any external API provider from the Admin Console without modifying or recompiling source code.

#### Key Architectural Highlights
- **Universal Provider Registry**: Built-in dynamic catalog supporting 10 core integration categories:
  - **SMS Gateways**: Fast2SMS, MSG91, Twilio, Textlocal, Gupshup, AWS SNS, custom REST.
  - **WhatsApp Business**: Meta WhatsApp Cloud API, Twilio WhatsApp, Interakt, AiSensy, Gupshup, WATI.
  - **Email Gateways**: SMTP, Microsoft 365, SendGrid, Amazon SES, Mailgun, Postmark.
  - **Push Notifications**: Firebase Cloud Messaging (FCM), OneSignal, Apple Push Notification service (APNs), Web Push.
  - **Payment Gateways**: Razorpay, Cashfree, PhonePe, Paytm, Stripe, PayPal.
  - **Video Conferencing**: Zoom, Google Meet, Microsoft Teams, Jitsi, BigBlueButton.
  - **Object Storage**: AWS S3, Cloudflare R2, Google Cloud Storage, Azure Blob Storage, MinIO.
  - **Artificial Intelligence**: OpenAI (GPT-4o), Google Gemini, Anthropic Claude, Grok, DeepSeek, OpenRouter, Ollama (local private).
  - **Geographic & Maps**: Google Maps Platform, Mapbox, OpenStreetMap, HERE Maps.
  - **One-Time Password (OTP)**: SMS OTP, Email OTP, WhatsApp OTP, TOTP.
  - **Webhooks**: Dynamic Inbound and Outbound event streams with HMAC-SHA256 signature verification.
- **Enterprise Credential Vault**: Symmetric encryption for tokens, passwords, private keys, and secrets. Passwords and API keys are masked (`****`) and never sent to frontend client code.
- **Circuit Breaker Pattern**: Automatic failure isolation (`CLOSED` → `OPEN` → `HALF_OPEN`) preventing cascade failures when downstream cloud providers experience outages.
- **Token Bucket Rate Limiter**: Configurable per-provider rate limits preventing quota burn or API suspension.
- **Zero Client-Side Storage**: Complete compliance with ERP security guidelines: zero usage of `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 2. Database Schema (6 Relational Tables)
Provisioned via Alembic revision `0016_api_framework`:
1. `api_providers`: Provider definition, category, auth type, base URL, rate limits, timeout, retry policy, circuit breaker threshold, failover provider pointer.
2. `api_credentials`: Encrypted credential payloads, key version numbers, and last rotation timestamps.
3. `api_endpoints`: HTTP methods, URL path templates, default headers, and JSON request/response schema maps.
4. `api_execution_logs`: Execution audit trail capturing HTTP status codes, latency in milliseconds, error messages, retry counts, and circuit breaker trip events.
5. `webhook_registrations`: Inbound and outbound webhook configurations, event types, target URLs, secret tokens, and signature headers.
6. `webhook_delivery_logs`: Delivery attempts, HTTP status codes, response previews, and delivery outcomes.

---

### 3. Core Framework Components
- **Credential Vault (`vault.py`)**:
  - Secure key derivation.
  - Encryption and decryption of provider credentials.
  - Credential masking utility (`mask_credentials`).
- **Universal API Connector (`connector.py`)**:
  - Reusable HTTP client abstraction.
  - Circuit Breaker failure counting and auto-recovery timeout.
  - Header builder injecting Bearer tokens, API Keys, Basic Auth, OAuth2, and Custom Headers.
  - HMAC-SHA256 signature calculation.
- **Universal Provider Registry (`provider_registry.py`)**:
  - Comprehensive pre-configured templates across all 10 provider categories.
- **Webhook Engine (`webhook_engine.py`)**:
  - Inbound signature verification with `hmac.compare_digest`.
  - Outbound payload signing and structured header dispatch.
- **API Analytics Engine (`analytics.py`)**:
  - Real-time success rate calculation, latency percentiles, and circuit breaker status telemetry.

---

### 4. Admin Panel & Frontend Interface
- **Path**: `frontend/src/modules/integrations/`
- **Delivered Views**:
  - `dashboard/ApiDashboardPage.tsx`: Live telemetry KPIs, 24h dispatches, latency timings, and health gauges.
  - `providers/ProviderDirectoryPage.tsx`: Categorized directory of connected and available provider templates.
  - `vault/CredentialVaultPage.tsx`: Key rotation manager with masked credential previews.
  - `tester/ConnectionTestTerminalPage.tsx`: Diagnostic terminal executing live ping tests.
  - `webhooks/WebhooksManagerPage.tsx`: Inbound and outbound webhook stream configuration.
  - `logs/ApiExecutionLogsPage.tsx`: Searchable audit logs with status codes and latency breakdown.
  - `analytics/ApiAnalyticsPage.tsx`: Quota burn charts, failure distribution, and gateway performance.
- **Routing**: Mounted under `/admin/integrations/*` with navigation item `API Integrations` (`PlugZap` icon).

---

### 5. Verification & Test Suite
- Comprehensive unit test suite `tests/unit/test_api_integration_framework.py`:
  - Python AST syntax across all 12 backend Python files.
  - Credential Vault encryption, decryption roundtrip, and masking.
  - Circuit Breaker transitions (`CLOSED` → `OPEN` → `HALF_OPEN` → `CLOSED`).
  - Authenticated header generation for Bearer, API_KEY, Basic, and Custom Header auth types.
  - Provider template coverage across all 10 categories.
  - Webhook inbound verification and outbound payload signing.
  - URL format validators and analytics calculation.
  - Zero browser storage audit: 0 instances of `localStorage`, `sessionStorage`, or `indexedDB`.
