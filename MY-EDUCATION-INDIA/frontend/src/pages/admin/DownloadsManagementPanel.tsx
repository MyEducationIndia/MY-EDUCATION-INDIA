import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Download,
  FileText,
  Plus,
  Trash2,
  ExternalLink,
  CheckCircle2,
  Layers,
  TrendingUp,
  Tag,
  Pin,
  Sparkles,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsDownloadCategory,
  CmsDownloadCategoryCreateRequest,
  CmsDownloadDocument,
  CmsDownloadDocumentCreateRequest,
} from "@/types/website.types";

interface DownloadsManagementPanelProps {
  initialSubTab?: "categories" | "documents";
}

export const DownloadsManagementPanel: React.FC<DownloadsManagementPanelProps> = ({
  initialSubTab = "documents",
}) => {
  const queryClient = useQueryClient();
  const [subTab, setSubTab] = useState<"categories" | "documents">(initialSubTab);
  const [selectedCategoryId, setSelectedCategoryId] = useState<string>("");
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Queries
  const { data: categories = [] } = useQuery({
    queryKey: ["admin-download-categories"],
    queryFn: websiteService.listAdminDownloadCategories,
  });

  const activeCategoryId = selectedCategoryId || (categories[0]?.id ?? "");

  const { data: documents = [] } = useQuery({
    queryKey: ["admin-download-documents", activeCategoryId],
    queryFn: () => websiteService.listAdminDownloadDocuments(activeCategoryId || undefined),
    enabled: true,
  });

  // Category Form State
  const [newCatName, setNewCatName] = useState("");
  const [newCatSlug, setNewCatSlug] = useState("");
  const [newCatDesc, setNewCatDesc] = useState("");
  const [newCatIcon, setNewCatIcon] = useState("FileText");

  // Document Form State
  const [newDocTitle, setNewDocTitle] = useState("");
  const [newDocSlug, setNewDocSlug] = useState("");
  const [newDocDesc, setNewDocDesc] = useState("");
  const [newDocAudience, setNewDocAudience] = useState("ALL");
  const [newDocProgram, setNewDocProgram] = useState("ALL_PROGRAMS");
  const [newDocYear, setNewDocYear] = useState("2026-2027");
  const [newDocUrl, setNewDocUrl] = useState("");
  const [newDocSize, setNewDocSize] = useState("2.5 MB");
  const [newDocFormat, setNewDocFormat] = useState("PDF");
  const [newDocVersion, setNewDocVersion] = useState("v1.0");
  const [newDocPinned, setNewDocPinned] = useState(false);
  const [newDocFeatured, setNewDocFeatured] = useState(false);

  // Mutations: Category
  const createCategoryMutation = useMutation({
    mutationFn: websiteService.createAdminDownloadCategory,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-download-categories"] });
      void queryClient.invalidateQueries({ queryKey: ["public-downloads-bundle"] });
      setStatusMessage("Download category created successfully.");
      setTimeout(() => setStatusMessage(null), 3500);
      setNewCatName("");
      setNewCatSlug("");
      setNewCatDesc("");
    },
  });

  const deleteCategoryMutation = useMutation({
    mutationFn: websiteService.deleteAdminDownloadCategory,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-download-categories"] });
      void queryClient.invalidateQueries({ queryKey: ["public-downloads-bundle"] });
      setStatusMessage("Download category removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Mutations: Document
  const createDocumentMutation = useMutation({
    mutationFn: websiteService.createAdminDownloadDocument,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-download-documents"] });
      void queryClient.invalidateQueries({ queryKey: ["admin-download-categories"] });
      void queryClient.invalidateQueries({ queryKey: ["public-downloads-bundle"] });
      setStatusMessage("Download document published to vault.");
      setTimeout(() => setStatusMessage(null), 3500);
      setNewDocTitle("");
      setNewDocSlug("");
      setNewDocDesc("");
      setNewDocUrl("");
      setNewDocPinned(false);
      setNewDocFeatured(false);
    },
  });

  const deleteDocumentMutation = useMutation({
    mutationFn: websiteService.deleteAdminDownloadDocument,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-download-documents"] });
      void queryClient.invalidateQueries({ queryKey: ["admin-download-categories"] });
      void queryClient.invalidateQueries({ queryKey: ["public-downloads-bundle"] });
      setStatusMessage("Document removed from vault.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Handlers
  const handleCreateCategory = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCatName.trim()) return;
    const slug =
      newCatSlug.trim().toLowerCase() ||
      newCatName.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-");

    createCategoryMutation.mutate({
      name: newCatName.trim(),
      slug,
      description: newCatDesc.trim() || null,
      icon_name: newCatIcon,
      display_order: categories.length + 1,
      is_active: true,
    });
  };

  const handleCreateDocument = (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeCategoryId) {
      alert("Please select a category first.");
      return;
    }
    if (!newDocTitle.trim() || !newDocDesc.trim() || !newDocUrl.trim()) {
      alert("Please fill in title, description, and file URL.");
      return;
    }

    const slug =
      newDocSlug.trim().toLowerCase() ||
      newDocTitle.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-");

    createDocumentMutation.mutate({
      category_id: activeCategoryId,
      title: newDocTitle.trim(),
      slug,
      description: newDocDesc.trim(),
      target_audience: newDocAudience,
      applicable_program: newDocProgram,
      academic_year: newDocYear,
      file_url: newDocUrl.trim(),
      file_size_formatted: newDocSize.trim(),
      file_format: newDocFormat,
      version: newDocVersion.trim() || "v1.0",
      is_pinned: newDocPinned,
      is_featured: newDocFeatured,
      display_order: documents.length + 1,
      is_active: true,
    });
  };

  return (
    <div className="space-y-6">
      {/* Status banner */}
      {statusMessage && (
        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-xs font-semibold text-emerald-800 animate-in fade-in">
          <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Subtab Navigation */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setSubTab("documents")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              subTab === "documents"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <FileText className="h-4 w-4" />
            <span>Document Vault ({documents.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setSubTab("categories")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              subTab === "categories"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Layers className="h-4 w-4" />
            <span>Download Categories ({categories.length})</span>
          </button>
        </div>

        <a
          href="/downloads"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-600 hover:text-brand-700"
        >
          <span>Live Downloads Center</span>
          <ExternalLink className="h-3.5 w-3.5" />
        </a>
      </div>

      {/* SUBTAB 1: DOCUMENTS */}
      {subTab === "documents" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Create Document Form */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Plus className="h-4 w-4 text-brand-600" />
              <span>Register Official Document / Asset</span>
            </h2>

            <form onSubmit={handleCreateDocument} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Category</label>
                <select
                  value={activeCategoryId}
                  onChange={(e) => setSelectedCategoryId(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  {categories.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.document_count} items)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Document Title</label>
                <input
                  type="text"
                  required
                  value={newDocTitle}
                  onChange={(e) => setNewDocTitle(e.target.value)}
                  placeholder="e.g. End-Semester Examination Time Table (Even Sem 2025-26)"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">URL Slug</label>
                <input
                  type="text"
                  value={newDocSlug}
                  onChange={(e) => setNewDocSlug(e.target.value)}
                  placeholder="e.g. end-sem-timetable-2026 (auto-generated if empty)"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Target Audience</label>
                  <select
                    value={newDocAudience}
                    onChange={(e) => setNewDocAudience(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="ALL">All Visitors</option>
                    <option value="STUDENTS">Current Students</option>
                    <option value="PROSPECTIVE">Prospective Applicants</option>
                    <option value="FACULTY">Faculty & Staff</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Applicable Program</label>
                  <select
                    value={newDocProgram}
                    onChange={(e) => setNewDocProgram(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="ALL_PROGRAMS">All Programs</option>
                    <option value="BTECH-CSE">B.Tech CSE</option>
                    <option value="BTECH-AI-DS">B.Tech AI & Data Science</option>
                    <option value="MTECH-CSE">M.Tech CSE</option>
                    <option value="BCA-HONS">BCA (Honours)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Format</label>
                  <select
                    value={newDocFormat}
                    onChange={(e) => setNewDocFormat(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="PDF">PDF</option>
                    <option value="DOCX">DOCX</option>
                    <option value="XLSX">XLSX</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">File Size</label>
                  <input
                    type="text"
                    value={newDocSize}
                    onChange={(e) => setNewDocSize(e.target.value)}
                    placeholder="2.5 MB"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Version</label>
                  <input
                    type="text"
                    value={newDocVersion}
                    onChange={(e) => setNewDocVersion(e.target.value)}
                    placeholder="v1.0"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Direct Download URL / PDF Link</label>
                <input
                  type="url"
                  required
                  value={newDocUrl}
                  onChange={(e) => setNewDocUrl(e.target.value)}
                  placeholder="https://myeducation.in/downloads/..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Document Summary</label>
                <textarea
                  rows={3}
                  required
                  value={newDocDesc}
                  onChange={(e) => setNewDocDesc(e.target.value)}
                  placeholder="Outline key information, dates, and instructions contained in this asset..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center gap-4">
                <div className="flex items-center gap-1.5">
                  <input
                    type="checkbox"
                    id="doc-pinned"
                    checked={newDocPinned}
                    onChange={(e) => setNewDocPinned(e.target.checked)}
                    className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
                  />
                  <label htmlFor="doc-pinned" className="text-xs font-medium text-slate-700">
                    Pin to Flagship Showcase
                  </label>
                </div>
                <div className="flex items-center gap-1.5">
                  <input
                    type="checkbox"
                    id="doc-featured"
                    checked={newDocFeatured}
                    onChange={(e) => setNewDocFeatured(e.target.checked)}
                    className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
                  />
                  <label htmlFor="doc-featured" className="text-xs font-medium text-slate-700">
                    Featured
                  </label>
                </div>
              </div>

              <button
                type="submit"
                disabled={createDocumentMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>{createDocumentMutation.isPending ? "Uploading..." : "Publish to Vault"}</span>
              </button>
            </form>
          </div>

          {/* Documents Table */}
          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Managed Documents ({documents.length})</span>
              <span className="text-xs font-normal text-slate-500">Live PostgreSQL Database</span>
            </h2>

            <div className="mt-4 space-y-3">
              {documents.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-start justify-between rounded-xl border border-slate-200 bg-white p-4 shadow-2xs hover:border-brand-200 transition-all"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span
                        className={`rounded-md px-2 py-0.5 text-[10px] font-extrabold uppercase ${
                          doc.file_format === "PDF"
                            ? "bg-rose-100 text-rose-700"
                            : "bg-blue-100 text-blue-700"
                        }`}
                      >
                        {doc.file_format}
                      </span>
                      <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-700">
                        {doc.file_size_formatted}
                      </span>
                      {doc.is_pinned && (
                        <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[9px] font-extrabold text-amber-800">
                          PINNED
                        </span>
                      )}
                      <h4 className="text-xs font-bold text-slate-900">{doc.title}</h4>
                    </div>

                    <p className="text-xs text-slate-600 line-clamp-1">{doc.description}</p>

                    <div className="flex items-center gap-4 text-[11px] text-slate-500">
                      <span>Program: {doc.applicable_program}</span>
                      <span>•</span>
                      <span>AY: {doc.academic_year}</span>
                      <span>•</span>
                      <span>Version: {doc.version}</span>
                      <span>•</span>
                      <span className="text-emerald-600 font-semibold flex items-center gap-1">
                        <TrendingUp className="h-3 w-3" />
                        {doc.download_count} downloads
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0 ml-4">
                    <a
                      href={doc.file_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-1 text-slate-400 hover:text-brand-600"
                      title="Open file"
                    >
                      <ExternalLink className="h-4 w-4" />
                    </a>
                    <button
                      onClick={() => {
                        if (confirm(`Remove "${doc.title}" from the official downloads repository?`)) {
                          deleteDocumentMutation.mutate(doc.id);
                        }
                      }}
                      className="p-1 text-slate-400 hover:text-red-600"
                      title="Delete document"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}

              {documents.length === 0 && (
                <div className="py-12 text-center text-slate-400 text-xs">
                  No documents found for this category. Use the form on the left to add a prospectus, syllabus, or form.
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* SUBTAB 2: CATEGORIES */}
      {subTab === "categories" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Create Category Form */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Plus className="h-4 w-4 text-brand-600" />
              <span>Create Download Category</span>
            </h2>

            <form onSubmit={handleCreateCategory} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Category Name</label>
                <input
                  type="text"
                  required
                  value={newCatName}
                  onChange={(e) => setNewCatName(e.target.value)}
                  placeholder="e.g. Examination Regulations"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">URL Slug</label>
                <input
                  type="text"
                  value={newCatSlug}
                  onChange={(e) => setNewCatSlug(e.target.value)}
                  placeholder="e.g. exam-regulations (auto-generated if empty)"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Icon Identifier</label>
                <select
                  value={newCatIcon}
                  onChange={(e) => setNewCatIcon(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  <option value="FileText">FileText (General Syllabi)</option>
                  <option value="BookOpen">BookOpen (Prospectus)</option>
                  <option value="ClipboardList">ClipboardList (Forms)</option>
                  <option value="Clock">Clock (Time Tables)</option>
                  <option value="Calendar">Calendar (Calendars)</option>
                  <option value="Award">Award (Circulars / Accreditations)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Description</label>
                <textarea
                  rows={3}
                  value={newCatDesc}
                  onChange={(e) => setNewCatDesc(e.target.value)}
                  placeholder="Scope of documents in this category..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createCategoryMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Category</span>
              </button>
            </form>
          </div>

          {/* Categories List */}
          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Configured Categories ({categories.length})</span>
            </h2>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              {categories.map((c) => (
                <div
                  key={c.id}
                  className="flex flex-col justify-between rounded-xl border border-slate-200 bg-white p-4 shadow-2xs hover:border-brand-200 transition-all"
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="rounded-md bg-brand-100 px-2 py-0.5 text-[10px] font-bold text-brand-700">
                        {c.slug}
                      </span>
                      <span className="text-xs font-semibold text-slate-500">
                        {c.document_count} files
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-slate-900">{c.name}</h3>
                    {c.description && (
                      <p className="mt-1 text-xs text-slate-500 line-clamp-2">{c.description}</p>
                    )}
                  </div>

                  <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-2 text-xs">
                    <button
                      onClick={() => {
                        setSelectedCategoryId(c.id);
                        setSubTab("documents");
                      }}
                      className="font-bold text-brand-600 hover:underline"
                    >
                      View Documents
                    </button>
                    <button
                      onClick={() => {
                        if (confirm(`Delete category "${c.name}" and all its documents?`)) {
                          deleteCategoryMutation.mutate(c.id);
                        }
                      }}
                      className="text-red-500 hover:text-red-700 p-1"
                      title="Delete category"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
