#!/usr/bin/env python3
"""
Production Enterprise Bootstrap Script for MY EDUCATION INDIA.
Seeds ONLY the single flagship institute ('MY EDUCATION INDIA'),
9 core institutional roles, 37 enterprise module definitions,
and initial Root Owner & Super Administrator credentials.
Zero dummy students, zero fake leads, zero sample courses.
"""
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from sqlalchemy import select
from app.auth.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.institute import Institute
from app.models.module_config import SystemModuleConfig
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from app.permissions.module_catalog import ENTERPRISE_MODULES_CATALOG

CORE_PERMISSIONS = [
    ("institutes:read", "View Institutes & Branding", "institute_management"),
    ("institutes:write", "Create & Update Institutes", "institute_management"),
    ("modules:toggle", "Enable/Disable Enterprise Modules", "settings"),
    ("roles:read", "View Roles & Permissions", "role_management"),
    ("roles:write", "Create & Modify Roles", "role_management"),
    ("users:read", "View Users Directory", "role_management"),
    ("users:write", "Provision & Suspend Users", "role_management"),
    ("audit:read", "View Security & Compliance Audit Logs", "audit_logs"),
]

SYSTEM_ROLES = [
    ("ROOT_OWNER", "Platform Root Sovereign Owner", "Sovereign platform ownership above Super Admin"),
    ("SUPER_ADMIN", "Enterprise Super Administrator", "Full administrative governance across all modules"),
    ("INSTITUTE_ADMIN", "Institute Principal & Dean", "Head of Institution academic & administrative oversight"),
    ("FACULTY", "Teaching Faculty & Professor", "Course delivery, marks entry, and student attendance"),
    ("STAFF", "Institutional Administrative Staff", "Day-to-day office operations, inventory, and support"),
    ("ACCOUNTANT", "Bursar & Finance Officer", "Fee collections, reconciliations, dues, and refunds"),
    ("RECEPTION", "Front Desk & Visitor Concierge", "Visitor management, inquiries, and appointments"),
    ("COUNSELLOR", "Admissions Counsellor", "Student guidance, lead qualification, and enrollment"),
    ("STUDENT", "Enrolled Scholar", "Course learning, attendance tracking, exams, and fee payments")
]

async def seed_production_baseline() -> None:
    admin_email = os.environ.get("INITIAL_SUPERADMIN_EMAIL", "superadmin@myeducation.in")
    admin_password = os.environ.get("INITIAL_SUPERADMIN_PASSWORD", "EduIndia#Production2026!")

    async with AsyncSessionLocal() as session:
        # 1. Seed Core Permissions
        perm_objects = []
        for code, name, mod_key in CORE_PERMISSIONS:
            res = await session.execute(select(Permission).where(Permission.code == code))
            perm = res.scalar_one_or_none()
            if not perm:
                perm = Permission(code=code, name=name, module_key=mod_key)
                session.add(perm)
            perm_objects.append(perm)
        await session.flush()

        # 2. Seed Single Flagship Institute: MY EDUCATION INDIA
        inst_res = await session.execute(select(Institute).where(Institute.code == "MEI-HQ"))
        institute = inst_res.scalar_one_or_none()
        if not institute:
            institute = Institute(
                code="MEI-HQ",
                name="MY EDUCATION INDIA",
                tagline="National Flagship Institution for Higher Education & Research",
                official_email=admin_email,
                official_phone="+917312456789",
                address_line1="Campus Square, Institutional Sector",
                city="Indore",
                state="Madhya Pradesh",
                postal_code="452001",
                country="India",
            )
            session.add(institute)
            await session.flush()

            for mod_def in ENTERPRISE_MODULES_CATALOG:
                session.add(
                    SystemModuleConfig(
                        institute_id=institute.id,
                        module_key=mod_def["module_key"],
                        display_name=mod_def["display_name"],
                        category=mod_def["category"],
                        subdomain=mod_def["subdomain"],
                        description=mod_def["description"],
                        is_enabled=True,
                        is_core_locked=mod_def["is_core_locked"],
                        configuration={},
                    )
                )

        # 3. Seed 9 System Roles
        role_map = {}
        for r_code, r_name, r_desc in SYSTEM_ROLES:
            r_res = await session.execute(select(Role).where(Role.code == r_code))
            role_obj = r_res.scalar_one_or_none()
            if not role_obj:
                role_obj = Role(
                    code=r_code,
                    name=r_name,
                    description=r_desc,
                    portal_subdomain="admin" if "ADMIN" in r_code or r_code == "ROOT_OWNER" else r_code.lower(),
                    is_system_role=True,
                    institute_id=institute.id,
                    permissions=perm_objects if "ADMIN" in r_code or r_code == "ROOT_OWNER" else []
                )
                session.add(role_obj)
            role_map[r_code] = role_obj
        await session.flush()

        # 4. Seed Root Owner Account (Sovereign Authority)
        root_email = "root.owner@myeducation.in"
        user_res = await session.execute(select(User).where(User.email == root_email))
        root_user = user_res.scalar_one_or_none()
        if not root_user:
            root_user = User(
                email=root_email,
                username="root_owner",
                phone_number="+919000000000",
                first_name="Root",
                last_name="Owner",
                password_hash=hash_password("RootOwner#Sovereign2026!"),
                is_active=True,
                is_super_admin=True,
                is_verified=True,
                institute_id=institute.id,
                roles=[role_map["ROOT_OWNER"]]
            )
            session.add(root_user)

        # 5. Seed Super Administrator Account
        admin_res = await session.execute(select(User).where(User.email == admin_email.lower()))
        admin_user = admin_res.scalar_one_or_none()
        if not admin_user:
            admin_user = User(
                email=admin_email.lower(),
                username="superadmin",
                phone_number="+919999999999",
                first_name="Enterprise",
                last_name="Administrator",
                password_hash=hash_password(admin_password),
                is_active=True,
                is_super_admin=True,
                is_verified=True,
                institute_id=institute.id,
                roles=[role_map["SUPER_ADMIN"]],
            )
            session.add(admin_user)

        await session.commit()
        print("Production baseline for MY EDUCATION INDIA seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_production_baseline())
