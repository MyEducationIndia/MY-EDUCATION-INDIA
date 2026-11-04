-- ==============================================================================
-- MY EDUCATION INSTITUTE - ENTERPRISE RELATIONAL DATABASE SCHEMA (SQLITE / POSTGRESQL)
-- Production Grade Normalized Schema with Strict Constraints & Indexes
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- 1. Institutes / Campus Settings
CREATE TABLE IF NOT EXISTS institutes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slogan TEXT,
    registration_no TEXT UNIQUE,
    iso_certification TEXT,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    whatsapp TEXT,
    currency TEXT DEFAULT 'INR (₹)',
    timezone TEXT DEFAULT 'Asia/Kolkata',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. System Roles
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- 3. Master User Registry (Authentication & Credentials)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    linked_id TEXT, -- Roll Number or Employee Code
    is_active INTEGER DEFAULT 1,
    failed_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP NULL,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 4. Course Catalog
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    category TEXT NOT NULL, -- 'diploma', 'certificate', 'professional'
    duration TEXT NOT NULL,
    fee REAL NOT NULL,
    eligibility TEXT NOT NULL,
    highlights TEXT,
    syllabus_modules TEXT,
    badge TEXT DEFAULT 'Standard',
    is_popular INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_courses_code ON courses(code);

-- 5. Faculty & Staff Members
CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_code TEXT NOT NULL UNIQUE,
    user_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    designation TEXT NOT NULL,
    department TEXT NOT NULL,
    qualification TEXT NOT NULL,
    salary_amount REAL,
    phone TEXT,
    email TEXT NOT NULL,
    joining_date DATE,
    status TEXT NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_staff_emp_code ON staff(employee_code);

-- 6. Batches & Classroom Scheduling
CREATE TABLE IF NOT EXISTS batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    trainer_id INTEGER,
    timing TEXT NOT NULL,
    room TEXT NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 30,
    status TEXT NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES staff (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_batches_code ON batches(code);

-- 7. Student Information & Roster
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number TEXT NOT NULL UNIQUE,
    user_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    dob TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    batch_id INTEGER,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    guardian_name TEXT NOT NULL,
    guardian_mobile TEXT,
    gender TEXT NOT NULL,
    blood_group TEXT,
    address TEXT,
    total_fee REAL NOT NULL,
    paid_fee REAL NOT NULL DEFAULT 0,
    due_fee REAL NOT NULL,
    attendance_rate REAL NOT NULL DEFAULT 100.0,
    status TEXT NOT NULL DEFAULT 'Enrolled', -- 'Enrolled', 'Completed', 'Suspended'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE RESTRICT,
    FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_students_roll ON students(roll_number);
CREATE INDEX IF NOT EXISTS idx_students_course ON students(course_id);

-- 8. Online Admissions Queue
CREATE TABLE IF NOT EXISTS admissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_number TEXT NOT NULL UNIQUE,
    applicant_name TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    preferred_timing TEXT,
    prior_qualification TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    guardian_name TEXT,
    status TEXT NOT NULL DEFAULT 'Pending Review', -- 'Pending Review', 'Approved', 'Rejected'
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_admissions_app_no ON admissions(application_number);

-- 9. Fee Payments & Official Tax Invoices
CREATE TABLE IF NOT EXISTS fee_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT NOT NULL UNIQUE,
    student_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_mode TEXT NOT NULL, -- 'UPI', 'Cash', 'Net Banking', 'Card'
    payment_date DATE NOT NULL,
    remarks TEXT,
    receipt_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_fees_invoice ON fee_payments(invoice_number);
CREATE INDEX IF NOT EXISTS idx_fees_student ON fee_payments(student_id);

-- 10. Daily Attendance Register
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    batch_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT NOT NULL, -- 'Present', 'Absent', 'Late'
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, batch_id, date),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_att_date ON attendance(date);
CREATE INDEX IF NOT EXISTS idx_att_student ON attendance(student_id);

-- 11. Study Materials & Lecture Notes
CREATE TABLE IF NOT EXISTS study_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    batch_id INTEGER,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size TEXT,
    author TEXT NOT NULL DEFAULT 'Faculty Desk',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE SET NULL
);

-- 12. Institutional Notices & Animated Circulars
CREATE TABLE IF NOT EXISTS notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    target_audience TEXT NOT NULL, -- 'All', 'Students', 'Staff'
    category TEXT NOT NULL, -- 'Urgent', 'Exam Alert', 'Holiday', 'Event', 'Academic'
    is_pinned INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. Academic Homework & Assignments
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    batch_id INTEGER NOT NULL,
    trainer_id INTEGER NOT NULL,
    due_date DATE NOT NULL,
    instructions TEXT NOT NULL,
    max_marks INTEGER DEFAULT 20,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES staff (id) ON DELETE CASCADE
);

-- 14. Assignment Submissions
CREATE TABLE IF NOT EXISTS assignment_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submission_text TEXT,
    file_path TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade TEXT,
    marks_obtained REAL,
    feedback TEXT,
    status TEXT DEFAULT 'Submitted', -- 'Submitted', 'Graded'
    UNIQUE(assignment_id, student_id),
    FOREIGN KEY (assignment_id) REFERENCES assignments (id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);

-- 15. Staff Leave Management
CREATE TABLE IF NOT EXISTS staff_leaves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    leave_type TEXT NOT NULL, -- 'Casual', 'Medical', 'Academic'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    status TEXT DEFAULT 'Pending', -- 'Pending', 'Approved', 'Rejected'
    approved_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE
);

-- 16. Public Inquiries & Callback Requests
CREATE TABLE IF NOT EXISTS enquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    course_interest TEXT,
    message TEXT,
    status TEXT DEFAULT 'New', -- 'New', 'Contacted', 'Resolved'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 17. Newsletter Subscribers
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 18. Website Testimonials
CREATE TABLE IF NOT EXISTS testimonials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    course TEXT NOT NULL,
    quote TEXT NOT NULL,
    rating INTEGER DEFAULT 5,
    is_featured INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 19. Website FAQs
CREATE TABLE IF NOT EXISTS faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 20. Photo Gallery & Campus Facilities
CREATE TABLE IF NOT EXISTS gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL, -- 'Labs', 'Classrooms', 'Events', 'Library'
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 21. Blog Posts & Career Guidance
CREATE TABLE IF NOT EXISTS blogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    summary TEXT NOT NULL,
    content TEXT NOT NULL,
    read_time TEXT DEFAULT '5 min read',
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 22. Security Audit Trail & System Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    module TEXT NOT NULL,
    ip_address TEXT,
    status TEXT NOT NULL DEFAULT 'Success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_logs(created_at);

-- 23. Master Website CMS Parameters
CREATE TABLE IF NOT EXISTS cms_content (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
