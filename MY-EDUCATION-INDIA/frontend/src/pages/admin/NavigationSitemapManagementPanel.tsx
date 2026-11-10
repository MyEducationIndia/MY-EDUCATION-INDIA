import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Compass,
  Menu,
  Sparkles,
  Search,
  FileCode,
  Layers,
  Plus,
  Trash2,
  Edit2,
  RefreshCw,
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  BarChart3,
  TrendingUp,
  Globe,
  Sliders,
  X,
  Send,
  Eye,
  Link as LinkIcon,
  FolderTree,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  NavigationMenuItem,
  WebsiteQuickLink,
  SearchAnalyticsSummary,
} from "@/types/website.types";

export const NavigationSitemapManagementPanel: React.FC = () => {
  const queryClient = useQueryClient();
  const [subTab, setSubTab] = useState<
    "menus" | "quick_links" | "indexer" | "analytics" | "sitemap"
  >("menus");

  const [selectedLocation, setSelectedLocation] = useState("HEADER_MAIN");

  // Navigation item modal state
  const [isNavModalOpen, setIsNavModalOpen] = useState(false);
  const [editingNavId, setEditingNavId] = useState<string | null>(null);
  const [navForm, setNavForm] = useState({
    menu_location: "HEADER_MAIN",
    title: "",
    path: "",
    icon_name: "",
    badge_text: "",
    description: "",
    category: "",
    parent_id: null as string | null,
    is_external: false,
    open_new_tab: false,
    is_mega_menu: false,
    display_order: 1,
    is_active: true,
  });

  // Quick link modal state
  const [isQlModalOpen, setIsQlModalOpen] = useState(false);
  const [editingQlId, setEditingQlId] = useState<string | null>(null);
  const [qlForm, setQlForm] = useState({
    title: "",
    path: "",
    icon_name: "Sparkles",
    badge_text: "",
    target_type: "INTERNAL",
    is_highlighted: false,
    display_order: 1,
    is_active: true,
  });

  // Status banners
  const [reindexStatus, setReindexStatus] = useState<string | null>(null);

  // Queries
  const {
    data: navItems = [],
    isLoading: navLoading,
    refetch: refetchNav,
  } = useQuery<NavigationMenuItem[]>({
    queryKey: ["admin_navigation_menus", selectedLocation],
    queryFn: async () => {
      return await websiteService.listAdminNavigationMenus(selectedLocation);
    },
  });

  const {
    data: quickLinks = [],
    isLoading: qlLoading,
    refetch: refetchQl,
  } = useQuery<WebsiteQuickLink[]>({
    queryKey: ["admin_quick_links"],
    queryFn: async () => {
      return await websiteService.listAdminQuickLinks();
    },
  });

  const {
    data: analytics,
    isLoading: analyticsLoading,
    refetch: refetchAnalytics,
  } = useQuery<SearchAnalyticsSummary>({
    queryKey: ["admin_search_analytics"],
    queryFn: async () => {
      return await websiteService.getAdminSearchAnalytics();
    },
  });

  // Mutations
  const createNavMutation = useMutation({
    mutationFn: async (payload: typeof navForm) => {
      return await websiteService.createAdminNavigationMenu(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_navigation_menus"] });
      setIsNavModalOpen(false);
      resetNavForm();
    },
  });

  const deleteNavMutation = useMutation({
    mutationFn: async (id: string) => {
      return await websiteService.deleteAdminNavigationMenu(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_navigation_menus"] });
    },
  });

  const createQlMutation = useMutation({
    mutationFn: async (payload: typeof qlForm) => {
      return await websiteService.createAdminQuickLink(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_quick_links"] });
      setIsQlModalOpen(false);
      resetQlForm();
    },
  });

  const deleteQlMutation = useMutation({
    mutationFn: async (id: string) => {
      return await websiteService.deleteAdminQuickLink(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_quick_links"] });
    },
  });

  const reindexMutation = useMutation({
    mutationFn: async () => {
      return await websiteService.reindexSearchCatalog();
    },
    onSuccess: (data) => {
      setReindexStatus(
        `Successfully crawled and indexed ${data.indexed_items} database entities into PostgreSQL search catalog!`
      );
    },
  });

  const resetNavForm = () => {
    setEditingNavId(null);
    setNavForm({
      menu_location: selectedLocation,
      title: "",
      path: "",
      icon_name: "",
      badge_text: "",
      description: "",
      category: "",
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: false,
      display_order: navItems.length + 1,
      is_active: true,
    });
  };

  const resetQlForm = () => {
    setEditingQlId(null);
    setQlForm({
      title: "",
      path: "",
      icon_name: "Sparkles",
      badge_text: "",
      target_type: "INTERNAL",
      is_highlighted: false,
      display_order: quickLinks.length + 1,
      is_active: true,
    });
  };

  // Group top-level and children for display
  const rootNavItems = navItems.filter((i) => !i.parent_id);

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-6 sm:p-8 shadow-xl border border-slate-800">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase mb-1">
              <Compass className="w-4 h-4" /> Module 15 Navigation & Search Governance
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              Search & Navigation Engine
            </h1>
            <p className="text-slate-300 text-sm mt-1 max-w-2xl">
              Configure hierarchical megamenu trees, curate quick portal links,
              trigger search re-indexing, monitor query analytics, and inspect
              sitemaps.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                refetchNav();
                refetchQl();
                refetchAnalytics();
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-sm font-semibold transition border border-slate-700"
            >
              <RefreshCw className="w-4 h-4" /> Refresh Engine
            </button>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Header Nav Nodes</p>
            <p className="text-2xl font-bold text-white mt-1">
              {navItems.length}
            </p>
            <span className="text-xs text-indigo-400 font-medium">
              {rootNavItems.length} Top-Level Sections
            </span>
          </div>
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Active Quick Links</p>
            <p className="text-2xl font-bold text-white mt-1">
              {quickLinks.length}
            </p>
            <span className="text-xs text-emerald-400 font-medium">
              {quickLinks.filter((q) => q.is_highlighted).length} Highlighted
            </span>
          </div>
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Search Inquiries Logged</p>
            <p className="text-2xl font-bold text-white mt-1">
              {analytics?.total_searches || 0}
            </p>
            <span className="text-xs text-amber-400 font-medium">
              {analytics?.zero_result_queries?.length || 0} Content Gaps
            </span>
          </div>
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Sitemap Status</p>
            <p className="text-2xl font-bold text-white mt-1">Canonical</p>
            <span className="text-xs text-blue-400 font-medium">
              sitemaps.org XML Live
            </span>
          </div>
        </div>
      </div>

      {/* Sub-Tabs Navigation */}
      <div className="flex border-b border-slate-200 space-x-1 sm:space-x-4 overflow-x-auto no-scrollbar">
        <button
          onClick={() => setSubTab("menus")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            subTab === "menus"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <FolderTree className="w-4 h-4" /> Navigation Trees ({navItems.length})
        </button>
        <button
          onClick={() => setSubTab("quick_links")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            subTab === "quick_links"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Sparkles className="w-4 h-4" /> Quick Links ({quickLinks.length})
        </button>
        <button
          onClick={() => setSubTab("indexer")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            subTab === "indexer"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Search className="w-4 h-4" /> Search Re-indexer
        </button>
        <button
          onClick={() => setSubTab("analytics")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            subTab === "analytics"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <BarChart3 className="w-4 h-4" /> Query Analytics & Gaps
        </button>
        <button
          onClick={() => setSubTab("sitemap")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            subTab === "sitemap"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <FileCode className="w-4 h-4" /> Sitemap & SEO
        </button>
      </div>

      {/* Tab 1: Navigation Trees */}
      {subTab === "menus" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <span className="text-xs font-bold text-slate-500 uppercase">
                Location:
              </span>
              <select
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                className="border border-slate-300 rounded-xl px-3 py-1.5 text-xs font-semibold bg-white text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="HEADER_MAIN">Main Header (HEADER_MAIN)</option>
                <option value="FOOTER_COL_1">Footer Column 1</option>
                <option value="FOOTER_COL_2">Footer Column 2</option>
                <option value="FOOTER_COL_3">Footer Column 3</option>
              </select>
            </div>

            <button
              onClick={() => {
                resetNavForm();
                setIsNavModalOpen(true);
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Add Navigation Node
            </button>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-700">
                <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Menu Node / Title</th>
                    <th className="py-3 px-4">Target Path</th>
                    <th className="py-3 px-4">Megamenu & Badges</th>
                    <th className="py-3 px-4">Order</th>
                    <th className="py-3 px-4">Status</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {navLoading ? (
                    <tr>
                      <td colSpan={6} className="py-8 text-center text-slate-400">
                        Loading navigation nodes...
                      </td>
                    </tr>
                  ) : navItems.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="py-8 text-center text-slate-500">
                        No navigation nodes found for this location.
                      </td>
                    </tr>
                  ) : (
                    navItems.map((item) => (
                      <tr key={item.id} className="hover:bg-slate-50/80 transition">
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-2">
                            {item.parent_id && (
                              <span className="text-slate-300 font-mono pl-3">
                                └─
                              </span>
                            )}
                            <div>
                              <p className="font-bold text-slate-900">
                                {item.title}
                              </p>
                              {item.description && (
                                <p className="text-xs text-slate-400 line-clamp-1">
                                  {item.description}
                                </p>
                              )}
                            </div>
                          </div>
                        </td>
                        <td className="py-3 px-4 font-mono text-xs text-slate-600">
                          {item.path}
                        </td>
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-1.5 flex-wrap">
                            {item.is_mega_menu && (
                              <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-purple-100 text-purple-800">
                                Mega Menu
                              </span>
                            )}
                            {item.badge_text && (
                              <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-amber-100 text-amber-800">
                                {item.badge_text}
                              </span>
                            )}
                            {item.is_external && (
                              <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-blue-100 text-blue-800">
                                External
                              </span>
                            )}
                          </div>
                        </td>
                        <td className="py-3 px-4 text-xs font-semibold text-slate-500">
                          #{item.display_order}
                        </td>
                        <td className="py-3 px-4">
                          <span
                            className={`inline-flex items-center gap-1 text-xs font-semibold ${
                              item.is_active ? "text-emerald-600" : "text-slate-400"
                            }`}
                          >
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            {item.is_active ? "Active" : "Hidden"}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-right">
                          <button
                            onClick={() => {
                              if (confirm(`Delete menu item "${item.title}"?`)) {
                                deleteNavMutation.mutate(item.id);
                              }
                            }}
                            className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg transition"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Quick Links */}
      {subTab === "quick_links" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">
                High-Visibility Quick Links
              </h2>
              <p className="text-xs text-slate-500">
                Quick jump buttons featured across hero banners, sticky utility
                bars, and mobile menus.
              </p>
            </div>
            <button
              onClick={() => {
                resetQlForm();
                setIsQlModalOpen(true);
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Add Quick Link
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {quickLinks.map((ql) => (
              <div
                key={ql.id}
                className="bg-white rounded-xl p-5 border border-slate-200 shadow-2xs hover:shadow-md transition relative group space-y-3"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
                      <Sparkles className="w-4 h-4" />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900 text-sm">
                        {ql.title}
                      </h4>
                      <p className="font-mono text-[11px] text-slate-500">
                        {ql.path}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      if (confirm(`Delete quick link "${ql.title}"?`)) {
                        deleteQlMutation.mutate(ql.id);
                      }
                    }}
                    className="text-slate-400 hover:text-rose-600 p-1 transition"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <div className="flex items-center justify-between text-xs pt-2 border-t border-slate-100">
                  <div className="flex items-center gap-1.5">
                    {ql.badge_text && (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">
                        {ql.badge_text}
                      </span>
                    )}
                    {ql.is_highlighted && (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-700">
                        Highlighted
                      </span>
                    )}
                  </div>
                  <span className="text-slate-400 text-[11px]">
                    Order: #{ql.display_order}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Search Re-indexer */}
      {subTab === "indexer" && (
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="max-w-2xl space-y-2">
            <h2 className="text-xl font-bold text-slate-900">
              PostgreSQL Global Search Indexer
            </h2>
            <p className="text-sm text-slate-600 leading-relaxed">
              Crawls all relational models in the database (Courses, Faculty,
              Seminars, Press Releases, Circulars, Syllabus Downloads, and FAQs)
              and rebuilds the unified <code className="bg-slate-100 px-1.5 py-0.5 rounded font-mono text-xs">website_search_index</code> table
              for sub-millisecond keyword lookup.
            </p>
          </div>

          {reindexStatus && (
            <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 text-sm font-semibold flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
              <span>{reindexStatus}</span>
            </div>
          )}

          <div className="p-5 bg-slate-50 rounded-xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-bold text-slate-800 text-sm">
                  Trigger Full Search Catalog Re-index
                </p>
                <p className="text-xs text-slate-500">
                  Recommended after bulk uploading courses, publications, or notices.
                </p>
              </div>
              <button
                onClick={() => reindexMutation.mutate()}
                disabled={reindexMutation.isPending}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-bold transition shadow-sm disabled:opacity-50"
              >
                {reindexMutation.isPending ? (
                  <RefreshCw className="w-4 h-4 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4" />
                )}
                <span>Re-index Catalog Now</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Tab 4: Search Analytics & Content Gaps */}
      {subTab === "analytics" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Top 10 Search Queries */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-indigo-600" /> Top Campus Search Queries
              </h3>
              <div className="divide-y divide-slate-100">
                {analytics?.top_queries?.length ? (
                  analytics.top_queries.map((q, idx) => (
                    <div
                      key={idx}
                      className="py-2.5 flex items-center justify-between text-xs"
                    >
                      <span className="font-semibold text-slate-800">
                        #{idx + 1}. {q.query}
                      </span>
                      <span className="px-2 py-0.5 rounded-full bg-indigo-50 font-bold text-indigo-700">
                        {q.count} searches
                      </span>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-400 py-4">
                    No search queries logged yet.
                  </p>
                )}
              </div>
            </div>

            {/* Zero-Result Queries (Content Gaps) */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-amber-500" /> Zero-Result Queries (Content Gaps)
              </h3>
              <p className="text-xs text-slate-500">
                Terms prospective students searched for where 0 records matched.
                Use this to curate new FAQs or articles.
              </p>
              <div className="divide-y divide-slate-100">
                {analytics?.zero_result_queries?.length ? (
                  analytics.zero_result_queries.map((q, idx) => (
                    <div
                      key={idx}
                      className="py-2.5 flex items-center justify-between text-xs"
                    >
                      <span className="font-semibold text-rose-700">
                        "{q.query}"
                      </span>
                      <span className="px-2 py-0.5 rounded-full bg-rose-50 font-bold text-rose-700">
                        {q.count} missed
                      </span>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-400 py-4">
                    Zero content gaps detected!
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 5: Sitemap & SEO */}
      {subTab === "sitemap" && (
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="max-w-2xl space-y-2">
            <h2 className="text-xl font-bold text-slate-900">
              Sitemap & Search Engine Telemetry
            </h2>
            <p className="text-sm text-slate-600 leading-relaxed">
              Standardized XML and JSON sitemaps generated dynamically from live
              PostgreSQL database records for Google, Bing, and autonomous web crawlers.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-indigo-700 font-bold text-sm">
                  <FileCode className="w-5 h-5" /> Standard XML Sitemap
                </div>
                <span className="text-[10px] font-bold uppercase px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded">
                  Live
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Conforms to sitemaps.org schema with &lt;loc&gt;, &lt;lastmod&gt;,
                &lt;changefreq&gt;, and &lt;priority&gt;.
              </p>
              <a
                href="/api/v1/public/sitemap/xml"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 text-xs font-bold text-indigo-600 hover:text-indigo-800"
              >
                /api/v1/public/sitemap/xml <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>

            <div className="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-indigo-700 font-bold text-sm">
                  <Layers className="w-5 h-5" /> Structured JSON Sitemap
                </div>
                <span className="text-[10px] font-bold uppercase px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded">
                  Live
                </span>
              </div>
              <p className="text-xs text-slate-500">
                JSON API payload powering the public /sitemap interactive directory
                page and crawler bots.
              </p>
              <a
                href="/api/v1/public/sitemap/json"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 text-xs font-bold text-indigo-600 hover:text-indigo-800"
              >
                /api/v1/public/sitemap/json <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Add Navigation Modal */}
      {isNavModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Add Navigation Node
              </h3>
              <button
                onClick={() => setIsNavModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Menu Title *
                </label>
                <input
                  type="text"
                  placeholder="e.g. Research & Publications"
                  value={navForm.title}
                  onChange={(e) =>
                    setNavForm({ ...navForm, title: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Target Path *
                </label>
                <input
                  type="text"
                  placeholder="e.g. /faculty/research"
                  value={navForm.path}
                  onChange={(e) =>
                    setNavForm({ ...navForm, path: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Badge Text
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. NEW, AICTE"
                    value={navForm.badge_text}
                    onChange={(e) =>
                      setNavForm({ ...navForm, badge_text: e.target.value })
                    }
                    className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Display Order
                  </label>
                  <input
                    type="number"
                    value={navForm.display_order}
                    onChange={(e) =>
                      setNavForm({
                        ...navForm,
                        display_order: parseInt(e.target.value) || 1,
                      })
                    }
                    className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Subtitle / Description
                </label>
                <input
                  type="text"
                  placeholder="Megamenu tooltip or description"
                  value={navForm.description}
                  onChange={(e) =>
                    setNavForm({ ...navForm, description: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Parent Menu (Optional)
                </label>
                <select
                  value={navForm.parent_id || ""}
                  onChange={(e) =>
                    setNavForm({
                      ...navForm,
                      parent_id: e.target.value ? e.target.value : null,
                    })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                >
                  <option value="">None (Top-Level Node)</option>
                  {rootNavItems.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.title}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center gap-4 pt-1">
                <label className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold cursor-pointer">
                  <input
                    type="checkbox"
                    checked={navForm.is_mega_menu}
                    onChange={(e) =>
                      setNavForm({ ...navForm, is_mega_menu: e.target.checked })
                    }
                    className="w-4 h-4 text-indigo-600 rounded"
                  />
                  <span>Enable Megamenu Dropdown</span>
                </label>
                <label className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold cursor-pointer">
                  <input
                    type="checkbox"
                    checked={navForm.is_active}
                    onChange={(e) =>
                      setNavForm({ ...navForm, is_active: e.target.checked })
                    }
                    className="w-4 h-4 text-indigo-600 rounded"
                  />
                  <span>Active</span>
                </label>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsNavModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-sm font-semibold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!navForm.title || !navForm.path) {
                    alert("Please provide title and path");
                    return;
                  }
                  createNavMutation.mutate(navForm);
                }}
                disabled={createNavMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition"
              >
                Save Navigation Node
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Quick Link Modal */}
      {isQlModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Add Quick Link
              </h3>
              <button
                onClick={() => setIsQlModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Title *
                </label>
                <input
                  type="text"
                  placeholder="e.g. Fee Payment Desk"
                  value={qlForm.title}
                  onChange={(e) =>
                    setQlForm({ ...qlForm, title: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Path / URL *
                </label>
                <input
                  type="text"
                  placeholder="e.g. /admissions or https://portal..."
                  value={qlForm.path}
                  onChange={(e) =>
                    setQlForm({ ...qlForm, path: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Badge Text
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. LIVE, APPLY"
                    value={qlForm.badge_text}
                    onChange={(e) =>
                      setQlForm({ ...qlForm, badge_text: e.target.value })
                    }
                    className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Display Order
                  </label>
                  <input
                    type="number"
                    value={qlForm.display_order}
                    onChange={(e) =>
                      setQlForm({
                        ...qlForm,
                        display_order: parseInt(e.target.value) || 1,
                      })
                    }
                    className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                  />
                </div>
              </div>

              <div className="flex items-center gap-4 pt-1">
                <label className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold cursor-pointer">
                  <input
                    type="checkbox"
                    checked={qlForm.is_highlighted}
                    onChange={(e) =>
                      setQlForm({ ...qlForm, is_highlighted: e.target.checked })
                    }
                    className="w-4 h-4 text-indigo-600 rounded"
                  />
                  <span>Highlight on Hero Banner</span>
                </label>
                <label className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold cursor-pointer">
                  <input
                    type="checkbox"
                    checked={qlForm.is_active}
                    onChange={(e) =>
                      setQlForm({ ...qlForm, is_active: e.target.checked })
                    }
                    className="w-4 h-4 text-indigo-600 rounded"
                  />
                  <span>Active</span>
                </label>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsQlModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-sm font-semibold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!qlForm.title || !qlForm.path) {
                    alert("Please provide title and path");
                    return;
                  }
                  createQlMutation.mutate(qlForm);
                }}
                disabled={createQlMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition"
              >
                Save Quick Link
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
