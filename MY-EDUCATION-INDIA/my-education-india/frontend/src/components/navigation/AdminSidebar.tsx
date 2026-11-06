import React from "react";
import { NavLink } from "react-router-dom";
import {
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
} from "lucide-react";
import { AuthenticatedUser } from "@/types/auth.types";import { AuthenticatedUser } from "@/types/auth.types";

interface AdminSidebarProps {
  user: AuthenticatedUser;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
  onLogout: () => Promise<void>;
}

const NAV_ITEMS = [
  {
    to: "/admin/dashboard",
    label: "Admin Control Center",
    icon: LayoutDashboard,
  },
  {
    to: "/admin/certificates",
    label: "Certificates & Verification",
    icon: FileBadge,
  },
  {
    to: "/admin/cbt",
    label: "CBT Testing Platform",
    icon: MonitorPlay,
  },
  {
    to: "/admin/exams",
    label: "Examinations & Results",
    icon: Award,
  },
  {
    to: "/admin/attendance",
    label: "Attendance & Leaves",
    icon: CalendarCheck,
  },
  {
    to: "/admin/fees",
    label: "Fee & Finance Management",
    icon: IndianRupee,
  },
  {
    to: "/admin/academics",
    label: "Academic Management",
    icon: BookOpen,
  },
  {
    to: "/admin/admissions",
    label: "Admission & CRM Pipeline",
    icon: ClipboardList,
  },
  {
    to: "/admin/students",
    label: "Student Information (SIMS)",
    icon: GraduationCap,
  },
  {
    to: "/admin/cms/pages",
    label: "Website CMS Builder",
    icon: Globe,
  },
  {
    to: "/admin/cms/enquiries",
    label: "Website Leads & Inquiries",
    icon: MessageSquare,
  },
  {
    to: "/admin/settings",
    label: "Core System Engine",
    icon: Sliders,
  },
  {
    to: "/admin/modules",
    label: "37 Subsystems Control",
    icon: Layers,
  },
  {
    to: "/admin/roles",
    label: "Roles & RBAC Matrix",
    icon: KeyRound,
  },
  {
    to: "/admin/users",
    label: "User Provisioning",
    icon: Users,
  },
  {
    to: "/admin/sessions",
    label: "Active Sessions & Force Logout",
    icon: MonitorSmartphone,
  },
  {
    to: "/admin/login-history",
    label: "Login History & Audit",
    icon: History,
  },
  {
    to: "/admin/audit-logs",
    label: "Security Audit Trail",
    icon: FileSearch,
  },
];

export const AdminSidebar: React.FC<AdminSidebarProps> = ({
  user,
  isOpenMobile,
  onCloseMobile,
  onLogout,
}) => {
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
        <div className="flex h-16 items-center justify-between border-b border-slate-800 px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-600 text-white shadow-xs">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-bold tracking-wide text-white">
                MY EDUCATION INDIA
              </p>
              <p className="text-[11px] font-medium text-slate-400">
                Enterprise Super Admin
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

        <nav className="flex-1 space-y-1 px-3 py-5 overflow-y-auto" aria-label="Main Navigation">
          {NAV_ITEMS.map((item) => {
            const IconComponent = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={onCloseMobile}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-lg px-3.5 py-2.5 text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-brand-600 text-white shadow-xs"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`
                }
              >
                <IconComponent className="h-4 w-4 shrink-0" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="border-t border-slate-800 p-4">
          <div className="mb-3 rounded-lg bg-slate-800/80 p-3">
            <p className="truncate text-xs font-semibold text-white">
              {user.first_name} {user.last_name}
            </p>
            <p className="truncate text-xs text-slate-400">{user.email}</p>
            <span className="mt-1.5 inline-block rounded-sm bg-brand-500/20 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-brand-100">
              {user.is_super_admin ? "Super Administrator" : user.roles[0] || "Staff"}
            </span>
          </div>
          <button
            type="button"
            onClick={() => void onLogout()}
            className="flex w-full items-center justify-center gap-2 rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 transition hover:bg-rose-600 hover:border-rose-600 hover:text-white"
          >
            <LogOut className="h-4 w-4" />
            <span>Sign Out Securely</span>
          </button>
        </div>
      </aside>
    </>
  );
};
