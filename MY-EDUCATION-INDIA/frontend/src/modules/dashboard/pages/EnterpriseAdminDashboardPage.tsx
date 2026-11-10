import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Search, Bell, Building2, GitBranch, Calendar } from "lucide-react";
import { dashboardApi } from "../api/dashboardApi";
import { QuickActionsBar } from "../components/QuickActionsBar";
import { KPIStatisticsCards } from "../widgets/KPIStatisticsCards";
import { InteractiveAnalyticsCharts } from "../charts/InteractiveAnalyticsCharts";
import { ActivityTimelineWidget } from "../components/ActivityTimelineWidget";
import { SystemHealthWidget } from "../components/SystemHealthWidget";
import { GlobalSearchModal } from "../components/GlobalSearchModal";
import { NotificationCenterDrawer } from "../components/NotificationCenterDrawer";

export const EnterpriseAdminDashboardPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [granularity, setGranularity] = useState<string>("MONTHLY");
  const [isSearchOpen, setIsSearchOpen] = useState<boolean>(false);
  const [isNotifDrawerOpen, setIsNotifDrawerOpen] = useState<boolean>(false);

  // Fetch unified dashboard bootstrap payload in one pass
  const { data, isLoading } = useQuery({
    queryKey: ["dashboardBootstrap", granularity],
    queryFn: () => dashboardApi.getDashboardSummary({ granularity }),
  });

  const markReadMutation = useMutation({
    mutationFn: (id: string) => dashboardApi.markNotificationRead(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["dashboardBootstrap"] });
    },
  });

  const markAllReadMutation = useMutation({
    mutationFn: () => dashboardApi.markAllNotificationsRead(),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["dashboardBootstrap"] });
    },
  });

  if (isLoading || !data) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-brand-600 border-t-transparent" />
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            Querying Enterprise PostgreSQL Analytics...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Header Controls: Switchers & Global Search Trigger */}
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-1.5 dark:border-slate-800">
            <Building2 className="h-4 w-4 text-brand-600" />
            <span className="font-bold text-slate-900 dark:text-white">MY EDUCATION INDIA HQ</span>
          </div>

          <div className="flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-1.5 dark:border-slate-800">
            <GitBranch className="h-4 w-4 text-teal-600" />
            <span className="font-semibold text-slate-700 dark:text-slate-300">All Regional Branches</span>
          </div>

          <div className="flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-1.5 dark:border-slate-800">
            <Calendar className="h-4 w-4 text-purple-600" />
            <span className="font-semibold text-slate-700 dark:text-slate-300">Session 2026-27</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setIsSearchOpen(true)}
            className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-1.5 text-xs text-slate-500 hover:border-brand-500 hover:bg-white dark:border-slate-800 dark:bg-slate-950 dark:text-slate-400"
          >
            <Search className="h-4 w-4" />
            <span>Search ERP (⌘K)...</span>
          </button>

          <button
            type="button"
            onClick={() => setIsNotifDrawerOpen(true)}
            className="relative flex h-9 w-9 items-center justify-center rounded-xl border border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-300"
            aria-label="Open notifications"
          >
            <Bell className="h-4 w-4" />
            {data.kpi_stats.unread_notifications_count > 0 && (
              <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-600 text-[9px] font-bold text-white">
                {data.kpi_stats.unread_notifications_count}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Quick Actions Bar */}
      <QuickActionsBar />

      {/* 20+ Statistics Cards Grid */}
      <KPIStatisticsCards stats={data.kpi_stats} />

      {/* Analytics Charts with Date Range Switching */}
      <InteractiveAnalyticsCharts
        data={data.charts}
        granularity={granularity}
        onGranularityChange={setGranularity}
      />

      {/* Bottom Grid: Activity Timeline & System Health */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ActivityTimelineWidget activities={data.activities} />
        <SystemHealthWidget health={data.system_health} />
      </div>

      {/* Global Search Modal */}
      <GlobalSearchModal isOpen={isSearchOpen} onClose={() => setIsSearchOpen(false)} />

      {/* Notification Center Drawer */}
      <NotificationCenterDrawer
        isOpen={isNotifDrawerOpen}
        onClose={() => setIsNotifDrawerOpen(false)}
        notifications={data.notifications}
        onMarkRead={(id) => markReadMutation.mutate(id)}
        onMarkAllRead={() => markAllReadMutation.mutate()}
      />
    </div>
  );
};
