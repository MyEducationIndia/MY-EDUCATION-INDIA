"""
API Integration Service Layer
"""
from typing import Dict, Any, Optional
from app.modules.integrations.repository import ApiIntegrationRepository
from app.modules.integrations.vault import CredentialVault
from app.modules.integrations.connector import UniversalApiConnector
from app.modules.integrations.validators import ApiIntegrationValidators
from app.modules.integrations.provider_registry import UniversalProviderRegistry

class ApiIntegrationService:
    def __init__(self, repo: ApiIntegrationRepository, vault: Optional[CredentialVault] = None):
        self.repo = repo
        self.vault = vault or CredentialVault()
        self.connector = UniversalApiConnector()

    async def register_provider_with_credentials(self, institute_id: str, provider_data: dict, credentials: Optional[dict] = None):
        if not ApiIntegrationValidators.validate_url(provider_data.get("base_url", "")):
            raise ValueError("Invalid Base URL format")
        provider = await self.repo.create_provider(institute_id, provider_data)
        if credentials:
            enc = self.vault.encrypt(credentials)
            await self.repo.save_credentials(provider.id, institute_id, enc)
        return provider

    def test_connection_mock(self, base_url: str, auth_type: str, credentials: dict) -> dict:
        # High speed dry-run ping
        headers = self.connector.build_authenticated_headers(auth_type, credentials)
        return {
            "is_connected": True,
            "status_code": 200,
            "latency_ms": 45.2,
            "message": "Connection verified successfully. Handshake acknowledged.",
            "response_preview": '{"status":"ok","ping":"pong"}'
        }
