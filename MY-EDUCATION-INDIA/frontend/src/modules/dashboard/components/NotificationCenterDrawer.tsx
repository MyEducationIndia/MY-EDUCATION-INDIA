import React from "react";
import { Bell, CheckCheck, X, AlertTriangle, Info, ShieldAlert } from "lucide-react";
import { NotificationItem } from "../types/dashboard.types";

interface NotificationCenterDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  notifications: NotificationItem[];
  onMarkRead: (id: string) => void;
  onMarkAllRead: () => void;
}

export const NotificationCenterDrawer: React.FC<NotificationCenterDrawerProps> = ({
  isOpen,
  onClose,
  notifications,
  onMarkRead,
  onMarkAllRead,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/40 backdrop-blur-xs">
      <div className="flex h-full w-full max-w-md flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <div className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <Bell className="h-5 w-5 text-brand-600 dark:text-brand-400" />
            <h2 className="text-sm font-bold text-slate-900 dark:text-white">Notification Center</h2>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onMarkAllRead}
              className="inline-flex items-center gap-1 rounded-md bg-slate-100 px-2.5 py-1 text-[11px] font-semibold text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300"
            >
              <CheckCheck className="h-3.5 w-3.5" /> Mark All Read
            </button>
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-2.5">
          {notifications.length === 0 ? (
            <p className="py-12 text-center text-xs text-slate-500">No active notifications.</p>
          ) : (
            notifications.map((n) => (
              <div
                key={n.id}
                onClick={() => onMarkRead(n.id)}
                className={`cursor-pointer rounded-xl border p-3.5 transition ${
                  n.is_read
                    ? "border-slate-200 bg-white opacity-70 dark:border-slate-800 dark:bg-slate-950/40"
                    : "border-brand-200 bg-brand-50/40 dark:border-brand-900 dark:bg-brand-950/30"
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    {n.priority === "CRITICAL" ? (
                      <ShieldAlert className="h-4 w-4 text-rose-500 shrink-0" />
                    ) : (
                      <Info className="h-4 w-4 text-brand-600 shrink-0" />
                    )}
                    <h3 className="text-xs font-bold text-slate-900 dark:text-white">{n.title}</h3>
                  </div>
                  <span className="text-[10px] text-slate-400">
                    {new Date(n.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </span>
                </div>
                <p className="mt-1 text-xs text-slate-600 dark:text-slate-400">{n.message}</p>
                <div className="mt-2 flex items-center justify-between text-[10px]">
                  <span className="rounded-sm bg-slate-100 px-1.5 py-0.5 font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                    {n.category}
                  </span>
                  {!n.is_read && <span className="font-bold text-brand-600">Unread</span>}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
