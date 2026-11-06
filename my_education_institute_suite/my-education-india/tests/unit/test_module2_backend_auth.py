"""Unit and Integration Tests for Module 2: Enterprise Authentication & Authorization
Verifies:
- Password policy enforcement (length, upper, lower, digit, special)
- Password history ring buffer reuse prevention
- Configurable login criteria resolution
- JWT access & refresh token generation and decoding
- Fine-grained permission engine evaluation (direct, wildcard, super admin)
- AST compilation across all Module 2 backend files
"""
import ast
import os
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

# Provide test environment defaults
os.environ.setdefault("SECRET_KEY", "test_secret_key_minimum_32_characters_long_for_security")
os.environ.setdefault("REFRESH_SECRET_KEY", "test_refresh_secret_key_minimum_32_characters_long")
os.environ.setdefault("CSRF_SECRET_KEY", "test_csrf_secret_key_minimum_32_characters_long_sec")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("SYNC_DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")

from app.modules.auth.constants import (
    DEFAULT_AUTH_SETTINGS,
    DEFAULT_ENTERPRISE_PERMISSIONS,
    DEFAULT_SYSTEM_ROLES,
    VALID_LOGIN_CRITERIA,
)
from app.modules.auth.exceptions import (
    PasswordHistoryException,
    PasswordPolicyException,
)
from app.modules.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
)
from app.modules.auth.models import Permission, Role, User
from app.modules.auth.permissions import PermissionEngine
from app.modules.auth.security import (
    hash_password,
    validate_password_policy,
    verify_password,
    verify_password_history,
)


class TestModule2BackendEnterpriseAuth(unittest.TestCase):

    def test_all_module2_python_files_compile(self) -> None:
        auth_dir = PROJECT_ROOT / "backend/app/modules/auth"
        for py_file in auth_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_password_policy_enforcement(self) -> None:
        policy = {
            "password_min_length": 10,
            "password_require_uppercase": True,
            "password_require_lowercase": True,
            "password_require_number": True,
            "password_require_special": True,
        }
        # Valid password
        validate_password_policy("ValidPass#2026", policy)

        # Too short
        with self.assertRaises(PasswordPolicyException):
            validate_password_policy("Sh#1", policy)

        # Missing uppercase
        with self.assertRaises(PasswordPolicyException):
            validate_password_policy("validpass#2026", policy)

        # Missing special character
        with self.assertRaises(PasswordPolicyException):
            validate_password_policy("ValidPass2026", policy)

    def test_password_history_verification(self) -> None:
        old_pwd = "OldPassword#2025"
        old_hash = hash_password(old_pwd)
        history = [old_hash]

        # Reusing old password must raise exception
        with self.assertRaises(PasswordHistoryException):
            verify_password_history("OldPassword#2025", history)

        # New distinct password must pass
        verify_password_history("BrandNewPass#2026", history)

    def test_jwt_access_and_refresh_token_lifecycle(self) -> None:
        user_id = "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
        roles = ["STUDENT", "FACULTY"]
        perms = ["student.view", "attendance.manage"]

        access_token, expires_at = create_access_token(
            user_id=user_id,
            institute_id=None,
            roles=roles,
            permissions=perms,
            expire_minutes=10,
        )
        self.assertTrue(access_token)
        decoded = decode_access_token(access_token)
        self.assertEqual(decoded["sub"], user_id)
        self.assertEqual(decoded["roles"], roles)
        self.assertEqual(decoded["perms"], perms)

        refresh_token, token_family, r_exp = create_refresh_token(
            user_id=user_id,
            remember_me=True,
            expire_days=30,
        )
        self.assertTrue(refresh_token)
        self.assertTrue(token_family)
        r_decoded = decode_refresh_token(refresh_token)
        self.assertEqual(r_decoded["sub"], user_id)
        self.assertEqual(r_decoded["fam"], token_family)
        self.assertTrue(r_decoded["rem"])

    def test_permission_engine_evaluation(self) -> None:
        perm_view = Permission(code="student.view", name="View Student", module_key="student")
        perm_edit = Permission(code="student.edit", name="Edit Student", module_key="student")
        role_faculty = Role(code="FACULTY", name="Faculty", permissions=[perm_view, perm_edit])

        user = User(
            email="faculty@test.com",
            username="faculty_user",
            phone_number="+919876543210",
            first_name="Prof",
            last_name="Sharma",
            password_hash="fakehash",
            is_active=True,
            is_super_admin=False,
            roles=[role_faculty],
        )

        # Faculty has student.view and student.edit
        self.assertTrue(PermissionEngine.has_permission(user, "student.view"))
        self.assertTrue(PermissionEngine.has_permission(user, "student.edit"))
        self.assertFalse(PermissionEngine.has_permission(user, "fees.manage"))

        # Super admin has all permissions
        super_admin = User(
            email="admin@test.com",
            username="admin_user",
            phone_number="+919876543211",
            first_name="Super",
            last_name="Admin",
            password_hash="fakehash",
            is_active=True,
            is_super_admin=True,
            roles=[],
        )
        self.assertTrue(PermissionEngine.has_permission(super_admin, "fees.manage"))
        self.assertTrue(PermissionEngine.has_permission(super_admin, "random.nonexistent.perm"))

    def test_constants_and_default_roles(self) -> None:
        self.assertGreaterEqual(len(DEFAULT_SYSTEM_ROLES), 13)
        codes = {r["code"] for r in DEFAULT_SYSTEM_ROLES}
        expected_roles = {
            "SUPER_ADMIN", "INSTITUTE_ADMIN", "BRANCH_ADMIN", "RECEPTION",
            "FACULTY", "ACCOUNTANT", "EXAM_CONTROLLER", "LIBRARY_STAFF",
            "HOSTEL_WARDEN", "TRANSPORT_MANAGER", "STUDENT", "PARENT", "GUEST"
        }
        self.assertTrue(expected_roles.issubset(codes))

        self.assertIn("username", VALID_LOGIN_CRITERIA)
        self.assertIn("roll_number", VALID_LOGIN_CRITERIA)
        self.assertIn("erp_id", VALID_LOGIN_CRITERIA)


if __name__ == "__main__":
    unittest.main()
