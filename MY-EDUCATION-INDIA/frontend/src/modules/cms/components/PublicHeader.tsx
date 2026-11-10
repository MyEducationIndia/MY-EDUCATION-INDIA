import React, { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { ShieldCheck, Phone, Mail, Menu, X, ArrowRight } from "lucide-react";
import { MenuStructure, WebsiteSettingsRecord } from "../types/cms.types";

interface PublicHeaderProps {
  settings?: WebsiteSettingsRecord | null;
  menu?: MenuStructure | null;
}

export const PublicHeader: React.FC<PublicHeaderProps> = ({ settings, menu }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const defaultNavItems = [
    { title: "Home", url: "/" },
    { title: "About", url: "/about" },
    { title: "Courses", url: "/courses" },
    { title: "Admissions", url: "/admissions" },
    { title: "Faculty", url: "/faculty" },
    { title: "Gallery", url: "/gallery" },
    { title: "News & Events", url: "/news" },
    { title: "Contact", url: "/contact" },
  ];

  const navLinks = menu?.items && menu.items.length > 0
    ? menu.items
    : defaultNavItems;

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 shadow-xs backdrop-blur-md dark:border-slate-800 dark:bg-slate-900/95">
      {/* Top Bar with Dynamic Contact Info */}
      <div className="border-b border-slate-100 bg-slate-50 px-4 py-1.5 text-xs text-slate-600 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-400">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <Phone className="h-3.5 w-3.5 text-brand-600" />
              <span>{settings?.contact_phone || "+91 755 2400000"}</span>
            </span>
            <span className="hidden items-center gap-1.5 sm:flex">
              <Mail className="h-3.5 w-3.5 text-brand-600" />
              <span>{settings?.contact_email || "contact@myeducationindia.edu.in"}</span>
            </span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/login" className="font-semibold text-brand-600 hover:text-brand-500 dark:text-brand-400">
              ERP Portal Login →
            </Link>
          </div>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3.5 sm:px-6">
        <Link to="/" className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-white shadow-xs">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <div>
            <span className="text-base font-extrabold tracking-tight text-slate-900 dark:text-white">
              {settings?.website_title || "MY EDUCATION INDIA"}
            </span>
            <span className="block text-[10px] font-medium text-slate-500">
              {settings?.tagline || "National Flagship Campus & Assessment Center"}
            </span>
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden items-center gap-6 lg:flex">
          {navLinks.map((item) => (
            <NavLink
              key={item.url}
              to={item.url}
              className={({ isActive }) =>
                `text-xs font-semibold transition ${
                  isActive
                    ? "text-brand-600 dark:text-brand-400"
                    : "text-slate-600 hover:text-brand-600 dark:text-slate-300 dark:hover:text-white"
                }`
              }
            >
              {item.title}
            </NavLink>
          ))}
          <Link
            to="/admissions"
            className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-xs transition hover:bg-brand-500"
          >
            <span>Apply Now</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </nav>

        {/* Mobile Hamburger Button */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen((p) => !p)}
          className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden dark:text-slate-300 dark:hover:bg-slate-800"
          aria-label="Toggle navigation menu"
        >
          {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {/* Mobile Nav Dropdown */}
      {mobileMenuOpen && (
        <div className="border-t border-slate-200 bg-white px-4 py-4 lg:hidden dark:border-slate-800 dark:bg-slate-900">
          <div className="space-y-2">
            {navLinks.map((item) => (
              <Link
                key={item.url}
                to={item.url}
                onClick={() => setMobileMenuOpen(false)}
                className="block rounded-lg px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800"
              >
                {item.title}
              </Link>
            ))}
            <Link
              to="/admissions"
              onClick={() => setMobileMenuOpen(false)}
              className="mt-3 block text-center rounded-xl bg-brand-600 py-2.5 text-xs font-bold text-white"
            >
              Apply Online
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};
