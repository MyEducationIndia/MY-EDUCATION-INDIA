import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Building2, Globe, Mail, Phone, MapPin } from "lucide-react";
import { systemApi } from "../api/systemApi";

export const InstituteManagementPage: React.FC = () => {
  const { data: institutes = [], isLoading } = useQuery({
    queryKey: ["systemInstitutes"],
    queryFn: systemApi.listInstitutes,
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">
            Multi-Institute Management
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Enterprise campus governance, franchise entities, and institutional credentials in Neon PostgreSQL.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {isLoading ? (
          <p className="text-xs text-slate-500">Loading institutes...</p>
        ) : (
          institutes.map((inst) => (
            <div
              key={inst.id}
              className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-400">
                    <Building2 className="h-6 w-6" />
                  </div>
                  <div>
                    <h2 className="text-sm font-bold text-slate-900 dark:text-white">
                      {inst.name}
                    </h2>
                    <span className="rounded-sm bg-slate-100 px-2 py-0.5 font-mono text-[11px] text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                      Code: {inst.code}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-1.5">
                  <span
                    className="h-4 w-4 rounded-full border border-slate-300"
                    style={{ backgroundColor: inst.primary_color_hex }}
                    title={`Primary: ${inst.primary_color_hex}`}
                  />
                  <span
                    className="h-4 w-4 rounded-full border border-slate-300"
                    style={{ backgroundColor: inst.secondary_color_hex }}
                    title={`Secondary: ${inst.secondary_color_hex}`}
                  />
                </div>
              </div>

              {inst.tagline && (
                <p className="mt-2 text-xs italic text-slate-500 dark:text-slate-400">
                  "{inst.tagline}"
                </p>
              )}

              <div className="mt-4 space-y-1.5 border-t border-slate-100 pt-3 text-xs text-slate-600 dark:border-slate-800 dark:text-slate-400">
                <div className="flex items-center gap-2">
                  <MapPin className="h-3.5 w-3.5 text-slate-400" />
                  <span>{inst.address_line1}, {inst.city}, {inst.state} - {inst.postal_code}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Mail className="h-3.5 w-3.5 text-slate-400" />
                  <span>{inst.official_email}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="h-3.5 w-3.5 text-slate-400" />
                  <span>{inst.official_phone}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
