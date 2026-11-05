import json
import time
from datetime import datetime
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.entities import (
    AuditLog,
    Branch,
    CMSContent,
    CertificateRecord,
    CommunicationLog,
    FeatureToggle,
    InventoryItem,
    LibraryBook,
    LibraryIssue,
    PayrollRecord,
    SharedInstitutionalState,
)
from app.repositories.base_repository import BaseRepository


DEFAULT_FEATURE_TOGGLES: List[Dict[str, Any]] = [
    # Website & Public Portal Features
    {"feature_key": "web_cbt_portal", "label": "Public & Student CBT Online Examination Portal", "category": "CBT & Exams", "enabled": 1},
    {"feature_key": "web_announcement_ticker", "label": "Live Announcement Ticker Bar", "category": "Website", "enabled": 1},
    {"feature_key": "web_quick_services", "label": "Quick Action Strip (Admissions & Portals)", "category": "Website", "enabled": 1},
    {"feature_key": "web_notice_board", "label": "Animated Live Notice Board & Spotlight Feed", "category": "Website", "enabled": 1},
    {"feature_key": "web_courses_catalog", "label": "Academic & Vocational Courses Catalog", "category": "Website", "enabled": 1},
    {"feature_key": "web_faculty_showcase", "label": "Expert Faculty & Mentors Showcase", "category": "Website", "enabled": 1},
    {"feature_key": "web_gallery", "label": "Campus Photo Gallery & Lightbox", "category": "Website", "enabled": 1},
    {"feature_key": "web_testimonials", "label": "Student Placement Stories & Alumni Reviews", "category": "Website", "enabled": 1},
    {"feature_key": "web_news_blog", "label": "Latest News, Events & Technical Articles", "category": "Website", "enabled": 1},
    {"feature_key": "web_downloads", "label": "Public Documents, Prospectus & Syllabi", "category": "Website", "enabled": 1},
    {"feature_key": "web_faq", "label": "Frequently Asked Questions (Accordion)", "category": "Website", "enabled": 1},
    {"feature_key": "web_whatsapp_float", "label": "Floating WhatsApp & Click-to-Call Widgets", "category": "Website", "enabled": 1},
    # Admin Console Modules (Hide/Show any feature from Admin Panel)
    {"feature_key": "adm_dashboard", "label": "Admin KPI Dashboard & Analytics", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_cms", "label": "Master Website CMS & Visual Customizer", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_students", "label": "Student Roster & Enrollment Management", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_admissions", "label": "Online Admissions & Lead Queue", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_courses", "label": "Courses, Subjects & Curriculum Manager", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_batches", "label": "Classroom Batches & Timetables", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_staff", "label": "Faculty, HR & Leave Management", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_fees", "label": "Fee Structure, Receipts & Accounts Ledger", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_attendance", "label": "Daily Attendance Register (QR/Biometric/Manual)", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_exams_cbt", "label": "Examination Controller, Admit Cards & CBT Engine", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_materials", "label": "LMS Study Materials & Assignments", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_notices", "label": "Institutional Notice Board & Circulars", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_enquiries", "label": "CRM Enquiries & Callback Desk", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_communications", "label": "Bulk & Single SMS, Email & WhatsApp Panel", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_library", "label": "Library Books, Barcode Issue & Return", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_inventory", "label": "Inventory, Computers & Lab Assets", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_payroll", "label": "HR Salary & Monthly Payroll Processing", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_branches", "label": "Multi-Branch & Franchise Network Portal", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_certificates", "label": "Digital Diploma & Certificate Generator", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_reports", "label": "Enterprise Reports & CSV/PDF Exports", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_users", "label": "Master User Accounts & 22-Role Permissions", "category": "Admin Console", "enabled": 1},
    {"feature_key": "adm_settings", "label": "System Settings, Backup & Restore Studio", "category": "Admin Console", "enabled": 1},
]


class EnterpriseERPService:
    """
    Clean Architecture Service Layer coordinating Multi-Branch, Library, Inventory,
    HR/Payroll, Communication, Certificates, and Granular Feature Visibility & CBT Toggle.
    """

    def __init__(self, db: Session):
        self.db = db
        self.branch_repo = BaseRepository(Branch, db)
        self.book_repo = BaseRepository(LibraryBook, db)
        self.issue_repo = BaseRepository(LibraryIssue, db)
        self.inventory_repo = BaseRepository(InventoryItem, db)
        self.payroll_repo = BaseRepository(PayrollRecord, db)
        self.comm_repo = BaseRepository(CommunicationLog, db)
        self.cert_repo = BaseRepository(CertificateRecord, db)
        self.toggle_repo = BaseRepository(FeatureToggle, db)

    def ensure_default_feature_toggles(self) -> List[FeatureToggle]:
        existing = {t.feature_key: t for t in self.db.query(FeatureToggle).all()}
        created_any = False
        for item in DEFAULT_FEATURE_TOGGLES:
            if item["feature_key"] not in existing:
                ft = FeatureToggle(
                    feature_key=item["feature_key"],
                    label=item["label"],
                    category=item["category"],
                    enabled=item["enabled"],
                )
                self.db.add(ft)
                created_any = True
        if created_any:
            self.db.commit()
        return self.db.query(FeatureToggle).order_by(FeatureToggle.category.asc(), FeatureToggle.feature_key.asc()).all()

    def update_feature_toggles(
        self,
        toggles: Dict[str, bool],
        hide_cbt: Any = None,
        sidebar_auto_collapse: Any = None,
        actor: str = "admin",
    ) -> Dict[str, Any]:
        try:
            self.ensure_default_feature_toggles()
            for key, is_enabled in toggles.items():
                ft = self.db.query(FeatureToggle).filter(FeatureToggle.feature_key == str(key)).first()
                if ft:
                    ft.enabled = 1 if is_enabled else 0
                    self.db.add(ft)
                else:
                    self.db.add(
                        FeatureToggle(
                            feature_key=str(key),
                            label=str(key).replace("_", " ").title(),
                            category="Custom",
                            enabled=1 if is_enabled else 0,
                        )
                    )

            # Synchronize CBT visibility & Sidebar Auto-Collapse into CMSContent and SharedInstitutionalState
            cms_updates: Dict[str, str] = {}
            if hide_cbt is not None:
                cbt_enabled = not bool(hide_cbt)
                ft_cbt = self.db.query(FeatureToggle).filter(FeatureToggle.feature_key == "web_cbt_portal").first()
                if ft_cbt:
                    ft_cbt.enabled = 1 if cbt_enabled else 0
                    self.db.add(ft_cbt)
                cms_updates["hideCbtFeature"] = "true" if hide_cbt else "false"

            if sidebar_auto_collapse is not None:
                cms_updates["sidebarAutoCollapse"] = "true" if sidebar_auto_collapse else "false"

            for ck, cv in cms_updates.items():
                cms_row = self.db.query(CMSContent).filter(CMSContent.key == ck).first()
                if cms_row:
                    cms_row.value = cv
                    self.db.add(cms_row)
                else:
                    self.db.add(CMSContent(key=ck, value=cv))

            shared_row = self.db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
            if shared_row and shared_row.state_json:
                try:
                    st = json.loads(shared_row.state_json)
                    if not isinstance(st.get("cms"), dict):
                        st["cms"] = {}
                    if hide_cbt is not None:
                        st["cms"]["hideCbtFeature"] = bool(hide_cbt)
                    if sidebar_auto_collapse is not None:
                        st["cms"]["sidebarAutoCollapse"] = bool(sidebar_auto_collapse)
                    if not isinstance(st.get("featureToggles"), dict):
                        st["featureToggles"] = {}
                    for k, v in toggles.items():
                        st["featureToggles"][str(k)] = bool(v)
                    shared_row.state_json = json.dumps(st, default=str)
                    self.db.add(shared_row)
                except Exception:
                    pass

            self.db.add(
                AuditLog(
                    actor=actor,
                    action=f"Updated feature visibility matrix ({len(toggles)} features) & CBT/Sidebar settings",
                    module="FeatureControl",
                )
            )
            self.db.commit()
            all_rows = self.db.query(FeatureToggle).all()
            return {r.feature_key: bool(r.enabled) for r in all_rows}
        except Exception:
            self.db.rollback()
            raise
