"""initial_postgresql_schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-11-04 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. institutes
    op.create_table(
        'institutes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slogan', sa.String(length=255), nullable=True),
        sa.Column('registration_no', sa.String(length=100), nullable=True),
        sa.Column('iso_certification', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('whatsapp', sa.String(length=50), nullable=True),
        sa.Column('currency', sa.String(length=20), server_default='INR (₹)', nullable=True),
        sa.Column('timezone', sa.String(length=50), server_default='Asia/Kolkata', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('registration_no')
    )

    # 2. roles
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # 3. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('linked_id', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Integer(), server_default='1', nullable=True),
        sa.Column('failed_attempts', sa.Integer(), server_default='0', nullable=True),
        sa.Column('locked_until', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index('idx_users_username', 'users', ['username'])
    op.create_index('idx_users_email', 'users', ['email'])

    # 4. courses
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('duration', sa.String(length=50), nullable=False),
        sa.Column('fee', sa.Float(), nullable=False),
        sa.Column('eligibility', sa.String(length=255), nullable=False),
        sa.Column('highlights', sa.Text(), nullable=True),
        sa.Column('syllabus_modules', sa.Text(), nullable=True),
        sa.Column('badge', sa.String(length=50), server_default='Standard', nullable=True),
        sa.Column('is_popular', sa.Integer(), server_default='0', nullable=True),
        sa.Column('is_active', sa.Integer(), server_default='1', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('idx_courses_code', 'courses', ['code'])

    # 5. staff
    op.create_table(
        'staff',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('employee_code', sa.String(length=50), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('designation', sa.String(length=100), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=False),
        sa.Column('qualification', sa.String(length=150), nullable=False),
        sa.Column('salary_amount', sa.Float(), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('joining_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='Active', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_code'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_staff_emp_code', 'staff', ['employee_code'])

    # 6. batches
    op.create_table(
        'batches',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('trainer_id', sa.Integer(), nullable=True),
        sa.Column('timing', sa.String(length=100), nullable=False),
        sa.Column('room', sa.String(length=50), nullable=False),
        sa.Column('capacity', sa.Integer(), server_default='30', nullable=False),
        sa.Column('status', sa.String(length=50), server_default='Active', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['trainer_id'], ['staff.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('idx_batches_code', 'batches', ['code'])

    # 7. students
    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('roll_number', sa.String(length=50), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('dob', sa.String(length=50), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=True),
        sa.Column('mobile', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('guardian_name', sa.String(length=150), nullable=False),
        sa.Column('guardian_mobile', sa.String(length=50), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=False),
        sa.Column('blood_group', sa.String(length=10), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('total_fee', sa.Float(), nullable=False),
        sa.Column('paid_fee', sa.Float(), server_default='0', nullable=False),
        sa.Column('due_fee', sa.Float(), nullable=False),
        sa.Column('attendance_rate', sa.Float(), server_default='100.0', nullable=False),
        sa.Column('status', sa.String(length=50), server_default='Enrolled', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('roll_number'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_students_roll', 'students', ['roll_number'])
    op.create_index('idx_students_course', 'students', ['course_id'])

    # 8. admissions
    op.create_table(
        'admissions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('application_number', sa.String(length=50), nullable=False),
        sa.Column('applicant_name', sa.String(length=150), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('preferred_timing', sa.String(length=50), nullable=True),
        sa.Column('prior_qualification', sa.String(length=150), nullable=False),
        sa.Column('mobile', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('guardian_name', sa.String(length=150), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='Pending Review', nullable=False),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('application_number')
    )
    op.create_index('idx_admissions_app_no', 'admissions', ['application_number'])

    # 9. fee_payments
    op.create_table(
        'fee_payments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('invoice_number', sa.String(length=50), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('payment_mode', sa.String(length=50), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=False),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('receipt_data', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('invoice_number')
    )
    op.create_index('idx_fees_invoice', 'fee_payments', ['invoice_number'])
    op.create_index('idx_fees_student', 'fee_payments', ['student_id'])

    # 10. attendance
    op.create_table(
        'attendance',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id', 'batch_id', 'date', name='uq_attendance_student_batch_date')
    )
    op.create_index('idx_att_date', 'attendance', ['date'])
    op.create_index('idx_att_student', 'attendance', ['student_id'])

    # 11. study_materials
    op.create_table(
        'study_materials',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=True),
        sa.Column('file_path', sa.Text(), nullable=False),
        sa.Column('file_type', sa.String(length=20), nullable=False),
        sa.Column('file_size', sa.String(length=50), nullable=True),
        sa.Column('author', sa.String(length=100), server_default='Faculty Desk', nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 12. notices
    op.create_table(
        'notices',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('target_audience', sa.String(length=50), server_default='All', nullable=False),
        sa.Column('category', sa.String(length=50), server_default='Urgent', nullable=False),
        sa.Column('is_pinned', sa.Integer(), server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 13. assignments
    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('trainer_id', sa.Integer(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('instructions', sa.Text(), nullable=False),
        sa.Column('max_marks', sa.Integer(), server_default='20', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['trainer_id'], ['staff.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 14. assignment_submissions
    op.create_table(
        'assignment_submissions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('submission_text', sa.Text(), nullable=True),
        sa.Column('file_path', sa.Text(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('grade', sa.String(length=20), nullable=True),
        sa.Column('marks_obtained', sa.Float(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='Submitted', nullable=True),
        sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('assignment_id', 'student_id', name='uq_assignment_student')
    )

    # 15. staff_leaves
    op.create_table(
        'staff_leaves',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('staff_id', sa.Integer(), nullable=False),
        sa.Column('leave_type', sa.String(length=50), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), server_default='Pending', nullable=True),
        sa.Column('approved_by', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 16. enquiries
    op.create_table(
        'enquiries',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('course_interest', sa.String(length=100), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='New', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 17. newsletter_subscribers
    op.create_table(
        'newsletter_subscribers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('subscribed_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # 18. testimonials
    op.create_table(
        'testimonials',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('course', sa.String(length=150), nullable=False),
        sa.Column('quote', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), server_default='5', nullable=True),
        sa.Column('is_featured', sa.Integer(), server_default='1', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 19. faqs
    op.create_table(
        'faqs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), server_default='General', nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 20. gallery
    op.create_table(
        'gallery',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('image_url', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 21. blogs
    op.create_table(
        'blogs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=150), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('read_time', sa.String(length=50), server_default='5 min read', nullable=True),
        sa.Column('published_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # 22. audit_logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('actor', sa.String(length=100), nullable=False),
        sa.Column('action', sa.String(length=255), nullable=False),
        sa.Column('module', sa.String(length=100), nullable=False),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='Success', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_time', 'audit_logs', ['created_at'])

    # 23. cms_content
    op.create_table(
        'cms_content',
        sa.Column('key', sa.String(length=150), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('key')
    )

    # 24. shared_institutional_state
    op.create_table(
        'shared_institutional_state',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('state_json', sa.Text(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 25. restore_points
    op.create_table(
        'restore_points',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=False),
        sa.Column('state_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 26. public_documents
    op.create_table(
        'public_documents',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('file_type', sa.String(length=50), server_default='PDF', nullable=True),
        sa.Column('file_size', sa.String(length=50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('download_url', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Integer(), server_default='1', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 27. exam_configurations
    op.create_table(
        'exam_configurations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('window_open', sa.Integer(), server_default='1', nullable=True),
        sa.Column('require_no_dues', sa.Integer(), server_default='1', nullable=True),
        sa.Column('session_title', sa.String(length=255), nullable=True),
        sa.Column('start_date', sa.String(length=50), nullable=True),
        sa.Column('last_form_date', sa.String(length=50), nullable=True),
        sa.Column('center_name', sa.String(length=255), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 28. exam_forms
    op.create_table(
        'exam_forms',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('form_no', sa.String(length=50), nullable=False),
        sa.Column('admit_card_no', sa.String(length=50), nullable=True),
        sa.Column('student_id', sa.String(length=50), nullable=False),
        sa.Column('student_name', sa.String(length=150), nullable=False),
        sa.Column('course', sa.String(length=100), nullable=False),
        sa.Column('batch', sa.String(length=100), nullable=True),
        sa.Column('exam_session', sa.String(length=255), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('medium', sa.String(length=20), nullable=True),
        sa.Column('papers', sa.Text(), nullable=True),
        sa.Column('no_dues_cert_no', sa.String(length=50), nullable=True),
        sa.Column('submitted_date', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='Pending', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('form_no')
    )

    # 29. website_sections
    op.create_table(
        'website_sections',
        sa.Column('id', sa.String(length=100), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('visible', sa.Integer(), server_default='1', nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 30. custom_sections
    op.create_table(
        'custom_sections',
        sa.Column('id', sa.String(length=100), nullable=False),
        sa.Column('badge', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('subtitle', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('cta_text', sa.String(length=100), nullable=True),
        sa.Column('cta_action', sa.String(length=255), nullable=True),
        sa.Column('theme', sa.String(length=50), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('visible', sa.Integer(), server_default='1', nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 31. question_bank
    op.create_table(
        'question_bank',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('course_code', sa.String(length=50), nullable=True),
        sa.Column('paper_code', sa.String(length=50), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('options', sa.Text(), nullable=False),
        sa.Column('correct_option', sa.Integer(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('marks', sa.Integer(), server_default='1', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 32. cbt_exam_results
    op.create_table(
        'cbt_exam_results',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('student_id', sa.String(length=50), nullable=False),
        sa.Column('roll_number', sa.String(length=50), nullable=False),
        sa.Column('exam_session', sa.String(length=255), nullable=True),
        sa.Column('score', sa.Float(), server_default='0', nullable=False),
        sa.Column('max_score', sa.Float(), server_default='100', nullable=False),
        sa.Column('percentage', sa.Float(), server_default='0', nullable=False),
        sa.Column('status', sa.String(length=50), server_default='Completed', nullable=False),
        sa.Column('answers_json', sa.Text(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 33. advertisements
    op.create_table(
        'advertisements',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('placement', sa.String(length=50), server_default='sidebar', nullable=True),
        sa.Column('image_url', sa.Text(), nullable=False),
        sa.Column('target_url', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Integer(), server_default='1', nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('impressions', sa.Integer(), server_default='0', nullable=True),
        sa.Column('clicks', sa.Integer(), server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 34. role_permissions
    op.create_table(
        'role_permissions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('role_name', sa.String(length=50), nullable=False),
        sa.Column('module_key', sa.String(length=100), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=False),
        sa.Column('enabled', sa.Integer(), server_default='1', nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('role_name', 'module_key', name='uq_role_module')
    )

    # 35. stored_files (Persistent Binary Storage)
    op.create_table(
        'stored_files',
        sa.Column('id', sa.String(length=64), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('content_type', sa.String(length=100), server_default='application/octet-stream', nullable=False),
        sa.Column('file_size', sa.Integer(), server_default='0', nullable=False),
        sa.Column('storage_backend', sa.String(length=50), server_default='postgres_bytea', nullable=False),
        sa.Column('file_data', sa.LargeBinary(), nullable=True),
        sa.Column('external_url', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    tables = [
        'stored_files', 'role_permissions', 'advertisements', 'cbt_exam_results',
        'question_bank', 'custom_sections', 'website_sections', 'exam_forms',
        'exam_configurations', 'public_documents', 'restore_points',
        'shared_institutional_state', 'cms_content', 'audit_logs', 'blogs',
        'gallery', 'faqs', 'testimonials', 'newsletter_subscribers', 'enquiries',
        'staff_leaves', 'assignment_submissions', 'assignments', 'notices',
        'study_materials', 'attendance', 'fee_payments', 'admissions', 'students',
        'batches', 'staff', 'courses', 'users', 'roles', 'institutes'
    ]
    for t in tables:
        op.drop_table(t)
