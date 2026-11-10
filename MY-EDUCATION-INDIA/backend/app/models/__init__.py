# Central Model Registration for Alembic and SQLAlchemy
from app.models.user import User, user_roles_association
from app.models.role import Role, role_permissions_association
from app.models.permission import Permission
from app.models.institute import Institute
from app.models.refresh_token import RefreshTokenSession
from app.models.audit_log import AuditLog
from app.models.module_config import SystemModuleConfig
from app.models.cms_about import CmsAccreditation, CmsCampusInfrastructure, CmsLeadershipMessage, CmsMilestone
from app.models.cms_courses import CmsCourse, CmsCourseCategory, CmsCourseCurriculum, CmsCourseFaculty
from app.models.cms_home import CmsFeaturedProgram, CmsHeroSlide, CmsNewsletterSubscriber, CmsQuickLink, CmsRecruiterLogo, CmsStatCounter, CmsTestimonial
from app.models.website import WebsiteNavigationMenu, WebsiteQuickLink, WebsiteSearchIndex, WebsiteSearchLog, WebsiteSetting, WebsiteSocialLink, WebsiteTheme, WebsiteTickerItem
