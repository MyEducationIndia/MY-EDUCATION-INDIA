import json
from app.core.database import get_db_context
from app.core.logging_config import get_logger, setup_logging
from app.core.security import hash_password
from app.models.entities import (
    CMSContent,
    Course,
    ExamConfiguration,
    FeeHead,
    Institute,
    QuestionBank,
    Role,
    User,
    WebsiteSection,
)

logger = get_logger(__name__)


def seed() -> None:
    """
    Seeds initial enterprise configuration, roles, courses, master accounts,
    fee heads, website sections, exam config, and CBT question bank into PostgreSQL.
    Idempotent across restarts and deployments.
    """
    with get_db_context() as db:
        # 1. System Roles
        roles_data = [
            (1, "admin", "Super Administrator with Root Authority"),
            (2, "staff", "Academic Faculty & Department Instructors"),
            (3, "student", "Enrolled Institute Students"),
            (4, "accounts", "Accounts & Finance Department Officer"),
        ]
        for rid, rname, rdesc in roles_data:
            role = db.query(Role).filter(Role.id == rid).first()
            if not role:
                db.add(Role(id=rid, name=rname, description=rdesc))

        # 2. Master Institute Information
        inst = db.query(Institute).filter(Institute.id == 1).first()
        if not inst:
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

        # 3. Courses Catalog
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
            c = db.query(Course).filter(Course.code == code).first()
            if not c:
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

        # 4. Master System Accounts (Super Admin + Accounts Officer)
        pwd_admin = hash_password("Admin@1234")
        pwd_accounts = hash_password("Accounts@1234")

        u_admin = db.query(User).filter(User.username == "admin").first()
        if not u_admin:
            db.add(
                User(
                    id=1,
                    username="admin",
                    email="admin@myeducation.edu.in",
                    password_hash=pwd_admin,
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
                    password_hash=pwd_accounts,
                    full_name="Chief Accounts Officer",
                    role_id=4,
                    linked_id="ACC-1",
                    is_active=1,
                )
            )

        # 5. Master CMS Configuration
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

        # 6. Default Public Website Sections Arrangement
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
            sec = db.query(WebsiteSection).filter(WebsiteSection.id == sid).first()
            if not sec:
                db.add(WebsiteSection(id=sid, label=label, icon=icon, visible=visible, display_order=order))

        # 7. Default Exam Configuration
        exam_cfg = db.query(ExamConfiguration).filter(ExamConfiguration.id == 1).first()
        if not exam_cfg:
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

        # 8. Default Master Fee Heads
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
            fh = db.query(FeeHead).filter(FeeHead.id == fhid).first()
            if not fh:
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

        # 9. Default CBT Question Bank (for live CBT Examinations)
        existing_q_count = db.query(QuestionBank).count()
        if existing_q_count == 0:
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

    logger.info("PostgreSQL production database seeded successfully using SQLAlchemy ORM.")


if __name__ == "__main__":
    setup_logging()
    seed()
