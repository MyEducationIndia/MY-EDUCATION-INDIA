import React from "react";
import { Link } from "react-router-dom";
import {
  ShieldCheck,
  Mail,
  Phone,
  MapPin,
  ExternalLink,
  ArrowRight,
  Globe,
} from "lucide-react";
import {
  WebsiteNavigationMenu,
  WebsiteSettings,
  WebsiteSocialLink,
} from "@/types/website.types";

interface PublicFooterProps {
  settings: WebsiteSettings;
  socialLinks: WebsiteSocialLink[];
}

export const PublicFooter: React.FC<PublicFooterProps> = ({
  settings,
  socialLinks,
}) => {
  return (
    <footer className="border-t border-slate-200 bg-white pt-16 pb-8 text-xs text-slate-500 font-sans">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-10 md:grid-cols-4 pb-12 border-b border-slate-200">
          {/* Column 1: Institutional Profile */}
          <div className="space-y-4 md:col-span-1">
            <Link to="/" className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-white shadow-xs">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm font-black tracking-tight text-slate-900 leading-tight">
                  {settings.site_title}
                </p>
                <p className="text-[10px] font-semibold text-brand-700 uppercase tracking-wider">
                  Flagship Campus
                </p>
              </div>
            </Link>

            <p className="text-xs text-slate-600 leading-relaxed">
              {settings.meta_description}
            </p>

            {/* Social Icons */}
            {socialLinks && socialLinks.length > 0 && (
              <div className="flex flex-wrap items-center gap-2 pt-2">
                {socialLinks.map((soc) => (
                  <a
                    key={soc.id}
                    href={soc.url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-slate-600 hover:border-brand-300 hover:bg-brand-50 hover:text-brand-700 transition capitalize"
                    title={soc.platform}
                  >
                    <Globe className="h-4 w-4" />
                  </a>
                ))}
              </div>
            )}
          </div>

          {/* Column 2: Quick Links */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 mb-4">
              Institutional Portals
            </h4>
            <ul className="space-y-2.5">
              <li>
                <Link to={settings.header_login_route || "/login"} className="hover:text-brand-600 transition flex items-center gap-1.5">
                  <span>Student Self-Service Portal</span>
                </Link>
              </li>
              <li>
                <Link to={settings.header_login_route || "/login"} className="hover:text-brand-600 transition flex items-center gap-1.5">
                  <span>Faculty & Dean Portal</span>
                </Link>
              </li>
              <li>
                <Link to={settings.header_login_route || "/login"} className="hover:text-brand-600 transition flex items-center gap-1.5">
                  <span>Administrative ERP Command Center</span>
                </Link>
              </li>
              <li>
                <Link to="/admissions/apply" className="hover:text-brand-600 transition flex items-center gap-1.5">
                  <span>Online Admission Application 2026</span>
                </Link>
              </li>
              <li>
                <Link to="/verify" className="hover:text-brand-600 transition flex items-center gap-1.5">
                  <span>Document & Degree Verification</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Campus Coordinates */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 mb-4">
              Flagship Campus Location
            </h4>
            <div className="space-y-3">
              <div className="flex items-start gap-2.5">
                <MapPin className="h-4 w-4 text-brand-600 shrink-0 mt-0.5" />
                <span className="leading-relaxed">{settings.contact_address}</span>
              </div>
              <div className="flex items-center gap-2.5">
                <Phone className="h-4 w-4 text-brand-600 shrink-0" />
                <span>{settings.contact_phone}</span>
              </div>
              <div className="flex items-center gap-2.5">
                <Mail className="h-4 w-4 text-brand-600 shrink-0" />
                <span>{settings.contact_email}</span>
              </div>
            </div>
          </div>

          {/* Column 4: Newsletter & Single Login CTA */}
          <div className="space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900">
              Institutional Access
            </h4>
            <p className="text-xs text-slate-500">
              Authorized access point for scholars, professors, and administrative personnel.
            </p>
            <Link
              to={settings.header_login_route || "/login"}
              className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
            >
              <span>{settings.header_login_button_text || "Login"}</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
        </div>

        {/* Bottom Bar: Copyright & Compliance */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-slate-400 text-[11px]">
          <p>© {new Date().getFullYear()} {settings.site_title}. All rights reserved.</p>
          <div className="flex items-center gap-4">
            <Link to="/privacy" className="hover:text-slate-600">Privacy Policy</Link>
            <Link to="/terms" className="hover:text-slate-600">Terms of Use</Link>
            <Link to="/refund-policy" className="hover:text-slate-600">Refund Policy</Link>
            <span>•</span>
            <span className="font-semibold text-slate-500">ERP V2 Architecture</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
