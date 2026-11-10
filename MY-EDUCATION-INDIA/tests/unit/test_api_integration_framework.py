import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import ast
import re

from app.modules.integrations.schemas import (
    ApiProviderCreate,
    ApiProviderUpdate,
    CredentialUpdateRequest,
    ConnectionTestRequest,
    WebhookRegistrationCreate
)
from app.modules.integrations.vault import CredentialVault
from app.modules.integrations.connector import UniversalApiConnector, CircuitBreaker
from app.modules.integrations.provider_registry import UniversalProviderRegistry
from app.modules.integrations.webhook_engine import WebhookEngine
from app.modules.integrations.validators import ApiIntegrationValidators
from app.modules.integrations.analytics import compute_provider_metrics

class TestUniversalApiIntegrationFramework(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.int_backend_dir = os.path.join(self.base_dir, "backend/app/modules/integrations")
        self.int_frontend_dir = os.path.join(self.base_dir, "frontend/src/modules/integrations")
        self.vault = CredentialVault("test_master_secret_key_123456789")
        self.connector = UniversalApiConnector()

    def test_integrations_ast_clean(self):
        """Verify all API Integration backend Python files parse cleanly."""
        self.assertTrue(os.path.exists(self.int_backend_dir))
        py_files = [f for f in os.listdir(self.int_backend_dir) if f.endswith(".py")]
        self.assertGreaterEqual(len(py_files), 11)
        for py_file in py_files:
            fp = os.path.join(self.int_backend_dir, py_file)
            with open(fp, "r", encoding="utf-8") as f:
                ast.parse(f.read(), filename=py_file)

    def test_credential_vault_encryption_and_masking(self):
        """Test symmetric encryption, round-trip decryption, and credential masking."""
        payload = {
            "api_key": "live_sk_1234567890abcdef",
            "secret": "super_secret_token_xyz"
        }
        encrypted = self.vault.encrypt(payload)
        self.assertIsInstance(encrypted, str)
        self.assertNotEqual(encrypted, payload["api_key"])

        decrypted = self.vault.decrypt(encrypted)
        self.assertEqual(decrypted["api_key"], payload["api_key"])
        self.assertEqual(decrypted["secret"], payload["secret"])

        masked = self.vault.mask_credentials(payload)
        self.assertEqual(masked["api_key"], "liv****def")
        self.assertEqual(masked["secret"], "sup****xyz")

    def test_circuit_breaker_lifecycle(self):
        """Test Circuit Breaker transition from CLOSED to OPEN and failure recovery."""
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout_seconds=1)
        self.assertEqual(cb.state, "CLOSED")
        self.assertTrue(cb.can_execute())

        cb.record_failure()
        cb.record_failure()
        self.assertEqual(cb.state, "CLOSED")
        self.assertTrue(cb.can_execute())

        cb.record_failure() # 3rd failure reaches threshold
        self.assertEqual(cb.state, "OPEN")
        self.assertFalse(cb.can_execute())

        # Test recovery after timeout
        import time
        time.sleep(1.1)
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, "HALF_OPEN")

        cb.record_success()
        self.assertEqual(cb.state, "CLOSED")

    def test_authenticated_headers_injection(self):
        """Test connector header building for Bearer, API_KEY, Basic, and Custom Header auth types."""
        bearer_headers = self.connector.build_authenticated_headers("BEARER", {"token": "my_jwt_token"})
        self.assertEqual(bearer_headers["Authorization"], "Bearer my_jwt_token")

        api_key_headers = self.connector.build_authenticated_headers("API_KEY", {"header_name": "X-API-KEY", "api_key": "secret123"})
        self.assertEqual(api_key_headers["X-API-KEY"], "secret123")

        basic_headers = self.connector.build_authenticated_headers("BASIC", {"username": "admin", "password": "password123"})
        self.assertTrue(basic_headers["Authorization"].startswith("Basic "))

        custom_headers = self.connector.build_authenticated_headers("CUSTOM_HEADER", {"header_authkey": "fast2sms_key_val"})
        self.assertEqual(custom_headers["authkey"], "fast2sms_key_val")

    def test_provider_registry_coverage(self):
        """Verify templates exist for all required provider categories."""
        templates = UniversalProviderRegistry.get_all_templates()
        categories = {t["category"] for t in templates}
        required_cats = {"SMS", "WHATSAPP", "EMAIL", "PUSH", "PAYMENT", "VIDEO", "STORAGE", "AI", "MAPS", "OTP"}
        for rc in required_cats:
            self.assertIn(rc, categories, f"Missing template for category {rc}")

        fast2sms = UniversalProviderRegistry.find_template("fast2sms")
        self.assertIsNotNone(fast2sms)
        self.assertEqual(fast2sms["category"], "SMS")

        razorpay = UniversalProviderRegistry.find_template("razorpay")
        self.assertIsNotNone(razorpay)
        self.assertEqual(razorpay["category"], "PAYMENT")

    def test_webhook_engine_signature(self):
        """Test inbound and outbound HMAC-SHA256 signature calculation and validation."""
        secret = "erp_webhook_secret_key"
        payload = b'{"event":"fee.collected","amount":25000}'
        out = WebhookEngine.prepare_outbound_payload("fee.collected", {"amount": 25000}, secret)
        self.assertIn("signature", out)
        self.assertEqual(out["signature_header"], "X-ERP-Signature")

        # Verify inbound signature
        import hmac, hashlib
        valid_sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        self.assertTrue(WebhookEngine.verify_inbound_signature(payload, valid_sig, secret))
        self.assertFalse(WebhookEngine.verify_inbound_signature(payload, "invalid_sig", secret))

    def test_validators_and_analytics(self):
        """Test URL validators, provider key validation, and analytics calculation."""
        self.assertTrue(ApiIntegrationValidators.validate_url("https://api.twilio.com/v1"))
        self.assertTrue(ApiIntegrationValidators.validate_url("smtp://smtp.sendgrid.net:587"))
        self.assertFalse(ApiIntegrationValidators.validate_url("invalid_url"))

        self.assertTrue(ApiIntegrationValidators.validate_provider_key("fast2sms_v2"))
        self.assertFalse(ApiIntegrationValidators.validate_provider_key("INVALID KEY WITH SPACES"))

        # Analytics
        logs = [
            {"is_success": True, "latency_ms": 100.0, "circuit_broken": False},
            {"is_success": True, "latency_ms": 200.0, "circuit_broken": False},
            {"is_success": False, "latency_ms": 300.0, "circuit_broken": True}
        ]
        metrics = compute_provider_metrics(logs)
        self.assertEqual(metrics["total_calls"], 3)
        self.assertEqual(metrics["success_rate"], 66.67)
        self.assertEqual(metrics["avg_latency_ms"], 200.0)
        self.assertEqual(metrics["circuit_trips"], 1)

    def test_zero_browser_storage_integrations(self):
        """Strictly enforce zero usage of localStorage, sessionStorage, or indexedDB in frontend."""
        storage_pattern = re.compile(r'\b(localStorage|sessionStorage|indexedDB)\b')
        violations = []
        for root, _, files in os.walk(self.int_frontend_dir):
            for file in files:
                if file.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        for line_idx, line in enumerate(f, 1):
                            if storage_pattern.search(line):
                                violations.append(f"{file}:{line_idx}")
        self.assertEqual(violations, [], f"Found forbidden browser storage usage: {violations}")

if __name__ == "__main__":
    unittest.main()
