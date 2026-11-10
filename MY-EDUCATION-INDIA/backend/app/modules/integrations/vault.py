"""
API Credential Vault
Provides symmetric encryption and credential masking for external API keys, tokens, and secrets.
"""
import base64
import json
import hashlib
from typing import Dict, Any

class CredentialVault:
    def __init__(self, master_key: str = "erp_enterprise_vault_master_key_2026"):
        # Derive 32-byte key from master secret
        self.key_bytes = hashlib.sha256(master_key.encode("utf-8")).digest()

    def encrypt(self, payload: Dict[str, Any]) -> str:
        raw_json = json.dumps(payload).encode("utf-8")
        # Simple high-speed XOR + base64 encoding with master key hash (pure standard library)
        encrypted_bytes = bytes([b ^ self.key_bytes[i % len(self.key_bytes)] for i, b in enumerate(raw_json)])
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def decrypt(self, encrypted_str: str) -> Dict[str, Any]:
        encrypted_bytes = base64.b64decode(encrypted_str.encode("utf-8"))
        raw_json = bytes([b ^ self.key_bytes[i % len(self.key_bytes)] for i, b in enumerate(encrypted_bytes)]).decode("utf-8")
        return json.loads(raw_json)

    @staticmethod
    def mask_credentials(credentials: Dict[str, Any]) -> Dict[str, str]:
        masked = {}
        for k, v in credentials.items():
            s = str(v)
            if len(s) <= 6:
                masked[k] = "******"
            else:
                masked[k] = f"{s[:3]}****{s[-3:]}"
        return masked
