import json
from app.core.database import get_db_context
from app.core.logging_config import get_logger, setup_logging
from app.core.security import hash_password
from app.services.erp_service import DEFAULT_FEATURE_TOGGLES
from app.models.entities import (
    FeatureToggle,
    CMSContent,
    Course,
    ExamConfiguration,
    FeeHead,
    Institute,
    QuestionBank,
    Role,
    SharedInstitutionalState,
    User,
    WebsiteSection,
)

logger = get_logger(__name__)


def seed() -> None:
    """
    Seeds initial enterprise configuration, roles, courses, master accounts,
    fee heads, website sections, exam config, and CBT question bank into PostgreSQL.
    Runs ONLY when database tables are empty and NEVER overwrites existing production data.
    """
    with get_db_context() as db:
        # 1. System Roles (only insert if missing)
        roles_data = [
            (1, "admin", "Super Administrator with Root Authority"),
            (2, "staff", "Academic Faculty & Department Instructors"),
            (3, "student", "Enrolled Institute Students"),
            (4, "accounts", "Accounts & Finance Department Officer"),
            (5, "super_admin", "Global Multi-Tenant Super Admin"),
            (6, "institute_owner", "Institute Owner / Chairman"),
            (7, "branch_manager", "Branch / Center Manager"),
            (8, "principal", "Campus Principal / Dean"),
            (9, "teacher", "Senior Subject Teacher"),
            (10, "reception", "Front Desk & Reception Executive"),
            (11, "admission_staff", "Admission Counselor & Telecaller"),
            (12, "exam_controller", "Controller of Examinations"),
            (13, "library_staff", "Chief Librarian"),
            (14, "store_manager", "Inventory & Store Manager"),
            (15, "hr", "Human Resources & Payroll Officer"),
            (16, "parent", "Parent / Guardian Portal User"),
            (17, "guest", "Prospective Guest / Visitor"),
            (18, "franchise_owner", "Franchise Partner Owner"),
            (19, "franchise_staff", "Franchise Center Coordinator"),
            (20, "question_paper_setter", "CBT Question Paper Setter"),
            (21, "invigilator", "Examination Hall Invigilator"),
            (22, "cbt_operator", "Computer Lab & CBT Server Operator"),
        ]
        for rid, rname, rdesc in roles_data:
            role = db.query(Role).filter(Role.id == rid).first()
            if not role:
                db.add(Role(id=rid, name=rname, description=rdesc))

        # 2. Master Institute Information (only insert if table is empty)
        if db.query(Institute).count() == 0:
            db.add(
                Institute(
                    id=1,
                    name="MY EDUCATION INSTITUTE",
                    slogan="Premier Institute of Computer & IT Studies",
                    registration_no="REG-MP-2008-84920",
                    iso_certification="ISO 9001:2015 Certified",
                    email="admission@myeducation.edu.in",
                    phone="+91 98765 43210",
                    address="Tech Innovation Park, Sector 4, Central IT Corridor, Indore, MP - 452001",
                    whatsapp="919876543210",
                    currency="INR (₹)",
                    timezone="Asia/Kolkata",
                )
            )

        # 3. Courses Catalog (only seed when courses table is completely empty)
        if db.query(Course).count() == 0:
            courses = [
                (1, "T.C.C.P", "Teacher Computer Certification Program", "diploma", "12 Months", 18000.0, "Graduation / 10+2 Any Stream", "Govt. School Teaching Eligibility, Pedagogy, Python, ICT Curriculum", "Master Certification", 1),
                (2, "C.C.A", "Certificate in Computer Applications", "certificate", "3 Months", 4500.0, "10th Standard or Equivalent", "Office Automation, Fast Typing, Internet Security, Operating Systems", "Foundation", 0),
                (3, "D.C.A", "Diploma in Computer Applications", "diploma", "6 Months", 9500.0, "10+2 Any Stream", "RDBMS, SQL Scripting, HTML5/CSS3, Tally Prime Fundamentals, Computer Architecture", "Popular Choice", 1),
                (4, "P.G.D.C.A", "Post Graduate Diploma in Computer Applications", "diploma", "12 Months", 22000.0, "Graduation in Any Discipline", "Advanced Programming, System Analysis, Enterprise DBMS, Software Engineering", "High Placement", 1),
                (5, "B.C.C", "Basic Computer & Digital Literacy", "certificate", "2 Months", 3500.0, "Open to All Learners", "Windows 11, MS Word, Excel Spreadsheet, Emailing & Cyber Safety", "Beginner Friendly", 0),
                (6, "D.E.O.P", "Data Entry Operator Professional", "professional", "4 Months", 6500.0, "10+2 or Equivalent", "Bilingual Typing 45+ WPM, Advanced Excel Analytics, Form Processing, Accuracy", "Skill Oriented", 0),
                (7, "F.S.W.D", "Full-Stack Web Development & Python", "professional", "6 Months", 24000.0, "10+2 with Logical Aptitude", "HTML5, Tailwind, Modern JavaScript, FastAPI, SQL Databases, Deployment", "Industry Ready", 1),
                (8, "T.A.G", "Financial Accounting with Tally & GST", "professional", "3 Months", 7500.0, "10+2 Commerce / Basic Math", "Voucher Entries, Inventory, Payroll, GST Calculation, E-Way Bill Reconciliation", "Job Guarantee", 0),
            ]
            for cid, code, title, cat, dur, fee, elig, high, badge, pop in courses:
                db.add(
                    Course(
                        id=cid,
                        code=code,
                        title=title,
                        category=cat,
                        duration=dur,
                        fee=fee,
                        eligibility=elig,
                        highlights=high,
                        badge=badge,
                        is_popular=pop,
                        is_active=1,
                    )
                )

        # 4. Master System Accounts (Super Admin + Accounts Officer - only insert if missing)
        u_admin = db.query(User).filter(User.username == "admin").first()
        if not u_admin:
            db.add(
                User(
                    id=1,
                    username="admin",
                    email="admin@myeducation.edu.in",
                    password_hash=hash_password("Admin@1234"),
                    full_name="Administrator (Super Admin)",
                    role_id=1,
                    linked_id="ADM-1",
                    is_active=1,
                )
            )

        u_acc = db.query(User).filter(User.username == "accounts").first()
        if not u_acc:
            db.add(
                User(
                    id=2,
                    username="accounts",
                    email="accounts@myeducation.edu.in",
                    password_hash=hash_password("Accounts@1234"),
                    full_name="Chief Accounts Officer",
                    role_id=4,
                    linked_id="ACC-1",
                    is_active=1,
                )
            )

        # 5. Master CMS Configuration (only insert missing keys; NEVER overwrite existing CMS keys)
        cms_defaults = {
            "instituteName": "MY EDUCATION INSTITUTE",
            "instituteSlogan": "Premier Institute of Computer & IT Studies",
            "regNo": "REG-MP-2008-84920",
            "isoCertification": "ISO 9001:2015 Certified",
            "heroBadge": "Govt. Recognized & ISO 9001:2015 Certified Center of Excellence",
            "heroTitle": "Shaping Digital Leaders in Computer Technology",
            "heroSubtitle": "Empowering students with industry-standard IT diplomas, government-recognized teaching certifications (TCCP), data analysis, accounting, and professional software skills with 100% placement support.",
            "announcementTicker": "ADMISSIONS OPEN 2026-27: DCA, PGDCA, TCCP, CCA & Tally Prime Batches Commencing 1st & 15th of Every Month • Call: +91 98765 43210",
            "statAlumni": "15,200+",
            "statPlacement": "98.4%",
            "statCourses": "25+",
            "statYears": "18+",
            "contactPhone": "+91 98765 43210",
            "contactEmail": "admission@myeducation.edu.in",
            "contactAddress": "Tech Innovation Park, Sector 4, Central IT Corridor, Indore, MP - 452001",
            "whatsApp": "919876543210",
            "hidePublicCourseFees": "true",
            "theme": "light",
        }
        for k, v in cms_defaults.items():
            cms_item = db.query(CMSContent).filter(CMSContent.key == k).first()
            if not cms_item:
                db.add(CMSContent(key=k, value=str(v)))

        # 6. Default Public Website Sections Arrangement (only when empty)
        if db.query(WebsiteSection).count() == 0:
            default_sections = [
                ("sec-marquee", "Live Announcement Ticker Bar", "fa-bullhorn", 1, 0),
                ("hero", "Hero Banner & Executive Spotlight Card", "fa-house-laptop", 1, 1),
                ("sec-quick-services", "Quick Action Strip (Admissions, Public Docs, Portals)", "fa-bolt", 1, 2),
                ("notice-board-section", "Animated Live Notice Board & Spotlight Feed", "fa-bell", 1, 3),
                ("about", "About Institute, ISO Credentials & Director Message", "fa-building-columns", 1, 4),
                ("courses", "Academic & Vocational Courses Catalog", "fa-graduation-cap", 1, 5),
                ("sec-labs", "Computer Labs & Infrastructure Showcase", "fa-computer", 1, 6),
                ("admissions", "4-Step Admission Process & Guide", "fa-user-check", 1, 7),
                ("faculty", "Expert Faculty & Academic Mentors", "fa-chalkboard-user", 1, 8),
                ("gallery", "Campus Photo Gallery & Lightbox", "fa-images", 1, 9),
                ("achievements", "Placement Hall of Fame & Toppers", "fa-trophy", 1, 10),
                ("sec-testimonials", "Student Placement Stories & Alumni Reviews", "fa-comments", 1, 11),
                ("news-blog", "Latest News, Events & Technical Articles", "fa-newspaper", 1, 12),
                ("downloads", "Public Documents, Prospectus & Syllabi", "fa-file-pdf", 1, 13),
                ("sec-faq", "Frequently Asked Questions (Accordion)", "fa-circle-question", 1, 14),
                ("contact", "Contact Desk, Enquiry Form & Campus Location", "fa-location-dot", 1, 15),
                ("floatingActionButtons", "Floating WhatsApp & Click-to-Call Widgets", "fa-whatsapp", 1, 16),
            ]
            for sid, label, icon, visible, order in default_sections:
                db.add(WebsiteSection(id=sid, label=label, icon=icon, visible=visible, display_order=order))

        # 7. Default Exam Configuration (only when empty)
        if db.query(ExamConfiguration).count() == 0:
            db.add(
                ExamConfiguration(
                    id=1,
                    window_open=1,
                    require_no_dues=1,
                    session_title="Winter Semester Diploma & Vocational Final Examination — Dec 2026",
                    start_date="2026-12-10",
                    last_form_date="2026-11-25",
                    center_name="MY EDUCATION Main Campus — Lab Complex 1 & 2, Indore",
                )
            )

        # 8. Default Master Fee Heads (only when empty)
        if db.query(FeeHead).count() == 0:
            default_fee_heads = [
                ("FH-101", "ADM-FEE", "Admission & Registration Fee", "One-Time", "All Courses", 500.0, "Exempt (0%)", 1),
                ("FH-102", "TUI-FEE", "Tuition / Academic Course Fee", "Installment / Semester", "All Courses", 4000.0, "Exempt (0%)", 1),
                ("FH-103", "LAB-FEE", "Computer Lab & Practical Workstation Fee", "Semester", "All Courses", 1500.0, "Exempt (0%)", 1),
                ("FH-104", "EXM-FEE", "Examination & Assessment Form Fee", "Term-End Exam", "All Courses", 800.0, "Exempt (0%)", 1),
                ("FH-105", "LIB-FEE", "Library, E-Books & Lab Manual Fee", "One-Time", "All Courses", 500.0, "Exempt (0%)", 0),
                ("FH-106", "IDC-FEE", "Smart Identity Card & Prospectus Fee", "One-Time", "All Courses", 200.0, "Exempt (0%)", 1),
                ("FH-107", "MIS-FEE", "Late Fine / Re-Admission / Miscellaneous", "Penalty / Optional", "All Courses", 0.0, "Exempt (0%)", 0),
            ]
            for fhid, code, title, cat, crs, amt, gst, mand in default_fee_heads:
                db.add(
                    FeeHead(
                        id=fhid,
                        code=code,
                        title=title,
                        category=cat,
                        course=crs,
                        default_amount=amt,
                        gst=gst,
                        mandatory=mand,
                    )
                )

        # 9. Default CBT Question Bank (only when empty)
        if db.query(QuestionBank).count() == 0:
            default_questions = [
                ("D.C.A", "DCA-101", "Which component of the CPU is responsible for executing arithmetic and logical operations?", ["Control Unit (CU)", "Arithmetic Logic Unit (ALU)", "Memory Address Register", "Cache Controller"], 1, "ALU performs all arithmetic and bitwise logic operations.", 1),
                ("D.C.A", "DCA-101", "Which SQL statement is used to retrieve records from a relational database table?", ["EXTRACT", "SELECT", "FETCH", "OPEN"], 1, "SELECT queries data from one or more tables in SQL.", 1),
                ("D.C.A", "DCA-101", "In HTML5, which semantic element is used to define navigation links?", ["<navigation>", "<nav>", "<header>", "<menu>"], 1, "The <nav> element represents a section of navigation links.", 1),
                ("P.G.D.C.A", "PGD-201", "Which normal form eliminates transitive dependency in relational database design?", ["First Normal Form (1NF)", "Second Normal Form (2NF)", "Third Normal Form (3NF)", "Unnormalized Form"], 2, "3NF requires 2NF and zero transitive functional dependencies.", 1),
                ("T.C.C.P", "TCP-101", "What does ICT stand for in modern digital education pedagogy?", ["Integrated Computer Training", "Information and Communication Technology", "Institute of Computer Teaching", "Interactive Classroom Terminal"], 1, "ICT stands for Information and Communication Technology.", 1),
            ]
            for idx, (cc, pc, qtext, opts, corr, expl, mrk) in enumerate(default_questions, 1):
                db.add(
                    QuestionBank(
                        id=idx,
                        course_code=cc,
                        paper_code=pc,
                        question_text=qtext,
                        options=json.dumps(opts),
                        correct_option=corr,
                        explanation=expl,
                        marks=mrk,
                    )
                )

        # 9b. Default Granular Feature Toggles (only insert missing keys)
        for ft_item in DEFAULT_FEATURE_TOGGLES:
            ft_existing = db.query(FeatureToggle).filter(FeatureToggle.feature_key == ft_item["feature_key"]).first()
            if not ft_existing:
                db.add(
                    FeatureToggle(
                        feature_key=ft_item["feature_key"],
                        label=ft_item["label"],
                        category=ft_item["category"],
                        enabled=ft_item["enabled"],
                    )
                )

        # 10. Clean SharedInstitutionalState (only when empty — zero fake students/staff/fees)
        if db.query(SharedInstitutionalState).count() == 0:
            clean_initial_state = {
                "cms": cms_defaults,
                "students": [],
                "staff": [],
                "admissions": [],
                "fees": [],
                "materials": [],
                "notices": [],
                "enquiries": [],
                "examForms": [],
                "submissions": [],
                "assignments": [],
                "expenses": [],
                "users": [
                    {
                        "id": "USR-ADMIN",
                        "username": "admin",
                        "name": "Administrator (Super Admin)",
                        "role": "admin",
                        "linkedId": "ADM-1",
                        "email": "admin@myeducation.edu.in",
                        "status": "Active",
                    },
                    {
                        "id": "USR-ACC",
                        "username": "accounts",
                        "name": "Chief Accounts Officer",
                        "role": "accounts",
                        "linkedId": "ACC-1",
                        "email": "accounts@myeducation.edu.in",
                        "status": "Active",
                    },
                ],
            }
            db.add(SharedInstitutionalState(id=1, state_json=json.dumps(clean_initial_state)))

    logger.info("PostgreSQL production database verified/seeded safely without overwriting existing data.")


if __name__ == "__main__":
    setup_logging()
    seed()
