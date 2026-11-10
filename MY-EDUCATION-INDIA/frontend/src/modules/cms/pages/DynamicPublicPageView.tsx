import React from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { cmsApi } from "../api/cmsApi";
import { PublicHeader } from "../components/PublicHeader";
import { PublicFooter } from "../components/PublicFooter";
import { DynamicSectionRenderer } from "../components/DynamicSectionRenderer";
import { systemApi } from "@/modules/system/api/systemApi";

export const DynamicPublicPageView: React.FC = () => {
  const { slug } = useParams<{ slug?: string }>();
  const activeSlug = slug || "home";

  const { data: institutes = [] } = useQuery({ queryKey: ["systemInstitutes"], queryFn: systemApi.listInstitutes });
  const instId = institutes[0]?.id;

  const { data: page, isLoading } = useQuery({
    queryKey: ["cmsPage", activeSlug, instId],
    queryFn: () => {
      if (!instId) return Promise.resolve(null);
      if (activeSlug === "home") {
        return cmsApi.getHomepage(instId).catch(() => cmsApi.getPageBySlug("home", instId));
      }
      return cmsApi.getPageBySlug(activeSlug, instId);
    },
    enabled: Boolean(instId),
  });

  const { data: settings } = useQuery({
    queryKey: ["websiteSettings", instId],
    queryFn: () => (instId ? cmsApi.getWebsiteSettings(instId) : Promise.resolve(null)),
    enabled: Boolean(instId),
  });

  const { data: menu } = useQuery({
    queryKey: ["headerMenu", instId],
    queryFn: () => (instId ? cmsApi.getMenu("HEADER_MENU", instId) : Promise.resolve(null)),
    enabled: Boolean(instId),
  });

  return (
    <div className="flex min-h-screen flex-col bg-white text-slate-900 selection:bg-brand-600 selection:text-white dark:bg-slate-950 dark:text-slate-100">
      <PublicHeader settings={settings} menu={menu} />

      <main className="flex-1">
        {isLoading ? (
          <div className="flex h-96 items-center justify-center">
            <div className="flex flex-col items-center gap-3">
              <div className="h-10 w-10 animate-spin rounded-full border-4 border-brand-600 border-t-transparent" />
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Rendering Page from PostgreSQL...</p>
            </div>
          </div>
        ) : !page ? (
          <div className="py-24 text-center">
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Page Not Found (404)</h1>
            <p className="mt-2 text-xs text-slate-500">The requested page "{activeSlug}" is not published yet.</p>
          </div>
        ) : (
          <div>
            {page.sections.map((sec) => (
              <DynamicSectionRenderer key={sec.id || sec.section_key} section={sec} />
            ))}
          </div>
        )}
      </main>

      <PublicFooter settings={settings} />
    </div>
  );
};
