import React from "react";
import { NavLink } from "react-router-dom";
import {
  Sparkles,
  Building2,
  GitBranch,
  Bell,
  FolderOpen,
  Workflow,
  Server,
  BarChart3,
  Cpu,
  Target,
  ShieldCheck,
  LayoutDashboard,
  FileBadge,
  MonitorPlay,
  Award,
  CalendarCheck,
  IndianRupee,
  BookOpen,
  GraduationCap,
  ClipboardList,
  Layers,
  Globe,
  MessageSquare,
  Users,
  KeyRound,
  FileSearch,
  MonitorSmartphone,
  History,
  Sliders,
  LogOut,
  X,
  Lock,
  Database,
  Terminal,
  BookMarked,
  PhoneCall,
  Laptop,
} from "lucide-react";
import { AuthenticatedUser } from "@/types/auth.types";

interface AdminSidebarProps {
  user: AuthenticatedUser;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
  onLogout: () => Promise<void>;
}

interface NavItem {
  to: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  roles?: string[]; // If omitted, available to all authorized users
  badge?: string;
}

const ALL_NAV_ITEMS: NavItem[] = [
  // Core Dashboards
  {
    to: "/admin/dashboard",
    label: "Admin Command Center",
    icon: LayoutDashboard,
  },

  // Sovereign / Root Controls
  {
    to: "/admin/modules",
    label: "37 Subsystems Matrix",
    icon: Layers,
    roles: ["ROOT_OWNER", "SUPER_ADMIN"],
    badge: "37",
  },
  {
    to: "/admin/institute",
    label: "Institute Setup & Campus",
    icon: Building2,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },
  {
    to: "/admin/departments",
    label: "Departments & Hierarchy",
    icon: GitBranch,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },
  {
    to: "/admin/notifications",
    label: "Notification Center",
    icon: Bell,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },
  {
    to: "/admin/media-manager",
    label: "Media & File Manager",
    icon: FolderOpen,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },
  {
    to: "/admin/workflows",
    label: "Workflow Engine",
    icon: Workflow,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },
  {
    to: "/admin/reports",
    label: "Reports Engine",
    icon: BarChart3,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },
  {
    to: "/admin/roles",
    label: "Roles & RBAC Matrix",
    icon: KeyRound,
    roles: ["ROOT_OWNER", "SUPER_ADMIN"],
  },
  {
    to: "/admin/users",
    label: "User Provisioning",
    icon: Users,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },

  // Academic & Evaluation Subsystems
  {
    to: "/admin/academics",
    label: "Academic Management",
    icon: BookOpen,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "INSTITUTE_ADMIN", "FACULTY", "STUDENT"],
  },
  {
    to: "/admin/students",
    label: "Student Information (SIMS)",
    icon: GraduationCap,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "INSTITUTE_ADMIN", "STAFF", "COUNSELLOR"],
  },
  {
    to: "/admin/attendance",
    label: "Attendance & Leaves",
    icon: CalendarCheck,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "INSTITUTE_ADMIN", "FACULTY", "STAFF", "STUDENT", "PARENT"],
  },
  {
    to: "/admin/cbt",
    label: "CBT Testing Platform",
    icon: MonitorPlay,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "FACULTY", "EXAM_CONTROLLER", "STUDENT"],
  },
  {
    to: "/admin/exams",
    label: "Examinations & Results",
    icon: Award,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "FACULTY", "EXAM_CONTROLLER", "STUDENT", "PARENT"],
  },
  {
    to: "/admin/certificates",
    label: "Certificates & Verification",
    icon: FileBadge,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "INSTITUTE_ADMIN", "STUDENT"],
  },
  {
    to: "/admin/library",
    label: "Library & Digital Knowledge",
    icon: BookMarked,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "LIBRARIAN", "FACULTY", "STUDENT"],
  },
  {
    to: "/admin/lxp",
    label: "Learning Experience (LXP)",
    icon: GraduationCap,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "FACULTY", "STUDENT"],
    badge: "LXP",
  },

  // Finance & Bursar Subsystems
  {
    to: "/admin/fees",
    label: "Fee & Finance Management",
    icon: IndianRupee,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "ACCOUNTANT", "STUDENT", "PARENT"],
  },

  // Admissions & Outreach Subsystems
  {
    to: "/admin/crm",
    label: "CRM & Franchise Centers",
    icon: Target,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "COUNSELLOR", "RECEPTION"],
    badge: "M17",
  },
  {
    to: "/admin/admissions",
    label: "Admission Pipeline",
    icon: ClipboardList,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "COUNSELLOR", "RECEPTION"],
  },

  // Website CMS Subsystems
  {
    to: "/admin/cms/pages",
    label: "Website CMS Builder",
    icon: Globe,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },
  {
    to: "/admin/cms/enquiries",
    label: "Website Leads & Inquiries",
    icon: MessageSquare,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "COUNSELLOR", "RECEPTION"],
  },

  // Security & Audit Governance
  {
    to: "/admin/audit-logs",
    label: "Security Audit Trail",
    icon: FileSearch,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN", "IT_SUPPORT"],
  },
  {
    to: "/admin/sessions",
    label: "Active Sessions & Logout",
    icon: MonitorSmartphone,
    roles: ["ROOT_OWNER", "SUPER_ADMIN"],
  },
  {
    to: "/admin/login-history",
    label: "Login History & Audit",
    icon: History,
    roles: ["ROOT_OWNER", "SUPER_ADMIN"],
  },
  {
    to: "/admin/bi",
    label: "Executive BI & Reports",
    icon: BarChart3,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
    badge: "BI",
  },
  {
    to: "/admin/experience",
    label: "Experience Portals Hub",
    icon: Sparkles,
    roles: ["ROOT_OWNER", "SUPER_ADMIN"],
    badge: "M20",
  },
  {
    to: "/admin/platform",
    label: "Platform DevOps & Cluster",
    icon: Server,
    roles: ["ROOT_OWNER", "SUPER_ADMIN"],
    badge: "DEVOPS",
  },
  {
    to: "/admin/integrations",
    label: "API Integrations & Vault",
    icon: Cpu,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
    badge: "API",
  },
  {
    to: "/admin/security-policies",
    label: "Security Policies",
    icon: ShieldCheck,
    roles: ["ROOT_OWNER", "SUPER_ADMIN"],
  },
  {
    to: "/admin/settings",
    label: "System Settings & Master Data",
    icon: Sliders,
    roles: ["ROOT_OWNER", "SUPER_ADMIN", "ADMIN"],
  },
];

export const AdminSidebar: React.FC<AdminSidebarProps> = ({
  user,
  isOpenMobile,
  onCloseMobile,
  onLogout,
}) => {
  // Filter navigation items by active user's roles
  const userRoles = user.roles || [];
  const isSuper = user.is_super_admin || userRoles.includes("ROOT_OWNER") || userRoles.includes("SUPER_ADMIN");

  const visibleItems = ALL_NAV_ITEMS.filter((item) => {
    if (isSuper) return true; // Super admins see all governed subsystems
    if (!item.roles || item.roles.length === 0) return true;
    return item.roles.some((role) => userRoles.includes(role));
  });

  return (
    <>
      {isOpenMobile && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/60 backdrop-blur-xs lg:hidden"
          onClick={onCloseMobile}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-72 flex-col bg-slate-900 text-slate-100 transition-transform duration-200 ease-in-out lg:static lg:translate-x-0 ${
          isOpenMobile ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Brand Header */}
        <div className="flex h-16 items-center justify-between border-b border-slate-800 px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-600 text-white shadow-xs">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-bold tracking-wide text-white">
                MY EDUCATION INDIA
              </p>
              <p className="text-[11px] font-medium text-slate-400 capitalize">
                {isSuper ? "Super Administrator" : userRoles[0] || "Staff Portal"}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onCloseMobile}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white lg:hidden"
            aria-label="Close navigation menu"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation Items (Filtered by RBAC Role) */}
        <nav className="flex-1 space-y-1 px-3 py-5 overflow-y-auto" aria-label="Main Navigation">
          <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Enterprise Subsystems
          </div>
          {visibleItems.map((item) => {
            const IconComponent = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={onCloseMobile}
                className={({ isActive }) =>
                  `flex items-center justify-between rounded-xl px-3.5 py-2 text-xs font-semibold transition-colors ${
                    isActive
                      ? "bg-brand-600 text-white shadow-xs"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <IconComponent className="h-4 w-4 shrink-0" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="rounded-full bg-brand-500/30 px-2 py-0.5 text-[10px] font-bold text-brand-300">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* User Card & Sign Out */}
        <div className="border-t border-slate-800 p-4">
          <div className="mb-3 rounded-xl bg-slate-800/80 p-3">
            <p className="truncate text-xs font-semibold text-white">
              {user.first_name} {user.last_name}
            </p>
            <p className="truncate text-[11px] text-slate-400">{user.email}</p>
            <span className="mt-1.5 inline-block rounded-md bg-brand-500/20 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-brand-300">
              {isSuper ? "Super Administrator" : userRoles[0] || "Authorized User"}
            </span>
          </div>
          <button
            type="button"
            onClick={() => void onLogout()}
            className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 transition hover:bg-rose-600 hover:border-rose-600 hover:text-white"
          >
            <LogOut className="h-4 w-4" />
            <span>Sign Out Securely</span>
          </button>
        </div>
      </aside>
    </>
  );
};
