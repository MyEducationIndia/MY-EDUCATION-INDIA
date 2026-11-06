import React, { useState } from "react";
import { Outlet, Navigate } from "react-router-dom";
import { Menu, Globe } from "lucide-react";
import { useAuthSession } from "@/hooks/useAuthSession";
import { AdminSidebar } from "@/components/navigation/AdminSidebar";
import { resolveCurrentSubdomain } from "@/utils/subdomainResolver";

export const SuperAdminLayout: React.FC = () => {
  const { user, isAuthenticated, isInitializing, logout } = useAuthSession();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const currentSubdomain = resolveCurrentSubdomain();

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
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex min-h-screen bg-slate-50">
      <AdminSidebar
        user={user}
        isOpenMobile={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
        onLogout={logout}
      />

      <div className="flex flex-1 flex-col min-w-0">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 sm:px-6 lg:px-8">
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
              <h1 className="text-sm font-bold text-slate-900 sm:text-base">
                Enterprise Command Center
              </h1>
              <p className="hidden text-xs text-slate-500 sm:block">
                Zero-LocalStorage Architecture • Neon PostgreSQL 16
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1.5 rounded-md bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700">
              <Globe className="h-3.5 w-3.5 text-brand-600" />
              Portal: <strong className="uppercase">{currentSubdomain}</strong>
            </span>
          </div>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
