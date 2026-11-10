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
from app.models.cms_courses import CmsCourseCategory, CmsCourse, CmsCourseCurriculum, CmsCourseFaculty
from app.models.cms_admissions import CmsAdmissionStep, CmsFeeStructure, CmsScholarship
from app.models.cms_faculty import CmsFacultyMember, CmsResearchPublication, CmsStaffMember
from app.models.cms_placements import CmsPlacementStat, CmsRecruiterPartner, CmsAlumniSuccessStory, CmsPlacementDrive, CmsTrainingProgram, CmsInternshipOpportunity
from app.models.cms_events_news import CmsEvent, CmsNewsArticle, CmsNoticeCircular, CmsAchievement
from app.models.cms_gallery import CmsGalleryAlbum, CmsGalleryMedia
from app.models.cms_downloads import CmsDownloadCategory, CmsDownloadDocument
from app.models.cms_home import CmsTestimonial
from app.models.cms_contact import CmsDepartmentContact, CmsFaqItem
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

        # 6. Seed Module 4 Course Management Catalog
        cat_res = await session.execute(select(CmsCourseCategory).where(CmsCourseCategory.institute_id == institute.id))
        existing_cats = {c.slug: c for c in cat_res.scalars().all()}
        
        categories_data = [
            ("Engineering & Technology", "engineering-technology", "Undergraduate and postgraduate professional engineering programs accredited by NBA Tier-1.", "Cpu", 1),
            ("Computer Applications & AI", "computer-applications-ai", "Cutting-edge software development, artificial intelligence, and cloud architecture curriculums.", "Terminal", 2),
            ("Management & Business Administration", "management-business", "Autonomous management leadership, technology commercialization, and executive administration.", "Briefcase", 3),
            ("Applied Sciences & Research", "applied-sciences-research", "Advanced doctoral and postgraduate research programs in computing and physics.", "Atom", 4),
        ]
        
        for name, slug, desc, icon, order in categories_data:
            if slug not in existing_cats:
                cat = CmsCourseCategory(
                    institute_id=institute.id,
                    name=name,
                    slug=slug,
                    description=desc,
                    icon_name=icon,
                    display_order=order,
                    is_active=True
                )
                session.add(cat)
                await session.flush()
                existing_cats[slug] = cat

        course_res = await session.execute(select(CmsCourse).where(CmsCourse.institute_id == institute.id))
        existing_courses = {c.code: c for c in course_res.scalars().all()}

        courses_data = [
            {
                "code": "BTECH-CSE",
                "slug": "b-tech-computer-science-engineering",
                "title": "B.Tech in Computer Science & Engineering (AI & ML)",
                "short_name": "B.Tech CSE",
                "category_slug": "engineering-technology",
                "degree_level": "UNDERGRADUATE",
                "duration": "4 Years (8 Semesters)",
                "study_mode": "Full-Time On-Campus",
                "annual_fee": "₹1,25,000 / Year",
                "total_fee": "₹5,00,000",
                "seats_intake": 120,
                "eligibility_summary": "10+2 with Physics, Mathematics & Chemistry/CS with minimum 60% aggregate and valid JEE/State CET rank.",
                "admission_process": "Merit-based admission through central state counseling followed by institute biometric document verification.",
                "career_prospects": "AI Research Engineer, Distributed Systems Architect, Cloud DevOps Specialist, Full-Stack Developer.",
                "summary": "Flagship 4-year autonomous engineering program accredited by NBA Tier-1 with integrated AI testbeds and high-density CBT exams.",
                "overview": "The B.Tech in Computer Science and Engineering with specialization in Artificial Intelligence and Machine Learning is designed to cultivate engineering leaders capable of architecting scalable computational systems. Benchmarked with premier global curricula, the program integrates algorithmic thinking, neural networks, distributed systems, and real-world industrial capstones.",
                "is_featured": True,
                "display_order": 1,
            },
            {
                "code": "BTECH-ECE",
                "slug": "b-tech-electronics-communication-engineering",
                "title": "B.Tech in Electronics & Communication Engineering (VLSI & IoT)",
                "short_name": "B.Tech ECE",
                "category_slug": "engineering-technology",
                "degree_level": "UNDERGRADUATE",
                "duration": "4 Years (8 Semesters)",
                "study_mode": "Full-Time On-Campus",
                "annual_fee": "₹1,10,000 / Year",
                "total_fee": "₹4,40,000",
                "seats_intake": 60,
                "eligibility_summary": "10+2 with Physics and Mathematics with minimum 55% aggregate.",
                "admission_process": "Centralized admission counseling and direct institutional merit rounds.",
                "career_prospects": "VLSI Design Engineer, Embedded Firmware Architect, 5G Telecommunications Engineer.",
                "summary": "Premier electronics program focusing on semiconductor design, silicon fabrication principles, and smart sensor networks.",
                "overview": "Accredited under NBA Tier-1, this program combines solid-state electronic fundamentals with modern VLSI chip design, embedded microcontrollers, and IoT protocols.",
                "is_featured": True,
                "display_order": 2,
            },
            {
                "code": "MBA-TECH",
                "slug": "mba-technology-business-management",
                "title": "Master of Business Administration (Tech Leadership & Analytics)",
                "short_name": "MBA Tech",
                "category_slug": "management-business",
                "degree_level": "POSTGRADUATE",
                "duration": "2 Years (4 Semesters)",
                "study_mode": "Full-Time On-Campus",
                "annual_fee": "₹1,40,000 / Year",
                "total_fee": "₹2,80,000",
                "seats_intake": 60,
                "eligibility_summary": "Bachelor degree in any discipline with minimum 50% aggregate and valid CAT/MAT/CMAT score.",
                "admission_process": "National entrance score shortlisting followed by Group Discussion and Personal Interview.",
                "career_prospects": "Product Manager, Tech Strategy Consultant, Operations Director, Financial Analyst.",
                "summary": "Executive-oriented dual specialization in digital product leadership, enterprise ERP governance, and business analytics.",
                "overview": "Blending rigorous business principles with technological acumen, our MBA program prepares modern leaders to drive digital transformation in Fortune 500 enterprises.",
                "is_featured": True,
                "display_order": 3,
            },
            {
                "code": "BCA-AI",
                "slug": "bca-artificial-intelligence-cloud",
                "title": "Bachelor of Computer Applications (AI & Cloud Systems)",
                "short_name": "BCA AI",
                "category_slug": "computer-applications-ai",
                "degree_level": "UNDERGRADUATE",
                "duration": "3 Years (6 Semesters)",
                "study_mode": "Full-Time On-Campus",
                "annual_fee": "₹75,000 / Year",
                "total_fee": "₹2,25,000",
                "seats_intake": 90,
                "eligibility_summary": "10+2 in any stream with Mathematics or Computer Science as a subject with min 50% aggregate.",
                "admission_process": "Direct merit round based on qualifying 10+2 marks.",
                "career_prospects": "Cloud Infrastructure Engineer, Full-Stack Developer, Database Administrator, App Developer.",
                "summary": "Three-year hands-on software development program featuring cloud containerization and machine learning models.",
                "overview": "Designed for rapid entry into the high-growth software and IT service sectors with continuous hands-on laboratory workshops and hackathons.",
                "is_featured": False,
                "display_order": 4,
            },
        ]

        for c_data in courses_data:
            if c_data["code"] not in existing_courses:
                cat = existing_cats[c_data.pop("category_slug")]
                course = CmsCourse(
                    institute_id=institute.id,
                    category_id=cat.id,
                    **c_data,
                    is_active=True
                )
                session.add(course)
                await session.flush()
                existing_courses[course.code] = course

                # Add sample curriculum semesters
                session.add(CmsCourseCurriculum(
                    course_id=course.id,
                    semester_number=1,
                    semester_title="Semester I: Computational Foundations",
                    credits=22,
                    subjects=[
                        {"code": "CS101", "title": "Programming & Problem Solving", "credits": 4, "type": "Core"},
                        {"code": "MA101", "title": "Discrete Mathematics & Linear Algebra", "credits": 4, "type": "Core"},
                        {"code": "PH101", "title": "Engineering Physics & Lab", "credits": 4, "type": "Core + Lab"},
                        {"code": "EE101", "title": "Basic Electrical & Electronic Engineering", "credits": 4, "type": "Core"},
                        {"code": "EN101", "title": "Professional Communication & Ethics", "credits": 2, "type": "Soft Skills"},
                        {"code": "CS102", "title": "Linux & Cloud Workshop", "credits": 4, "type": "Lab"}
                    ],
                    display_order=1
                ))
                session.add(CmsCourseCurriculum(
                    course_id=course.id,
                    semester_number=2,
                    semester_title="Semester II: Data Structures & Core Computing",
                    credits=24,
                    subjects=[
                        {"code": "CS201", "title": "Data Structures & Algorithms", "credits": 4, "type": "Core"},
                        {"code": "CS202", "title": "Object Oriented Programming via Modern C++", "credits": 4, "type": "Core"},
                        {"code": "MA201", "title": "Probability & Statistical Inference", "credits": 4, "type": "Core"},
                        {"code": "CS203", "title": "Digital Logic & Computer Organization", "credits": 4, "type": "Core"},
                        {"code": "CS204", "title": "Data Structures Implementation Lab", "credits": 4, "type": "Lab"},
                        {"code": "CS205", "title": "Open Source Capstone Project I", "credits": 4, "type": "Project"}
                    ],
                    display_order=2
                ))

                # Add sample faculty
                session.add(CmsCourseFaculty(
                    course_id=course.id,
                    faculty_name="Prof. (Dr.) Arvind Mehta",
                    designation="Professor & Head of Department",
                    qualifications="Ph.D. (IIT Bombay), M.Tech (CSE)",
                    specialization="Machine Learning, Distributed Systems",
                    avatar_url=None,
                    display_order=1
                ))
                session.add(CmsCourseFaculty(
                    course_id=course.id,
                    faculty_name="Dr. Priya Nambiar",
                    designation="Associate Professor",
                    qualifications="Ph.D. (BITS Pilani), M.E. (Software Engineering)",
                    specialization="Cloud Native Architectures, Microservices",
                    avatar_url=None,
                    display_order=2
                ))

        # 7. Seed Module 5 Admission System Baseline
        step_res = await session.execute(select(CmsAdmissionStep).where(CmsAdmissionStep.institute_id == institute.id))
        existing_steps = {s.step_number: s for s in step_res.scalars().all()}
        
        steps_data = [
            (1, "Digital Application Submission", "Fill the online application form with candidate personal, academic, and contact details.", "FileText", "Step 1: Online"),
            (2, "Document Scrutiny & Verification", "Academic marksheets, transfer certificates, and category credentials are electronically verified.", "CheckCircle2", "Step 2: Scrutiny"),
            (3, "CBT Exam / National Merit Mapping", "Performance evaluated via National CBT Examination scores or valid JEE/CET rankings.", "MonitorPlay", "Step 3: Evaluation"),
            (4, "Provisional Seat Allocation", "Eligible scholars receive provisional offer letters with branch allocation details.", "Award", "Step 4: Allocation"),
            (5, "Fee Payment & Final Enrollment", "Digital fee payment confirmation and generation of official institute roll numbers.", "IndianRupee", "Step 5: Enrollment")
        ]
        for step_num, title, desc, icon, badge in steps_data:
            if step_num not in existing_steps:
                session.add(CmsAdmissionStep(
                    institute_id=institute.id,
                    step_number=step_num,
                    title=title,
                    description=desc,
                    icon_name=icon,
                    timeline_badge=badge,
                    display_order=step_num,
                    is_active=True
                ))

        fee_res = await session.execute(select(CmsFeeStructure).where(CmsFeeStructure.institute_id == institute.id))
        existing_fees = {f.program_code: f for f in fee_res.scalars().all()}
        
        fees_data = [
            ("B.Tech Computer Science & Engineering (AI & ML)", "BTECH-CSE", "₹15,000", "₹55,000", "₹10,000", "₹5,000", "₹10,000 (Refundable)", "₹1,25,000 / Year", 1),
            ("B.Tech Electronics & Communication Engineering", "BTECH-ECE", "₹15,000", "₹47,500", "₹10,000", "₹5,000", "₹10,000 (Refundable)", "₹1,10,000 / Year", 2),
            ("Master of Business Administration (Tech Leadership)", "MBA-TECH", "₹20,000", "₹60,000", "₹15,000", "₹5,000", "₹10,000 (Refundable)", "₹1,40,000 / Year", 3),
            ("Bachelor of Computer Applications (AI & Cloud)", "BCA-AI", "₹10,000", "₹32,500", "₹5,000", "₹5,000", "₹5,000 (Refundable)", "₹75,000 / Year", 4)
        ]
        for p_name, p_code, adm, tuit, dev, exam, caut, tot, ord_num in fees_data:
            if p_code not in existing_fees:
                session.add(CmsFeeStructure(
                    institute_id=institute.id,
                    program_name=p_name,
                    program_code=p_code,
                    academic_year="2026-2027",
                    admission_fee=adm,
                    tuition_fee_per_semester=tuit,
                    development_fee=dev,
                    examination_fee=exam,
                    caution_deposit_refundable=caut,
                    total_annual_fee=tot,
                    display_order=ord_num,
                    is_active=True
                ))

        schol_res = await session.execute(select(CmsScholarship).where(CmsScholarship.institute_id == institute.id))
        existing_schols = {s.title: s for s in schol_res.scalars().all()}
        
        schol_data = [
            ("Chanakya Sovereign Merit Scholarship", "MERIT", "Students achieving >=95% aggregate in 10+2 CBSE/ICSE or Top 500 in National Entrance.", "100% Tuition Fee Waiver across all 4 years", 100, 20, 1),
            ("Dr. APJ Abdul Kalam Innovation Fellowship", "MERIT", "Candidates with exceptional STEM prototypes, patent filings, or >=85% in qualifying boards.", "50% Tuition Fee Waiver for academic tenure", 50, 40, 2),
            ("Beti Padhao Women in Technology Grant", "WOMEN_IN_TECH", "Meritorious female engineering applicants enrolling in Computer Science or Electronics.", "30% Tuition Fee Concession for all semesters", 30, 50, 3),
            ("National Armed Forces & Martyrs Ward Concession", "DEFENSE", "Wards of serving or retired defense personnel, CAPF, and state police martyrs.", "25% Fixed Fee Concession on annual tuition", 25, 30, 4)
        ]
        for s_title, s_cat, s_elig, s_ben, s_waiv, s_seats, s_ord in schol_data:
            if s_title not in existing_schols:
                session.add(CmsScholarship(
                    institute_id=institute.id,
                    title=s_title,
                    category=s_cat,
                    eligibility_criteria=s_elig,
                    benefit_summary=s_ben,
                    waiver_percentage=s_waiv,
                    seats_available=s_seats,
                    validity_period="Academic Year 2026-27",
                    display_order=s_ord,
                    is_active=True
                ))

        # 8. Seed Module 6 Faculty, Staff & Research Baseline
        fac_res = await session.execute(select(CmsFacultyMember).where(CmsFacultyMember.institute_id == institute.id))
        existing_fac = {f.email: f for f in fac_res.scalars().all()}

        faculty_data = [
            {
                "first_name": "Arvind",
                "last_name": "Mehta",
                "full_name": "Prof. (Dr.) Arvind Mehta",
                "slug": "dr-arvind-mehta",
                "department": "Computer Science & Engineering",
                "designation": "Professor & Head of Department",
                "qualifications": "Ph.D. (IIT Bombay), M.Tech (CSE)",
                "specialization": "Artificial Intelligence, Neural Computations, Distributed Systems",
                "email": "arvind.mehta@myeducation.in",
                "phone": "+91 (0731) 4900-110",
                "experience_years": 22,
                "office_location": "Technology Tower, Room 401",
                "research_interests": "Deep Neural Architectures, Autonomous Robotics, Edge AI Acceleration, Federated Learning",
                "teaching_courses": "CS601 (Machine Learning & Neural Networks), CS605L (AI Lab), CS802 (Advanced Neural Systems)",
                "google_scholar_url": "https://scholar.google.com/citations?user=arvindmehta",
                "orcid_id": "0000-0002-1823-9210",
                "linkedin_url": "https://linkedin.com/in/arvindmehta-ai",
                "researchgate_url": "https://www.researchgate.net/profile/Arvind-Mehta",
                "bio": "Prof. Mehta has over 22 years of research and teaching experience in scalable machine learning systems and algorithmic foundations. Recipient of national research awards, he chairs the Autonomous Academic Board for Computing.",
                "total_citations": 1420,
                "h_index": 18,
                "patents_count": 3,
                "is_head_of_department": True,
                "display_order": 1,
            },
            {
                "first_name": "Priya",
                "last_name": "Nambiar",
                "full_name": "Dr. Priya Nambiar",
                "slug": "dr-priya-nambiar",
                "department": "Computer Science & Engineering",
                "designation": "Associate Professor",
                "qualifications": "Ph.D. (BITS Pilani), M.E. (Software Engineering)",
                "specialization": "Cloud-Native Architectures, Microservices, Kubernetes Optimization",
                "email": "priya.nambiar@myeducation.in",
                "phone": "+91 (0731) 4900-112",
                "experience_years": 14,
                "office_location": "Computing Block, Room 208",
                "research_interests": "Cloud Native Microservices, Distributed Systems, Container Security, Serverless Latency Optimization",
                "teaching_courses": "CS602 (Cloud Computing & Distributed Systems), CS401 (Operating Systems), CS703 (DevOps Engineering)",
                "google_scholar_url": "https://scholar.google.com/citations?user=priyanambiar",
                "orcid_id": "0000-0003-4921-1102",
                "linkedin_url": "https://linkedin.com/in/priyanambiar-cloud",
                "researchgate_url": "https://www.researchgate.net/profile/Priya-Nambiar",
                "bio": "Dr. Nambiar specializes in cloud native infrastructures, distributed ledger security, and software containerization. She leads the cloud research laboratory at MEI Indore.",
                "total_citations": 860,
                "h_index": 12,
                "patents_count": 1,
                "is_head_of_department": False,
                "display_order": 2,
            },
            {
                "first_name": "Vikramaditya",
                "last_name": "Rao",
                "full_name": "Prof. (Dr.) Vikramaditya Rao",
                "slug": "dr-vikramaditya-rao",
                "department": "Electronics & Communication Engineering",
                "designation": "Professor & Dean of Research",
                "qualifications": "Ph.D. (IISc Bangalore), M.Tech (VLSI Design)",
                "specialization": "Semiconductor Physics, VLSI Chip Architectures, 5G Sensor Networks",
                "email": "vikram.rao@myeducation.in",
                "phone": "+91 (0731) 4900-120",
                "experience_years": 25,
                "office_location": "Microelectronics Wing, Room 305",
                "research_interests": "Semiconductor VLSI, 5G RF Transceivers, Quantum Sensing, Nano-dielectrics",
                "teaching_courses": "EC501 (VLSI Design), EC504L (Embedded Systems Lab), EC701 (Wireless Communications)",
                "google_scholar_url": "https://scholar.google.com/citations?user=vikramadityarao",
                "orcid_id": "0000-0001-9012-3814",
                "linkedin_url": "https://linkedin.com/in/dr-vikramaditya-rao",
                "researchgate_url": "https://www.researchgate.net/profile/Vikramaditya-Rao",
                "bio": "With more than 50 published IEEE journal articles, Dr. Rao spearheads the institute R&D Directorate and industry collaborations with leading semiconductor foundry consortiums.",
                "total_citations": 2150,
                "h_index": 24,
                "patents_count": 5,
                "is_head_of_department": True,
                "display_order": 3,
            },
            {
                "first_name": "Meenakshi",
                "last_name": "Sundaram",
                "full_name": "Dr. Meenakshi Sundaram",
                "slug": "dr-meenakshi-sundaram",
                "department": "Management Studies",
                "designation": "Professor & Head of Department",
                "qualifications": "Ph.D. (IIM Ahmedabad), MBA (Finance)",
                "specialization": "Technology Commercialization, Enterprise Strategy, FinTech Analytics",
                "email": "meenakshi.s@myeducation.in",
                "phone": "+91 (0731) 4900-130",
                "experience_years": 18,
                "office_location": "Management Annex, Room 102",
                "research_interests": "FinTech Innovation, Technology Commercialization, Corporate Strategy, Capital Markets",
                "teaching_courses": "MBA602 (Strategic Management), MBA608 (Corporate Finance), MBA701 (FinTech Disruption)",
                "google_scholar_url": "https://scholar.google.com/citations?user=meenakshisundaram",
                "orcid_id": "0000-0002-7714-9921",
                "linkedin_url": "https://linkedin.com/in/dr-meenakshi-sundaram",
                "researchgate_url": "https://www.researchgate.net/profile/Meenakshi-Sundaram",
                "bio": "Dr. Sundaram bridges technological innovation with executive corporate governance. Consultant to multinational financial institutions and author of premier business case studies.",
                "total_citations": 940,
                "h_index": 14,
                "patents_count": 0,
                "is_head_of_department": True,
                "display_order": 4,
            },
        ]

        for f_data in faculty_data:
            if f_data["email"] not in existing_fac:
                fac = CmsFacultyMember(
                    institute_id=institute.id,
                    **f_data,
                    is_active=True
                )
                session.add(fac)
                await session.flush()
                existing_fac[fac.email] = fac

                # Add sample research papers
                spec_keyword = fac.specialization.split(",")[0]
                session.add(CmsResearchPublication(
                    faculty_id=fac.id,
                    title=f"Scalable High-Throughput Processing in {spec_keyword} Networks",
                    journal_or_conference="IEEE Transactions on Knowledge and Data Engineering",
                    publication_year=2025,
                    doi_or_url="https://doi.org/10.1109/TKDE.2025.1092812",
                    citation_count=45,
                    indexing="SCI / Scopus Q1"
                ))

        staff_res = await session.execute(select(CmsStaffMember).where(CmsStaffMember.institute_id == institute.id))
        existing_staff = {s.official_email: s for s in staff_res.scalars().all()}

        staff_data = [
            ("Mr. Sudhir K. Tiwari", "Registrar Directorate", "Deputy Registrar (Academic Administration)", "Admin Block, Room 101", "registrar.desk@myeducation.in", "Ext 101", 1),
            ("Ms. Ananya Sen", "Finance & Accounts", "Finance Controller & Accounts Officer", "Finance Wing, Room 204", "accounts@myeducation.in", "Ext 204", 2),
            ("Dr. R. K. Mukherjee", "Examination & CBT Cell", "Chief Controller of Examinations", "Technology Tower, Room 302", "exam.cell@myeducation.in", "Ext 302", 3),
            ("Mr. Devendra Solanki", "Library & Information Science", "Chief University Librarian", "Central Digital Library, Ground Floor", "library@myeducation.in", "Ext 150", 4),
        ]

        for s_name, s_div, s_desig, s_room, s_mail, s_ext, s_ord in staff_data:
            if s_mail not in existing_staff:
                session.add(CmsStaffMember(
                    institute_id=institute.id,
                    full_name=s_name,
                    division=s_div,
                    designation=s_desig,
                    office_room_number=s_room,
                    official_email=s_mail,
                    extension_number=s_ext,
                    visiting_hours="Mon–Fri (2:00 PM – 4:30 PM)",
                    display_order=s_ord,
                    is_active=True
                ))

        # 9. Seed Module 7 Placements, Recruiters & Alumni Stories
        stat_res = await session.execute(select(CmsPlacementStat).where(CmsPlacementStat.institute_id == institute.id))
        existing_stats = {s.academic_year: s for s in stat_res.scalars().all()}

        stats_data = [
            ("2025-2026", "₹52.0 LPA", "₹12.8 LPA", "₹10.5 LPA", 1450, 98.50, 250, 1),
            ("2024-2025", "₹48.0 LPA", "₹11.4 LPA", "₹9.8 LPA", 1380, 97.80, 230, 2),
            ("2023-2024", "₹44.0 LPA", "₹10.2 LPA", "₹8.9 LPA", 1260, 96.50, 210, 3),
        ]
        for yr, high, avg, med, offers, pct, comps, ord_num in stats_data:
            if yr not in existing_stats:
                session.add(CmsPlacementStat(
                    institute_id=institute.id,
                    academic_year=yr,
                    highest_package_lpa=high,
                    average_package_lpa=avg,
                    median_package_lpa=med,
                    total_offers=offers,
                    placement_percentage=pct,
                    participating_companies=comps,
                    display_order=ord_num,
                    is_active=True
                ))

        rec_res = await session.execute(select(CmsRecruiterPartner).where(CmsRecruiterPartner.institute_id == institute.id))
        existing_recs = {r.slug: r for r in rec_res.scalars().all()}

        recruiters_data = [
            ("Google", "google", "IT & Software", "DAY_0", "₹52.0 LPA", "https://google.com", "Bangalore & Hyderabad", 1),
            ("Microsoft", "microsoft", "IT & Software", "DAY_0", "₹48.0 LPA", "https://microsoft.com", "Redmond & Hyderabad", 2),
            ("NVIDIA", "nvidia", "AI & Hardware", "DAY_0", "₹45.0 LPA", "https://nvidia.com", "Pune & Bangalore", 3),
            ("Amazon AWS", "amazon-aws", "Cloud & Distributed Systems", "TIER_1", "₹44.0 LPA", "https://amazon.com", "Hyderabad", 4),
            ("Deloitte", "deloitte", "Consulting & Analytics", "TIER_1", "₹18.0 LPA", "https://deloitte.com", "Mumbai & Gurgaon", 5),
            ("Larsen & Toubro", "larsen-toubro", "Core Engineering & Infrastructure", "TIER_1", "₹15.0 LPA", "https://larsentoubro.com", "Mumbai", 6),
            ("Tata Consultancy Services", "tcs", "Enterprise Digital Systems", "REGULAR", "₹12.0 LPA", "https://tcs.com", "Indore & Mumbai", 7),
        ]
        for c_name, c_slug, c_sec, c_tier, c_pkg, c_web, c_hq, c_ord in recruiters_data:
            if c_slug not in existing_recs:
                session.add(CmsRecruiterPartner(
                    institute_id=institute.id,
                    company_name=c_name,
                    slug=c_slug,
                    sector=c_sec,
                    tier=c_tier,
                    highest_package_lpa=c_pkg,
                    website_url=c_web,
                    headquarters=c_hq,
                    display_order=c_ord,
                    is_active=True
                ))

        alumni_res = await session.execute(select(CmsAlumniSuccessStory).where(CmsAlumniSuccessStory.institute_id == institute.id))
        existing_stories = {s.alumni_name: s for s in alumni_res.scalars().all()}

        stories_data = [
            ("Aarushi Jain", "B.Tech Computer Science & Engineering (AI & ML)", 2024, "Google Cloud", "AI Solutions Engineer", "₹48.0 LPA", "The rigorous AI lab coursework, high-density CBT exams, and doctoral mentorship at MY EDUCATION INDIA prepared me to excel in global engineering challenges.", 1),
            ("Siddharth Saxena", "B.Tech Electronics & Communication Engineering", 2023, "NVIDIA", "Silicon Verification Engineer", "₹42.5 LPA", "Hands-on VLSI chip design testbeds and IEEE paper publications at MEI Indore directly shaped my hiring trajectory at NVIDIA.", 2),
            ("Megha Rajput", "Master of Business Administration (Tech Leadership)", 2024, "Microsoft", "Senior Product Manager", "₹36.0 LPA", "The executive MBA program gave me deep command over enterprise ERP architectures and technology commercialization.", 3),
        ]
        for a_name, a_prog, a_yr, a_comp, a_desig, a_pkg, a_quote, a_ord in stories_data:
            if a_name not in existing_stories:
                session.add(CmsAlumniSuccessStory(
                    institute_id=institute.id,
                    alumni_name=a_name,
                    degree_program=a_prog,
                    graduation_year=a_yr,
                    company_name=a_comp,
                    designation=a_desig,
                    package_lpa=a_pkg,
                    testimonial_quote=a_quote,
                    is_featured=True,
                    display_order=a_ord,
                    is_active=True
                ))

        # 10. Seed Module 8 Events, News, Notices & Achievements Baseline
        event_res = await session.execute(select(CmsEvent).where(CmsEvent.institute_id == institute.id))
        existing_events = {e.slug: e for e in event_res.scalars().all()}

        events_data = [
            ("National Conference on Applied AI & Deep Neural Systems", "national-ai-conference-2026", "ACADEMIC", "2026-03-24", "2026-03-26", "09:30 AM – 05:00 PM", "Main Auditorium, Block A", "A 3-day premier international academic gathering bringing together computer scientists, neural engineers, and doctoral scholars.", "https://myeducation.in/events/register/ai-2026", True, 1),
            ("Smart Campus 36-Hour Hackathon 2026", "smart-campus-hackathon-2026", "HACKATHON", "2026-04-10", "2026-04-12", "36 Hours Continuous", "Innovation Hub & CBT Center", "National student hackathon tackling enterprise ERP challenges, autonomous drones, and IoT edge hardware.", "https://myeducation.in/events/register/hack-2026", True, 2),
            ("Annual Cultural Fest & Tech Carnival: INVICTUS 2026", "invictus-cultural-fest-2026", "CULTURAL", "2026-04-20", "2026-04-22", "10:00 AM – 09:00 PM", "Open Air Amphitheatre & Sports Arena", "Central India largest inter-university technical and cultural confluence with 10,000+ student attendees.", None, False, 3),
        ]
        for title, slug, cat, start, end, tim, ven, sum_t, reg_l, flag, ord_n in events_data:
            if slug not in existing_events:
                session.add(CmsEvent(
                    institute_id=institute.id,
                    title=title,
                    slug=slug,
                    category=cat,
                    start_date=start,
                    end_date=end,
                    time_window=tim,
                    venue=ven,
                    summary=sum_t,
                    registration_link=reg_l,
                    is_flagship=flag,
                    display_order=ord_n,
                    is_active=True
                ))

        news_res = await session.execute(select(CmsNewsArticle).where(CmsNewsArticle.institute_id == institute.id))
        existing_news = {n.slug: n for n in news_res.scalars().all()}

        news_data = [
            ("MY EDUCATION INDIA Secures Top Rank in Central India for AI & Autonomous Research", "mei-top-rank-ai-research-2026", "Research", "2026-02-15", "National higher education survey ranks MEI Indore as the premier autonomous institute in artificial intelligence and outcome-based engineering education.", "The Ministry of Education and national higher education councils have recognized MY EDUCATION INDIA Indore campus for exceptional performance in research citations, high-density CBT platform delivery, and Fortune 500 corporate placements.", 1),
            ("Flagship 500-Seat National CBT Center Commissioned at Technology Tower", "flagship-cbt-center-commissioned", "Campus Life", "2026-01-20", "Dedicated biometric test center equipped with redundant dual-gigabit optical fiber lines and isolated testing nodes.", "Commissioned under the Directorate of Examinations, the new CBT facility enables sub-second real-time examination submissions with zero single-point-of-failure risks.", 2),
        ]
        for h, sl, c, pd, sm, cnt, ord_n in news_data:
            if sl not in existing_news:
                session.add(CmsNewsArticle(
                    institute_id=institute.id,
                    headline=h,
                    slug=sl,
                    category=c,
                    publish_date=pd,
                    summary=sm,
                    content=cnt,
                    display_order=ord_n,
                    is_active=True
                ))

        not_res = await session.execute(select(CmsNoticeCircular).where(CmsNoticeCircular.institute_id == institute.id))
        existing_not = {nt.circular_number: nt for nt in not_res.scalars().all()}

        notices_data = [
            ("MEI/EXAM/2026/041", "End-Semester Theory & CBT Examination Schedule Announced", "EXAMINATION", "2026-03-01", "Detailed examination timetable, seat matrix, and biometric admit card issuance instructions for all undergraduate and postgraduate cohorts.", True, 1),
            ("MEI/ACAD/2026/018", "Commencement of Academic Session 2026-27 Enrollment & Registration", "ACADEMIC", "2026-02-28", "Official registrar circular detailing semester fee installments, course selection deadlines, and laboratory batch allocations.", False, 2),
        ]
        for cno, t, cat, pd, desc, urg, ord_n in notices_data:
            if cno not in existing_not:
                session.add(CmsNoticeCircular(
                    institute_id=institute.id,
                    circular_number=cno,
                    title=t,
                    category=cat,
                    publish_date=pd,
                    description=desc,
                    is_urgent=urg,
                    display_order=ord_n,
                    is_active=True
                ))

        ach_res = await session.execute(select(CmsAchievement).where(CmsAchievement.institute_id == institute.id))
        existing_ach = {a.title: a for a in ach_res.scalars().all()}

        ach_data = [
            ("NAAC Institutional Grade A+ Accreditation (3.68 CGPA)", "INSTITUTIONAL", "National Assessment and Accreditation Council", "2024", "Recognized for institutional excellence, research publications, autonomous curriculum flexibility, and student outcome benchmarks.", 1),
            ("National Best Campus in Autonomous Cloud ERP Innovation", "RESEARCH", "Ministry of Education / AICTE", "2025", "Awarded national distinction for digital campus transformation, encrypted student identity QR cards, and real-time examination telemetry.", 2),
        ]
        for at, ac, ab, ay, ad, aord in ach_data:
            if at not in existing_ach:
                session.add(CmsAchievement(
                    institute_id=institute.id,
                    title=at,
                    category=ac,
                    awarding_body=ab,
                    award_year=ay,
                    description=ad,
                    display_order=aord,
                    is_active=True
                ))


        # Module 9: Gallery Management CMS (Albums & Media)
        alb_res = await session.execute(select(CmsGalleryAlbum).where(CmsGalleryAlbum.institute_id == institute.id))
        existing_albs = {a.slug: a for a in alb_res.scalars().all()}

        albums_data = [
            {
                "title": "Annual Convocation & Degree Ceremony 2025",
                "slug": "convocation-2025",
                "category": "CONVOCATION",
                "description": "Celebration of the graduating undergraduate, postgraduate, and doctoral classes with Chancellor's gold medals.",
                "cover_image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1200&q=80",
                "academic_year": "2024-2025",
                "event_date": "2025-01-20",
                "is_featured": True,
                "display_order": 1,
                "media": [
                    ("IMAGE", "Chancellor's Gold Medal Presentation", "Awarded for highest cumulative academic standing in engineering.", "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1200&q=80", 1, True),
                    ("IMAGE", "Doctoral Faculty Academic Procession", "Senior academic senate leading the ceremonial march into the main auditorium.", "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80", 2, False),
                    ("VIDEO", "Valedictorian Commemorative Address", "Speech by computer science valedictorian on autonomous technology frontiers.", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 3, False),
                    ("IMAGE", "Graduating Cohort Ceremonial Cap Toss", "Over 800 graduates celebrating their engineering and business degrees.", "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80", 4, False),
                ]
            },
            {
                "title": "Smart Campus 36-Hour National Hackathon",
                "slug": "hackathon-2025",
                "category": "HACKATHON",
                "description": "National student developers building cloud ERP microservices, neural vision edge devices, and EV fleet telemetry.",
                "cover_image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
                "academic_year": "2025-2026",
                "event_date": "2025-11-14",
                "is_featured": True,
                "display_order": 2,
                "media": [
                    ("IMAGE", "Hardware IoT Prototyping Station", "Teams integrating LoRaWAN sensors with edge microcontrollers.", "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80", 1, True),
                    ("IMAGE", "Midnight Algorithm & Architecture Sprint", "Over 60 teams coding in the high-performance computing center.", "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80", 2, False),
                    ("VIDEO", "Jury Grand Finale Live Demonstrations", "Industry engineering directors evaluating real-time student prototypes.", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 3, False),
                ]
            },
            {
                "title": "Vibrance Annual Cultural & Arts Festival",
                "slug": "vibrance-cultural-2026",
                "category": "CULTURAL",
                "description": "A 3-day inter-collegiate cultural extravaganza featuring musical bands, classical recitals, and theatrical productions.",
                "cover_image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=80",
                "academic_year": "2025-2026",
                "event_date": "2026-02-18",
                "is_featured": True,
                "display_order": 3,
                "media": [
                    ("IMAGE", "Classical Bharatnatyam Ensemble", "Student cultural troupe performing at the open-air amphitheater.", "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=80", 1, True),
                    ("IMAGE", "National Battle of the Bands Finals", "Campus rock and fusion bands competing in the central arena.", "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80", 2, False),
                ]
            },
            {
                "title": "Advanced Neural Robotics & Cleanroom Laboratories",
                "slug": "research-laboratories",
                "category": "RESEARCH",
                "description": "Tour of state-of-the-art semiconductor prototyping cleanroom, high-performance computing clusters, and robotics test beds.",
                "cover_image_url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1200&q=80",
                "academic_year": "2025-2026",
                "event_date": "2025-09-10",
                "is_featured": False,
                "display_order": 4,
                "media": [
                    ("IMAGE", "NVIDIA HGX AI Supercomputing Rig", "Dedicated enterprise GPU compute cluster for doctoral neural model training.", "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1200&q=80", 1, True),
                    ("IMAGE", "Autonomous Drone Aerodynamics Cage", "Sensor-instrumented flight test chamber for multi-rotor obstacle avoidance.", "https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?auto=format&fit=crop&w=1200&q=80", 2, False),
                ]
            },
            {
                "title": "Inter-University Sports Championship 2025",
                "slug": "sports-championship-2025",
                "category": "SPORTS",
                "description": "Championship athletic meets, basketball tournaments, and badminton finals across the Olympic-standard sports complex.",
                "cover_image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1200&q=80",
                "academic_year": "2025-2026",
                "event_date": "2025-10-05",
                "is_featured": False,
                "display_order": 5,
                "media": [
                    ("IMAGE", "Basketball Championship Finals", "High-intensity varsity tournament match at the indoor sports pavilion.", "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=1200&q=80", 1, True),
                    ("IMAGE", "Track & Field 100m Gold Sprint Finish", "Varsity athlete claiming gold at the state university athletic meet.", "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1200&q=80", 2, False),
                ]
            },
            {
                "title": "Campus Architecture & Smart Quadrangle",
                "slug": "campus-architecture",
                "category": "CAMPUS_LIFE",
                "description": "Visual journey across the 50-acre smart autonomous campus at Indore: green courtyards, rotunda, and libraries.",
                "cover_image_url": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?auto=format&fit=crop&w=1200&q=80",
                "academic_year": "2025-2026",
                "event_date": "2025-08-01",
                "is_featured": False,
                "display_order": 6,
                "media": [
                    ("IMAGE", "Central Autonomous Knowledge Rotunda", "Solar-passive library housing over 150,000 physical volumes and digital kiosks.", "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?auto=format&fit=crop&w=1200&q=80", 1, True),
                    ("IMAGE", "Smart Student Innovation Incubator", "Glass-enclosed collaborative study spaces and entrepreneurship pods.", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80", 2, False),
                ]
            }
        ]

        for ad in albums_data:
            alb = existing_albs.get(ad["slug"])
            if not alb:
                alb = CmsGalleryAlbum(
                    institute_id=institute.id,
                    title=ad["title"],
                    slug=ad["slug"],
                    category=ad["category"],
                    description=ad["description"],
                    cover_image_url=ad["cover_image_url"],
                    academic_year=ad["academic_year"],
                    event_date=ad["event_date"],
                    item_count=len(ad["media"]),
                    is_featured=ad["is_featured"],
                    display_order=ad["display_order"],
                    is_active=True
                )
                session.add(alb)
                await session.flush()
                for m_type, m_title, m_cap, m_url, m_ord, m_cov in ad["media"]:
                    session.add(CmsGalleryMedia(
                        album_id=alb.id,
                        media_type=m_type,
                        title=m_title,
                        caption=m_cap,
                        url=m_url,
                        thumbnail_url=m_url,
                        video_provider="YOUTUBE" if m_type == "VIDEO" else None,
                        video_embed_id="dQw4w9WgXcQ" if m_type == "VIDEO" else None,
                        display_order=m_ord,
                        is_cover=m_cov,
                        is_active=True
                    ))


        # Module 10: Downloads CMS (Categories & Documents)
        dl_cat_res = await session.execute(select(CmsDownloadCategory).where(CmsDownloadCategory.institute_id == institute.id))
        existing_dl_cats = {c.slug: c for c in dl_cat_res.scalars().all()}

        dl_data = [
            {
                "name": "Prospectus & Brochures",
                "slug": "prospectus",
                "description": "Comprehensive admission brochures, institutional overview, fee charts, and autonomous campus guidelines.",
                "icon_name": "BookOpen",
                "display_order": 1,
                "docs": [
                    ("Comprehensive Information Brochure & Prospectus 2026-27", "prospectus-2026-27", "Official guide containing program catalogs, eligibility criteria, laboratory infrastructure, and faculty credentials.", "ALL", "ALL_PROGRAMS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "4.8 MB", "PDF", "v2.6", 1240, True, True, 1),
                    ("Autonomous Campus Overview & Placement Highlights 2025-26", "placement-highlights-2025-26", "Executive summary of corporate campus recruitment records, high packages, and recruiters roster.", "ALL", "ALL_PROGRAMS", "2025-2026", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "2.1 MB", "PDF", "v1.4", 860, False, False, 2),
                ]
            },
            {
                "name": "Academic Syllabi",
                "slug": "syllabus",
                "description": "AICTE & UGC compliant Choice Based Credit System (CBCS) curriculum schemes, course outcomes, and lab manuals.",
                "icon_name": "FileText",
                "display_order": 2,
                "docs": [
                    ("B.Tech Computer Science & Engineering CBCS Syllabus (Sem I - VIII)", "btech-cse-syllabus-full", "Complete 4-year engineering scheme including AI, Machine Learning, Cloud Systems, and Neural Networks.", "STUDENTS", "BTECH-CSE", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "3.4 MB", "PDF", "v3.2", 3420, True, True, 1),
                    ("B.Tech AI & Data Science Specialized Curriculum Handbook", "btech-aids-syllabus", "Detailed curriculum on deep learning, computer vision, data warehousing, and ethical AI governance.", "STUDENTS", "BTECH-AI-DS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "2.8 MB", "PDF", "v2.0", 1850, False, True, 2),
                    ("M.Tech Advanced Computing & Neural Systems Scheme", "mtech-cse-syllabus", "Postgraduate research scheme in distributed computing, quantum algorithms, and neural architecture.", "STUDENTS", "MTECH-CSE", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "1.9 MB", "PDF", "v1.8", 620, False, False, 3),
                    ("Bachelor of Computer Applications (Honours) Scheme", "bca-hons-syllabus", "Full 3-year curriculum in full-stack cloud development, database engineering, and DevOps pipelines.", "STUDENTS", "BCA-HONS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "2.2 MB", "PDF", "v2.1", 1140, False, False, 4),
                ]
            },
            {
                "name": "Application & Official Forms",
                "slug": "forms",
                "description": "Standard institutional administrative forms, scholarship claims, transcript requisitions, and hostel bookings.",
                "icon_name": "ClipboardList",
                "display_order": 3,
                "docs": [
                    ("Official Transcript & Degree Verification Request Form", "transcript-request-form", "Proforma for requesting certified grade transcripts, duplicate marksheets, and migration certificates.", "STUDENTS", "ALL_PROGRAMS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "420 KB", "PDF", "v1.2", 530, False, False, 1),
                    ("Hostel Accommodation Application & Anti-Ragging Undertaking", "hostel-application-form", "Mandatory affidavit, code of conduct, mess enrollment, and medical history declaration form.", "STUDENTS", "ALL_PROGRAMS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "680 KB", "PDF", "v2.0", 890, False, False, 2),
                    ("Merit-Cum-Means Scholarship Application Form", "scholarship-application-form", "Application form for institutional tuition fee concessions, parent income declaration, and bank details.", "PROSPECTIVE", "ALL_PROGRAMS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "510 KB", "PDF", "v1.5", 940, False, False, 3),
                    ("No Dues Clearance Certificate Form", "no-dues-form", "Multi-department clearance form across library, labs, sports, hostel, and accounts for degree convocation.", "STUDENTS", "ALL_PROGRAMS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "310 KB", "PDF", "v1.0", 710, False, False, 4),
                ]
            },
            {
                "name": "Exam Time Tables",
                "slug": "time-tables",
                "description": "Autonomous examination schedules, midterm practical evaluations, and hall ticket distribution windows.",
                "icon_name": "Clock",
                "display_order": 4,
                "docs": [
                    ("End-Semester Examination Time Table (Even Sem 2025-26)", "end-sem-exam-timetable-even-2026", "Official datesheet, session timings (Morning/Afternoon), reporting protocols, and seating blocks.", "STUDENTS", "ALL_PROGRAMS", "2025-2026", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "850 KB", "PDF", "v1.1", 4120, True, True, 1),
                    ("Mid-Term Assessment & Practical Lab Schedule", "midterm-practical-schedule-2026", "Internal continuous assessment timetable for all technical and applied computing laboratories.", "STUDENTS", "ALL_PROGRAMS", "2025-2026", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "540 KB", "PDF", "v1.0", 2300, False, False, 2),
                ]
            },
            {
                "name": "Academic Calendars",
                "slug": "academic-calendar",
                "description": "Institutional terms, commencement of classes, examination dates, cultural festivals, and vacation windows.",
                "icon_name": "Calendar",
                "display_order": 5,
                "docs": [
                    ("Autonomous Institutional Academic Calendar 2026-27", "academic-calendar-2026-27", "Comprehensive term calendar covering 180 instructional days, fee payment deadlines, and convocation dates.", "ALL", "ALL_PROGRAMS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "1.2 MB", "PDF", "v1.0", 2890, True, True, 1),
                    ("Gazetted Holidays & Semester Break Schedule 2026", "holidays-schedule-2026", "State and national holidays list, Diwali break, winter recess, and preparatory leaves.", "ALL", "ALL_PROGRAMS", "2025-2026", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "380 KB", "PDF", "v1.0", 1450, False, False, 2),
                ]
            },
            {
                "name": "Circulars & Guidelines",
                "slug": "circulars",
                "description": "Statutory regulatory guidelines, UGC autonomous rubrics, anti-ragging policies, and student research codes.",
                "icon_name": "Award",
                "display_order": 6,
                "docs": [
                    ("Autonomous Examination Code of Conduct & Rubrics", "exam-code-of-conduct", "Guidelines on unfair means prevention, grading rubrics, attendance thresholds (75%), and grade recalculation.", "ALL", "ALL_PROGRAMS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "1.4 MB", "PDF", "v2.2", 1180, False, False, 1),
                    ("Student Research Publication & Patent Grant Policy", "research-publication-policy", "Financial incentive rules, publication fee reimbursements, and patent filing support frameworks.", "STUDENTS", "ALL_PROGRAMS", "2026-2027", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "1.1 MB", "PDF", "v1.3", 760, False, False, 2),
                ]
            }
        ]

        for cat_data in dl_data:
            cat = existing_dl_cats.get(cat_data["slug"])
            if not cat:
                cat = CmsDownloadCategory(
                    institute_id=institute.id,
                    name=cat_data["name"],
                    slug=cat_data["slug"],
                    description=cat_data["description"],
                    icon_name=cat_data["icon_name"],
                    display_order=cat_data["display_order"],
                    is_active=True
                )
                session.add(cat)
                await session.flush()
                for doc_title, doc_slug, doc_desc, doc_aud, doc_prog, doc_yr, doc_url, doc_size, doc_fmt, doc_ver, doc_cnt, doc_pin, doc_feat, doc_ord in cat_data["docs"]:
                    session.add(CmsDownloadDocument(
                        category_id=cat.id,
                        institute_id=institute.id,
                        title=doc_title,
                        slug=doc_slug,
                        description=doc_desc,
                        target_audience=doc_aud,
                        applicable_program=doc_prog,
                        academic_year=doc_yr,
                        file_url=doc_url,
                        file_size_formatted=doc_size,
                        file_format=doc_fmt,
                        version=doc_ver,
                        download_count=doc_cnt,
                        is_pinned=doc_pin,
                        is_featured=doc_feat,
                        display_order=doc_ord,
                        is_active=True
                    ))


        # Module 12: Placement Cell CMS (Drives, Training, Internships)
        drive_res = await session.execute(select(CmsPlacementDrive).where(CmsPlacementDrive.institute_id == institute.id))
        existing_drives = {d.slug: d for d in drive_res.scalars().all()}

        drives_data = [
            ("Google Cloud India - Campus Pool Drive 2026", "google-cloud-drive-2026", "Member Technical Staff / SDE-1", "₹38.5 LPA", "2026-03-24", "2026-03-18", "B.Tech CSE, AI & Data Science (CGPA >= 8.0)", "1. Online Algorithmic Test -> 2. Technical System Design -> 3. Executive HR", "Bengaluru / Hyderabad", "UPCOMING", "https://myeducation.in/placements/register/google-2026", 1),
            ("Microsoft India Development Center (IDC)", "microsoft-idc-drive-2026", "Software Engineer - Core Platform", "₹44.0 LPA", "2026-04-05", "2026-03-28", "B.Tech CSE, AI & Data Science, ECE (CGPA >= 7.5)", "1. Codility Test -> 2. Technical Architecture -> 3. Executive Fit", "Hyderabad / Noida", "UPCOMING", "https://myeducation.in/placements/register/microsoft-2026", 2),
            ("Amazon AWS Cloud Services", "amazon-aws-drive-2026", "Cloud Support & SDE Associate", "₹32.0 LPA", "2026-04-12", "2026-04-02", "B.Tech All Engineering Branches", "1. Online Assessment -> 2. Virtual Bar Raiser -> 3. Technical Rounds", "Bengaluru / Indore", "UPCOMING", "https://myeducation.in/placements/register/amazon-2026", 3),
            ("Goldman Sachs Engineering", "goldman-sachs-drive-2026", "Financial Tech Analyst & Developer", "₹28.0 LPA", "2026-04-20", "2026-04-10", "B.Tech CSE, AI & Data Science, MBA Finance", "1. HackerRank Math/Algo -> 2. Technical Rounds -> 3. Managing Director Interview", "Bengaluru", "UPCOMING", "https://myeducation.in/placements/register/goldman-2026", 4),
        ]

        for d_comp, d_slug, d_role, d_pkg, d_date, d_dl, d_br, d_proc, d_loc, d_st, d_lnk, d_ord in drives_data:
            if d_slug not in existing_drives:
                session.add(CmsPlacementDrive(
                    institute_id=institute.id,
                    company_name=d_comp,
                    slug=d_slug,
                    job_role=d_role,
                    package_ctc=d_pkg,
                    drive_date=d_date,
                    registration_deadline=d_dl,
                    eligible_branches=d_br,
                    selection_process=d_proc,
                    job_location=d_loc,
                    drive_status=d_st,
                    registration_link=d_lnk,
                    display_order=d_ord,
                    is_active=True
                ))

        train_res = await session.execute(select(CmsTrainingProgram).where(CmsTrainingProgram.institute_id == institute.id))
        existing_train = {t.slug: t for t in train_res.scalars().all()}

        train_data = [
            ("Enterprise Full-Stack Cloud & System Design Bootcamp", "fullstack-cloud-bootcamp", "TECHNICAL_BOOTCAMP", "Industry Principal Architects & FAANG Mentors", 8, "2026-01-15", "2026-03-12", "Microservices Architecture, PostgreSQL Scaling, Docker/Kubernetes, Distributed Caching, High-Concurrency APIs", "3rd & 4th Year B.Tech Students", "HYBRID", 1),
            ("Competitive Coding & Data Structures Sprint", "dsa-competitive-coding-sprint", "TECHNICAL_BOOTCAMP", "ACM-ICPC Regional Finalists", 6, "2026-02-01", "2026-03-15", "Dynamic Programming, Graph Theory, Trie Algorithms, Bit Manipulation, Complexity Optimization", "2nd & 3rd Year B.Tech Students", "OFFLINE", 2),
            ("Corporate Leadership, Communication & HR Interview Preparation", "corporate-soft-skills-workshop", "SOFT_SKILLS", "Corporate HR Directors & Executive Coaches", 4, "2026-02-15", "2026-03-15", "Executive Presence, Group Discussion Dynamics, STAR Behavioral Interview Methodology, Case Interviews", "Final Year Students", "HYBRID", 3),
        ]

        for t_title, t_slug, t_type, t_tr, t_dur, t_start, t_end, t_syl, t_batch, t_mode, t_ord in train_data:
            if t_slug not in existing_train:
                session.add(CmsTrainingProgram(
                    institute_id=institute.id,
                    title=t_title,
                    slug=t_slug,
                    training_type=t_type,
                    trainer_name=t_tr,
                    duration_weeks=t_dur,
                    start_date=t_start,
                    end_date=t_end,
                    syllabus_highlights=t_syl,
                    batch_eligibility=t_batch,
                    mode=t_mode,
                    display_order=t_ord,
                    is_active=True
                ))

        intern_res = await session.execute(select(CmsInternshipOpportunity).where(CmsInternshipOpportunity.institute_id == institute.id))
        existing_intern = {i.slug: i for i in intern_res.scalars().all()}

        intern_data = [
            ("NVIDIA AI Research Laboratory", "nvidia-ai-internship-2026", "Summer Research Intern - Deep Learning & GPU Acceleration", "₹85,000 / Month", 6, "Bengaluru (Hybrid)", "2026-03-31", "B.Tech 3rd Year with Python/C++ & Deep Learning coursework (CGPA >= 8.5)", "https://myeducation.in/placements/internships/apply/nvidia-2026", True, 1),
            ("Oracle Cloud Infrastructure (OCI)", "oracle-cloud-internship-2026", "Cloud Systems Engineering Intern", "₹65,000 / Month", 6, "Hyderabad", "2026-04-15", "B.Tech CSE/ECE Pre-final year with Linux & Network systems background", "https://myeducation.in/placements/internships/apply/oracle-2026", True, 2),
            ("Infosys InStep International Internship", "infosys-instep-internship-2026", "Software Solutions Research Intern", "₹45,000 / Month", 3, "Bengaluru Campus", "2026-04-30", "B.Tech & BCA students with Full-Stack Web Development proficiency", "https://myeducation.in/placements/internships/apply/infosys-2026", False, 3),
        ]

        for i_comp, i_slug, i_role, i_stip, i_dur, i_loc, i_dl, i_elig, i_url, i_feat, i_ord in intern_data:
            if i_slug not in existing_intern:
                session.add(CmsInternshipOpportunity(
                    institute_id=institute.id,
                    company_name=i_comp,
                    slug=i_slug,
                    role_title=i_role,
                    stipend_monthly=i_stip,
                    duration_months=i_dur,
                    location=i_loc,
                    application_deadline=i_dl,
                    eligibility_criteria=i_elig,
                    apply_url=i_url,
                    is_featured=i_feat,
                    display_order=i_ord,
                    is_active=True
                ))


        # Module 13: Testimonials CMS (Student, Parent, Faculty, Recruiter, Alumni)
        test_res = await session.execute(select(CmsTestimonial).where(CmsTestimonial.institute_id == institute.id))
        existing_tests = {t.author_name: t for t in test_res.scalars().all()}

        testimonials_data = [
            ("Aarushi Jain", "B.Tech CSE Graduate (Placed at Google Cloud)", "Student", 5, "The autonomous curriculum, AI research cleanrooms, and high-density CBT exams at MY EDUCATION INDIA shaped my algorithmic mindset and prepared me for high-scale cloud challenges.", "Google Cloud", "Class of 2024", "dQw4w9WgXcQ", True, 1),
            ("Rajesh & Sunita Sharma", "Parents of Rohan Sharma (B.Tech AI-DS '25)", "Parent", 5, "The transparent ERP governance, regular attendance SMS alerts, and dedicated faculty mentors gave us complete confidence in our son's academic trajectory and safety on campus.", "Parent Community", "Batch 2021-25", None, True, 2),
            ("Prof. (Dr.) Arvind Mehta", "Head of Department, Computer Science", "Faculty", 5, "Teaching at an autonomous institution where curriculum can evolve rapidly to integrate neural engineering and scalable cloud architectures is an extraordinary academic privilege.", "Academic Senate", "Faculty Senate", None, True, 3),
            ("Meera Krishnan", "Director of University Talent Acquisition", "Recruiter", 5, "MY EDUCATION INDIA graduates consistently demonstrate exceptional systems thinking, hands-on production code proficiency, and corporate maturity during Day-0 interview rounds.", "Microsoft IDC", "Campus Partner", "dQw4w9WgXcQ", True, 4),
            ("Siddharth Saxena", "Senior Hardware Systems Engineer", "Alumni", 5, "The VLSI laboratory cleanroom and semiconductor coursework at MY EDUCATION INDIA gave me the exact foundation required to lead chip design teams globally.", "Texas Instruments", "Class of 2023", None, True, 5),
        ]

        for a_name, a_role, a_cat, a_stars, a_quote, a_comp, a_batch, a_vid, a_feat, a_ord in testimonials_data:
            if a_name not in existing_tests:
                session.add(CmsTestimonial(
                    institute_id=institute.id,
                    author_name=a_name,
                    author_role=a_role,
                    author_category=a_cat,
                    rating_stars=a_stars,
                    quote=a_quote,
                    company_or_institution=a_comp,
                    batch_year=a_batch,
                    avatar_url=None,
                    video_url="https://www.youtube.com/watch?v=" + a_vid if a_vid else None,
                    video_thumbnail_url="https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80" if a_vid else None,
                    video_embed_id=a_vid,
                    moderation_status="APPROVED",
                    is_featured=a_feat,
                    display_order=a_ord,
                    is_active=True
                ))


        # Module 14: Contact & Inquiry CMS (Departments & FAQs)
        dept_res = await session.execute(select(CmsDepartmentContact).where(CmsDepartmentContact.institute_id == institute.id))
        existing_depts = {d.slug: d for d in dept_res.scalars().all()}

        departments_data = [
            ("Admissions Directorate", "admissions-desk", "Dr. Meenal Sharma (Chief Admissions Officer)", "admissions@myeducation.in", "+91 (0731) 4900-100 / 101", "Administrative Block, Ground Floor, Room 102", "Mon–Sat (9:00 AM – 5:30 PM)", 1),
            ("Registrar & Academic Affairs", "academic-registrar", "Mr. Sudhir K. Tiwari (Deputy Registrar)", "registrar.desk@myeducation.in", "+91 (0731) 4900-105", "Admin Block, First Floor, Room 201", "Mon–Fri (9:30 AM – 5:00 PM)", 2),
            ("Examination & CBT Control Cell", "exam-cell", "Dr. R. K. Mukherjee (Controller of Examinations)", "exam.cell@myeducation.in", "+91 (0731) 4900-115", "Technology Tower, Third Floor, Room 302", "Mon–Fri (10:00 AM – 4:30 PM)", 3),
            ("Accounts & Student Fee Desk", "accounts-finance", "Ms. Ananya Sen (Finance Officer)", "accounts@myeducation.in", "+91 (0731) 4900-108", "Finance Wing, Ground Floor, Room 108", "Mon–Fri (9:30 AM – 4:00 PM)", 4),
            ("Hostel & Student Welfare Office", "student-welfare", "Col. (Retd.) V. S. Chauhan (Chief Warden)", "welfare@myeducation.in", "+91 (0731) 4900-125", "Student Activity Center, Room 105", "24x7 Emergency / Office 9 AM - 6 PM", 5),
            ("Corporate Relations & Placements", "placement-cell", "Mr. Vikramaditya Rao (Director T&P)", "placements@myeducation.in", "+91 (0731) 4900-135", "Placement Tower, Level 2", "Mon–Sat (9:00 AM – 6:00 PM)", 6),
        ]

        for d_name, d_slug, d_person, d_mail, d_ph, d_loc, d_hrs, d_ord in departments_data:
            if d_slug not in existing_depts:
                session.add(CmsDepartmentContact(
                    institute_id=institute.id,
                    department_name=d_name,
                    slug=d_slug,
                    contact_person=d_person,
                    email=d_mail,
                    phone_numbers=d_ph,
                    office_location=d_loc,
                    operating_hours=d_hrs,
                    display_order=d_ord,
                    is_active=True
                ))

        faq_res = await session.execute(select(CmsFaqItem).where(CmsFaqItem.institute_id == institute.id))
        existing_faqs = {f.question: f for f in faq_res.scalars().all()}

        faqs_data = [
            ("ADMISSION", "What are the eligibility criteria for B.Tech programs?", "Candidates must have passed 10+2 with Physics, Mathematics, and Chemistry/Computer Science with at least 60% aggregate marks, along with a valid JEE Main score or state entrance rank.", 1, True),
            ("FEES_SCHOLARSHIPS", "Are scholarships available for meritorious students?", "Yes, MY EDUCATION INDIA offers up to 100% tuition fee waivers for top JEE rankers, state board toppers, national sports champions, and defense wards.", 2, True),
            ("EXAMINATIONS", "How are autonomous examinations and CBT tests conducted?", "Examinations are administered in dedicated on-campus computer-based testing (CBT) laboratories with automated question shuffling, tamper detection, and continuous internal evaluations.", 3, True),
            ("CAMPUS_HOSTEL", "What are the hostel accommodations and dining facilities?", "The campus provides air-conditioned and non-AC single/double occupancy rooms with high-speed Wi-Fi, 24x7 security surveillance, multi-cuisine dining, and indoor sports facilities.", 4, True),
            ("ACADEMICS", "What is the average and highest placement package in the latest cycle?", "In the 2025-26 recruitment cycle, the highest package achieved was ₹52.0 LPA, with an institutional average of ₹12.8 LPA across 250+ recruiting partners.", 5, True),
            ("GENERAL", "How can prospective students schedule a campus tour?", "Campus tours are conducted every Saturday from 10:00 AM to 2:00 PM. Visitors can register online via the Contact portal or speak directly with the Admissions Directorate.", 6, False),
        ]

        for f_cat, f_q, f_ans, f_ord, f_feat in faqs_data:
            if f_q not in existing_faqs:
                session.add(CmsFaqItem(
                    institute_id=institute.id,
                    category=f_cat,
                    question=f_q,
                    answer=f_ans,
                    display_order=f_ord,
                    is_featured=f_feat,
                    is_active=True
                ))


        # Module 15: Search & Navigation Engine (Megamenu & Quick Links)
        nav_res = await session.execute(select(WebsiteNavigationMenu).where(WebsiteNavigationMenu.institute_id == institute.id))
        existing_navs = {n.title: n for n in nav_res.scalars().all()}

        if not existing_navs:
            # Root items
            about_root = WebsiteNavigationMenu(
                institute_id=institute.id,
                menu_location="HEADER_MAIN",
                title="About",
                path="/about",
                is_mega_menu=True,
                display_order=1,
                is_active=True
            )
            acad_root = WebsiteNavigationMenu(
                institute_id=institute.id,
                menu_location="HEADER_MAIN",
                title="Academics",
                path="/courses",
                is_mega_menu=True,
                display_order=2,
                is_active=True
            )
            adm_root = WebsiteNavigationMenu(
                institute_id=institute.id,
                menu_location="HEADER_MAIN",
                title="Admissions",
                path="/admissions",
                is_mega_menu=True,
                display_order=3,
                is_active=True
            )
            fac_root = WebsiteNavigationMenu(
                institute_id=institute.id,
                menu_location="HEADER_MAIN",
                title="Faculty",
                path="/faculty",
                is_mega_menu=False,
                display_order=4,
                is_active=True
            )
            place_root = WebsiteNavigationMenu(
                institute_id=institute.id,
                menu_location="HEADER_MAIN",
                title="Placements",
                path="/placements",
                is_mega_menu=True,
                display_order=5,
                is_active=True
            )
            campus_root = WebsiteNavigationMenu(
                institute_id=institute.id,
                menu_location="HEADER_MAIN",
                title="Campus Life",
                path="/events",
                is_mega_menu=False,
                display_order=6,
                is_active=True
            )
            contact_root = WebsiteNavigationMenu(
                institute_id=institute.id,
                menu_location="HEADER_MAIN",
                title="Contact",
                path="/contact",
                is_mega_menu=False,
                display_order=7,
                is_active=True
            )

            session.add_all([about_root, acad_root, adm_root, fac_root, place_root, campus_root, contact_root])
            await session.flush()

            # Children of About
            session.add_all([
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=about_root.id, title="Overview & Leadership", path="/about", badge_text="Vision", description="Statutory governance and Chancellor vision", display_order=1, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=about_root.id, title="Accreditations & NAAC", path="/about", badge_text="Grade A+", description="Autonomous NIRF & NBA quality certifications", display_order=2, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=about_root.id, title="Campus Infrastructure", path="/about", badge_text="Indore HQ", description="Smart classrooms, labs, and sports arenas", display_order=3, is_active=True),
            ])

            # Children of Academics
            session.add_all([
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=acad_root.id, title="All Degree Programs", path="/courses", badge_text="UG/PG", description="Industry-aligned undergraduate and master curricula", display_order=1, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=acad_root.id, title="B.Tech Computer Science", path="/courses", badge_text="AICTE", description="Four-year autonomous engineering degree", display_order=2, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=acad_root.id, title="M.Tech Cloud & AI", path="/courses", badge_text="New", description="Specialized advanced research program", display_order=3, is_active=True),
            ])

            # Children of Admissions
            session.add_all([
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=adm_root.id, title="Admissions 2026-27", path="/admissions", badge_text="Open", description="Application guidelines, cutoffs, and registration", display_order=1, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=adm_root.id, title="Fee Structure", path="/admissions", description="Tuition schedules, hostel dues, and installment plans", display_order=2, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=adm_root.id, title="Merit Scholarships", path="/admissions", badge_text="Up to 100%", description="Financial assistance and fee waivers", display_order=3, is_active=True),
            ])

            # Children of Placements
            session.add_all([
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=place_root.id, title="Placement Records", path="/placements", badge_text="₹52 LPA", description="Annual compensation metrics and highest offers", display_order=1, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=place_root.id, title="Recruiter Directory", path="/recruiters", description="250+ Fortune 500 corporate recruiting partners", display_order=2, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=place_root.id, title="Alumni Success Stories", path="/stories", description="Global alumni leadership profiles and career journeys", display_order=3, is_active=True),
            ])

            # Children of Campus Life
            session.add_all([
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=campus_root.id, title="Events & Hackathons", path="/events", description="Campus technical fests, symposiums, and sports", display_order=1, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=campus_root.id, title="News & Press", path="/news", description="Institutional announcements and achievements", display_order=2, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=campus_root.id, title="Notices & Circulars", path="/notices", badge_text="Live", description="Examination schedules and academic circulars", display_order=3, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=campus_root.id, title="Campus Gallery", path="/gallery", description="Photo archives and campus facilities", display_order=4, is_active=True),
                WebsiteNavigationMenu(institute_id=institute.id, menu_location="HEADER_MAIN", parent_id=campus_root.id, title="Downloads & Forms", path="/downloads", description="Syllabus, circulars, and academic forms", display_order=5, is_active=True),
            ])

        # Quick Links Seeding
        ql_res = await session.execute(select(WebsiteQuickLink).where(WebsiteQuickLink.institute_id == institute.id))
        existing_qls = {q.title: q for q in ql_res.scalars().all()}

        quick_links_data = [
            ("Admissions 2026-27", "/admissions", "Sparkles", "APPLY NOW", "INTERNAL", True, 1),
            ("Examination & CBT Results", "/notices", "Award", "LIVE", "INTERNAL", True, 2),
            ("Fee Payment Portal", "/admissions", "CreditCard", "FEE DESK", "INTERNAL", False, 3),
            ("Academic Syllabus & Forms", "/downloads", "FileText", "PDF", "INTERNAL", False, 4),
            ("Faculty & Student Login", "/login", "Lock", "ERP V3", "INTERNAL", True, 5),
            ("Anti-Ragging Squad", "/contact", "ShieldCheck", "HELPLINE", "INTERNAL", False, 6),
            ("NIRF & Accreditations", "/about", "CheckCircle", "NAAC A+", "INTERNAL", False, 7),
        ]

        for q_title, q_path, q_icon, q_badge, q_target, q_high, q_ord in quick_links_data:
            if q_title not in existing_qls:
                session.add(WebsiteQuickLink(
                    institute_id=institute.id,
                    title=q_title,
                    path=q_path,
                    icon_name=q_icon,
                    badge_text=q_badge,
                    target_type=q_target,
                    is_highlighted=q_high,
                    display_order=q_ord,
                    is_active=True
                ))

        await session.commit()
        print("Production baseline for MY EDUCATION INDIA (Modules 1-15) seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_production_baseline())
