import React, { useState, useMemo } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  BookOpen,
  Search,
  Filter,
  GraduationCap,
  Clock,
  IndianRupee,
  Users,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  SlidersHorizontal,
  RotateCcw,
  Building2,
  ChevronRight,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsCourseCategory,
  CmsCourseSummary,
  PublicCoursesBundle,
} from "@/types/website.types";

const FALLBACK_COURSES_BUNDLE: PublicCoursesBundle = {
  categories: [
    {
      id: "cat-1",
      institute_id: "default-inst",
      name: "Engineering & Technology",
      slug: "engineering-technology",
      description: "NBA Tier-1 accredited autonomous engineering programs with high-performance labs.",
      icon_name: "Cpu",
      display_order: 1,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "cat-2",
      institute_id: "default-inst",
      name: "Computer Applications & AI",
      slug: "computer-applications-ai",
      description: "Next-gen computing, machine learning, and cloud native architectures.",
      icon_name: "Terminal",
      display_order: 2,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "cat-3",
      institute_id: "default-inst",
      name: "Management & Business",
      slug: "management-business",
      description: "Executive leadership, business analytics, and digital technology commercialization.",
      icon_name: "Briefcase",
      display_order: 3,
      is_active: true,
      created_at: new Date().toISOString(),
    },
  ],
  courses: [
    {
      id: "c-1",
      institute_id: "default-inst",
      category_id: "cat-1",
      code: "BTECH-CSE",
      slug: "b-tech-computer-science-engineering",
      title: "B.Tech in Computer Science & Engineering (AI & ML)",
      short_name: "B.Tech CSE",
      degree_level: "UNDERGRADUATE",
      duration: "4 Years (8 Semesters)",
      study_mode: "Full-Time On-Campus",
      annual_fee: "₹1,25,000 / Year",
      total_fee: "₹5,00,000",
      seats_intake: 120,
      eligibility_summary: "10+2 with Physics, Mathematics & Chemistry/CS (min 60%) + valid JEE/CET rank.",
      summary: "NBA Tier-1 accredited autonomous flagship program featuring high-density AI computing and modern distributed architectures.",
      image_url: null,
      is_admissions_open: true,
      is_featured: true,
      display_order: 1,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "c-2",
      institute_id: "default-inst",
      category_id: "cat-1",
      code: "BTECH-ECE",
      slug: "b-tech-electronics-communication-engineering",
      title: "B.Tech in Electronics & Communication Engineering (VLSI & IoT)",
      short_name: "B.Tech ECE",
      degree_level: "UNDERGRADUATE",
      duration: "4 Years (8 Semesters)",
      study_mode: "Full-Time On-Campus",
      annual_fee: "₹1,10,000 / Year",
      total_fee: "₹4,40,000",
      seats_intake: 60,
      eligibility_summary: "10+2 with Physics and Mathematics (min 55%).",
      summary: "Specialized focus on VLSI design, semiconductor hardware, and smart sensor IoT networks.",
      image_url: null,
      is_admissions_open: true,
      is_featured: true,
      display_order: 2,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "c-3",
      institute_id: "default-inst",
      category_id: "cat-3",
      code: "MBA-TECH",
      slug: "mba-technology-business-management",
      title: "Master of Business Administration (Tech Leadership & Analytics)",
      short_name: "MBA Tech",
      degree_level: "POSTGRADUATE",
      duration: "2 Years (4 Semesters)",
      study_mode: "Full-Time On-Campus",
      annual_fee: "₹1,40,000 / Year",
      total_fee: "₹2,80,000",
      seats_intake: 60,
      eligibility_summary: "Bachelor degree in any discipline (min 50%) + CAT/MAT/CMAT score.",
      summary: "Executive postgraduate curriculum bridging technology innovation with strategic business analytics.",
      image_url: null,
      is_admissions_open: true,
      is_featured: true,
      display_order: 3,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "c-4",
      institute_id: "default-inst",
      category_id: "cat-2",
      code: "BCA-AI",
      slug: "bca-artificial-intelligence-cloud",
      title: "Bachelor of Computer Applications (AI & Cloud Systems)",
      short_name: "BCA AI",
      degree_level: "UNDERGRADUATE",
      duration: "3 Years (6 Semesters)",
      study_mode: "Full-Time On-Campus",
      annual_fee: "₹75,000 / Year",
      total_fee: "₹2,25,000",
      seats_intake: 90,
      eligibility_summary: "10+2 with Mathematics or Computer Science (min 50%).",
      summary: "Hands-on software development program focusing on cloud architectures, DevOps, and machine learning models.",
      image_url: null,
      is_admissions_open: true,
      is_featured: false,
      display_order: 4,
      is_active: true,
      created_at: new Date().toISOString(),
    },
  ],
  featured_courses: [],
  total_courses: 4,
};

export const PublicCoursesPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const [searchQuery, setSearchQuery] = useState(searchParams.get("q") || "");
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get("category") || "ALL");
  const [selectedDegree, setSelectedDegree] = useState(searchParams.get("level") || "ALL");

  const { data: coursesBundle, isLoading } = useQuery<PublicCoursesBundle>({
    queryKey: ["public-courses-bundle"],
    queryFn: () => websiteService.getPublicCoursesBundle(),
    staleTime: 1000 * 60 * 5,
  });

  const bundle = coursesBundle || FALLBACK_COURSES_BUNDLE;

  // Filter courses in memory for instantaneous UX
  const filteredCourses = useMemo(() => {
    return bundle.courses.filter((c) => {
      // 1. Category Filter
      if (selectedCategory !== "ALL") {
        const cat = bundle.categories.find((cat) => cat.slug === selectedCategory);
        if (cat && c.category_id !== cat.id) return false;
      }

      // 2. Degree Level Filter
      if (selectedDegree !== "ALL" && c.degree_level !== selectedDegree) {
        return false;
      }

      // 3. Search Query Filter
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        const matchesTitle = c.title.toLowerCase().includes(q);
        const matchesCode = c.code.toLowerCase().includes(q);
        const matchesSummary = c.summary.toLowerCase().includes(q);
        const matchesShort = c.short_name.toLowerCase().includes(q);
        if (!matchesTitle && !matchesCode && !matchesSummary && !matchesShort) {
          return false;
        }
      }

      return true;
    });
  }, [bundle, selectedCategory, selectedDegree, searchQuery]);

  const handleResetFilters = () => {
    setSearchQuery("");
    setSelectedCategory("ALL");
    setSelectedDegree("ALL");
    setSearchParams({});
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* 1. Header Banner */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-brand-950 to-blue-900 text-white py-14 lg:py-20">
        <div className="absolute inset-0 opacity-15">
          <div className="absolute -top-32 -right-32 h-96 w-96 rounded-full bg-blue-500 blur-3xl pointer-events-none" />
          <div className="absolute -bottom-32 -left-32 h-96 w-96 rounded-full bg-brand-400 blur-3xl pointer-events-none" />
        </div>

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-300 mb-4">
            <Link to="/" className="hover:text-white transition-colors">
              Home
            </Link>
            <ChevronRight className="h-3 w-3" />
            <span>Academic Programs</span>
            <ChevronRight className="h-3 w-3" />
            <span className="text-white">Degree Directory</span>
          </div>

          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-blue-400/30 bg-blue-500/10 px-3.5 py-1 text-xs font-semibold text-blue-200 mb-5 backdrop-blur-xs">
              <Sparkles className="h-3.5 w-3.5 text-blue-300" />
              <span>AICTE & UGC Autonomous Approved Curricula • Session 2026-27</span>
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl lg:text-5xl text-white">
              Academic Degree Programs & Specialized Disciplines
            </h1>
            <p className="mt-4 text-base sm:text-lg text-slate-300 leading-relaxed">
              Explore our outcome-based curricula benchmarked with national accreditation standards.
              Every degree program is supported by hands-on laboratories, research mentorship, and
              verified placement pipelines.
            </p>
          </div>

          {/* Search Box in Hero */}
          <div className="mt-8 max-w-2xl">
            <div className="relative flex items-center">
              <Search className="absolute left-4 h-5 w-5 text-slate-400 pointer-events-none" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by degree title, code (e.g. BTECH-CSE), or specialization..."
                className="w-full rounded-2xl border-2 border-white/20 bg-white/10 px-12 py-3.5 text-sm font-medium text-white placeholder-slate-400 backdrop-blur-md focus:border-brand-400 focus:bg-white/20 focus:outline-hidden transition"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery("")}
                  className="absolute right-4 text-xs font-semibold text-slate-400 hover:text-white"
                >
                  Clear
                </button>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* 2. Filter Navigation Bar */}
      <section className="sticky top-16 z-20 border-b border-slate-200 bg-white/95 backdrop-blur-md shadow-xs">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            {/* Category Pills */}
            <div className="flex items-center space-x-1.5 overflow-x-auto no-scrollbar py-1">
              <button
                type="button"
                onClick={() => setSelectedCategory("ALL")}
                className={`shrink-0 rounded-lg px-3.5 py-1.5 text-xs font-bold transition-all ${
                  selectedCategory === "ALL"
                    ? "bg-brand-600 text-white shadow-2xs"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900"
                }`}
              >
                All Faculties ({bundle.courses.length})
              </button>
              {bundle.categories
                .filter((c) => c.is_active)
                .map((cat) => (
                  <button
                    key={cat.id}
                    type="button"
                    onClick={() => setSelectedCategory(cat.slug)}
                    className={`shrink-0 rounded-lg px-3.5 py-1.5 text-xs font-bold transition-all ${
                      selectedCategory === cat.slug
                        ? "bg-brand-600 text-white shadow-2xs"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900"
                    }`}
                  >
                    {cat.name}
                  </button>
                ))}
            </div>

            {/* Level Selector & Reset */}
            <div className="flex items-center gap-2 shrink-0">
              <div className="flex items-center gap-1.5 bg-slate-100 rounded-lg p-1 text-xs">
                <button
                  type="button"
                  onClick={() => setSelectedDegree("ALL")}
                  className={`rounded-md px-2.5 py-1 font-semibold transition ${
                    selectedDegree === "ALL" ? "bg-white text-slate-900 shadow-2xs" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  All Levels
                </button>
                <button
                  type="button"
                  onClick={() => setSelectedDegree("UNDERGRADUATE")}
                  className={`rounded-md px-2.5 py-1 font-semibold transition ${
                    selectedDegree === "UNDERGRADUATE" ? "bg-white text-slate-900 shadow-2xs" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  UG
                </button>
                <button
                  type="button"
                  onClick={() => setSelectedDegree("POSTGRADUATE")}
                  className={`rounded-md px-2.5 py-1 font-semibold transition ${
                    selectedDegree === "POSTGRADUATE" ? "bg-white text-slate-900 shadow-2xs" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  PG
                </button>
              </div>

              {(selectedCategory !== "ALL" || selectedDegree !== "ALL" || searchQuery) && (
                <button
                  type="button"
                  onClick={handleResetFilters}
                  className="flex items-center gap-1 text-xs font-semibold text-rose-600 hover:text-rose-800 p-1.5"
                  title="Reset all filters"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  <span>Reset</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* 3. Main Course Catalog Grid */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex items-center justify-between mb-6">
          <div className="text-xs sm:text-sm font-semibold text-slate-500">
            Showing <span className="font-bold text-slate-900">{filteredCourses.length}</span> verified degree programs
          </div>
          {bundle.total_courses > 0 && (
            <div className="text-xs text-brand-700 font-bold bg-brand-50 px-2.5 py-1 rounded-md">
              Admissions Open 2026–27
            </div>
          )}
        </div>

        {filteredCourses.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center">
            <BookOpen className="mx-auto h-12 w-12 text-slate-400 mb-3" />
            <h3 className="text-base font-bold text-slate-800">No matching degree programs found</h3>
            <p className="mt-1 text-xs sm:text-sm text-slate-500 max-w-md mx-auto">
              We couldn&apos;t find any programs matching your current filter criteria. Try adjusting your
              search term or clearing the filters.
            </p>
            <button
              type="button"
              onClick={handleResetFilters}
              className="mt-5 inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              <span>Reset All Filters</span>
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredCourses.map((course) => (
              <div
                key={course.id}
                className="group flex flex-col justify-between overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xs hover:shadow-md hover:border-brand-300 transition-all"
              >
                <div>
                  {/* Card Header Top Badges */}
                  <div className="border-b border-slate-100 bg-slate-50/50 p-4 flex items-center justify-between">
                    <span className="rounded-md bg-brand-100 px-2.5 py-0.5 text-xs font-mono font-bold text-brand-800">
                      {course.code}
                    </span>
                    <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800 uppercase">
                      {course.degree_level}
                    </span>
                  </div>

                  {/* Card Content Body */}
                  <div className="p-6 space-y-4">
                    <div>
                      <h3 className="text-base font-bold text-slate-900 group-hover:text-brand-600 transition-colors line-clamp-2">
                        {course.title}
                      </h3>
                      <p className="mt-2 text-xs text-slate-600 line-clamp-3 leading-relaxed">
                        {course.summary}
                      </p>
                    </div>

                    {/* Metric Quick Stats */}
                    <div className="grid grid-cols-2 gap-2 rounded-xl bg-slate-50 p-3 text-xs">
                      <div className="flex items-center gap-1.5 text-slate-600">
                        <Clock className="h-3.5 w-3.5 text-brand-600 shrink-0" />
                        <span className="truncate">{course.duration}</span>
                      </div>
                      <div className="flex items-center gap-1.5 text-slate-600">
                        <Users className="h-3.5 w-3.5 text-brand-600 shrink-0" />
                        <span>{course.seats_intake} Seats</span>
                      </div>
                      <div className="flex items-center gap-1.5 text-slate-900 font-bold col-span-2 pt-1 border-t border-slate-200/60">
                        <IndianRupee className="h-3.5 w-3.5 text-emerald-600 shrink-0" />
                        <span>Annual Fee: {course.annual_fee}</span>
                      </div>
                    </div>

                    {/* Eligibility Snippet */}
                    <div className="text-[11px] text-slate-500 bg-blue-50/50 rounded-lg p-2.5 border border-blue-100/50">
                      <strong className="text-slate-700">Eligibility:</strong> {course.eligibility_summary}
                    </div>
                  </div>
                </div>

                {/* Card Footer CTAs */}
                <div className="border-t border-slate-100 bg-white p-4 flex items-center justify-between gap-3">
                  <Link
                    to={`/courses/${course.slug}`}
                    className="inline-flex items-center gap-1 text-xs font-bold text-brand-600 hover:text-brand-800 transition"
                  >
                    <span>View Curriculum</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Link>

                  <Link
                    to={`/admissions/apply?course=${encodeURIComponent(course.code)}`}
                    className="rounded-lg bg-brand-600 px-3 py-1.5 text-xs font-bold text-white shadow-2xs hover:bg-brand-700 transition"
                  >
                    Apply Now
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};
