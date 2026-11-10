#!/usr/bin/env python3
"""
Production Enterprise Bootstrap Script for MY EDUCATION INDIA.
Seeds Flagship Institute, 9 core roles, 37 enterprise modules,
Root Owner & Super Admin credentials, Website Framework defaults,
Module 2 Home Page CMS defaults, and Module 3 About Institute CMS defaults
(Milestones, Leadership Messages, Accreditations, Campus Infrastructure).
"""
import asyncio
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select
from app.auth.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.cms_about import (
    CmsAccreditation,
    CmsCampusInfrastructure,
    CmsLeadershipMessage,
    CmsMilestone,
)
from app.models.cms_home import (
    CmsFeaturedProgram,
    CmsHeroSlide,
    CmsQuickLink,
    CmsRecruiterLogo,
    CmsStatCounter,
    CmsTestimonial,
)
from app.models.institute import Institute
from app.models.module_config import SystemModuleConfig
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from app.models.website import (
    WebsiteNavigationMenu,
    WebsiteSearchIndex,
    WebsiteSetting,
    WebsiteSocialLink,
    WebsiteTheme,
    WebsiteTickerItem,
)
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
    ("website:read", "View Website Configuration & Content", "website_cms"),
    ("website:write", "Manage Website Settings, Header, Ticker, Menus, Themes, Home, About", "website_cms"),
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
    ("STUDENT", "Enrolled Scholar", "Course learning, attendance tracking, exams, and fee payments"),
    ("EXAM_CONTROLLER", "Controller of Examinations", "Examination scheduling, CBT, and marks moderation"),
    ("LIBRARIAN", "Head Librarian", "Library catalog, digital assets, and fine collection"),
    ("IT_SUPPORT", "IT Systems Administrator", "System monitoring, user passwords, and logs"),
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

        # 2. Seed Flagship Institute: MY EDUCATION INDIA
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

        # 3. Seed System Roles
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
                    permissions=perm_objects if "ADMIN" in r_code or r_code == "ROOT_OWNER" else [],
                )
                session.add(role_obj)
            role_map[r_code] = role_obj
        await session.flush()

        # 4. Seed Root Owner Account
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
                roles=[role_map["ROOT_OWNER"]],
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

        # 6. Seed Website Settings Defaults
        ws_res = await session.execute(select(WebsiteSetting).where(WebsiteSetting.institute_id == institute.id))
        ws = ws_res.scalar_one_or_none()
        if not ws:
            ws = WebsiteSetting(
                institute_id=institute.id,
                site_title="MY EDUCATION INDIA",
                tagline="National Flagship Higher Education Institution",
                header_is_sticky=True,
                header_show_search=True,
                header_show_login=True,
                header_login_button_text="Login",
                header_login_route="/login",
                contact_phone="+91 731 245 6789",
                contact_email="admissions@myeducation.in",
                contact_address="Campus Square, Institutional Sector, Indore, Madhya Pradesh 452001",
                meta_description="Official Portal of MY EDUCATION INDIA. Autonomous Higher Education & Research Campus.",
                meta_keywords="higher education, degrees, indore, engineering, management, cbt, admissions",
                is_maintenance_mode=False,
            )
            session.add(ws)

        # 7. Seed Website Theme Defaults
        wt_res = await session.execute(select(WebsiteTheme).where(WebsiteTheme.institute_id == institute.id))
        wt = wt_res.scalar_one_or_none()
        if not wt:
            wt = WebsiteTheme(
                institute_id=institute.id,
                primary_color="#1E40AF",
                secondary_color="#0D9488",
                accent_color="#F59E0B",
                background_color="#F8FAFC",
                surface_color="#FFFFFF",
                text_primary_color="#0F172A",
                text_secondary_color="#475569",
                font_family="Inter, system-ui, sans-serif",
                heading_font_family="Inter, system-ui, sans-serif",
                border_radius="0.75rem",
                button_style="rounded",
                shadow_style="soft",
                animation_enabled=True,
            )
            session.add(wt)

        # 8. Seed Default Live Update Ticker Items
        ticker_res = await session.execute(select(WebsiteTickerItem).where(WebsiteTickerItem.institute_id == institute.id))
        if not ticker_res.scalars().first():
            ticker_defaults = [
                ("National Entrance Examination 2026-27 Registrations Open Now — Apply Online", "Admission", "/admissions/apply", 1, False),
                ("End-Term Semester Examination Timetable & Seating Chart Released", "Examination", "/admin/exams", 2, False),
                ("Merit-cum-Means Scholarships 2026 Application Window Extended to Nov 30", "Scholarship", "/admissions/scholarships", 3, False),
                ("Campus Placement Drive: 48 Global Corporate Recruiters Visiting MEI-HQ Indore", "Placement", "/placements", 4, False),
            ]
            for order, (title, category, link, priority, emergency) in enumerate(ticker_defaults, start=1):
                session.add(
                    WebsiteTickerItem(
                        institute_id=institute.id,
                        title=title,
                        category=category,
                        link_url=link,
                        is_external=False,
                        open_new_tab=False,
                        is_emergency=emergency,
                        priority_level=priority,
                        display_order=order,
                        is_active=True,
                    )
                )

        # 9. Seed Dynamic Main Header Navigation Tree
        nav_res = await session.execute(select(WebsiteNavigationMenu).where(WebsiteNavigationMenu.institute_id == institute.id))
        if not nav_res.scalars().first():
            nav_tree = [
                ("Home", "/", "Home", 1, []),
                ("About", "/about", "Building2", 2, [
                    ("Vision & Mission", "/about/vision-mission"),
                    ("Director's Message", "/about/directors-message"),
                    ("Accreditation & Approvals", "/about#accreditations"),
                    ("Campus Infrastructure", "/about#infrastructure"),
                ]),
                ("Academics", "/courses", "BookOpen", 3, [
                    ("Undergraduate Degrees", "/courses"),
                    ("Postgraduate Degrees", "/courses"),
                    ("Doctoral & Research", "/courses"),
                    ("Academic Calendar", "/admin/academics"),
                ]),
                ("Admissions", "/admissions", "ClipboardList", 4, [
                    ("Admission Process", "/admissions/process"),
                    ("Eligibility Criteria", "/admissions/eligibility"),
                    ("Fee Structure", "/admissions/fees"),
                    ("Apply Online 2026", "/admissions/apply"),
                    ("Scholarships", "/admissions/scholarships"),
                ]),
                ("Placements", "/placements", "Award", 5, [
                    ("Placement Records", "/placements"),
                    ("Corporate Recruiters", "/placements/recruiters"),
                    ("Success Stories", "/placements/success-stories"),
                ]),
                ("Verification", "/verify", "FileBadge", 6, []),
                ("Contact", "/contact", "Phone", 7, []),
            ]

            for order, (title, path, icon, pos, children) in enumerate(nav_tree, start=1):
                parent_menu = WebsiteNavigationMenu(
                    institute_id=institute.id,
                    menu_location="HEADER_MAIN",
                    title=title,
                    path=path,
                    icon_name=icon,
                    is_external=False,
                    open_new_tab=False,
                    is_mega_menu=len(children) > 0,
                    display_order=pos,
                    is_active=True,
                )
                session.add(parent_menu)
                await session.flush()

                for c_order, (c_title, c_path) in enumerate(children, start=1):
                    session.add(
                        WebsiteNavigationMenu(
                            institute_id=institute.id,
                            menu_location="HEADER_MAIN",
                            title=c_title,
                            path=c_path,
                            parent_id=parent_menu.id,
                            is_external=False,
                            open_new_tab=False,
                            display_order=c_order,
                            is_active=True,
                        )
                    )

        # 10. Seed Default Social Links
        soc_res = await session.execute(select(WebsiteSocialLink).where(WebsiteSocialLink.institute_id == institute.id))
        if not soc_res.scalars().first():
            social_defaults = [
                ("linkedin", "https://linkedin.com/company/myeducationindia", 1),
                ("twitter", "https://twitter.com/myeducationin", 2),
                ("youtube", "https://youtube.com/@myeducationindia", 3),
                ("facebook", "https://facebook.com/myeducationin", 4),
            ]
            for platform, url, order in social_defaults:
                session.add(
                    WebsiteSocialLink(
                        institute_id=institute.id,
                        platform=platform,
                        url=url,
                        display_order=order,
                        is_active=True,
                    )
                )

        # 11. Seed Search Index Catalog
        search_res = await session.execute(select(WebsiteSearchIndex).where(WebsiteSearchIndex.institute_id == institute.id))
        if not search_res.scalars().first():
            search_items = [
                ("course", "Bachelor of Technology (Computer Science & Engineering)", "4-year AICTE-accredited engineering program specializing in AI, Cloud, and Software Architecture", "btech, cse, computer science, engineering, ai", "/courses"),
                ("course", "Master of Business Administration (Executive MBA)", "2-year flagship management degree covering Finance, Marketing, Analytics, and Corporate Strategy", "mba, management, business, executive, finance", "/courses"),
                ("notice", "National Entrance Examination & Scholarship Schedule 2026-27", "Official circular detailing exam dates, centers, admit card download, and eligibility cutoff", "entrance exam, scholarship, admit card, circular", "/notices"),
                ("page", "Digital Document & Certificate Verification Portal", "Public zero-login credential verification ledger to authenticate degrees and marksheets", "verification, degree verify, marksheets, qr code", "/verify"),
                ("page", "About MY EDUCATION INDIA Campus & Leadership", "History, UGC/AICTE accreditations, Director's message, and research facilities", "about, history, director, aicte, ugc, campus", "/about"),
            ]
            for entity_type, title, summary, keywords, target_url in search_items:
                session.add(
                    WebsiteSearchIndex(
                        institute_id=institute.id,
                        entity_type=entity_type,
                        title=title,
                        summary=summary,
                        keywords=keywords,
                        target_url=target_url,
                        is_published=True,
                    )
                )

        # 12. Seed Module 2 Home Page Defaults
        slide_res = await session.execute(select(CmsHeroSlide).where(CmsHeroSlide.institute_id == institute.id))
        if not slide_res.scalars().first():
            slides_data = [
                (
                    "National Entrance Examination 2026",
                    "Shaping Global Leaders in Technology, Management & Sciences",
                    "Join India's premier autonomous flagship institution at Indore. Accredited curricula, AI-powered CBT examinations, and verified digital credentials.",
                    "Apply for Admission 2026",
                    "/admissions/apply",
                    "Explore Degree Programs",
                    "/courses",
                    1,
                ),
                (
                    "Autonomous Research Excellence",
                    "World-Class Infrastructure & Innovation Labs",
                    "Experience high-performance computing, advanced research incubation, and seamless student-lifecycle administration on a modern digital campus.",
                    "Take Virtual Campus Tour",
                    "/about",
                    "Placement Records",
                    "/placements",
                    2,
                ),
            ]
            for badge, title, subtitle, p_cta, p_link, s_cta, s_link, order in slides_data:
                session.add(
                    CmsHeroSlide(
                        institute_id=institute.id,
                        badge_text=badge,
                        title=title,
                        subtitle=subtitle,
                        primary_cta_text=p_cta,
                        primary_cta_link=p_link,
                        secondary_cta_text=s_cta,
                        secondary_cta_link=s_link,
                        display_order=order,
                        is_active=True,
                    )
                )

        stat_res = await session.execute(select(CmsStatCounter).where(CmsStatCounter.institute_id == institute.id))
        if not stat_res.scalars().first():
            stats_data = [
                ("37+", 37, "Integrated Subsystems", "Real-Time Cloud ERP Architecture", "Layers", 1),
                ("100%", 100, "Placement Assistance", "Top Multinational Corporate Recruiters", "Award", 2),
                ("15,000+", 15000, "Scholars & Alumni", "Empowered Across National Industry", "Users", 3),
                ("A+", None, "Autonomous Governance", "Flagship Campus at Indore, MP", "ShieldCheck", 4),
            ]
            for val, target, lbl, sub, icon, order in stats_data:
                session.add(
                    CmsStatCounter(
                        institute_id=institute.id,
                        metric_value=val,
                        numeric_target=target,
                        label=lbl,
                        subtext=sub,
                        icon_name=icon,
                        display_order=order,
                        is_active=True,
                    )
                )

        ql_res = await session.execute(select(CmsQuickLink).where(CmsQuickLink.institute_id == institute.id))
        if not ql_res.scalars().first():
            quick_links_data = [
                ("Online Admissions", "Submit 2026 degree application", "/admissions/apply", "FileText", "Open", False, 1),
                ("Online Fee Settlement", "Instant payment with GST receipt", "/pay-online", "IndianRupee", "Secure", False, 2),
                ("Academic Examination Portal", "Schedules, CBT tests & results", "/admin/exams", "Award", "Live", False, 3),
                ("Document Verification", "Cryptographic QR credential validation", "/verify", "ShieldCheck", "Zero Login", False, 4),
            ]
            for title, desc, path, icon, badge, ext, order in quick_links_data:
                session.add(
                    CmsQuickLink(
                        institute_id=institute.id,
                        title=title,
                        description=desc,
                        path=path,
                        icon_name=icon,
                        badge_label=badge,
                        is_external=ext,
                        display_order=order,
                        is_active=True,
                    )
                )

        prog_res = await session.execute(select(CmsFeaturedProgram).where(CmsFeaturedProgram.institute_id == institute.id))
        if not prog_res.scalars().first():
            programs_data = [
                (
                    "B.Tech Computer Science & Engineering",
                    "BTECH-CSE",
                    "Engineering & Technology",
                    "Undergraduate",
                    "4 Years (8 Semesters)",
                    "₹95,000 / Year",
                    "10+2 with PCM >= 60%",
                    "Specialization in Artificial Intelligence, Cloud Computing, Full-Stack Architecture, and Autonomous Systems with modern lab access.",
                    1,
                ),
                (
                    "Master of Business Administration (Executive MBA)",
                    "MBA-EXEC",
                    "Management Studies",
                    "Postgraduate",
                    "2 Years (4 Semesters)",
                    "₹1,20,000 / Year",
                    "Bachelor Degree >= 50%",
                    "Advanced institutional management degree focusing on Corporate Strategy, Financial Analytics, Supply Chain, and Global Business Leadership.",
                    2,
                ),
                (
                    "Bachelor of Computer Applications (BCA)",
                    "BCA-HONS",
                    "Computer Applications",
                    "Undergraduate",
                    "3 Years (6 Semesters)",
                    "₹65,000 / Year",
                    "10+2 Any Stream >= 50%",
                    "Comprehensive software development curriculum covering Cloud DevOps, Database Administration, Web Technologies, and Cyber Security.",
                    3,
                ),
            ]
            for title, code, cat, deg, dur, fee, elig, summ, order in programs_data:
                session.add(
                    CmsFeaturedProgram(
                        institute_id=institute.id,
                        title=title,
                        code=code,
                        category=cat,
                        degree_level=deg,
                        duration=dur,
                        annual_fee=fee,
                        eligibility_summary=elig,
                        summary=summ,
                        is_admissions_open=True,
                        display_order=order,
                        is_active=True,
                    )
                )

        rec_res = await session.execute(select(CmsRecruiterLogo).where(CmsRecruiterLogo.institute_id == institute.id))
        if not rec_res.scalars().first():
            recruiters_data = [
                ("Microsoft", "Tier 1", "44.0 LPA", 1),
                ("Amazon", "Tier 1", "38.5 LPA", 2),
                ("Tata Consultancy Services", "Regular", "9.5 LPA", 3),
                ("Infosys", "Regular", "8.5 LPA", 4),
                ("Deloitte", "Tier 1", "14.0 LPA", 5),
                ("HCL Technologies", "Regular", "7.5 LPA", 6),
            ]
            for name, tier, ctc, order in recruiters_data:
                session.add(
                    CmsRecruiterLogo(
                        institute_id=institute.id,
                        company_name=name,
                        tier=tier,
                        highest_package_lpa=ctc,
                        display_order=order,
                        is_active=True,
                    )
                )

        test_res = await session.execute(select(CmsTestimonial).where(CmsTestimonial.institute_id == institute.id))
        if not test_res.scalars().first():
            testimonials_data = [
                (
                    "Aarav Sharma",
                    "B.Tech CSE, Batch 2024 (Placed at Microsoft)",
                    "Student",
                    5,
                    "The autonomous curriculum and real-time CBT testing platform at MY EDUCATION INDIA prepared me for the rigorous interviews of top global tech firms. The faculty mentorship was extraordinary.",
                    1,
                ),
                (
                    "Priya Patel",
                    "MBA Executive, Batch 2023 (Consultant at Deloitte)",
                    "Alumni",
                    5,
                    "From campus case study competitions to corporate leadership seminars in Indore, the institute's emphasis on practical management disciplines gave my career an incredible leap.",
                    2,
                ),
            ]
            for author, role, cat, stars, quote, order in testimonials_data:
                session.add(
                    CmsTestimonial(
                        institute_id=institute.id,
                        author_name=author,
                        author_role=role,
                        author_category=cat,
                        rating_stars=stars,
                        quote=quote,
                        display_order=order,
                        is_active=True,
                    )
                )

        # =========================================================================
        # 13. SEED MODULE 3: ABOUT INSTITUTE CMS DEFAULTS
        # =========================================================================
        # A. Milestones Timeline
        ms_res = await session.execute(select(CmsMilestone).where(CmsMilestone.institute_id == institute.id))
        if not ms_res.scalars().first():
            milestones_data = [
                (
                    "2010",
                    "Institutional Foundation & Inception",
                    "MY EDUCATION INDIA was established with a singular charter: to establish an autonomous center of excellence in higher engineering and applied sciences in Central India.",
                    "Building2",
                    1,
                ),
                (
                    "2015",
                    "AICTE & University Autonomous Status",
                    "Achieved autonomous accreditation from statutory bodies and expanded degree curricula across multidisciplinary computing and management faculties.",
                    "Award",
                    2,
                ),
                (
                    "2020",
                    "Flagship Innovation & Research Incubation Wing",
                    "Inaugurated dedicated robotics, artificial intelligence, and high-performance computing centers with 500+ seat computer-based testing laboratories.",
                    "Sparkles",
                    3,
                ),
                (
                    "2026",
                    "Digital Campus Cloud & ERP V2 Evolution",
                    "Pioneered complete zero-trust digital campus governance uniting 37 integrated subsystems with cryptographic QR degree verification.",
                    "ShieldCheck",
                    4,
                ),
            ]
            for year, title, desc, icon, order in milestones_data:
                session.add(
                    CmsMilestone(
                        institute_id=institute.id,
                        year=year,
                        title=title,
                        description=desc,
                        icon_name=icon,
                        display_order=order,
                        is_active=True,
                    )
                )

        # B. Leadership Messages
        lm_res = await session.execute(select(CmsLeadershipMessage).where(CmsLeadershipMessage.institute_id == institute.id))
        if not lm_res.scalars().first():
            leadership_data = [
                (
                    "Dr. Rajeshwar Verma",
                    "Chairman & Chancellor",
                    "CHAIRMAN",
                    "Empowering Scholars to Shape India's Technological Frontier",
                    "At MY EDUCATION INDIA, education transcends the classroom. We have built an ecosystem that harmonizes academic rigor, scientific inquiry, and ethical leadership. Our graduates carry not just degrees, but the intellectual agility to lead global enterprise transformations.",
                    1,
                ),
                (
                    "Prof. Sunita Deshmukh",
                    "Campus Director & Academic Dean",
                    "DIRECTOR",
                    "Excellence Driven by Technology, Ethics and Innovation",
                    "As we pioneer autonomous education, our priority remains student-centric innovation. Through digital transparency, computer-based testing excellence, and deep corporate partnerships, we cultivate professionals who excel at the highest echelons of industry.",
                    2,
                ),
            ]
            for name, desig, role, salut, body, order in leadership_data:
                session.add(
                    CmsLeadershipMessage(
                        institute_id=institute.id,
                        leader_name=name,
                        leader_designation=desig,
                        role_category=role,
                        salutation_title=salut,
                        message_body=body,
                        display_order=order,
                        is_active=True,
                    )
                )

        # C. Accreditations & Approvals
        acc_res = await session.execute(select(CmsAccreditation).where(CmsAccreditation.institute_id == institute.id))
        if not acc_res.scalars().first():
            accreditation_data = [
                ("AICTE", "All India Council for Technical Education (AICTE)", "F.No. Central/1-931829102/2026/EOA", "2024", "2029", 1),
                ("UGC", "University Grants Commission (UGC 2f/12B Recognition)", "UGC/AUT/MEI-HQ/2022-771", "2022", "2032", 2),
                ("NAAC", "National Assessment and Accreditation Council (Grade A+)", "NAAC/A+/2023/MP-0192", "2023", "2028", 3),
                ("NBA", "National Board of Accreditation (Tier-1 Accredited Programs)", "NBA/ENGG/2024/718", "2024", "2027", 4),
            ]
            for body, title, ref, v_from, v_upto, order in accreditation_data:
                session.add(
                    CmsAccreditation(
                        institute_id=institute.id,
                        accrediting_body=body,
                        title=title,
                        approval_reference_number=ref,
                        valid_from=v_from,
                        valid_upto=v_upto,
                        display_order=order,
                        is_active=True,
                    )
                )

        # D. Campus Infrastructure Facilities
        infra_res = await session.execute(select(CmsCampusInfrastructure).where(CmsCampusInfrastructure.institute_id == institute.id))
        if not infra_res.scalars().first():
            infra_data = [
                ("Central Academic Knowledge Center", "ACADEMIC", "75,000+ Print & Digital Volumes", "Multi-tier research library with automated RFID borrowing, private scholar study pods, and global IEEE/Springer digital subscriptions.", "Block A, Level 2", 1),
                ("High-Performance CBT & AI Testing Labs", "DIGITAL", "600+ Enterprise Testing Terminals", "Dedicated air-conditioned terminal halls equipped with gigabit fiber, hardware-locked anti-cheat proctoring, and zero-latency examination servers.", "Tech Wing, Block B", 2),
                ("Advanced Robotics & Incubation Hub", "RESEARCH", "20+ Sponsored Research Stations", "Autonomous technology center with 3D prototyping, IoT testbeds, embedded micro-controller labs, and industrial collaborative workstations.", "Innovation Block", 3),
                ("Olympic Multi-Sport Indoor Complex", "SPORTS", "2,000 Spectator Pavilion", "Indoor badminton courts, synthetic turf sports ground, gymnasium, and certified sports medicine facilities.", "Campus Sports Sector", 4),
            ]
            for name, cat, cap, desc, loc, order in infra_data:
                session.add(
                    CmsCampusInfrastructure(
                        institute_id=institute.id,
                        facility_name=name,
                        category=cat,
                        capacity_metric=cap,
                        description=desc,
                        floor_or_location=loc,
                        display_order=order,
                        is_active=True,
                    )
                )

        await session.commit()
        print("Production baseline, Module 2 Home Page, and Module 3 About Institute CMS defaults seeded successfully.")


if __name__ == "__main__":
    asyncio.run(seed_production_baseline())
