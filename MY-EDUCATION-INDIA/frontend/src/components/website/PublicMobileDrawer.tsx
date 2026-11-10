import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  X,
  Lock,
  ChevronDown,
  ChevronRight,
  ExternalLink,
  ShieldCheck,
  Search,
} from "lucide-react";
import { NavigationMenuItem, WebsiteSettings } from "@/types/website.types";

interface PublicMobileDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  settings: WebsiteSettings;
  navigation: NavigationMenuItem[];
  onOpenSearch: () => void;
}

export const PublicMobileDrawer: React.FC<PublicMobileDrawerProps> = ({
  isOpen,
  onClose,
  settings,
  navigation,
  onOpenSearch,
}) => {
  const [expandedItems, setExpandedItems] = useState<Record<string, boolean>>({});

  if (!isOpen) return null;

  const toggleExpand = (id: string) => {
    setExpandedItems((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  return (
    <div className="fixed inset-0 z-50 lg:hidden" role="dialog" aria-modal="true">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Slide Drawer Panel */}
      <div className="fixed inset-y-0 right-0 z-50 flex w-full max-w-xs flex-col bg-white shadow-2xl animate-in slide-in-from-right duration-200">
        {/* Drawer Header */}
        <div className="flex h-20 items-center justify-between border-b border-slate-200 px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-600 text-white shadow-xs">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <p className="text-sm font-bold text-slate-900 truncate">
              {settings.site_title}
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
            aria-label="Close menu"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Quick Search Action */}
        {settings.header_show_search && (
          <div className="p-4 border-b border-slate-100">
            <button
              type="button"
              onClick={() => {
                onClose();
                onOpenSearch();
              }}
              className="flex w-full items-center justify-between rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2 text-xs font-semibold text-slate-500 hover:bg-white"
            >
              <span className="flex items-center gap-2">
                <Search className="h-4 w-4" />
                <span>Search website...</span>
              </span>
            </button>
          </div>
        )}

        {/* Scrollable Navigation Tree */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-1">
          {navigation.map((item) => {
            const hasChildren = item.children && item.children.length > 0;
            const isExpanded = Boolean(expandedItems[item.id]);

            if (hasChildren) {
              return (
                <div key={item.id} className="space-y-1">
                  <button
                    type="button"
                    onClick={() => toggleExpand(item.id)}
                    className="flex w-full items-center justify-between rounded-xl px-3.5 py-2.5 text-xs font-semibold text-slate-800 hover:bg-slate-100 transition"
                  >
                    <span>{item.title}</span>
                    {isExpanded ? (
                      <ChevronDown className="h-4 w-4 text-slate-500" />
                    ) : (
                      <ChevronRight className="h-4 w-4 text-slate-500" />
                    )}
                  </button>

                  {/* Submenu Drawer */}
                  {isExpanded && (
                    <div className="ml-4 pl-2 border-l border-slate-200 space-y-1 py-1">
                      {item.children.map((child) => (
                        <div key={child.id}>
                          {child.is_external ? (
                            <a
                              href={child.path}
                              target={child.open_new_tab ? "_blank" : "_self"}
                              rel="noreferrer"
                              onClick={onClose}
                              className="flex items-center justify-between rounded-lg px-3 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100"
                            >
                              <span>{child.title}</span>
                              <ExternalLink className="h-3 w-3 text-slate-400" />
                            </a>
                          ) : (
                            <Link
                              to={child.path}
                              onClick={onClose}
                              className="block rounded-lg px-3 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100"
                            >
                              {child.title}
                            </Link>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            }

            return item.is_external ? (
              <a
                key={item.id}
                href={item.path}
                target={item.open_new_tab ? "_blank" : "_self"}
                rel="noreferrer"
                onClick={onClose}
                className="flex items-center justify-between rounded-xl px-3.5 py-2.5 text-xs font-semibold text-slate-800 hover:bg-slate-100"
              >
                <span>{item.title}</span>
                <ExternalLink className="h-3.5 w-3.5 text-slate-400" />
              </a>
            ) : (
              <Link
                key={item.id}
                to={item.path}
                onClick={onClose}
                className="block rounded-xl px-3.5 py-2.5 text-xs font-semibold text-slate-800 hover:bg-slate-100"
              >
                {item.title}
              </Link>
            );
          })}
        </nav>

        {/* Drawer Bottom Action: Single Login */}
        {settings.header_show_login && (
          <div className="border-t border-slate-200 p-4">
            <Link
              to={settings.header_login_route || "/login"}
              onClick={onClose}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 py-3 text-xs font-bold text-white shadow-md shadow-brand-600/20 hover:bg-brand-700"
            >
              <Lock className="h-4 w-4" />
              <span>{settings.header_login_button_text || "Login"}</span>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};
