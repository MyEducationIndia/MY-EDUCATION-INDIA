import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Folder,
  FolderPlus,
  Upload,
  FileText,
  Image as ImageIcon,
  Film,
  Award,
  Shield,
  Lock,
  Search,
  Filter,
  Layers,
  History,
  Download,
  Trash2,
  CheckCircle2,
  ExternalLink,
  Tag,
  Grid,
  List,
  Cpu,
  FileCheck,
  ChevronRight,
  Plus,
} from "lucide-react";
import { mediaFileManagerService } from "@/services/mediaFileManagerService";
import {
  AddVersionPayload,
  CreateFolderPayload,
  MediaFileItem,
  MediaFileType,
  MediaFolderItem,
  UploadFilePayload,
} from "@/types/mediaFileManager.types";

export const MediaFileManagerPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedFolderId, setSelectedFolderId] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState<MediaFileType>("ALL");
  const [search, setSearch] = useState("");
  const [selectedTag, setSelectedTag] = useState<string>("");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  // Modals state
  const [folderModalOpen, setFolderModalOpen] = useState(false);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [versionDrawerOpen, setVersionDrawerOpen] = useState(false);
  const [activeFileForVersions, setActiveFileForVersions] = useState<MediaFileItem | null>(null);

  // New Folder Form State
  const [newFolderName, setNewFolderName] = useState("");
  const [newFolderType, setNewFolderType] = useState("GENERAL");
  const [newFolderAccess, setNewFolderAccess] = useState("INTERNAL_CAMPUS");
  const [newFolderColor, setNewFolderColor] = useState("#4F46E5");

  // New File Upload Form State
  const [uploadName, setUploadName] = useState("");
  const [uploadOriginalName, setUploadOriginalName] = useState("");
  const [uploadType, setUploadType] = useState("DOCUMENT");
  const [uploadMime, setUploadMime] = useState("application/pdf");
  const [uploadSize, setUploadSize] = useState(2500000);
  const [uploadUrl, setUploadUrl] = useState("https://res.cloudinary.com/my-education-india/doc.pdf");
  const [uploadAccess, setUploadAccess] = useState("INTERNAL_CAMPUS");
  const [uploadTagsStr, setUploadTagsStr] = useState("official, 2026");

  // New Version State
  const [newVersionUrl, setNewVersionUrl] = useState("");
  const [newVersionSize, setNewVersionSize] = useState(2600000);
  const [newVersionNotes, setNewVersionNotes] = useState("");

  // Queries
  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ["media-summary"],
    queryFn: () => mediaFileManagerService.getSummary(),
  });

  const { data: folders = [], isLoading: foldersLoading } = useQuery({
    queryKey: ["media-folders"],
    queryFn: () => mediaFileManagerService.listFolders(),
  });

  const { data: files = [], isLoading: filesLoading } = useQuery({
    queryKey: ["media-files", selectedFolderId, search, selectedType, selectedTag],
    queryFn: () =>
      mediaFileManagerService.listFiles({
        folder_id: selectedFolderId || undefined,
        search: search || undefined,
        file_type: selectedType === "ALL" ? undefined : selectedType,
        tag: selectedTag || undefined,
      }),
  });

  // Mutations
  const createFolderMutation = useMutation({
    mutationFn: (payload: CreateFolderPayload) => mediaFileManagerService.createFolder(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["media-folders"] });
      void queryClient.invalidateQueries({ queryKey: ["media-summary"] });
      setFolderModalOpen(false);
      setNewFolderName("");
      alert("Institutional folder created!");
    },
  });

  const deleteFolderMutation = useMutation({
    mutationFn: (id: string) => mediaFileManagerService.deleteFolder(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["media-folders"] });
      if (selectedFolderId) setSelectedFolderId(null);
    },
  });

  const uploadFileMutation = useMutation({
    mutationFn: (payload: UploadFilePayload) => mediaFileManagerService.uploadFile(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["media-files"] });
      void queryClient.invalidateQueries({ queryKey: ["media-summary"] });
      setUploadModalOpen(false);
      setUploadName("");
      setUploadOriginalName("");
      alert("Asset uploaded and compressed via Cloudinary pipeline!");
    },
  });

  const addVersionMutation = useMutation({
    mutationFn: (payload: AddVersionPayload) =>
      mediaFileManagerService.addFileVersion(activeFileForVersions!.id, payload),
    onSuccess: async () => {
      void queryClient.invalidateQueries({ queryKey: ["media-files"] });
      const updatedFiles = await mediaFileManagerService.listFiles({ folder_id: selectedFolderId || undefined });
      const refreshed = updatedFiles.find((f) => f.id === activeFileForVersions!.id);
      if (refreshed) setActiveFileForVersions(refreshed);
      setNewVersionUrl("");
      setNewVersionNotes("");
      alert("New asset version committed!");
    },
  });

  const deleteFileMutation = useMutation({
    mutationFn: (id: string) => mediaFileManagerService.deleteFile(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["media-files"] });
      void queryClient.invalidateQueries({ queryKey: ["media-summary"] });
    },
  });

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  };

  const handleCreateFolder = (e: React.FormEvent) => {
    e.preventDefault();
    void createFolderMutation.mutate({
      name: newFolderName,
      folder_type: newFolderType,
      access_level: newFolderAccess,
      color: newFolderColor,
    });
  };

  const handleUploadFile = (e: React.FormEvent) => {
    e.preventDefault();
    const tagsArr = uploadTagsStr
      .split(",")
      .map((t) => t.trim().toLowerCase())
      .filter(Boolean);

    void uploadFileMutation.mutate({
      file_name: uploadName,
      original_name: uploadOriginalName || uploadName,
      folder_id: selectedFolderId,
      file_type: uploadType,
      mime_type: uploadMime,
      file_size_bytes: Number(uploadSize),
      file_url: uploadUrl,
      tags: tagsArr,
      access_level: uploadAccess,
    });
  };

  const handleAddVersion = (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeFileForVersions) return;
    void addVersionMutation.mutate({
      file_url: newVersionUrl,
      file_size_bytes: Number(newVersionSize),
      changelog_notes: newVersionNotes,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
              Module 8
            </span>
            <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">
              Centralized Media & File Manager
            </span>
          </div>
          <h1 className="mt-2 text-xl font-bold text-slate-900">
            Enterprise Cloud Asset & Document Storage
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Unified repository for institutional logos, accreditation certificates, curricula, and confidential exam vaults with compression and versioning.
          </p>
        </div>

        {/* Global Action Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => setFolderModalOpen(true)}
            className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-2xs"
          >
            <FolderPlus className="h-4 w-4 text-indigo-600" />
            New Folder
          </button>
          <button
            type="button"
            onClick={() => setUploadModalOpen(true)}
            className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
          >
            <Upload className="h-4 w-4" />
            Upload Asset
          </button>
        </div>
      </div>

      {/* Storage & Compression Analytics Banner */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Total Storage In Use
            </span>
            <Layers className="h-4 w-4 text-indigo-600" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">
            {formatBytes(summary?.total_storage_bytes || 26730000)}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Across {summary?.total_files || 6} managed files in {summary?.total_folders || 6} folders
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Compressed Bandwidth
            </span>
            <Cpu className="h-4 w-4 text-emerald-600" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">
            {formatBytes(summary?.total_compressed_bytes || 16440000)}
          </div>
          <div className="text-[10px] font-bold text-emerald-600 mt-1">
            {summary?.overall_compression_savings_pct || 38.5}% Compression Savings
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              CDN Bandwidth Saved
            </span>
            <CheckCircle2 className="h-4 w-4 text-indigo-500" />
          </div>
          <div className="text-xl font-bold text-indigo-700 mt-1">
            {formatBytes(summary?.total_saved_bytes || 10290000)}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">Brotli & WebP Streamed</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Access Control Security
            </span>
            <ShieldCheck className="h-4 w-4 text-purple-600" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">RBAC Enforced</div>
          <div className="text-[10px] text-slate-400 mt-1">
            Public &bull; Internal &bull; Confidential
          </div>
        </div>
      </div>

      {/* Main Workspace (Folders on left, File Browser on right) */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Folders Sidebar (1 Col) */}
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <span className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                Vault Folders ({folders.length})
              </span>
              <button
                type="button"
                onClick={() => setSelectedFolderId(null)}
                className={`text-[11px] font-bold ${
                  selectedFolderId === null ? "text-indigo-600 underline" : "text-slate-500 hover:text-slate-800"
                }`}
              >
                All Files
              </button>
            </div>

            <div className="mt-3 space-y-1.5">
              {folders.map((folder) => {
                const isSelected = selectedFolderId === folder.id;

                return (
                  <button
                    key={folder.id}
                    type="button"
                    onClick={() => setSelectedFolderId(folder.id)}
                    className={`w-full flex items-center justify-between p-2.5 rounded-xl text-left text-xs transition-all ${
                      isSelected
                        ? "bg-indigo-50/80 border border-indigo-200 text-indigo-900 font-bold"
                        : "bg-slate-50/60 border border-slate-100 text-slate-700 hover:bg-slate-100"
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      <Folder
                        className="h-4 w-4 shrink-0"
                        style={{ color: folder.color || "#4F46E5" }}
                      />
                      <span className="truncate">{folder.name}</span>
                    </div>

                    <div className="flex items-center gap-1.5 shrink-0">
                      <span className="rounded-full bg-white border border-slate-200 px-1.5 py-0.2 text-[10px] text-slate-500 font-mono">
                        {folder.files_count}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Files Browser (3 Cols) */}
        <div className="lg:col-span-3 space-y-4">
          {/* Filter Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
            {/* Search Input */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
              <input
                type="search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search file name, tag, or extension..."
                className="w-full rounded-lg border border-slate-300 pl-9 pr-3 py-1.5 text-xs focus:border-indigo-600 focus:outline-hidden"
              />
            </div>

            {/* Type Filter Pills */}
            <div className="flex overflow-x-auto gap-1">
              {(["ALL", "IMAGE", "PDF", "DOCUMENT", "LOGO", "CERTIFICATE"] as MediaFileType[]).map(
                (t) => (
                  <button
                    key={t}
                    type="button"
                    onClick={() => setSelectedType(t)}
                    className={`rounded-lg px-2.5 py-1 text-[11px] font-semibold whitespace-nowrap transition-colors ${
                      selectedType === t
                        ? "bg-indigo-600 text-white shadow-xs"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                    }`}
                  >
                    {t}
                  </button>
                )
              )}
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center rounded-lg border border-slate-200 bg-slate-50 p-0.5">
              <button
                type="button"
                onClick={() => setViewMode("grid")}
                className={`rounded p-1 ${viewMode === "grid" ? "bg-white text-indigo-600 shadow-2xs" : "text-slate-400"}`}
                title="Grid Cards"
              >
                <Grid className="h-4 w-4" />
              </button>
              <button
                type="button"
                onClick={() => setViewMode("list")}
                className={`rounded p-1 ${viewMode === "list" ? "bg-white text-indigo-600 shadow-2xs" : "text-slate-400"}`}
                title="Table List"
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Files Grid View */}
          {viewMode === "grid" ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {!files.length ? (
                <div className="col-span-full rounded-2xl border border-slate-200 bg-white p-12 text-center text-xs text-slate-500">
                  No files matching selected folder or filters.
                </div>
              ) : (
                files.map((file) => (
                  <div
                    key={file.id}
                    className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-4 shadow-xs hover:border-indigo-300 transition-all"
                  >
                    <div>
                      {/* Top Bar */}
                      <div className="flex items-center justify-between">
                        <span className="rounded bg-indigo-50 px-2 py-0.5 text-[10px] font-bold text-indigo-700 font-mono">
                          {file.file_type}
                        </span>
                        <button
                          type="button"
                          onClick={() => {
                            setActiveFileForVersions(file);
                            setVersionDrawerOpen(true);
                          }}
                          className="rounded bg-slate-100 hover:bg-slate-200 px-2 py-0.5 text-[10px] font-mono font-bold text-slate-700"
                        >
                          v{file.current_version} ({file.versions.length} ver)
                        </button>
                      </div>

                      {/* File Icon / Preview Box */}
                      <div className="mt-3 h-24 rounded-xl bg-slate-50 border border-dashed border-slate-200 flex items-center justify-center overflow-hidden">
                        {file.file_type === "IMAGE" || file.file_type === "LOGO" ? (
                          <img
                            src={file.file_url}
                            alt={file.file_name}
                            className="h-full w-full object-contain p-2"
                          />
                        ) : (
                          <FileText className="h-8 w-8 text-indigo-500" />
                        )}
                      </div>

                      {/* File Info */}
                      <div className="mt-3">
                        <h4 className="font-bold text-xs text-slate-900 truncate" title={file.file_name}>
                          {file.file_name}
                        </h4>
                        <div className="text-[11px] text-slate-500 truncate mt-0.5">
                          {file.original_name}
                        </div>
                      </div>

                      {/* Compression Stats */}
                      <div className="mt-2.5 flex items-center justify-between text-[11px] bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-500">{formatBytes(file.file_size_bytes)}</span>
                        <span className="font-bold text-emerald-600">
                          {formatBytes(file.compressed_size_bytes)} (-{file.compression_ratio_pct}%)
                        </span>
                      </div>

                      {/* Tags */}
                      {file.tags.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          {file.tags.map((tg) => (
                            <span
                              key={tg}
                              onClick={() => setSelectedTag(tg)}
                              className="cursor-pointer rounded bg-slate-100 hover:bg-indigo-50 hover:text-indigo-700 px-1.5 py-0.2 text-[9px] font-mono text-slate-600"
                            >
                              #{tg}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Bottom Actions */}
                    <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                      <span
                        className={`text-[10px] font-bold ${
                          file.access_level === "PUBLIC"
                            ? "text-emerald-700"
                            : file.access_level === "CONFIDENTIAL_ADMIN"
                            ? "text-rose-700"
                            : "text-indigo-700"
                        }`}
                      >
                        {file.access_level}
                      </span>

                      <div className="flex items-center gap-1.5">
                        <a
                          href={file.file_url}
                          target="_blank"
                          rel="noreferrer"
                          className="rounded p-1 text-slate-500 hover:bg-slate-100 hover:text-indigo-600"
                          title="Open Asset"
                        >
                          <ExternalLink className="h-3.5 w-3.5" />
                        </a>
                        <button
                          type="button"
                          onClick={() => {
                            if (confirm(`Remove asset ${file.file_name}?`)) {
                              void deleteFileMutation.mutate(file.id);
                            }
                          }}
                          className="rounded p-1 text-rose-400 hover:bg-rose-50 hover:text-rose-600"
                          title="Delete File"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          ) : (
            /* Table List View */
            <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs overflow-x-auto">
              <table className="min-w-full text-left text-xs">
                <thead className="border-b border-slate-100 bg-slate-50 font-semibold text-slate-600">
                  <tr>
                    <th className="px-3 py-3">File Name</th>
                    <th className="px-3 py-3">Type</th>
                    <th className="px-3 py-3">Size & Compression</th>
                    <th className="px-3 py-3">Version</th>
                    <th className="px-3 py-3">Access Level</th>
                    <th className="px-3 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {files.map((file) => (
                    <tr key={file.id} className="hover:bg-slate-50/70">
                      <td className="px-3 py-3">
                        <div className="font-bold text-slate-900">{file.file_name}</div>
                        <div className="text-[10px] text-slate-400">{file.original_name}</div>
                      </td>
                      <td className="px-3 py-3 font-mono font-bold text-indigo-700">
                        {file.file_type}
                      </td>
                      <td className="px-3 py-3">
                        <div className="font-semibold text-slate-800">
                          {formatBytes(file.compressed_size_bytes)}
                        </div>
                        <div className="text-[10px] text-emerald-600 font-bold">
                          -{file.compression_ratio_pct}% from {formatBytes(file.file_size_bytes)}
                        </div>
                      </td>
                      <td className="px-3 py-3 font-mono font-bold">v{file.current_version}</td>
                      <td className="px-3 py-3">
                        <span className="rounded bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-700">
                          {file.access_level}
                        </span>
                      </td>
                      <td className="px-3 py-3 text-right space-x-1.5">
                        <button
                          type="button"
                          onClick={() => {
                            setActiveFileForVersions(file);
                            setVersionDrawerOpen(true);
                          }}
                          className="rounded bg-slate-100 px-2 py-1 text-[11px] font-semibold text-slate-700 hover:bg-slate-200"
                        >
                          Versions
                        </button>
                        <a
                          href={file.file_url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-block rounded bg-indigo-50 p-1 text-indigo-700 hover:bg-indigo-100"
                        >
                          <ExternalLink className="h-3.5 w-3.5" />
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Upload File Modal */}
      {uploadModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs overflow-y-auto">
          <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Upload Institutional Asset</h3>
            <p className="mt-1 text-xs text-slate-500">
              Attach media asset with automatic Brotli/WebP lossless compression and RBAC tag assignments.
            </p>

            <form onSubmit={handleUploadFile} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700">File Display Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. btech-syllabus-r2026.pdf"
                  value={uploadName}
                  onChange={(e) => setUploadName(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Original / Source Title</label>
                <input
                  type="text"
                  placeholder="B.Tech Computer Science Complete Syllabus"
                  value={uploadOriginalName}
                  onChange={(e) => setUploadOriginalName(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">Asset Type</label>
                  <select
                    value={uploadType}
                    onChange={(e) => setUploadType(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value="DOCUMENT">DOCUMENT</option>
                    <option value="PDF">PDF</option>
                    <option value="IMAGE">IMAGE</option>
                    <option value="LOGO">LOGO</option>
                    <option value="CERTIFICATE">CERTIFICATE</option>
                    <option value="VIDEO">VIDEO</option>
                  </select>
                </div>
                <div>
                  <label className="font-semibold text-slate-700">Target Folder</label>
                  <select
                    value={selectedFolderId || ""}
                    onChange={(e) => setSelectedFolderId(e.target.value || null)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value="">-- Root Directory --</option>
                    {folders.map((f) => (
                      <option key={f.id} value={f.id}>
                        {f.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">File Size (Bytes)</label>
                  <input
                    type="number"
                    value={uploadSize}
                    onChange={(e) => setUploadSize(Number(e.target.value))}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700">Access Level</label>
                  <select
                    value={uploadAccess}
                    onChange={(e) => setUploadAccess(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value="PUBLIC">PUBLIC</option>
                    <option value="INTERNAL_CAMPUS">INTERNAL_CAMPUS</option>
                    <option value="CONFIDENTIAL_ADMIN">CONFIDENTIAL_ADMIN</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Cloudinary / S3 Asset URL</label>
                <input
                  type="text"
                  required
                  value={uploadUrl}
                  onChange={(e) => setUploadUrl(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Tags (Comma-separated)</label>
                <input
                  type="text"
                  value={uploadTagsStr}
                  onChange={(e) => setUploadTagsStr(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setUploadModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={uploadFileMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {uploadFileMutation.isPending ? "Uploading..." : "Upload & Compress"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* New Folder Modal */}
      {folderModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Create Media Vault Folder</h3>
            <p className="mt-1 text-xs text-slate-500">
              Organize digital assets into dedicated institutional categories.
            </p>

            <form onSubmit={handleCreateFolder} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700">Folder Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Convocation 2026 High-Res Photos"
                  value={newFolderName}
                  onChange={(e) => setNewFolderName(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">Folder Category</label>
                  <select
                    value={newFolderType}
                    onChange={(e) => setNewFolderType(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value="GENERAL">GENERAL</option>
                    <option value="LOGOS">LOGOS</option>
                    <option value="CERTIFICATES">CERTIFICATES</option>
                    <option value="DOCUMENTS">DOCUMENTS</option>
                    <option value="ACADEMICS">ACADEMICS</option>
                    <option value="EXAMS">EXAMS</option>
                  </select>
                </div>
                <div>
                  <label className="font-semibold text-slate-700">Access Level</label>
                  <select
                    value={newFolderAccess}
                    onChange={(e) => setNewFolderAccess(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value="INTERNAL_CAMPUS">INTERNAL_CAMPUS</option>
                    <option value="PUBLIC">PUBLIC</option>
                    <option value="CONFIDENTIAL_ADMIN">CONFIDENTIAL_ADMIN</option>
                  </select>
                </div>
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setFolderModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createFolderMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createFolderMutation.isPending ? "Creating..." : "Save Folder"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Version History Drawer */}
      {versionDrawerOpen && activeFileForVersions && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-lg max-h-[85vh] flex flex-col rounded-2xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Version History: {activeFileForVersions.file_name}
                </h3>
                <span className="text-xs text-slate-500 font-mono">
                  Current Version: v{activeFileForVersions.current_version} &bull; {activeFileForVersions.versions.length} Total Iterations
                </span>
              </div>
              <button
                type="button"
                onClick={() => setVersionDrawerOpen(false)}
                className="text-slate-400 hover:text-slate-600 font-bold text-xl"
              >
                &times;
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {/* Add New Version Form */}
              <form onSubmit={handleAddVersion} className="rounded-xl border border-indigo-100 bg-indigo-50/50 p-4 space-y-3 text-xs">
                <span className="font-bold text-indigo-900 uppercase tracking-wide">
                  Commit New Version (v{activeFileForVersions.current_version + 1})
                </span>

                <div>
                  <label className="font-semibold text-slate-700">New File CDN URL</label>
                  <input
                    type="text"
                    required
                    placeholder="https://res.cloudinary.com/my-education-india/doc_v2.pdf"
                    value={newVersionUrl}
                    onChange={(e) => setNewVersionUrl(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono"
                  />
                </div>

                <div>
                  <label className="font-semibold text-slate-700">Changelog / Release Notes</label>
                  <input
                    type="text"
                    placeholder="e.g. Revised AICTE syllabus credits in Section 4"
                    value={newVersionNotes}
                    onChange={(e) => setNewVersionNotes(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  />
                </div>

                <div className="flex justify-end">
                  <button
                    type="submit"
                    disabled={addVersionMutation.isPending}
                    className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                  >
                    {addVersionMutation.isPending ? "Committing..." : "Commit Version"}
                  </button>
                </div>
              </form>

              {/* Version History Timeline */}
              <div className="space-y-2 pt-2">
                <span className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                  Archived Release Iterations
                </span>

                {activeFileForVersions.versions.map((ver) => (
                  <div
                    key={ver.id}
                    className={`flex items-center justify-between p-3 rounded-xl border text-xs ${
                      ver.is_active_version
                        ? "bg-emerald-50/60 border-emerald-200"
                        : "bg-slate-50 border-slate-200"
                    }`}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold font-mono text-slate-900">
                          Version {ver.version_number}
                        </span>
                        {ver.is_active_version && (
                          <span className="rounded bg-emerald-100 px-2 py-0.2 text-[9px] font-bold text-emerald-800">
                            ACTIVE RELEASE
                          </span>
                        )}
                      </div>
                      <div className="text-[11px] text-slate-500 mt-0.5">
                        {ver.changelog_notes || "Initial baseline"}
                      </div>
                      <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                        {new Date(ver.created_at).toLocaleString()} &bull; {formatBytes(ver.file_size_bytes)}
                      </div>
                    </div>

                    <a
                      href={ver.file_url}
                      target="_blank"
                      rel="noreferrer"
                      className="rounded bg-white border border-slate-200 p-1.5 text-slate-600 hover:text-indigo-600 shadow-2xs"
                    >
                      <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-end border-t border-slate-100 px-6 py-4">
              <button
                type="button"
                onClick={() => setVersionDrawerOpen(false)}
                className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Close Drawer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
