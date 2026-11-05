-- ==============================================================================
-- MY EDUCATION INSTITUTE - ENTERPRISE RELATIONAL DATABASE SCHEMA (POSTGRESQL)
-- Production Grade Normalized PostgreSQL Schema with Strict Constraints & Indexes
-- ==============================================================================

-- 1. Institutes / Campus Settings
CREATE TABLE IF NOT EXISTS institutes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slogan VARCHAR(255),
    registration_no VARCHAR(100) UNIQUE,
    iso_certification VARCHAR(100),
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    whatsapp VARCHAR(50),
    currency VARCHAR(20) DEFAULT 'INR (₹)',
    timezone VARCHAR(50) DEFAULT 'Asia/Kolkata',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. System Roles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- 3. Master User Registry (Authentication & Credentials)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    linked_id VARCHAR(100),
    is_active INTEGER DEFAULT 1,
    failed_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITHOUT TIME ZONE NULL,
    last_login TIMESTAMP WITHOUT TIME ZONE NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 4. Course Catalog
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    duration VARCHAR(50) NOT NULL,
    fee DOUBLE PRECISION NOT NULL,
    eligibility VARCHAR(255) NOT NULL,
    highlights TEXT,
    syllabus_modules TEXT,
    badge VARCHAR(50) DEFAULT 'Standard',
    is_popular INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_courses_code ON courses(code);

-- 5. Faculty & Staff Members
CREATE TABLE IF NOT EXISTS staff (
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) NOT NULL UNIQUE,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(150) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    qualification VARCHAR(150) NOT NULL,
    salary_amount DOUBLE PRECISION,
    phone VARCHAR(50),
    email VARCHAR(150) NOT NULL,
    joining_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_staff_emp_code ON staff(employee_code);

-- 6. Batches & Classroom Scheduling
CREATE TABLE IF NOT EXISTS batches (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    trainer_id INTEGER REFERENCES staff(id) ON DELETE SET NULL,
    timing VARCHAR(100) NOT NULL,
    room VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 30,
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_batches_code ON batches(code);

-- 7. Student Information & Roster
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    roll_number VARCHAR(50) NOT NULL UNIQUE,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(150) NOT NULL,
    dob VARCHAR(50) NOT NULL,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    batch_id INTEGER REFERENCES batches(id) ON DELETE SET NULL,
    mobile VARCHAR(50) NOT NULL,
    email VARCHAR(150) NOT NULL,
    guardian_name VARCHAR(150) NOT NULL,
    guardian_mobile VARCHAR(50),
    gender VARCHAR(20) NOT NULL,
    blood_group VARCHAR(10),
    address TEXT,
    total_fee DOUBLE PRECISION NOT NULL,
    paid_fee DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    due_fee DOUBLE PRECISION NOT NULL,
    attendance_rate DOUBLE PRECISION NOT NULL DEFAULT 100.0,
    status VARCHAR(50) NOT NULL DEFAULT 'Enrolled',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_students_roll ON students(roll_number);
CREATE INDEX IF NOT EXISTS idx_students_course ON students(course_id);

-- 8. Online Admissions Queue
CREATE TABLE IF NOT EXISTS admissions (
    id SERIAL PRIMARY KEY,
    application_number VARCHAR(50) NOT NULL UNIQUE,
    applicant_name VARCHAR(150) NOT NULL,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    preferred_timing VARCHAR(50),
    prior_qualification VARCHAR(150) NOT NULL,
    mobile VARCHAR(50) NOT NULL,
    email VARCHAR(150) NOT NULL,
    guardian_name VARCHAR(150),
    status VARCHAR(50) NOT NULL DEFAULT 'Pending Review',
    remarks TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_admissions_app_no ON admissions(application_number);

-- 9. Fee Payments & Official Tax Invoices
CREATE TABLE IF NOT EXISTS fee_payments (
    id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    amount DOUBLE PRECISION NOT NULL,
    payment_mode VARCHAR(50) NOT NULL,
    payment_date DATE NOT NULL,
    remarks TEXT,
    receipt_data TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_fees_invoice ON fee_payments(invoice_number);
CREATE INDEX IF NOT EXISTS idx_fees_student ON fee_payments(student_id);

-- 10. Daily Attendance Register
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    batch_id INTEGER NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_attendance_student_batch_date UNIQUE (student_id, batch_id, date)
);
CREATE INDEX IF NOT EXISTS idx_att_date ON attendance(date);
CREATE INDEX IF NOT EXISTS idx_att_student ON attendance(student_id);

-- 11. Study Materials & Lecture Notes
CREATE TABLE IF NOT EXISTS study_materials (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    batch_id INTEGER REFERENCES batches(id) ON DELETE SET NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(20) NOT NULL,
    file_size VARCHAR(50),
    author VARCHAR(100) NOT NULL DEFAULT 'Faculty Desk',
    uploaded_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 12. Institutional Notices & Animated Circulars
CREATE TABLE IF NOT EXISTS notices (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    target_audience VARCHAR(50) NOT NULL DEFAULT 'All',
    category VARCHAR(50) NOT NULL DEFAULT 'Urgent',
    is_pinned INTEGER DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 13. Academic Homework & Assignments
CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    batch_id INTEGER NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
    trainer_id INTEGER NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    due_date DATE NOT NULL,
    instructions TEXT NOT NULL,
    max_marks INTEGER DEFAULT 20,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 14. Assignment Submissions
CREATE TABLE IF NOT EXISTS assignment_submissions (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    submission_text TEXT,
    file_path TEXT,
    submitted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    grade VARCHAR(20),
    marks_obtained DOUBLE PRECISION,
    feedback TEXT,
    status VARCHAR(50) DEFAULT 'Submitted',
    CONSTRAINT uq_assignment_student UNIQUE (assignment_id, student_id)
);

-- 15. Staff Leave Management
CREATE TABLE IF NOT EXISTS staff_leaves (
    id SERIAL PRIMARY KEY,
    staff_id INTEGER NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    leave_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    approved_by VARCHAR(100),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 16. Public Inquiries & Callback Requests
CREATE TABLE IF NOT EXISTS enquiries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(150),
    course_interest VARCHAR(100),
    message TEXT,
    status VARCHAR(50) DEFAULT 'New',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 17. Newsletter Subscribers
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    subscribed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 18. Website Testimonials
CREATE TABLE IF NOT EXISTS testimonials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    course VARCHAR(150) NOT NULL,
    quote TEXT NOT NULL,
    rating INTEGER DEFAULT 5,
    is_featured INTEGER DEFAULT 1,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 19. Website FAQs
CREATE TABLE IF NOT EXISTS faqs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'General',
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 20. Photo Gallery & Campus Facilities
CREATE TABLE IF NOT EXISTS gallery (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    image_url TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 21. Blog Posts & Career Guidance
CREATE TABLE IF NOT EXISTS blogs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    author VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    summary TEXT NOT NULL,
    content TEXT NOT NULL,
    read_time VARCHAR(50) DEFAULT '5 min read',
    published_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 22. Security Audit Trail & System Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    actor VARCHAR(100) NOT NULL,
    action VARCHAR(255) NOT NULL,
    module VARCHAR(100) NOT NULL,
    ip_address VARCHAR(50),
    status VARCHAR(50) NOT NULL DEFAULT 'Success',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_logs(created_at);

-- 23. Master Website CMS Parameters
CREATE TABLE IF NOT EXISTS cms_content (
    key VARCHAR(150) PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 24. Shared Institutional State (Real-Time Cloud State Sync)
CREATE TABLE IF NOT EXISTS shared_institutional_state (
    id INTEGER PRIMARY KEY,
    state_json TEXT NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 25. Database Restore Points
CREATE TABLE IF NOT EXISTS restore_points (
    id VARCHAR(50) PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    state_json TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 26. Public Downloads & Institutional Documents
CREATE TABLE IF NOT EXISTS public_documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    file_type VARCHAR(50) DEFAULT 'PDF',
    file_size VARCHAR(50),
    description TEXT,
    content TEXT,
    download_url TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 27. Exam Portal Configuration
CREATE TABLE IF NOT EXISTS exam_configurations (
    id INTEGER PRIMARY KEY,
    window_open INTEGER DEFAULT 1,
    require_no_dues INTEGER DEFAULT 1,
    session_title VARCHAR(255),
    start_date VARCHAR(50),
    last_form_date VARCHAR(50),
    center_name VARCHAR(255),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 28. Exam Registration Forms & Admit Cards
CREATE TABLE IF NOT EXISTS exam_forms (
    id SERIAL PRIMARY KEY,
    form_no VARCHAR(50) NOT NULL UNIQUE,
    admit_card_no VARCHAR(50) UNIQUE,
    student_id VARCHAR(50) NOT NULL,
    student_name VARCHAR(150) NOT NULL,
    course VARCHAR(100) NOT NULL,
    batch VARCHAR(100),
    exam_session VARCHAR(255),
    category VARCHAR(50),
    medium VARCHAR(20),
    papers TEXT,
    no_dues_cert_no VARCHAR(50),
    submitted_date VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 29. Public Website Sections Arrangement & Visibility
CREATE TABLE IF NOT EXISTS website_sections (
    id VARCHAR(100) PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    icon VARCHAR(50),
    visible INTEGER DEFAULT 1,
    display_order INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 30. Custom Admin Website Sections
CREATE TABLE IF NOT EXISTS custom_sections (
    id VARCHAR(100) PRIMARY KEY,
    badge VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    subtitle TEXT,
    content TEXT,
    cta_text VARCHAR(100),
    cta_action VARCHAR(255),
    theme VARCHAR(50),
    image_url TEXT,
    visible INTEGER DEFAULT 1,
    display_order INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 31. Question Bank for CBT & Semester Exams
CREATE TABLE IF NOT EXISTS question_bank (
    id SERIAL PRIMARY KEY,
    course_code VARCHAR(50),
    paper_code VARCHAR(50),
    question_text TEXT NOT NULL,
    options TEXT NOT NULL,
    correct_option INTEGER NOT NULL,
    explanation TEXT,
    marks INTEGER DEFAULT 1,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 32. CBT Examination Results
CREATE TABLE IF NOT EXISTS cbt_exam_results (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    roll_number VARCHAR(50) NOT NULL,
    exam_session VARCHAR(255),
    score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    max_score DOUBLE PRECISION NOT NULL DEFAULT 100.0,
    percentage DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    status VARCHAR(50) NOT NULL DEFAULT 'Completed',
    answers_json TEXT,
    submitted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 33. Marketing Advertisements & Banners
CREATE TABLE IF NOT EXISTS advertisements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    placement VARCHAR(50) DEFAULT 'sidebar',
    image_url TEXT NOT NULL,
    target_url TEXT,
    is_active INTEGER DEFAULT 1,
    start_date DATE,
    end_date DATE,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 34. Role Permissions Matrix
CREATE TABLE IF NOT EXISTS role_permissions (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL,
    module_key VARCHAR(100) NOT NULL,
    label VARCHAR(255) NOT NULL,
    enabled INTEGER DEFAULT 1,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_role_module UNIQUE (role_name, module_key)
);

-- 35. Persistent File Storage (PostgreSQL Binary / S3 Object Storage)
CREATE TABLE IF NOT EXISTS stored_files (
    id VARCHAR(64) PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    content_type VARCHAR(100) NOT NULL DEFAULT 'application/octet-stream',
    file_size INTEGER NOT NULL DEFAULT 0,
    storage_backend VARCHAR(50) NOT NULL DEFAULT 'postgres_bytea',
    file_data BYTEA,
    external_url TEXT,
    category VARCHAR(50),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
-- 36. Master Fee Heads Structure
CREATE TABLE IF NOT EXISTS fee_heads (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL DEFAULT 'One-Time',
    course VARCHAR(100) NOT NULL DEFAULT 'All Courses',
    default_amount DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    gst VARCHAR(50) NOT NULL DEFAULT 'Exempt (0%)',
    mandatory INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_fee_heads_code ON fee_heads(code);

-- 37. Institute Expense Vouchers & Petty Cash Ledger
CREATE TABLE IF NOT EXISTS expenses (
    id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(150) NOT NULL,
    amount DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    payee VARCHAR(150) NOT NULL,
    mode VARCHAR(100) NOT NULL DEFAULT 'Cash Voucher',
    notes TEXT,
    expense_date VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category);
