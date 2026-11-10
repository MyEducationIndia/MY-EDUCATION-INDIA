import React from "react";
import { Link } from "react-router-dom";
import { ShieldCheck, MapPin, Phone, Mail } from "lucide-react";
import { WebsiteSettingsRecord } from "../types/cms.types";

interface PublicFooterProps {
  settings?: WebsiteSettingsRecord | null;
}

export const PublicFooter: React.FC<PublicFooterProps> = ({ settings }) => {
  return (
    <footer className="border-t border-slate-200 bg-slate-950 text-slate-400 dark:border-slate-800">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          <div>
            <div className="flex items-center gap-3 text-white">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-600">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <span className="text-base font-extrabold tracking-tight">
                {settings?.website_title || "MY EDUCATION INDIA"}
              </span>
            </div>
            <p className="mt-3 text-xs leading-relaxed text-slate-400">
              {settings?.tagline || "Leading digital education platform, CBT examination engine, and autonomous university accreditation."}
            </p>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Quick Links</h3>
            <ul className="mt-3 space-y-2 text-xs">
              <li><Link to="/about" className="hover:text-white">About Institute</Link></li>
              <li><Link to="/courses" className="hover:text-white">Academic Programs</Link></li>
              <li><Link to="/admissions" className="hover:text-white">Online Admissions</Link></li>
              <li><Link to="/gallery" className="hover:text-white">Campus Gallery</Link></li>
              <li><Link to="/news" className="hover:text-white">News & Circulars</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Institutional Policies</h3>
            <ul className="mt-3 space-y-2 text-xs">
              <li><Link to="/privacy-policy" className="hover:text-white">Privacy Policy</Link></li>
              <li><Link to="/terms" className="hover:text-white">Terms & Conditions</Link></li>
              <li><Link to="/refund-policy" className="hover:text-white">Fee Refund Policy</Link></li>
              <li><Link to="/contact" className="hover:text-white">Grievance Redressal</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Contact & Campus</h3>
            <div className="mt-3 space-y-2 text-xs text-slate-400">
              <p className="flex items-start gap-2">
                <MapPin className="h-4 w-4 shrink-0 text-brand-400 mt-0.5" />
                <span>{settings?.address_display || "Main Campus, Institutional Area, Bhopal, MP 462011"}</span>
              </p>
              <p className="flex items-center gap-2">
                <Phone className="h-4 w-4 shrink-0 text-brand-400" />
                <span>{settings?.contact_phone || "+91 755 2400000"}</span>
              </p>
              <p className="flex items-center gap-2">
                <Mail className="h-4 w-4 shrink-0 text-brand-400" />
                <span>{settings?.contact_email || "contact@myeducationindia.edu.in"}</span>
              </p>
            </div>
          </div>
        </div>

        <div className="mt-10 border-t border-slate-800 pt-6 text-center text-xs text-slate-500">
          <p>{settings?.footer_text || "© 2026 MY EDUCATION INDIA ERP V2. All rights reserved. Powered by PostgreSQL CMS Engine."}</p>
        </div>
      </div>
    </footer>
  );
};
