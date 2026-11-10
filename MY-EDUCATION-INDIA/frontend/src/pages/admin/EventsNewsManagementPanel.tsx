import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Calendar,
  Newspaper,
  Bell,
  Award,
  Plus,
  Trash2,
  ExternalLink,
  CheckCircle2,
  Clock,
  Sparkles,
  AlertTriangle,
  FileText,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsEvent,
  CmsEventCreateRequest,
  CmsNewsArticle,
  CmsNewsArticleCreateRequest,
  CmsNoticeCircular,
  CmsNoticeCircularCreateRequest,
  CmsAchievement,
  CmsAchievementCreateRequest,
} from "@/types/website.types";

interface EventsNewsManagementPanelProps {
  initialSubTab?: "events" | "news" | "notices" | "achievements";
}

export const EventsNewsManagementPanel: React.FC<EventsNewsManagementPanelProps> = ({
  initialSubTab = "events",
}) => {
  const queryClient = useQueryClient();
  const [subTab, setSubTab] = useState<"events" | "news" | "notices" | "achievements">(
    initialSubTab
  );
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Queries
  const { data: events = [] } = useQuery({
    queryKey: ["admin-events-list"],
    queryFn: websiteService.listAdminEvents,
  });

  const { data: news = [] } = useQuery({
    queryKey: ["admin-news-list"],
    queryFn: websiteService.listAdminNews,
  });

  const { data: notices = [] } = useQuery({
    queryKey: ["admin-notices-list"],
    queryFn: websiteService.listAdminNotices,
  });

  const { data: achievements = [] } = useQuery({
    queryKey: ["admin-achievements-list"],
    queryFn: websiteService.listAdminAchievements,
  });

  // Mutations
  const createEventMutation = useMutation({
    mutationFn: websiteService.createAdminEvent,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-events-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-events-news-bundle"] });
      setStatusMessage("Event successfully published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteEventMutation = useMutation({
    mutationFn: websiteService.deleteAdminEvent,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-events-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-events-news-bundle"] });
      setStatusMessage("Event successfully removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createNewsMutation = useMutation({
    mutationFn: websiteService.createAdminNews,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-news-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-events-news-bundle"] });
      setStatusMessage("News article published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteNewsMutation = useMutation({
    mutationFn: websiteService.deleteAdminNews,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-news-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-events-news-bundle"] });
      setStatusMessage("News article removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createNoticeMutation = useMutation({
    mutationFn: websiteService.createAdminNotice,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-notices-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-events-news-bundle"] });
      setStatusMessage("Official circular gazetted.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteNoticeMutation = useMutation({
    mutationFn: websiteService.deleteAdminNotice,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-notices-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-events-news-bundle"] });
      setStatusMessage("Circular removed from gazette.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createAchievementMutation = useMutation({
    mutationFn: websiteService.createAdminAchievement,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-achievements-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-events-news-bundle"] });
      setStatusMessage("Accolade record saved.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteAchievementMutation = useMutation({
    mutationFn: websiteService.deleteAdminAchievement,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-achievements-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-events-news-bundle"] });
      setStatusMessage("Accolade record removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Form states: Event
  const [eventTitle, setEventTitle] = useState("");
  const [eventCategory, setEventCategory] = useState("ACADEMIC");
  const [eventStartDate, setEventStartDate] = useState("2026-04-15");
  const [eventEndDate, setEventEndDate] = useState("2026-04-17");
  const [eventTimeWindow, setEventTimeWindow] = useState("09:30 AM – 05:00 PM");
  const [eventVenue, setEventVenue] = useState("Main Auditorium, Block A");
  const [eventSummary, setEventSummary] = useState("");
  const [eventRegLink, setEventRegLink] = useState("");
  const [eventIsFlagship, setEventIsFlagship] = useState(false);

  // Form states: News
  const [newsTitle, setNewsTitle] = useState("");
  const [newsCategory, setNewsCategory] = useState("RESEARCH");
  const [newsAuthor, setNewsAuthor] = useState("Dean Research Directorate");
  const [newsPubDate, setNewsPubDate] = useState("2026-03-01");
  const [newsSummary, setNewsSummary] = useState("");
  const [newsContent, setNewsContent] = useState("");
  const [newsIsFeatured, setNewsIsFeatured] = useState(false);
  const [newsIsBreaking, setNewsIsBreaking] = useState(false);

  // Form states: Notice
  const [noticeRef, setNoticeRef] = useState(`MEI/NOT/${new Date().getFullYear()}/001`);
  const [noticeTitle, setNoticeTitle] = useState("");
  const [noticeCategory, setNoticeCategory] = useState("EXAMINATION");
  const [noticeIssuedBy, setNoticeIssuedBy] = useState("Controller of Examinations");
  const [noticeIssuedDate, setNoticeIssuedDate] = useState("2026-03-01");
  const [noticePdfUrl, setNoticePdfUrl] = useState("/downloads/notices/exam-circular.pdf");
  const [noticeIsUrgent, setNoticeIsUrgent] = useState(false);

  // Form states: Achievement
  const [achTitle, setAchTitle] = useState("");
  const [achCategory, setAchCategory] = useState("INSTITUTIONAL");
  const [achYear, setAchYear] = useState("2026");
  const [achBody, setAchBody] = useState("Ministry of Education & NIRF");
  const [achRankBadge, setAchRankBadge] = useState("Top 10 Autonomous");
  const [achDesc, setAchDesc] = useState("");

  const handleAddEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!eventTitle.trim()) return;
    const slug = eventTitle.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    await createEventMutation.mutateAsync({
      title: eventTitle.trim(),
      slug,
      category: eventCategory,
      start_date: eventStartDate,
      end_date: eventEndDate || null,
      time_window: eventTimeWindow,
      venue: eventVenue,
      summary: eventSummary.trim(),
      registration_link: eventRegLink.trim() || null,
      image_url: null,
      is_flagship: eventIsFlagship,
      display_order: events.length + 1,
      is_active: true,
    });
    setEventTitle("");
    setEventSummary("");
    setEventRegLink("");
  };

  const handleAddNews = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newsTitle.trim() || !newsSummary.trim()) return;
    const slug = newsTitle.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    await createNewsMutation.mutateAsync({
      title: newsTitle.trim(),
      slug,
      category: newsCategory,
      author_name: newsAuthor.trim() || "Editorial Board",
      published_date: newsPubDate,
      summary: newsSummary.trim(),
      content: newsContent.trim() || newsSummary.trim(),
      image_url: null,
      is_featured: newsIsFeatured,
      is_breaking: newsIsBreaking,
      display_order: news.length + 1,
      is_active: true,
    });
    setNewsTitle("");
    setNewsSummary("");
    setNewsContent("");
  };

  const handleAddNotice = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!noticeRef.trim() || !noticeTitle.trim()) return;
    await createNoticeMutation.mutateAsync({
      reference_number: noticeRef.trim(),
      title: noticeTitle.trim(),
      category: noticeCategory,
      issued_by: noticeIssuedBy.trim(),
      issued_date: noticeIssuedDate,
      expiry_date: null,
      pdf_url: noticePdfUrl.trim() || null,
      is_urgent: noticeIsUrgent,
      display_order: notices.length + 1,
      is_active: true,
    });
    setNoticeTitle("");
    setNoticeRef(`MEI/NOT/${new Date().getFullYear()}/${String(notices.length + 2).padStart(3, "0")}`);
  };

  const handleAddAchievement = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!achTitle.trim() || !achDesc.trim()) return;
    await createAchievementMutation.mutateAsync({
      title: achTitle.trim(),
      category: achCategory,
      year: achYear.trim(),
      awarding_body: achBody.trim() || null,
      rank_or_badge: achRankBadge.trim() || null,
      description: achDesc.trim(),
      certificate_url: null,
      display_order: achievements.length + 1,
      is_active: true,
    });
    setAchTitle("");
    setAchDesc("");
  };

  return (
    <div className="space-y-6">
      {statusMessage && (
        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 border border-emerald-200 p-3.5 text-xs font-semibold text-emerald-800">
          <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Sub-tab selection bar */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-3">
        <button
          onClick={() => setSubTab("events")}
          className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
            subTab === "events"
              ? "bg-brand-600 text-white shadow-xs"
              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
          }`}
        >
          <Calendar className="h-3.5 w-3.5" />
          <span>Campus Events ({events.length})</span>
        </button>

        <button
          onClick={() => setSubTab("news")}
          className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
            subTab === "news"
              ? "bg-brand-600 text-white shadow-xs"
              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
          }`}
        >
          <Newspaper className="h-3.5 w-3.5" />
          <span>News & Articles ({news.length})</span>
        </button>

        <button
          onClick={() => setSubTab("notices")}
          className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
            subTab === "notices"
              ? "bg-brand-600 text-white shadow-xs"
              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
          }`}
        >
          <Bell className="h-3.5 w-3.5" />
          <span>Official Circulars ({notices.length})</span>
        </button>

        <button
          onClick={() => setSubTab("achievements")}
          className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
            subTab === "achievements"
              ? "bg-brand-600 text-white shadow-xs"
              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
          }`}
        >
          <Award className="h-3.5 w-3.5" />
          <span>Accolades & Ranks ({achievements.length})</span>
        </button>
      </div>

      {/* 1. EVENTS PANEL */}
      {subTab === "events" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Calendar className="h-4 w-4 text-brand-600" />
              <span>Schedule New Campus Event</span>
            </h2>

            <form onSubmit={handleAddEvent} className="mt-4 space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Event Title</label>
                <input
                  type="text"
                  required
                  value={eventTitle}
                  onChange={(e) => setEventTitle(e.target.value)}
                  placeholder="e.g. Smart Campus 36-Hr Hackathon"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-2.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Category</label>
                  <select
                    value={eventCategory}
                    onChange={(e) => setEventCategory(e.target.value)}
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="ACADEMIC">Academic</option>
                    <option value="HACKATHON">Hackathon</option>
                    <option value="CULTURAL">Cultural</option>
                    <option value="SPORTS">Sports</option>
                    <option value="WORKSHOP">Workshop</option>
                    <option value="CONFERENCE">Conference</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Venue</label>
                  <input
                    type="text"
                    required
                    value={eventVenue}
                    onChange={(e) => setEventVenue(e.target.value)}
                    placeholder="Main Auditorium"
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Start Date</label>
                  <input
                    type="date"
                    required
                    value={eventStartDate}
                    onChange={(e) => setEventStartDate(e.target.value)}
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">End Date</label>
                  <input
                    type="date"
                    value={eventEndDate}
                    onChange={(e) => setEventEndDate(e.target.value)}
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Time Window</label>
                <input
                  type="text"
                  required
                  value={eventTimeWindow}
                  onChange={(e) => setEventTimeWindow(e.target.value)}
                  placeholder="09:30 AM – 05:00 PM"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Registration Link</label>
                <input
                  type="url"
                  value={eventRegLink}
                  onChange={(e) => setEventRegLink(e.target.value)}
                  placeholder="https://myeducation.in/events/register/..."
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Event Summary</label>
                <textarea
                  rows={3}
                  required
                  value={eventSummary}
                  onChange={(e) => setEventSummary(e.target.value)}
                  placeholder="Detailed description of the gathering..."
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center gap-2 pt-1">
                <input
                  type="checkbox"
                  id="eventFlagship"
                  checked={eventIsFlagship}
                  onChange={(e) => setEventIsFlagship(e.target.checked)}
                  className="rounded-sm border-slate-300 text-brand-600 focus:ring-brand-500"
                />
                <label htmlFor="eventFlagship" className="text-xs font-semibold text-slate-700">
                  Mark as Flagship Showcase Event
                </label>
              </div>

              <button
                type="submit"
                disabled={createEventMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Event</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Published Campus Events ({events.length})</span>
              <span className="text-xs text-slate-500 font-normal">Real-Time Database Records</span>
            </h2>
            <div className="mt-4 space-y-3">
              {events.map((ev) => (
                <div key={ev.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="rounded-md bg-brand-100 px-2 py-0.5 text-[10px] font-bold text-brand-700">
                        {ev.category}
                      </span>
                      {ev.is_flagship && (
                        <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-extrabold text-amber-800">
                          FLAGSHIP
                        </span>
                      )}
                      <h4 className="text-xs font-bold text-slate-900">{ev.title}</h4>
                    </div>
                    <div className="text-[11px] text-slate-500">
                      {ev.start_date} {ev.end_date ? `to ${ev.end_date}` : ""} • {ev.time_window} • Venue: {ev.venue}
                    </div>
                    <p className="text-xs text-slate-600 line-clamp-2">{ev.summary}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteEventMutation.mutate(ev.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 2. NEWS PANEL */}
      {subTab === "news" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Newspaper className="h-4 w-4 text-brand-600" />
              <span>Publish Press Release / Article</span>
            </h2>

            <form onSubmit={handleAddNews} className="mt-4 space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Article Title</label>
                <input
                  type="text"
                  required
                  value={newsTitle}
                  onChange={(e) => setNewsTitle(e.target.value)}
                  placeholder="e.g. Faculty Secures ₹2.4 Crore Research Grant"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-2.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Category</label>
                  <select
                    value={newsCategory}
                    onChange={(e) => setNewsCategory(e.target.value)}
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="RESEARCH">Research</option>
                    <option value="CAMPUS">Campus</option>
                    <option value="ACADEMIC">Academic</option>
                    <option value="PLACEMENTS">Placements</option>
                    <option value="ACHIEVEMENT">Achievement</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Author</label>
                  <input
                    type="text"
                    required
                    value={newsAuthor}
                    onChange={(e) => setNewsAuthor(e.target.value)}
                    placeholder="Editorial Desk"
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Publish Date</label>
                <input
                  type="date"
                  required
                  value={newsPubDate}
                  onChange={(e) => setNewsPubDate(e.target.value)}
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Short Summary</label>
                <textarea
                  rows={2}
                  required
                  value={newsSummary}
                  onChange={(e) => setNewsSummary(e.target.value)}
                  placeholder="Key highlight for ticker and previews..."
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Full Content</label>
                <textarea
                  rows={4}
                  value={newsContent}
                  onChange={(e) => setNewsContent(e.target.value)}
                  placeholder="Complete text of the press release..."
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center gap-4 pt-1">
                <label className="flex items-center gap-1.5 text-xs font-semibold text-slate-700">
                  <input
                    type="checkbox"
                    checked={newsIsFeatured}
                    onChange={(e) => setNewsIsFeatured(e.target.checked)}
                    className="rounded-sm border-slate-300 text-brand-600"
                  />
                  Featured
                </label>
                <label className="flex items-center gap-1.5 text-xs font-semibold text-slate-700">
                  <input
                    type="checkbox"
                    checked={newsIsBreaking}
                    onChange={(e) => setNewsIsBreaking(e.target.checked)}
                    className="rounded-sm border-slate-300 text-brand-600"
                  />
                  Breaking News
                </label>
              </div>

              <button
                type="submit"
                disabled={createNewsMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Press Release</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Articles & Press Releases ({news.length})</span>
            </h2>
            <div className="mt-4 space-y-3">
              {news.map((n) => (
                <div key={n.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="rounded-md bg-purple-100 px-2 py-0.5 text-[10px] font-bold text-purple-700">
                        {n.category}
                      </span>
                      {n.is_breaking && (
                        <span className="rounded-full bg-rose-100 px-2 py-0.5 text-[10px] font-extrabold text-rose-800 animate-pulse">
                          BREAKING
                        </span>
                      )}
                      {n.is_featured && (
                        <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-extrabold text-emerald-800">
                          FEATURED
                        </span>
                      )}
                      <h4 className="text-xs font-bold text-slate-900">{n.title}</h4>
                    </div>
                    <div className="text-[11px] text-slate-500">
                      By {n.author_name} • Published on {n.published_date}
                    </div>
                    <p className="text-xs text-slate-600 line-clamp-2">{n.summary}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteNewsMutation.mutate(n.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 3. NOTICES PANEL */}
      {subTab === "notices" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Bell className="h-4 w-4 text-brand-600" />
              <span>Gazette Official Notice / Circular</span>
            </h2>

            <form onSubmit={handleAddNotice} className="mt-4 space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Reference Number</label>
                <input
                  type="text"
                  required
                  value={noticeRef}
                  onChange={(e) => setNoticeRef(e.target.value)}
                  placeholder="MEI/NOT/2026/042"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Notice Subject / Title</label>
                <input
                  type="text"
                  required
                  value={noticeTitle}
                  onChange={(e) => setNoticeTitle(e.target.value)}
                  placeholder="e.g. End-Semester Examination Schedule"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-2.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Category</label>
                  <select
                    value={noticeCategory}
                    onChange={(e) => setNoticeCategory(e.target.value)}
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="EXAMINATION">Examination</option>
                    <option value="ACADEMIC">Academic</option>
                    <option value="ADMINISTRATIVE">Administrative</option>
                    <option value="HOLIDAY">Holiday</option>
                    <option value="SCHOLARSHIP">Scholarship</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Issued Date</label>
                  <input
                    type="date"
                    required
                    value={noticeIssuedDate}
                    onChange={(e) => setNoticeIssuedDate(e.target.value)}
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Issued Authority</label>
                <input
                  type="text"
                  required
                  value={noticeIssuedBy}
                  onChange={(e) => setNoticeIssuedBy(e.target.value)}
                  placeholder="Registrar / CoE Directorate"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">PDF Gazette Download URL</label>
                <input
                  type="text"
                  value={noticePdfUrl}
                  onChange={(e) => setNoticePdfUrl(e.target.value)}
                  placeholder="/downloads/notices/circular-042.pdf"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center gap-2 pt-1">
                <input
                  type="checkbox"
                  id="noticeUrgent"
                  checked={noticeIsUrgent}
                  onChange={(e) => setNoticeIsUrgent(e.target.checked)}
                  className="rounded-sm border-slate-300 text-rose-600"
                />
                <label htmlFor="noticeUrgent" className="text-xs font-semibold text-rose-700">
                  Mark as URGENT Gazetted Circular
                </label>
              </div>

              <button
                type="submit"
                disabled={createNoticeMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Circular</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Gazetted Institutional Notices ({notices.length})</span>
            </h2>
            <div className="mt-4 space-y-3">
              {notices.map((not) => (
                <div key={not.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="rounded-md bg-slate-200 px-2 py-0.5 text-[10px] font-mono font-bold text-slate-800">
                        {not.reference_number}
                      </span>
                      {not.is_urgent && (
                        <span className="rounded-full bg-rose-100 px-2 py-0.5 text-[10px] font-extrabold text-rose-800 animate-pulse">
                          URGENT
                        </span>
                      )}
                      <span className="rounded-md bg-brand-100 px-2 py-0.5 text-[10px] font-bold text-brand-700">
                        {not.category}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{not.title}</h4>
                    </div>
                    <div className="text-[11px] text-slate-500">
                      Issued by {not.issued_by} • Date: {not.issued_date}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteNoticeMutation.mutate(not.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 4. ACHIEVEMENTS PANEL */}
      {subTab === "achievements" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Award className="h-4 w-4 text-brand-600" />
              <span>Record Institutional Accolade</span>
            </h2>

            <form onSubmit={handleAddAchievement} className="mt-4 space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Accolade Title</label>
                <input
                  type="text"
                  required
                  value={achTitle}
                  onChange={(e) => setAchTitle(e.target.value)}
                  placeholder="e.g. NAAC 'A++' Grade Accreditation"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-2.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Category</label>
                  <select
                    value={achCategory}
                    onChange={(e) => setAchCategory(e.target.value)}
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="INSTITUTIONAL">Institutional</option>
                    <option value="RANKING">Ranking</option>
                    <option value="RESEARCH">Research</option>
                    <option value="STUDENT">Student</option>
                    <option value="SPORTS">Sports</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Year</label>
                  <input
                    type="text"
                    required
                    value={achYear}
                    onChange={(e) => setAchYear(e.target.value)}
                    placeholder="2026"
                    className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Awarding Body</label>
                <input
                  type="text"
                  value={achBody}
                  onChange={(e) => setAchBody(e.target.value)}
                  placeholder="e.g. National Assessment and Accreditation Council"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Rank / Badge Text</label>
                <input
                  type="text"
                  value={achRankBadge}
                  onChange={(e) => setAchRankBadge(e.target.value)}
                  placeholder="e.g. Score 3.82 CGPA (Highest in Region)"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Accolade Description</label>
                <textarea
                  rows={3}
                  required
                  value={achDesc}
                  onChange={(e) => setAchDesc(e.target.value)}
                  placeholder="Official citation and details..."
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createAchievementMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Accolade</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Recorded Accolades & Accreditations ({achievements.length})</span>
            </h2>
            <div className="mt-4 space-y-3">
              {achievements.map((ach) => (
                <div key={ach.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="rounded-md bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-800">
                        {ach.year}
                      </span>
                      {ach.rank_or_badge && (
                        <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-extrabold text-emerald-800">
                          {ach.rank_or_badge}
                        </span>
                      )}
                      <h4 className="text-xs font-bold text-slate-900">{ach.title}</h4>
                    </div>
                    {ach.awarding_body && (
                      <div className="text-[11px] text-slate-500">Conferred by: {ach.awarding_body}</div>
                    )}
                    <p className="text-xs text-slate-600 line-clamp-2">{ach.description}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteAchievementMutation.mutate(ach.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
