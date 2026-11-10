import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Star,
  Quote,
  CheckCircle2,
  XCircle,
  Trash2,
  Plus,
  ExternalLink,
  MessageSquare,
  ShieldCheck,
  Filter,
  Play,
  Clock,
  Sparkles,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsTestimonial,
  CmsTestimonialCreateRequest,
} from "@/types/website.types";

interface TestimonialsModerationPanelProps {
  initialStatus?: "PENDING" | "APPROVED" | "REJECTED" | "ALL";
}

export const TestimonialsModerationPanel: React.FC<TestimonialsModerationPanelProps> = ({
  initialStatus = "PENDING",
}) => {
  const queryClient = useQueryClient();
  const [selectedStatus, setSelectedStatus] = useState<string>(initialStatus);
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Queries
  const { data: reviews = [] } = useQuery({
    queryKey: ["admin-testimonials-reviews", selectedStatus, selectedCategory],
    queryFn: () =>
      websiteService.listAdminTestimonials({
        moderation_status: selectedStatus === "ALL" ? undefined : selectedStatus,
        category: selectedCategory === "ALL" ? undefined : selectedCategory,
      }),
  });

  // Create Form State
  const [authorName, setAuthorName] = useState("");
  const [authorRole, setAuthorRole] = useState("");
  const [authorCategory, setAuthorCategory] = useState("Student");
  const [companyName, setCompanyName] = useState("");
  const [batchYear, setBatchYear] = useState("Class of 2025");
  const [ratingStars, setRatingStars] = useState(5);
  const [quote, setQuote] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [videoEmbedId, setVideoEmbedId] = useState("");
  const [isFeatured, setIsFeatured] = useState(false);

  // Mutations
  const approveMutation = useMutation({
    mutationFn: websiteService.approveTestimonial,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-testimonials-reviews"] });
      void queryClient.invalidateQueries({ queryKey: ["public-testimonials-bundle"] });
      setStatusMessage("Testimonial approved and published live.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const rejectMutation = useMutation({
    mutationFn: websiteService.rejectTestimonial,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-testimonials-reviews"] });
      void queryClient.invalidateQueries({ queryKey: ["public-testimonials-bundle"] });
      setStatusMessage("Testimonial review rejected and suppressed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: websiteService.deleteAdminTestimonial,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-testimonials-reviews"] });
      void queryClient.invalidateQueries({ queryKey: ["public-testimonials-bundle"] });
      setStatusMessage("Testimonial review purged.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createMutation = useMutation({
    mutationFn: websiteService.createAdminTestimonial,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-testimonials-reviews"] });
      void queryClient.invalidateQueries({ queryKey: ["public-testimonials-bundle"] });
      setStatusMessage("Official institutional testimonial published.");
      setTimeout(() => setStatusMessage(null), 3500);
      setAuthorName("");
      setAuthorRole("");
      setCompanyName("");
      setQuote("");
      setVideoUrl("");
      setVideoEmbedId("");
      setIsFeatured(false);
    },
  });

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!authorName.trim() || !authorRole.trim() || !quote.trim()) return;

    createMutation.mutate({
      author_name: authorName.trim(),
      author_role: authorRole.trim(),
      author_category: authorCategory,
      rating_stars: ratingStars,
      quote: quote.trim(),
      company_or_institution: companyName.trim() || null,
      batch_year: batchYear.trim() || null,
      avatar_url: null,
      video_url: videoUrl.trim() || null,
      video_embed_id: videoEmbedId.trim() || null,
      moderation_status: "APPROVED",
      is_featured: isFeatured,
      display_order: 1,
      is_active: true,
    });
  };

  const pendingCount = reviews.filter((r) => r.moderation_status === "PENDING").length;

  return (
    <div className="space-y-6">
      {/* Status banner */}
      {statusMessage && (
        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-xs font-semibold text-emerald-800 animate-in fade-in">
          <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Moderation Controls Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-slate-200 pb-4">
        {/* Status Filter Tabs */}
        <div className="flex items-center gap-2">
          {[
            { id: "PENDING", label: "Pending Moderation Queue" },
            { id: "APPROVED", label: "Approved Live" },
            { id: "REJECTED", label: "Rejected" },
            { id: "ALL", label: "All Reviews" },
          ].map((st) => (
            <button
              key={st.id}
              onClick={() => setSelectedStatus(st.id)}
              className={`rounded-xl px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 ${
                selectedStatus === st.id
                  ? "bg-brand-600 text-white shadow-xs"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              <span>{st.label}</span>
              {st.id === "PENDING" && pendingCount > 0 && (
                <span className="rounded-full bg-amber-400 px-1.5 py-0.2 text-[10px] font-black text-slate-900">
                  {pendingCount}
                </span>
              )}
            </button>
          ))}
        </div>

        <a
          href="/testimonials"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-600 hover:text-brand-700"
        >
          <span>Live Reviews Showcase</span>
          <ExternalLink className="h-3.5 w-3.5" />
        </a>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* 1. Add Official Testimonial Form */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
            <Plus className="h-4 w-4 text-brand-600" />
            <span>Publish Verified Testimonial</span>
          </h2>

          <form onSubmit={handleCreate} className="mt-4 space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Author Full Name</label>
              <input
                type="text"
                required
                value={authorName}
                onChange={(e) => setAuthorName(e.target.value)}
                placeholder="e.g. Aarushi Jain"
                className="w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs focus:border-brand-600 focus:outline-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Category</label>
                <select
                  value={authorCategory}
                  onChange={(e) => setAuthorCategory(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 px-3 py-2 text-xs focus:border-brand-600 focus:outline-none"
                >
                  <option value="Student">Student</option>
                  <option value="Parent">Parent</option>
                  <option value="Faculty">Faculty</option>
                  <option value="Recruiter">Recruiter</option>
                  <option value="Alumni">Alumni</option>
                </select>
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Star Rating</label>
                <select
                  value={ratingStars}
                  onChange={(e) => setRatingStars(Number(e.target.value))}
                  className="w-full rounded-xl border border-slate-300 px-3 py-2 text-xs focus:border-brand-600 focus:outline-none"
                >
                  <option value={5}>5 Stars (Excellent)</option>
                  <option value={4}>4 Stars (Very Good)</option>
                  <option value={3}>3 Stars (Good)</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Role / Designation</label>
              <input
                type="text"
                required
                value={authorRole}
                onChange={(e) => setAuthorRole(e.target.value)}
                placeholder="e.g. B.Tech CSE (Placed at Google Cloud)"
                className="w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs focus:border-brand-600 focus:outline-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Company / Institution</label>
                <input
                  type="text"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="e.g. Google Cloud"
                  className="w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs focus:border-brand-600 focus:outline-none"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Batch / Cohort</label>
                <input
                  type="text"
                  value={batchYear}
                  onChange={(e) => setBatchYear(e.target.value)}
                  placeholder="Class of 2024"
                  className="w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs focus:border-brand-600 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Testimonial Quote</label>
              <textarea
                rows={3}
                required
                value={quote}
                onChange={(e) => setQuote(e.target.value)}
                placeholder="Direct feedback from the stakeholder..."
                className="w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs focus:border-brand-600 focus:outline-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Video Story URL</label>
                <input
                  type="url"
                  value={videoUrl}
                  onChange={(e) => setVideoUrl(e.target.value)}
                  placeholder="https://youtube.com/..."
                  className="w-full rounded-xl border border-slate-300 px-3 py-2 text-xs focus:border-brand-600 focus:outline-none"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">YouTube Video ID</label>
                <input
                  type="text"
                  value={videoEmbedId}
                  onChange={(e) => setVideoEmbedId(e.target.value)}
                  placeholder="dQw4w9WgXcQ"
                  className="w-full rounded-xl border border-slate-300 px-3 py-2 text-xs focus:border-brand-600 focus:outline-none"
                />
              </div>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="feat-test"
                checked={isFeatured}
                onChange={(e) => setIsFeatured(e.target.checked)}
                className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
              />
              <label htmlFor="feat-test" className="font-medium text-slate-700">
                Pin to Home and Testimonials showcase
              </label>
            </div>

            <button
              type="submit"
              disabled={createMutation.isPending}
              className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
            >
              <Plus className="h-4 w-4" />
              <span>Publish Official Review</span>
            </button>
          </form>
        </div>

        {/* 2. Moderation Queue & Review List */}
        <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
            <span>
              {selectedStatus === "PENDING"
                ? `Pending Approval Queue (${reviews.length})`
                : `Testimonials Database (${reviews.length})`}
            </span>
            <span className="text-xs font-normal text-slate-500">Live PostgreSQL Records</span>
          </h2>

          <div className="mt-4 space-y-3">
            {reviews.map((r) => (
              <div
                key={r.id}
                className="rounded-xl border border-slate-200 bg-white p-4 shadow-2xs hover:border-brand-200 transition-all space-y-2"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span
                        className={`rounded-md px-2 py-0.5 text-[10px] font-black uppercase ${
                          r.moderation_status === "APPROVED"
                            ? "bg-emerald-100 text-emerald-800"
                            : r.moderation_status === "PENDING"
                            ? "bg-amber-100 text-amber-800 animate-pulse"
                            : "bg-rose-100 text-rose-800"
                        }`}
                      >
                        {r.moderation_status}
                      </span>
                      <span className="rounded-md bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700">
                        {r.author_category}
                      </span>
                      <div className="flex text-amber-400">
                        {Array.from({ length: r.rating_stars }).map((_, idx) => (
                          <Star key={idx} className="h-3 w-3 fill-current" />
                        ))}
                      </div>
                      <h4 className="text-xs font-bold text-slate-900">{r.author_name}</h4>
                    </div>

                    <p className="text-[11px] text-slate-500">
                      {r.author_role} {r.company_or_institution ? `• ${r.company_or_institution}` : ""}
                    </p>
                  </div>

                  {/* Moderation Actions */}
                  <div className="flex items-center gap-1.5 shrink-0">
                    {r.moderation_status !== "APPROVED" && (
                      <button
                        onClick={() => approveMutation.mutate(r.id)}
                        className="rounded-lg bg-emerald-50 border border-emerald-200 px-2.5 py-1 text-[11px] font-bold text-emerald-700 hover:bg-emerald-100 transition"
                        title="Approve Review"
                      >
                        Approve
                      </button>
                    )}
                    {r.moderation_status !== "REJECTED" && (
                      <button
                        onClick={() => rejectMutation.mutate(r.id)}
                        className="rounded-lg bg-rose-50 border border-rose-200 px-2.5 py-1 text-[11px] font-bold text-rose-700 hover:bg-rose-100 transition"
                        title="Reject Review"
                      >
                        Reject
                      </button>
                    )}
                    <button
                      onClick={() => {
                        if (confirm(`Purge testimonial from "${r.author_name}"?`)) {
                          deleteMutation.mutate(r.id);
                        }
                      }}
                      className="p-1 text-slate-400 hover:text-red-600 transition"
                      title="Delete review"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>

                <p className="text-xs text-slate-700 italic leading-relaxed bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                  &ldquo;{r.quote}&rdquo;
                </p>

                {r.video_url && (
                  <div className="flex items-center gap-1.5 text-[11px] text-purple-700 font-semibold">
                    <Play className="h-3 w-3 fill-current" />
                    <span>Includes Video Story ({r.video_embed_id || "Embedded"})</span>
                  </div>
                )}
              </div>
            ))}

            {reviews.length === 0 && (
              <div className="py-12 text-center text-slate-400 text-xs">
                No reviews found for status: <span className="font-bold">{selectedStatus}</span>.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
