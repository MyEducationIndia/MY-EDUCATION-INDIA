import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Camera,
  Film,
  Plus,
  Trash2,
  ExternalLink,
  CheckCircle2,
  Clock,
  Sparkles,
  Layers,
  Image as ImageIcon,
  Play,
  Calendar,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsGalleryAlbum,
  CmsGalleryAlbumCreateRequest,
  CmsGalleryMedia,
  CmsGalleryMediaCreateRequest,
} from "@/types/website.types";

interface GalleryManagementPanelProps {
  initialSubTab?: "albums" | "media";
}

export const GalleryManagementPanel: React.FC<GalleryManagementPanelProps> = ({
  initialSubTab = "albums",
}) => {
  const queryClient = useQueryClient();
  const [subTab, setSubTab] = useState<"albums" | "media">(initialSubTab);
  const [selectedAlbumId, setSelectedAlbumId] = useState<string>("");
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Queries
  const { data: albums = [] } = useQuery({
    queryKey: ["admin-gallery-albums"],
    queryFn: websiteService.listAdminGalleryAlbums,
  });

  const activeAlbumId = selectedAlbumId || (albums[0]?.id ?? "");

  const { data: mediaItems = [] } = useQuery({
    queryKey: ["admin-gallery-media", activeAlbumId],
    queryFn: () => websiteService.listAdminGalleryMedia(activeAlbumId),
    enabled: !!activeAlbumId,
  });

  // Album Form State
  const [newAlbumTitle, setNewAlbumTitle] = useState("");
  const [newAlbumSlug, setNewAlbumSlug] = useState("");
  const [newAlbumCategory, setNewAlbumCategory] = useState("CAMPUS_LIFE");
  const [newAlbumDesc, setNewAlbumDesc] = useState("");
  const [newAlbumCover, setNewAlbumCover] = useState("");
  const [newAlbumYear, setNewAlbumYear] = useState("2025-2026");
  const [newAlbumDate, setNewAlbumDate] = useState("");
  const [newAlbumFeatured, setNewAlbumFeatured] = useState(false);

  // Media Form State
  const [newMediaTitle, setNewMediaTitle] = useState("");
  const [newMediaType, setNewMediaType] = useState<"IMAGE" | "VIDEO">("IMAGE");
  const [newMediaCaption, setNewMediaCaption] = useState("");
  const [newMediaUrl, setNewMediaUrl] = useState("");
  const [newMediaVideoId, setNewMediaVideoId] = useState("");
  const [newMediaIsCover, setNewMediaIsCover] = useState(false);

  // Mutations
  const createAlbumMutation = useMutation({
    mutationFn: websiteService.createAdminGalleryAlbum,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-gallery-albums"] });
      void queryClient.invalidateQueries({ queryKey: ["public-gallery-bundle"] });
      setStatusMessage("Curated gallery album created successfully.");
      setTimeout(() => setStatusMessage(null), 3500);
      setNewAlbumTitle("");
      setNewAlbumSlug("");
      setNewAlbumDesc("");
      setNewAlbumCover("");
      setNewAlbumDate("");
      setNewAlbumFeatured(false);
    },
  });

  const deleteAlbumMutation = useMutation({
    mutationFn: websiteService.deleteAdminGalleryAlbum,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-gallery-albums"] });
      void queryClient.invalidateQueries({ queryKey: ["public-gallery-bundle"] });
      setStatusMessage("Gallery album removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createMediaMutation = useMutation({
    mutationFn: websiteService.createAdminGalleryMedia,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-gallery-media", activeAlbumId] });
      void queryClient.invalidateQueries({ queryKey: ["admin-gallery-albums"] });
      void queryClient.invalidateQueries({ queryKey: ["public-gallery-bundle"] });
      setStatusMessage("Media asset uploaded and mapped to album.");
      setTimeout(() => setStatusMessage(null), 3500);
      setNewMediaTitle("");
      setNewMediaCaption("");
      setNewMediaUrl("");
      setNewMediaVideoId("");
      setNewMediaIsCover(false);
    },
  });

  const deleteMediaMutation = useMutation({
    mutationFn: websiteService.deleteAdminGalleryMedia,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-gallery-media", activeAlbumId] });
      void queryClient.invalidateQueries({ queryKey: ["admin-gallery-albums"] });
      void queryClient.invalidateQueries({ queryKey: ["public-gallery-bundle"] });
      setStatusMessage("Media asset deleted.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Handlers
  const handleCreateAlbum = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAlbumTitle.trim() || !newAlbumDesc.trim() || !newAlbumCover.trim()) {
      alert("Please enter title, description, and cover image URL.");
      return;
    }

    const slug =
      newAlbumSlug.trim().toLowerCase() ||
      newAlbumTitle
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-");

    createAlbumMutation.mutate({
      title: newAlbumTitle.trim(),
      slug,
      category: newAlbumCategory,
      description: newAlbumDesc.trim(),
      cover_image_url: newAlbumCover.trim(),
      academic_year: newAlbumYear,
      event_date: newAlbumDate.trim() || null,
      is_featured: newAlbumFeatured,
      display_order: albums.length + 1,
      is_active: true,
    });
  };

  const handleCreateMedia = (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeAlbumId) {
      alert("Please select or create an album first.");
      return;
    }
    if (!newMediaTitle.trim() || !newMediaUrl.trim()) {
      alert("Please fill in the title and media URL.");
      return;
    }

    createMediaMutation.mutate({
      album_id: activeAlbumId,
      media_type: newMediaType,
      title: newMediaTitle.trim(),
      caption: newMediaCaption.trim() || null,
      url: newMediaUrl.trim(),
      thumbnail_url: newMediaUrl.trim(),
      video_provider: newMediaType === "VIDEO" ? "YOUTUBE" : null,
      video_embed_id: newMediaType === "VIDEO" ? newMediaVideoId.trim() || "dQw4w9WgXcQ" : null,
      aspect_ratio: "16:9",
      display_order: mediaItems.length + 1,
      is_cover: newMediaIsCover,
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
            onClick={() => setSubTab("albums")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              subTab === "albums"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Layers className="h-4 w-4" />
            <span>Curated Albums</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {albums.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setSubTab("media")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              subTab === "media"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Camera className="h-4 w-4" />
            <span>Media Assets & Video Reels</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {mediaItems.length}
            </span>
          </button>
        </div>

        <a
          href="/gallery"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-600 hover:text-brand-700"
        >
          <span>Live Gallery View</span>
          <ExternalLink className="h-3.5 w-3.5" />
        </a>
      </div>

      {/* SUBTAB 1: ALBUMS */}
      {subTab === "albums" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Create Form */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Plus className="h-4 w-4 text-brand-600" />
              <span>Create Curated Album</span>
            </h2>

            <form onSubmit={handleCreateAlbum} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Album Title</label>
                <input
                  type="text"
                  required
                  value={newAlbumTitle}
                  onChange={(e) => setNewAlbumTitle(e.target.value)}
                  placeholder="e.g. Annual Convocation & Degree Ceremony 2026"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">URL Slug</label>
                <input
                  type="text"
                  value={newAlbumSlug}
                  onChange={(e) => setNewAlbumSlug(e.target.value)}
                  placeholder="e.g. convocation-2026 (auto-generated if empty)"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Category</label>
                  <select
                    value={newAlbumCategory}
                    onChange={(e) => setNewAlbumCategory(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="CAMPUS_LIFE">Campus Life & Architecture</option>
                    <option value="CONVOCATION">Convocation & Senate</option>
                    <option value="HACKATHON">Hackathons & Innovation</option>
                    <option value="SPORTS">Sports & Athletics</option>
                    <option value="CULTURAL">Cultural & Arts</option>
                    <option value="RESEARCH">Research & Cleanrooms</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Academic Year</label>
                  <input
                    type="text"
                    value={newAlbumYear}
                    onChange={(e) => setNewAlbumYear(e.target.value)}
                    placeholder="2025-2026"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Event Date (Optional)</label>
                <input
                  type="date"
                  value={newAlbumDate}
                  onChange={(e) => setNewAlbumDate(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Cover Image URL</label>
                <input
                  type="url"
                  required
                  value={newAlbumCover}
                  onChange={(e) => setNewAlbumCover(e.target.value)}
                  placeholder="https://images.unsplash.com/..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Album Description</label>
                <textarea
                  rows={3}
                  required
                  value={newAlbumDesc}
                  onChange={(e) => setNewAlbumDesc(e.target.value)}
                  placeholder="Summary of the ceremonies, participants, and milestones covered..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="featured-album"
                  checked={newAlbumFeatured}
                  onChange={(e) => setNewAlbumFeatured(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
                />
                <label htmlFor="featured-album" className="text-xs font-medium text-slate-700">
                  Feature prominently on Home and Gallery landing
                </label>
              </div>

              <button
                type="submit"
                disabled={createAlbumMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>{createAlbumMutation.isPending ? "Creating..." : "Save Album"}</span>
              </button>
            </form>
          </div>

          {/* Albums List */}
          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Curated Media Albums ({albums.length})</span>
              <span className="text-xs font-normal text-slate-500">Live PostgreSQL Database</span>
            </h2>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
              {albums.map((alb) => (
                <div
                  key={alb.id}
                  className="group relative overflow-hidden rounded-xl border border-slate-200 bg-white shadow-2xs hover:shadow-md transition-all p-3"
                >
                  <div className="relative h-36 w-full rounded-lg overflow-hidden bg-slate-100 mb-3">
                    <img
                      src={alb.cover_image_url}
                      alt={alb.title}
                      className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <div className="absolute top-2 left-2 flex items-center gap-1.5">
                      <span className="rounded-full bg-slate-900/80 px-2 py-0.5 text-[9px] font-bold text-white">
                        {alb.category}
                      </span>
                      {alb.is_featured && (
                        <span className="rounded-full bg-amber-500 px-2 py-0.5 text-[9px] font-bold text-white">
                          Featured
                        </span>
                      )}
                    </div>
                    <div className="absolute bottom-2 right-2 rounded-md bg-black/70 px-2 py-0.5 text-[10px] font-bold text-white">
                      {alb.item_count} items
                    </div>
                  </div>

                  <h3 className="text-xs font-bold text-slate-900 line-clamp-1">{alb.title}</h3>
                  <p className="mt-1 text-[11px] text-slate-500 line-clamp-2">{alb.description}</p>

                  <div className="mt-3 flex items-center justify-between border-t border-slate-100 pt-2 text-[10px] text-slate-500">
                    <span>{alb.academic_year}</span>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          setSelectedAlbumId(alb.id);
                          setSubTab("media");
                        }}
                        className="text-brand-600 font-semibold hover:underline"
                      >
                        Manage Media
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`Delete album "${alb.title}" and all its media items?`)) {
                            deleteAlbumMutation.mutate(alb.id);
                          }
                        }}
                        className="text-red-500 hover:text-red-700"
                        title="Delete album"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* SUBTAB 2: MEDIA ASSETS */}
      {subTab === "media" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Add Media Form */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Plus className="h-4 w-4 text-brand-600" />
              <span>Add Media to Album</span>
            </h2>

            <form onSubmit={handleCreateMedia} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Target Album</label>
                <select
                  value={activeAlbumId}
                  onChange={(e) => setSelectedAlbumId(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  {albums.map((alb) => (
                    <option key={alb.id} value={alb.id}>
                      {alb.title} ({alb.category})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Media Type</label>
                <div className="mt-1.5 grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setNewMediaType("IMAGE")}
                    className={`inline-flex items-center justify-center gap-1.5 rounded-lg py-2 text-xs font-bold transition ${
                      newMediaType === "IMAGE"
                        ? "bg-brand-600 text-white"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                    }`}
                  >
                    <ImageIcon className="h-3.5 w-3.5" />
                    <span>Photo</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setNewMediaType("VIDEO")}
                    className={`inline-flex items-center justify-center gap-1.5 rounded-lg py-2 text-xs font-bold transition ${
                      newMediaType === "VIDEO"
                        ? "bg-purple-600 text-white"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                    }`}
                  >
                    <Play className="h-3.5 w-3.5" />
                    <span>Video Embed</span>
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Media Title</label>
                <input
                  type="text"
                  required
                  value={newMediaTitle}
                  onChange={(e) => setNewMediaTitle(e.target.value)}
                  placeholder="e.g. Chancellor's Medal Presentation"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Caption / Narrative</label>
                <input
                  type="text"
                  value={newMediaCaption}
                  onChange={(e) => setNewMediaCaption(e.target.value)}
                  placeholder="Brief descriptive context for the lightbox viewer..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">
                  {newMediaType === "IMAGE" ? "High-Resolution Image URL" : "Video Poster / Thumbnail URL"}
                </label>
                <input
                  type="url"
                  required
                  value={newMediaUrl}
                  onChange={(e) => setNewMediaUrl(e.target.value)}
                  placeholder="https://images.unsplash.com/..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              {newMediaType === "VIDEO" && (
                <div>
                  <label className="block text-xs font-semibold text-slate-700">YouTube Video ID</label>
                  <input
                    type="text"
                    value={newMediaVideoId}
                    onChange={(e) => setNewMediaVideoId(e.target.value)}
                    placeholder="e.g. dQw4w9WgXcQ"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              )}

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="media-cover"
                  checked={newMediaIsCover}
                  onChange={(e) => setNewMediaIsCover(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
                />
                <label htmlFor="media-cover" className="text-xs font-medium text-slate-700">
                  Set as album cover photo
                </label>
              </div>

              <button
                type="submit"
                disabled={createMediaMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>{createMediaMutation.isPending ? "Adding..." : "Add to Album"}</span>
              </button>
            </form>
          </div>

          {/* Media Items Grid */}
          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Media Items in Selected Album ({mediaItems.length})</span>
              <span className="text-xs font-normal text-slate-500">Live PostgreSQL Database</span>
            </h2>

            <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-3">
              {mediaItems.map((item) => (
                <div
                  key={item.id}
                  className="group relative overflow-hidden rounded-xl border border-slate-200 bg-slate-50 shadow-2xs"
                >
                  <img
                    src={item.thumbnail_url || item.url}
                    alt={item.title}
                    className="h-32 w-full object-cover"
                  />
                  <div className="p-2.5">
                    <span className="block text-[11px] font-bold text-slate-900 truncate">
                      {item.title}
                    </span>
                    {item.caption && (
                      <p className="text-[10px] text-slate-500 truncate">{item.caption}</p>
                    )}
                  </div>
                  <button
                    onClick={() => {
                      if (confirm(`Remove media item "${item.title}"?`)) {
                        deleteMediaMutation.mutate(item.id);
                      }
                    }}
                    className="absolute top-2 right-2 flex h-6 w-6 items-center justify-center rounded-full bg-red-600/90 text-white opacity-0 group-hover:opacity-100 transition shadow-xs"
                    title="Delete item"
                  >
                    <Trash2 className="h-3 w-3" />
                  </button>
                </div>
              ))}

              {mediaItems.length === 0 && (
                <div className="col-span-full py-12 text-center text-slate-400 text-xs">
                  No media items added to this album yet. Use the form on the left to add photos or video reels.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
