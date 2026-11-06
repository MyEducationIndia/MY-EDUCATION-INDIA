import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Building2, Layers, CheckCircle2, Lock, Sliders } from "lucide-react";
import { instituteService } from "@/services/instituteService";
import { StatusBadge } from "@/components/ui/StatusBadge";

export const SuperAdminDashboardPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");

  const { data: institutes = [], isLoading } = useQuery({
    queryKey: ["institutes"],
    queryFn: instituteService.listInstitutes,
  });

  const activeInstitute = institutes[0] || null;

  const toggleMutation = useMutation({
    mutationFn: (params: {
      instituteId: string;
      moduleKey: string;
      isEnabled: boolean;
    }) =>
      instituteService.toggleModule(
        params.instituteId,
        params.moduleKey,
        params.isEnabled
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["institutes"] });
    },
  });

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center text-sm text-slate-600">
        Loading institute governance registry from Neon PostgreSQL...
      </div>
    );
  }

  if (!activeInstitute) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">
        <h2 className="text-base font-bold text-slate-900">
          No Institute Provisioned Yet
        </h2>
        <p className="mt-1 text-sm text-slate-600">
          Run the database seed script or create your primary institute via POST /api/v1/institutes.
        </p>
      </div>
    );
  }

  const modules = activeInstitute.module_configs || [];
  const categories = [
    "ALL",
    ...Array.from(new Set(modules.map((m) => m.category))),
  ];
  const filteredModules =
    selectedCategory === "ALL"
      ? modules
      : modules.filter((m) => m.category === selectedCategory);

  const enabledCount = modules.filter((m) => m.is_enabled).length;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Primary Institute
            </span>
            <Building2 className="h-5 w-5 text-brand-600" />
          </div>
          <p className="mt-2 text-lg font-bold text-slate-900">
            {activeInstitute.name}
          </p>
          <p className="mt-0.5 text-xs text-slate-500">
            Code: {activeInstitute.code} • {activeInstitute.city},{" "}
            {activeInstitute.state}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Enabled Modules
            </span>
            <Layers className="h-5 w-5 text-emerald-600" />
          </div>
          <p className="mt-2 text-2xl font-extrabold text-slate-900">
            {enabledCount} / {modules.length}
          </p>
          <p className="mt-0.5 text-xs text-slate-500">
            Real-time PostgreSQL module state
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Branding Theme
            </span>
            <Sliders className="h-5 w-5 text-accent-600" />
          </div>
          <div className="mt-3 flex items-center gap-3">
            <div className="flex items-center gap-2">
              <span
                className="h-6 w-6 rounded-full border border-slate-300"
                style={{ backgroundColor: activeInstitute.primary_color_hex }}
              />
              <span className="text-xs font-mono text-slate-700">
                {activeInstitute.primary_color_hex}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span
                className="h-6 w-6 rounded-full border border-slate-300"
                style={{ backgroundColor: activeInstitute.secondary_color_hex }}
              />
              <span className="text-xs font-mono text-slate-700">
                {activeInstitute.secondary_color_hex}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs sm:p-6">
        <div className="flex flex-col justify-between gap-4 border-b border-slate-200 pb-4 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-base font-bold text-slate-900">
              Enterprise Module Control Matrix (37 Subsystems)
            </h2>
            <p className="text-xs text-slate-500">
              Enable or disable individual platform modules and subdomain services in real time.
            </p>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {categories.map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => setSelectedCategory(cat)}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
                  selectedCategory === cat
                    ? "bg-brand-600 text-white"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filteredModules.map((mod) => (
            <div
              key={mod.id}
              className="flex flex-col justify-between rounded-xl border border-slate-200 bg-slate-50/60 p-4 transition hover:border-slate-300 hover:bg-white"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      {mod.display_name}
                    </h3>
                    <span className="mt-0.5 inline-block text-[11px] font-medium text-brand-600">
                      {mod.subdomain}.myeducationindia.edu.in • {mod.category}
                    </span>
                  </div>
                  <StatusBadge active={mod.is_enabled} />
                </div>
                <p className="mt-2 text-xs leading-relaxed text-slate-600">
                  {mod.description}
                </p>
              </div>

              <div className="mt-4 flex items-center justify-between border-t border-slate-200/80 pt-3">
                {mod.is_core_locked ? (
                  <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-slate-500">
                    <Lock className="h-3.5 w-3.5" /> Core System Locked
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-[11px] text-slate-500">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />{" "}
                    Configurable
                  </span>
                )}

                <button
                  type="button"
                  disabled={mod.is_core_locked || toggleMutation.isPending}
                  onClick={() =>
                    toggleMutation.mutate({
                      instituteId: activeInstitute.id,
                      moduleKey: mod.module_key,
                      isEnabled: !mod.is_enabled,
                    })
                  }
                  className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition disabled:cursor-not-allowed disabled:opacity-50 ${
                    mod.is_enabled
                      ? "border border-slate-300 bg-white text-slate-700 hover:bg-slate-100"
                      : "bg-brand-600 text-white hover:bg-brand-500"
                  }`}
                >
                  {mod.is_enabled ? "Disable Module" : "Enable Module"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
