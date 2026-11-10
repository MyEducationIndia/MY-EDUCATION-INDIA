import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  ShieldCheck,
  Search,
  Menu,
  X,
  ChevronDown,
  ExternalLink,
  Lock,
} from "lucide-react";
import { NavigationMenuItem, WebsiteSettings } from "@/types/website.types";

interface PublicMainHeaderProps {
  settings: WebsiteSettings;
  navigation: NavigationMenuItem[];
  onOpenSearch: () => void;
  onOpenMobileMenu: () => void;
}

export const PublicMainHeader: React.FC<PublicMainHeaderProps> = ({
  settings,
  navigation,
  onOpenSearch,
  onOpenMobileMenu,
}) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const location = useLocation();

  // Scroll listener for elevation shadow and sticky header transition
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`top-0 z-40 w-full transition-all duration-200 ${
        settings.header_is_sticky ? "sticky" : "relative"
      } ${
        isScrolled
          ? "border-b border-slate-200 bg-white/95 shadow-md shadow-slate-900/5 backdrop-blur-md"
          : "border-b border-slate-100 bg-white"
      }`}
    >
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Left: Brand Identity */}
        <Link to="/" className="flex items-center gap-3.5 group">
          {settings.header_logo_url ? (
            <img
              src={settings.header_logo_url}
              alt={settings.site_title}
              className="h-11 w-auto object-contain transition-transform group-hover:scale-105"
            />
          ) : (
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-600 text-white shadow-md shadow-brand-600/20 transition-transform group-hover:scale-105">
              <ShieldCheck className="h-6 w-6" />
            </div>
          )}
          <div>
            <p className="text-lg font-black tracking-tight text-slate-900 leading-tight">
              {settings.site_title}
            </p>
            <p className="text-[11px] font-semibold tracking-wider text-brand-700 uppercase">
              {settings.tagline}
            </p>
          </div>
        </Link>

        {/* Center: Dynamic Desktop Navigation Menu */}
        <nav className="hidden lg:flex items-center gap-7 text-sm font-semibold text-slate-700">
          {navigation.map((item) => {
            const hasChildren = item.children && item.children.length > 0;
            const isDropdownActive = activeDropdown === item.id;
            const isActive =
              location.pathname === item.path ||
              (item.path !== "/" && location.pathname.startsWith(item.path));

            if (hasChildren) {
              return (
                <div
                  key={item.id}
                  className="relative"
                  onMouseEnter={() => setActiveDropdown(item.id)}
                  onMouseLeave={() => setActiveDropdown(null)}
                >
                  <button
                    type="button"
                    className={`flex items-center gap-1.5 py-2 transition-colors hover:text-brand-600 ${
                      isDropdownActive || isActive ? "text-brand-600" : "text-slate-700"
                    }`}
                  >
                    <span>{item.title}</span>
                    <ChevronDown className="h-3.5 w-3.5 transition-transform duration-200" />
                  </button>

                  {/* Mega Menu / Dropdown Container */}
                  {isDropdownActive && (
                    <div className="absolute top-full left-0 mt-1 min-w-[240px] rounded-2xl border border-slate-200 bg-white p-2.5 shadow-xl animate-in fade-in zoom-in-95 duration-150">
                      <div className="space-y-1">
                        {item.children.map((child) => (
                          <div key={child.id}>
                            {child.is_external ? (
                              <a
                                href={child.path}
                                target={child.open_new_tab ? "_blank" : "_self"}
                                rel="noreferrer"
                                className="flex items-center justify-between rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-700 hover:bg-brand-50 hover:text-brand-700 transition"
                              >
                                <span>{child.title}</span>
                                <ExternalLink className="h-3 w-3 text-slate-400" />
                              </a>
                            ) : (
                              <Link
                                to={child.path}
                                onClick={() => setActiveDropdown(null)}
                                className="block rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-700 hover:bg-brand-50 hover:text-brand-700 transition"
                              >
                                {child.title}
                              </Link>
                            )}
                          </div>
                        ))}
                      </div>
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
                className="transition-colors hover:text-brand-600"
              >
                {item.title}
              </a>
            ) : (
              <Link
                key={item.id}
                to={item.path}
                className={`transition-colors hover:text-brand-600 ${
                  isActive ? "text-brand-600 font-bold" : "text-slate-700"
                }`}
              >
                {item.title}
              </Link>
            );
          })}
        </nav>

        {/* Right Controls: Global Search, Single Login, Mobile Menu Toggle */}
        <div className="flex items-center gap-3">
          {/* Global Search Button */}
          {settings.header_show_search && (
            <button
              type="button"
              onClick={onOpenSearch}
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-slate-50 text-slate-600 hover:border-slate-300 hover:bg-white transition shadow-2xs"
              aria-label="Open global search"
              title="Search website (Ctrl + K)"
            >
              <Search className="h-4 w-4" />
            </button>
          )}

          {/* SINGLE LOGIN BUTTON: Universal Authentication Entrypoint */}
          {settings.header_show_login && (
            <Link
              to={settings.header_login_route || "/login"}
              className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-xs font-bold text-white shadow-md shadow-brand-600/20 hover:bg-brand-700 transition"
            >
              <Lock className="h-3.5 w-3.5" />
              <span>{settings.header_login_button_text || "Login"}</span>
            </Link>
          )}

          {/* Mobile Menu Hamburger Toggle */}
          <button
            type="button"
            onClick={onOpenMobileMenu}
            className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-100 transition lg:hidden"
            aria-label="Open navigation menu"
          >
            <Menu className="h-5 w-5" />
          </button>
        </div>
      </div>
    </header>
  );
};
