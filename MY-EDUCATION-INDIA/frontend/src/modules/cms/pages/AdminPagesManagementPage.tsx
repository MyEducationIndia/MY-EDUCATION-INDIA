import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Edit3, Eye, FileText, CheckCircle2 } from "lucide-react";
import { cmsApi } from "../api/cmsApi";
import { VisualPageBuilder } from "../builder/VisualPageBuilder";
import { DynamicPageItem } from "../types/cms.types";
import { systemApi } from "@/modules/system/api/systemApi";

export const AdminPagesManagementPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [editingPage, setEditingPage] = useState<DynamicPageItem | null>(null);

  const { data: institutes = [] } = useQuery({ queryKey: ["systemInstitutes"], queryFn: systemApi.listInstitutes });
  const instId = institutes[0]?.id;

  const { data: pages = [], isLoading } = useQuery({
    queryKey: ["adminCmsPages"],
    queryFn: cmsApi.listAdminPages,
  });

  const createPageMutation = useMutation({
    mutationFn: (slug: string) => {
      if (!instId) throw new Error("Institute required");
      return cmsApi.createPage({
        title: slug.replace("-", " ").title(),
        slug: slug.toLowerCase(),
        status: "PUBLISHED",
        institute_id: instId,
        sections: [
          {
            section_key: "hero",
            block_type: "HERO",
            display_order: 0,
            is_visible: true,
            container_width: "FULL_WIDTH",
            padding_top: 40,
            padding_bottom: 40,
            content_payload: { heading: `${slug} Page Title` },
          },
        ],
      });
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["adminCmsPages"] });
    },
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">Website CMS Page Manager</h1>
          <p className="text-xs text-slate-500">Create, edit, visual-build, and publish fully dynamic institutional pages.</p>
        </div>
        <button
          type="button"
          onClick={() => {
            const slug = prompt("Enter new page slug (e.g. scholarships, campus-life):");
            if (slug) createPageMutation.mutate(slug);
          }}
          className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-md hover:bg-brand-500"
        >
          <Plus className="h-4 w-4" /> Create New Page
        </button>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-left text-xs dark:divide-slate-800">
            <thead>
              <tr className="bg-slate-50 uppercase text-slate-500 dark:bg-slate-950">
                <th className="px-4 py-3">Page Title</th>
                <th className="px-4 py-3">Slug</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Sections</th>
                <th className="px-4 py-3">Views</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {isLoading ? (
                <tr><td colSpan={6} className="p-6 text-center text-slate-500">Loading pages from PostgreSQL...</td></tr>
              ) : pages.length === 0 ? (
                <tr><td colSpan={6} className="p-6 text-center text-slate-500">No CMS pages provisioned yet.</td></tr>
              ) : (
                pages.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td className="px-4 py-3 font-bold text-slate-900 dark:text-white">
                      {p.title} {p.is_homepage && <span className="ml-1 rounded-sm bg-brand-50 px-1.5 py-0.5 text-[10px] text-brand-700">Homepage</span>}
                    </td>
                    <td className="px-4 py-3 font-mono text-slate-500">/{p.slug}</td>
                    <td className="px-4 py-3">
                      <span className="rounded-sm bg-emerald-50 px-2 py-0.5 font-bold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300">
                        {p.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">{p.sections.length} Blocks</td>
                    <td className="px-4 py-3 font-mono">{p.view_count}</td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          type="button"
                          onClick={() => setEditingPage(p)}
                          className="rounded-lg border border-slate-300 bg-white px-2.5 py-1 font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
                        >
                          Visual Builder
                        </button>
                        <a
                          href={`/${p.slug === "home" ? "" : p.slug}`}
                          target="_blank"
                          rel="noreferrer"
                          className="p-1 text-slate-400 hover:text-brand-600"
                        >
                          <Eye className="h-4 w-4" />
                        </a>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {editingPage && (
        <VisualPageBuilder
          initialSections={editingPage.sections}
          onSave={async (sections) => {
            await cmsApi.updatePage(editingPage.id, { sections });
            void queryClient.invalidateQueries({ queryKey: ["adminCmsPages"] });
          }}
          onClose={() => setEditingPage(null)}
        />
      )}
    </div>
  );
};
