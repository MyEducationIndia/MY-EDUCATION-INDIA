"""
Module 20: Enterprise Experience Platform - Models
Provisions 17 master tables for Root Owner controls, Portals, Dynamic Menus,
Page Builder, Form Builder, Global Search, Support Tickets, Developer Tools,
and Module Registry.
"""
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON, Index
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class RootOwnerControl(Base):
    __tablename__ = "root_owner_controls"
    id = Column(String(36), primary_key=True)
    owner_username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_passphrase = Column(String(255), nullable=False)
    emergency_lockdown_active = Column(Boolean, default=False, nullable=False)
    developer_mode_enabled = Column(Boolean, default=True, nullable=False)
    license_tier = Column(String(50), default="UNLIMITED_PROPRIETARY", nullable=False)
    global_encryption_key_hash = Column(String(128), nullable=False)
    platform_clone_token = Column(String(128), nullable=True)
    last_root_login_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class SystemOwnerSession(Base):
    __tablename__ = "system_owner_sessions"
    id = Column(String(36), primary_key=True)
    session_token = Column(String(128), unique=True, nullable=False, index=True)
    ip_address = Column(String(50), nullable=False)
    user_agent = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class PortalConfiguration(Base):
    __tablename__ = "portal_configurations"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    portal_type = Column(String(50), nullable=False, index=True) 
    # ROOT_OWNER, SUPER_ADMIN, INSTITUTE_ADMIN, BRANCH_ADMIN, FACULTY, STUDENT, COUNSELLOR, ACCOUNTANT, RECEPTION, DEVELOPER
    display_title = Column(String(150), nullable=False)
    theme_palette = Column(JSON, nullable=True)
    allowed_roles = Column(JSON, nullable=False) # ["STUDENT"], ["FACULTY"]
    default_route = Column(String(100), default="/dashboard", nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    navigation_tree_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class UserPortalPreference(Base):
    __tablename__ = "user_portal_preferences"
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    portal_type = Column(String(50), nullable=False, index=True)
    dark_mode = Column(Boolean, default=False, nullable=False)
    sidebar_collapsed = Column(Boolean, default=False, nullable=False)
    accent_color = Column(String(20), default="#4f46e5", nullable=False)
    dashboard_layout_id = Column(String(36), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class DynamicMenu(Base):
    __tablename__ = "dynamic_menus"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    menu_key = Column(String(60), nullable=False, index=True) # e.g. MAIN_ADMIN_SIDEBAR, STUDENT_PORTAL_NAV
    menu_name = Column(String(150), nullable=False)
    target_portal = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    items = relationship("DynamicMenuItem", back_populates="menu", cascade="all, delete-orphan", order_by="DynamicMenuItem.order_index")

class DynamicMenuItem(Base):
    __tablename__ = "dynamic_menu_items"
    id = Column(String(36), primary_key=True)
    menu_id = Column(String(36), ForeignKey("dynamic_menus.id"), nullable=False, index=True)
    parent_item_id = Column(String(36), ForeignKey("dynamic_menu_items.id"), nullable=True)
    label = Column(String(100), nullable=False)
    route_path = Column(String(200), nullable=False)
    icon_name = Column(String(50), default="Circle", nullable=False)
    order_index = Column(Integer, default=1, nullable=False)
    required_permission = Column(String(100), nullable=True)
    badge_text = Column(String(30), nullable=True)
    is_visible = Column(Boolean, default=True, nullable=False)

    menu = relationship("DynamicMenu", back_populates="items")

class PageDefinition(Base):
    __tablename__ = "page_definitions"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    page_slug = Column(String(150), nullable=False, index=True)
    page_title = Column(String(200), nullable=False)
    content_blocks_json = Column(JSON, nullable=False)
    seo_meta_tags = Column(JSON, nullable=True)
    custom_css = Column(Text, nullable=True)
    custom_js = Column(Text, nullable=True)
    status = Column(String(30), default="PUBLISHED", nullable=False) # DRAFT, PUBLISHED, ARCHIVED
    access_level = Column(String(30), default="PUBLIC", nullable=False) # PUBLIC, AUTHENTICATED, ROLE_RESTRICTED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class FormDefinition(Base):
    __tablename__ = "form_definitions"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    form_key = Column(String(60), nullable=False, index=True)
    form_title = Column(String(200), nullable=False)
    schema_fields_json = Column(JSON, nullable=False) # Visual fields, validation rules, types
    conditional_rules_json = Column(JSON, nullable=True)
    workflow_steps_json = Column(JSON, nullable=True)
    target_module = Column(String(50), nullable=False) # ADMISSIONS, SIMS, LXP, CRM, FEEDBACK
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    submissions = relationship("FormSubmission", back_populates="form", cascade="all, delete-orphan")

class FormSubmission(Base):
    __tablename__ = "form_submissions"
    id = Column(String(36), primary_key=True)
    form_id = Column(String(36), ForeignKey("form_definitions.id"), nullable=False, index=True)
    institute_id = Column(String(36), nullable=False, index=True)
    submitted_by_user_id = Column(String(36), nullable=True)
    submission_data_json = Column(JSON, nullable=False)
    workflow_status = Column(String(30), default="SUBMITTED", nullable=False) # SUBMITTED, APPROVED, REJECTED, PENDING_REVIEW
    reference_number = Column(String(60), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    form = relationship("FormDefinition", back_populates="submissions")

class DashboardBuilderConfig(Base):
    __tablename__ = "dashboard_builder_configs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    dashboard_key = Column(String(60), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    target_role = Column(String(50), nullable=False)
    grid_layout_json = Column(JSON, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class CustomFieldDefinition(Base):
    __tablename__ = "custom_field_definitions"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, index=True) # STUDENT, FACULTY, LEAD, COURSE, CERTIFICATE
    field_name = Column(String(100), nullable=False)
    field_label = Column(String(150), nullable=False)
    data_type = Column(String(30), default="TEXT", nullable=False) # TEXT, NUMBER, DATE, SELECT, BOOLEAN, FILE
    is_required = Column(Boolean, default=False, nullable=False)
    options_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class GlobalSearchIndex(Base):
    __tablename__ = "global_search_index"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    module_name = Column(String(50), nullable=False, index=True) # STUDENTS, COURSES, FEES, LEADS, CERTIFICATES, LXP
    record_id = Column(String(100), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    subtitle = Column(String(255), nullable=True)
    keywords_tsv = Column(Text, nullable=False) # Space-separated search tokens
    target_route = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    ticket_number = Column(String(50), unique=True, nullable=False, index=True)
    created_by_user_id = Column(String(36), nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    category = Column(String(50), default="SYSTEM_QUERY", nullable=False) # ACADEMIC, FEE, IT_SUPPORT, BUG_REPORT, FEATURE_REQUEST
    priority = Column(String(20), default="MEDIUM", nullable=False) # LOW, MEDIUM, HIGH, URGENT
    status = Column(String(30), default="OPEN", nullable=False) # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    assigned_staff_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    messages = relationship("SupportTicketMessage", back_populates="ticket", cascade="all, delete-orphan", order_by="SupportTicketMessage.created_at")

class SupportTicketMessage(Base):
    __tablename__ = "support_ticket_messages"
    id = Column(String(36), primary_key=True)
    ticket_id = Column(String(36), ForeignKey("support_tickets.id"), nullable=False, index=True)
    sender_user_id = Column(String(36), nullable=False)
    message_text = Column(Text, nullable=False)
    attachment_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    ticket = relationship("SupportTicket", back_populates="messages")

class DeveloperConsoleLog(Base):
    __tablename__ = "developer_console_logs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    session_id = Column(String(60), nullable=False)
    command_executed = Column(String(255), nullable=False)
    execution_result = Column(Text, nullable=True)
    duration_ms = Column(Float, default=0.0, nullable=False)
    is_success = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class ModuleRegistryConfig(Base):
    __tablename__ = "module_registry_configs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    module_key = Column(String(50), nullable=False, index=True) # e.g. MODULE_1_ARCHITECTURE ... MODULE_20_EXPERIENCE
    module_name = Column(String(100), nullable=False)
    version = Column(String(20), default="2.0.0", nullable=False)
    is_installed = Column(Boolean, default=True, nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    license_required = Column(Boolean, default=False, nullable=False)
    role_access_list = Column(JSON, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class BrandingTheme(Base):
    __tablename__ = "branding_themes"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    institute_display_name = Column(String(200), nullable=False)
    primary_logo_url = Column(String(500), nullable=True)
    dark_logo_url = Column(String(500), nullable=True)
    favicon_url = Column(String(500), nullable=True)
    primary_color = Column(String(20), default="#4f46e5", nullable=False)
    secondary_color = Column(String(20), default="#06b6d4", nullable=False)
    font_family = Column(String(100), default="Inter, sans-serif", nullable=False)
    custom_domain = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
