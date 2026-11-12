import React, { useState, useEffect } from "react";
import { Link, useNavigate, Outlet } from "react-router-dom";
import {
  Menu,
  Globe,
  Bell,
  Search,
  Command,
  Sun,
  Moon,
  LogOut,
  User,
  Shield,
  HelpCircle,
  FileText,
  Clock,
  Sparkles,
  ChevronDown,
  CheckCircle2,
  X,
  ExternalLink,
} from "lucide-react";
import { useAuthSession } from "@/hooks/useAuthSession";
import { AdminSidebar } from "@/components/navigation/AdminSidebar";
import { resolveCurrentSubdomain } from "@/utils/subdomainResolver";

interface LayoutProps {
  children?: React.ReactNode;
}

export const SuperAdminLayout: React.FC<LayoutProps> = () => {
  const { user, isAuthenticated, isInitializing, logout } = useAuthSession();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDarkMode, setIsDarkMode] = useState(false);
  const navigate = useNavigate();
  const currentSubdomain = resolveCurrentSubdomain();

  // Keyboard shortcut for Command Palette: Ctrl+K or Cmd+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setCommandPaletteOpen((prev) => !prev);
      }
      if (e.key === "Escape") {
        setCommandPaletteOpen(false);
        setNotificationsOpen(false);
        setProfileMenuOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const COMMAND_ITEMS = [
    { label: "Admin Control Center", path: "/admin/dashboard", category: "Core" },
    { label: "37 Subsystems Matrix", path: "/admin/modules", category: "Governance" },
    { label: "User Provisioning", path: "/admin/users", category: "Access" },
    { label: "Roles & RBAC Matrix", path: "/admin/roles", category: "Access" },
    { label: "Certificates & Verification", path: "/admin/certificates", category: "Academic" },
    { label: "CBT Testing Platform", path: "/admin/cbt", category: "Academic" },
    { label: "Examinations & Results", path: "/admin/exams", category: "Academic" },
    { label: "Attendance & Leaves", path: "/admin/attendance", category: "Operations" },
    { label: "Fee & Finance Management", path: "/admin/fees", category: "Finance" },
    { label: "Academic Curricula", path: "/admin/academics", category: "Academic" },
    { label: "CRM & Franchise Centers (M17)", path: "/admin/crm", category: "Admissions" },
    { label: "Admission & CRM Pipeline", path: "/admin/admissions", category: "Admissions" },
    { label: "Student Information (SIMS)", path: "/admin/students", category: "Core" },
    { label: "Website CMS Builder", path: "/admin/cms/pages", category: "Website" },
    { label: "Website Leads & Inquiries", path: "/admin/cms/enquiries", category: "Website" },
    { label: "Security Audit Trail", path: "/admin/audit-logs", category: "Security" },
    { label: "Active Sessions", path: "/admin/sessions", category: "Security" },
    { label: "Login History", path: "/admin/login-history", category: "Security" },
    { label: "Security Policies", path: "/admin/security-policies", category: "Security" },
    { label: "Experience Portals Hub (M20)", path: "/admin/experience", category: "Experience" },
    { label: "Platform DevOps & Cluster (M19)", path: "/admin/platform", category: "DevOps" },
    { label: "Core System Settings", path: "/admin/settings", category: "Settings" },
    { label: "Executive BI & Reports (M18)", path: "/admin/bi", category: "Analytics" },
    { label: "API Integrations & Vault", path: "/admin/integrations", category: "Platform" },
  ];

  const filteredCommands = searchQuery.trim()
    ? COMMAND_ITEMS.filter((item) =>
        item.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.category.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : COMMAND_ITEMS;

  if (isInitializing) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-brand-600 border-t-transparent" />
          <p className="text-sm font-medium text-slate-600">
            Verifying encrypted session with PostgreSQL...
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <Link to="/login" replace />;
  }

  return (
    <div className={`flex min-h-screen ${isDarkMode ? "dark bg-slate-950 text-slate-100" : "bg-slate-50 text-slate-900"}`}>
      {/* Role-Based Sidebar */}
      <AdminSidebar
        user={user}
        isOpenMobile={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
        onLogout={logout}
      />

      {/* Main Container */}
      <div className="flex flex-1 flex-col min-w-0">
        {/* Enterprise Top Navigation Bar */}
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-4 backdrop-blur-md sm:px-6 lg:px-8">
          {/* Left: Mobile Toggle & Title */}
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => setMobileMenuOpen(true)}
              className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden"
              aria-label="Open navigation sidebar"
            >
              <Menu className="h-5 w-5" />
            </button>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-sm font-bold text-slate-900 sm:text-base">
                  Enterprise Command Center
                </h1>
                <span className="hidden rounded-full bg-brand-50 px-2 py-0.5 text-[10px] font-semibold text-brand-700 sm:inline-block">
                  v2.0 Production
                </span>
              </div>
              <p className="hidden text-xs text-slate-500 sm:block">
                Flagship Campus • Zero-LocalStorage Memory Architecture • Neon PostgreSQL 16
              </p>
            </div>
          </div>

          {/* Center: Command Palette Trigger */}
          <div className="hidden md:flex flex-1 max-w-md mx-6">
            <button
              type="button"
              onClick={() => setCommandPaletteOpen(true)}
              className="flex w-full items-center justify-between rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-1.5 text-xs text-slate-400 shadow-2xs hover:border-slate-300 hover:bg-white transition"
            >
              <span className="flex items-center gap-2">
                <Search className="h-3.5 w-3.5 text-slate-400" />
                <span>Search modules, students, or actions...</span>
              </span>
              <kbd className="inline-flex items-center gap-0.5 rounded border border-slate-300 bg-white px-1.5 py-0.5 text-[10px] font-semibold text-slate-500 shadow-2xs">
                <Command className="h-2.5 w-2.5" /> K
              </kbd>
            </button>
          </div>

          {/* Right: Notifications, Quick Actions, Profile */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* View Public Website */}
            <Link
              to="/"
              target="_blank"
              rel="noreferrer"
              className="hidden sm:inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-2.5 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
              title="Open Public Website in New Tab"
            >
              <Globe className="h-3.5 w-3.5 text-brand-600" />
              <span>Public Site</span>
              <ExternalLink className="h-3 w-3 text-slate-400" />
            </Link>

            {/* Notification Bell */}
            <div className="relative">
              <button
                type="button"
                onClick={() => setNotificationsOpen(!notificationsOpen)}
                className="relative rounded-lg p-2 text-slate-600 hover:bg-slate-100 transition"
                aria-label="View notifications"
              >
                <Bell className="h-4 w-4" />
                <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-emerald-500 ring-2 ring-white"></span>
              </button>

              {notificationsOpen && (
                <div className="absolute right-0 mt-2 w-80 rounded-2xl border border-slate-200 bg-white p-4 shadow-xl z-50">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                    <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                      System Notifications
                    </h3>
                    <span className="rounded-full bg-brand-50 px-2 py-0.5 text-[10px] font-semibold text-brand-700">
                      Live Stream
                    </span>
                  </div>
                  <div className="mt-3 space-y-2.5 text-xs">
                    <div className="flex items-start gap-2.5 rounded-lg p-2 bg-slate-50">
                      <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-slate-800">Neon Database Operational</p>
                        <p className="text-slate-500 text-[11px]">Serverless connection pool healthy</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-2.5 rounded-lg p-2">
                      <Shield className="h-4 w-4 text-brand-600 shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-slate-800">Argon2 Password Vault</p>
                        <p className="text-slate-500 text-[11px]">Cryptographic handshake active</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* User Profile Dropdown */}
            <div className="relative">
              <button
                type="button"
                onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                className="flex items-center gap-2 rounded-xl p-1.5 hover:bg-slate-100 transition"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600 text-xs font-bold text-white shadow-xs">
                  {user.first_name?.[0] || "U"}
                </div>
                <div className="hidden text-left sm:block">
                  <p className="text-xs font-semibold text-slate-800 leading-none">
                    {user.first_name} {user.last_name}
                  </p>
                  <p className="text-[10px] text-slate-500 mt-0.5 font-medium">
                    {user.is_super_admin ? "Super Admin" : user.roles[0] || "Staff"}
                  </p>
                </div>
                <ChevronDown className="h-3.5 w-3.5 text-slate-400 hidden sm:block" />
              </button>

              {profileMenuOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-2xl border border-slate-200 bg-white p-2 shadow-xl z-50 text-xs">
                  <div className="px-3 py-2 border-b border-slate-100 mb-1">
                    <p className="font-bold text-slate-900 truncate">{user.email}</p>
                    <p className="text-[10px] text-slate-500 capitalize">{user.roles.join(", ") || "User"}</p>
                  </div>
                  <Link
                    to="/admin/dashboard"
                    onClick={() => setProfileMenuOpen(false)}
                    className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-slate-700 hover:bg-slate-50"
                  >
                    <User className="h-4 w-4 text-slate-400" />
                    <span>Dashboard Profile</span>
                  </Link>
                  <Link
                    to="/admin/settings"
                    onClick={() => setProfileMenuOpen(false)}
                    className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-slate-700 hover:bg-slate-50"
                  >
                    <Shield className="h-4 w-4 text-slate-400" />
                    <span>System Settings</span>
                  </Link>
                  <Link
                    to="/admin/audit-logs"
                    onClick={() => setProfileMenuOpen(false)}
                    className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-slate-700 hover:bg-slate-50"
                  >
                    <Clock className="h-4 w-4 text-slate-400" />
                    <span>My Activity Log</span>
                  </Link>
                  <div className="border-t border-slate-100 my-1 pt-1">
                    <button
                      type="button"
                      onClick={() => void logout()}
                      className="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-rose-600 hover:bg-rose-50"
                    >
                      <LogOut className="h-4 w-4" />
                      <span>Sign Out Securely</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Command Palette Modal (Ctrl+K) */}
        {commandPaletteOpen && (
          <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-slate-900/60 backdrop-blur-xs p-4">
            <div className="w-full max-w-xl rounded-2xl border border-slate-200 bg-white p-4 shadow-2xl">
              <div className="flex items-center gap-3 border-b border-slate-200 pb-3">
                <Search className="h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  autoFocus
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Type a command or jump to subsystem..."
                  className="w-full text-sm outline-hidden placeholder:text-slate-400"
                />
                <button
                  type="button"
                  onClick={() => setCommandPaletteOpen(false)}
                  className="rounded p-1 text-slate-400 hover:text-slate-600"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>

              <div className="mt-3 max-h-72 overflow-y-auto space-y-1">
                {filteredCommands.length > 0 ? (
                  filteredCommands.map((cmd) => (
                    <button
                      key={cmd.path}
                      type="button"
                      onClick={() => {
                        navigate(cmd.path);
                        setCommandPaletteOpen(false);
                      }}
                      className="flex w-full items-center justify-between rounded-xl px-3 py-2 text-left text-xs font-semibold text-slate-700 hover:bg-brand-50 hover:text-brand-700 transition"
                    >
                      <span>{cmd.label}</span>
                      <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-500">
                        {cmd.category}
                      </span>
                    </button>
                  ))
                ) : (
                  <p className="py-6 text-center text-xs text-slate-500">No matching subsystems found.</p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Page Content Viewport */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
