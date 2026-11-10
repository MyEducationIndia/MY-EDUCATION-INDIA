from app.models.cms_contact import (
    CmsContactInquiry,
    CmsDepartmentContact,
    CmsFaqItem,
    CmsSupportFeedback,
)
from app.models.auth_identity import (
    LoginHistory,
    OtpVerification,
    SecurityPolicyConfig,
)
from app.models.audit_log import AuditLog
from app.models.academic_session import AcademicSession
from app.models.cms_about import (
    CmsAccreditation,
    CmsCampusInfrastructure,
    CmsLeadershipMessage,
    CmsMilestone,
)
from app.models.cms_admissions import (
    CmsAdmissionApplication,
    CmsAdmissionEnquiry,
    CmsAdmissionStep,
    CmsFeeStructure,
    CmsScholarship,
)
from app.models.cms_courses import (
    CmsCourse,
    CmsCourseCategory,
    CmsCourseCurriculum,
    CmsCourseFaculty,
)
from app.models.cms_downloads import (
    CmsDownloadCategory,
    CmsDownloadDocument,
)
from app.models.cms_events_news import (
    CmsAchievement,
    CmsEvent,
    CmsNewsArticle,
    CmsNoticeCircular,
)
from app.models.cms_faculty import (
    CmsFacultyMember,
    CmsResearchPublication,
    CmsStaffMember,
)
from app.models.cms_gallery import (
    CmsGalleryAlbum,
    CmsGalleryMedia,
)
from app.models.cms_home import (
    CmsFeaturedProgram,
    CmsHeroSlide,
    CmsNewsletterSubscriber,
    CmsQuickLink,
    CmsRecruiterLogo,
    CmsStatCounter,
    CmsTestimonial,
)
from app.models.cms_placements import (
    CmsAlumniSuccessStory,
    CmsInternshipOpportunity,
    CmsPlacementDrive,
    CmsPlacementStat,
    CmsRecruiterPartner,
    CmsTrainingProgram,
)
from app.models.institute import Institute
from app.models.module_config import SystemModuleConfig
from app.models.permission import Permission
from app.models.rbac_extended import PermissionGroup, RoleTemplate
from app.models.refresh_token import RefreshTokenSession
from app.models.role import Role, role_permissions_association
from app.models.user import User, user_roles_association
from app.models.user_document import UserDocument
from app.models.system_settings import (
    CampusHoliday,
    DocumentTemplate,
    MasterDataEntry,
    NumberingRule,
    WorkingDaysConfig,
)

from app.models.website import (
    WebsiteNavigationMenu,
    WebsiteQuickLink,
    WebsiteSearchIndex,
    WebsiteSearchLog,
    WebsiteSetting,
    WebsiteSocialLink,
    WebsiteTheme,
    WebsiteTickerItem,
)

__all__ = [
    "AcademicSession",
    "AuditLog",
    "LoginHistory",
    "OtpVerification",
    "SecurityPolicyConfig",
    "CmsAccreditation",
    "CmsAchievement",
    "CmsAdmissionApplication",
    "CmsAdmissionEnquiry",
    "CmsAdmissionStep",
    "CmsAlumniSuccessStory",
    "CmsCampusInfrastructure",
    "CmsContactInquiry",
    "CmsDepartmentContact",
    "CmsFaqItem",
    "CmsSupportFeedback",
    "CmsCourse",
    "CmsCourseCategory",
    "CmsCourseCurriculum",
    "CmsCourseFaculty",
    "CmsDownloadCategory",
    "CmsDownloadDocument",
    "CmsEvent",
    "CmsFacultyMember",
    "CmsFeaturedProgram",
    "CmsFeeStructure",
    "CmsGalleryAlbum",
    "CmsGalleryMedia",
    "CmsHeroSlide",
    "CmsLeadershipMessage",
    "CmsMilestone",
    "CmsNewsArticle",
    "CmsNewsletterSubscriber",
    "CmsNoticeCircular",
    "CmsPlacementStat",
    "CmsQuickLink",
    "CmsRecruiterLogo",
    "CmsRecruiterPartner",
    "CmsResearchPublication",
    "CmsScholarship",
    "CmsStaffMember",
    "CmsStatCounter",
    "CmsTestimonial",
    "CampusHoliday",
    "DocumentTemplate",
    "Institute",
    "MasterDataEntry",
    "NumberingRule",
    "Permission",
    "PermissionGroup",
    "RoleTemplate",
    "RefreshTokenSession",
    "Role",
    "SystemModuleConfig",
    "User",
    "UserDocument",
    "WebsiteNavigationMenu",
    "WebsiteQuickLink",
    "WebsiteSearchIndex",
    "WebsiteSearchLog",
    "WebsiteSetting",
    "WebsiteSocialLink",
    "WebsiteTheme",
    "WebsiteTickerItem",
    "WorkingDaysConfig",
    "role_permissions_association",
    "user_roles_association",
]
