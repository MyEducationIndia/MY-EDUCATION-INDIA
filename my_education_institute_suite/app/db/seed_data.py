import sqlite3, os
from app.core.config import settings
from app.core.security import hash_password

def seed():
    os.makedirs(os.path.dirname(settings.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()

    # 1. System Roles
    cur.execute("INSERT OR IGNORE INTO roles (id, name, description) VALUES (1, 'admin', 'Super Administrator with Root Authority')")
    cur.execute("INSERT OR IGNORE INTO roles (id, name, description) VALUES (2, 'staff', 'Academic Faculty & Department Instructors')")
    cur.execute("INSERT OR IGNORE INTO roles (id, name, description) VALUES (3, 'student', 'Enrolled Institute Students')")
    cur.execute("INSERT OR IGNORE INTO roles (id, name, description) VALUES (4, 'accounts', 'Accounts & Finance Department Officer')")

    # 2. Master Institute Information
    cur.execute('''
        INSERT OR REPLACE INTO institutes (id, name, slogan, registration_no, iso_certification, email, phone, address, whatsapp, currency, timezone)
        VALUES (1, 'MY EDUCATION INSTITUTE', 'Premier Institute of Computer & IT Studies', 'REG-MP-2008-84920', 'ISO 9001:2015 Certified', 'admission@myeducation.edu.in', '+91 98765 43210', 'Tech Innovation Park, Sector 4, Central IT Corridor, Indore, MP - 452001', '919876543210', 'INR (₹)', 'Asia/Kolkata')
    ''')

    # 3. Courses Catalog
    courses = [
        (1, "T.C.C.P", "Teacher Computer Certification Program", "diploma", "12 Months", 18000.0, "Graduation / 10+2 Any Stream", "Govt. School Teaching Eligibility, Pedagogy, Python, ICT Curriculum", "Master Certification", 1),
        (2, "C.C.A", "Certificate in Computer Applications", "certificate", "3 Months", 4500.0, "10th Standard or Equivalent", "Office Automation, Fast Typing, Internet Security, Operating Systems", "Foundation", 0),
        (3, "D.C.A", "Diploma in Computer Applications", "diploma", "6 Months", 9500.0, "10+2 Any Stream", "RDBMS, SQL Scripting, HTML5/CSS3, Tally Prime Fundamentals, Computer Architecture", "Popular Choice", 1),
        (4, "P.G.D.C.A", "Post Graduate Diploma in Computer Applications", "diploma", "12 Months", 22000.0, "Graduation in Any Discipline", "Advanced Programming, System Analysis, Enterprise DBMS, Software Engineering", "High Placement", 1),
        (5, "B.C.C", "Basic Computer & Digital Literacy", "certificate", "2 Months", 3500.0, "Open to All Learners", "Windows 11, MS Word, Excel Spreadsheet, Emailing & Cyber Safety", "Beginner Friendly", 0),
        (6, "D.E.O.P", "Data Entry Operator Professional", "professional", "4 Months", 6500.0, "10+2 or Equivalent", "Bilingual Typing 45+ WPM, Advanced Excel Analytics, Form Processing, Accuracy", "Skill Oriented", 0),
        (7, "F.S.W.D", "Full-Stack Web Development & Python", "professional", "6 Months", 24000.0, "10+2 with Logical Aptitude", "HTML5, Tailwind, Modern JavaScript, FastAPI, SQL Databases, Deployment", "Industry Ready", 1),
        (8, "T.A.G", "Financial Accounting with Tally & GST", "professional", "3 Months", 7500.0, "10+2 Commerce / Basic Math", "Voucher Entries, Inventory, Payroll, GST Calculation, E-Way Bill Reconciliation", "Job Guarantee", 0)
    ]
    for c in courses:
        cur.execute('''
            INSERT OR REPLACE INTO courses (id, code, title, category, duration, fee, eligibility, highlights, badge, is_popular)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', c)

    # 4. Master System Accounts (Super Admin + Accounts Officer ONLY — Zero Dummy Students/Staff/Fees)
    pwd_admin = hash_password("Admin@1234")
    pwd_accounts = hash_password("Accounts@1234")

    cur.execute('''
        INSERT OR REPLACE INTO users (id, username, email, password_hash, full_name, role_id, linked_id)
        VALUES (1, 'admin', 'admin@myeducation.edu.in', ?, 'Administrator (Super Admin)', 1, 'ADM-1')
    ''', (pwd_admin,))

    cur.execute('''
        INSERT OR REPLACE INTO users (id, username, email, password_hash, full_name, role_id, linked_id)
        VALUES (2, 'accounts', 'accounts@myeducation.edu.in', ?, 'Chief Accounts Officer', 4, 'ACC-1')
    ''', (pwd_accounts,))

    # 5. Master CMS Configuration (Clean State, Public Course Fees Hidden by Default)
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
        "hidePublicCourseFees": "true"
    }
    for k, v in cms_defaults.items():
        cur.execute("INSERT OR REPLACE INTO cms_content (key, value) VALUES (?, ?)", (k, v))

    conn.commit()
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.close()
    print("Clean production database initialized (0 dummy students, staff, or fee records).")

if __name__ == "__main__":
    seed()
