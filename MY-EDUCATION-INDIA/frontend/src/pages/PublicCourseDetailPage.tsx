import React, { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  BookOpen,
  Calendar,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Clock,
  Compass,
  Download,
  FileText,
  GraduationCap,
  HelpCircle,
  IndianRupee,
  Layers,
  MapPin,
  Share2,
  Sparkles,
  UserCheck,
  Users,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import { CmsCourseDetail } from "@/types/website.types";

const FALLBACK_COURSE_DETAIL: CmsCourseDetail = {
  id: "default-course",
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
  eligibility_summary:
    "10+2 with Physics, Mathematics & Chemistry/CS with minimum 60% aggregate and valid JEE/State CET rank.",
  admission_process:
    "Admissions are conducted through Centralized State Counseling based on entrance rankings. Institute level quota seats are allocated via direct merit counseling followed by biometric verification.",
  career_prospects:
    "Graduates are recruited by leading technology organizations as AI Research Engineers, Cloud Architects, Distributed Systems Specialists, Full-Stack Engineers, and Cyber Security Consultants.",
  summary:
    "NBA Tier-1 accredited autonomous 4-year engineering curriculum integrating artificial intelligence, cloud architectures, and algorithmic optimization.",
  overview:
    "The Bachelor of Technology in Computer Science and Engineering with specialization in Artificial Intelligence and Machine Learning prepares tomorrow's engineers to tackle complex algorithmic problems. Supported by state-of-the-art computational infrastructure, high-density CBT examination pipelines, and corporate research alliances, scholars gain deep theoretical foundations and extensive laboratory practice across 8 comprehensive semesters.",
  image_url: null,
  brochure_pdf_url: null,
  syllabus_pdf_url: null,
  is_admissions_open: true,
  is_featured: true,
  display_order: 1,
  is_active: true,
  created_at: new Date().toISOString(),
  curricula: [
    {
      id: "sem-1",
      course_id: "default-course",
      semester_number: 1,
      semester_title: "Semester I: Computational Foundations",
      credits: 22,
      subjects: [
        { code: "CS101", title: "Programming & Problem Solving via Python", credits: 4, type: "Core" },
        { code: "MA101", title: "Discrete Mathematics & Linear Algebra", credits: 4, type: "Core" },
        { code: "PH101", title: "Engineering Physics & Applied Optics", credits: 4, type: "Core + Lab" },
        { code: "EE101", title: "Basic Electrical & Electronics Engineering", credits: 4, type: "Core" },
        { code: "EN101", title: "Professional Technical Communication & Ethics", credits: 2, type: "Soft Skills" },
        { code: "CS102", title: "Linux Systems & Cloud Shell Laboratory", credits: 4, type: "Lab" },
      ],
      display_order: 1,
      created_at: new Date().toISOString(),
    },
    {
      id: "sem-2",
      course_id: "default-course",
      semester_number: 2,
      semester_title: "Semester II: Data Structures & Core Computing",
      credits: 24,
      subjects: [
        { code: "CS201", title: "Data Structures & Algorithm Design", credits: 4, type: "Core" },
        { code: "CS202", title: "Object Oriented Programming via Modern C++", credits: 4, type: "Core" },
        { code: "MA201", title: "Probability & Statistical Inference", credits: 4, type: "Core" },
        { code: "CS203", title: "Digital Logic & Computer Organization", credits: 4, type: "Core" },
        { code: "CS204", title: "Data Structures Implementation Laboratory", credits: 4, type: "Lab" },
        { code: "CS205", title: "Open Source Engineering Capstone Project I", credits: 4, type: "Project" },
      ],
      display_order: 2,
      created_at: new Date().toISOString(),
    },
    {
      id: "sem-3",
      course_id: "default-course",
      semester_number: 3,
      semester_title: "Semester III: Artificial Intelligence & Cloud Platforms",
      credits: 24,
      subjects: [
        { code: "CS301", title: "Foundations of Artificial Intelligence & Search", credits: 4, type: "Core" },
        { code: "CS302", title: "Database Engineering & Distributed Stores", credits: 4, type: "Core" },
        { code: "CS303", title: "Operating Systems Principles & Concurrency", credits: 4, type: "Core" },
        { code: "CS304", title: "Computer Networks & Protocol Architectures", credits: 4, type: "Core" },
        { code: "CS305", title: "AI Modeling & Neural Frameworks Lab", credits: 4, type: "Lab" },
        { code: "CS306", title: "Database Administration & SQL Benchmarking Lab", credits: 4, type: "Lab" },
      ],
      display_order: 3,
      created_at: new Date().toISOString(),
    },
  ],
  faculty_members: [
    {
      id: "fac-1",
      course_id: "default-course",
      faculty_name: "Prof. (Dr.) Arvind Mehta",
      designation: "Professor & Head of Department",
      qualifications: "Ph.D. (IIT Bombay), M.Tech (CSE)",
      specialization: "Machine Learning, Distributed Systems, High-Performance Computing",
      avatar_url: null,
      display_order: 1,
      created_at: new Date().toISOString(),
    },
    {
      id: "fac-2",
      course_id: "default-course",
      faculty_name: "Dr. Priya Nambiar",
      designation: "Associate Professor",
      qualifications: "Ph.D. (BITS Pilani), M.E. (Software Engineering)",
      specialization: "Cloud-Native Architectures, Kubernetes, Microservices",
      avatar_url: null,
      display_order: 2,
      created_at: new Date().toISOString(),
    },
    {
      id: "fac-3",
      course_id: "default-course",
      faculty_name: "Prof. Rajesh K. Verma",
      designation: "Assistant Professor",
      qualifications: "M.Tech (IISc Bangalore), B.Tech (NIT Bhopal)",
      specialization: "Natural Language Processing, Deep Learning Algorithms",
      avatar_url: null,
      display_order: 3,
      created_at: new Date().toISOString(),
    },
  ],
};

export const PublicCourseDetailPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [activeTab, setActiveTab] = useState<"overview" | "curriculum" | "faculty" | "admission">(
    "overview"
  );
  const [expandedSemesters, setExpandedSemesters] = useState<Record<number, boolean>>({
    1: true,
    2: true,
  });

  const { data: courseData, isLoading } = useQuery<CmsCourseDetail>({
    queryKey: ["public-course-detail", slug],
    queryFn: () => websiteService.getPublicCourseDetail(slug || ""),
    enabled: !!slug,
    staleTime: 1000 * 60 * 5,
  });

  const course = courseData || FALLBACK_COURSE_DETAIL;

  const toggleSemester = (semNum: number) => {
    setExpandedSemesters((prev) => ({
      ...prev,
      [semNum]: !prev[semNum],
    }));
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* 1. Header Banner */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-brand-950 to-blue-900 text-white py-12 lg:py-16">
        <div className="absolute inset-0 opacity-15">
          <div className="absolute -top-32 -right-32 h-96 w-96 rounded-full bg-blue-500 blur-3xl pointer-events-none" />
        </div>

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {/* Breadcrumbs */}
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-300 mb-4">
            <Link to="/" className="hover:text-white transition-colors">
              Home
            </Link>
            <ChevronRight className="h-3 w-3" />
            <Link to="/courses" className="hover:text-white transition-colors">
              Courses
            </Link>
            <ChevronRight className="h-3 w-3" />
            <span className="text-white truncate max-w-xs">{course.short_name}</span>
          </div>

          <div className="grid grid-cols-1 gap-8 lg:grid-cols-12 items-center">
            <div className="lg:col-span-8 space-y-4">
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-md bg-blue-500/20 px-3 py-1 font-mono text-xs font-bold text-blue-300 border border-blue-400/30">
                  {course.code}
                </span>
                <span className="rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-bold text-emerald-300 border border-emerald-400/30 uppercase">
                  {course.degree_level}
                </span>
                <span className="rounded-full bg-brand-500/20 px-3 py-1 text-xs font-semibold text-brand-200 border border-brand-400/30">
                  Autonomous Curriculum
                </span>
              </div>

              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-white tracking-tight">
                {course.title}
              </h1>

              <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed">
                {course.summary}
              </p>

              <div className="flex flex-wrap items-center gap-4 pt-4">
                <Link
                  to={`/admissions/apply?course=${encodeURIComponent(course.code)}`}
                  className="rounded-xl bg-white px-6 py-3 text-xs font-bold text-brand-900 shadow-md hover:bg-slate-100 transition"
                >
                  Apply for Admission 2026
                </Link>
                <a
                  href="#curriculum"
                  onClick={() => setActiveTab("curriculum")}
                  className="rounded-xl border border-white/30 bg-white/10 px-5 py-3 text-xs font-bold text-white hover:bg-white/20 transition backdrop-blur-xs"
                >
                  Inspect Curriculum
                </a>
              </div>
            </div>

            {/* Quick Hero Metric */}
            <div className="lg:col-span-4 rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md">
              <h3 className="text-xs font-bold uppercase tracking-wider text-blue-300 mb-4">
                Program Snapshot
              </h3>
              <dl className="space-y-3 text-xs sm:text-sm">
                <div className="flex justify-between border-b border-white/10 pb-2">
                  <dt className="text-slate-400">Duration</dt>
                  <dd className="font-semibold text-white">{course.duration}</dd>
                </div>
                <div className="flex justify-between border-b border-white/10 pb-2">
                  <dt className="text-slate-400">Annual Tuition</dt>
                  <dd className="font-bold text-emerald-400">{course.annual_fee}</dd>
                </div>
                <div className="flex justify-between border-b border-white/10 pb-2">
                  <dt className="text-slate-400">Sanctioned Seats</dt>
                  <dd className="font-semibold text-white">{course.seats_intake} Intake</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-400">Delivery Mode</dt>
                  <dd className="font-semibold text-white">{course.study_mode}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </section>

      {/* 2. In-Page Tab Navigation */}
      <nav className="sticky top-16 z-20 border-b border-slate-200 bg-white/95 backdrop-blur-md shadow-xs">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1 overflow-x-auto py-2.5 no-scrollbar">
            <button
              onClick={() => setActiveTab("overview")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition ${
                activeTab === "overview"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <FileText className="h-4 w-4" />
              Program Overview
            </button>
            <button
              onClick={() => setActiveTab("curriculum")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition ${
                activeTab === "curriculum"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Layers className="h-4 w-4" />
              Semester Curriculum ({course.curricula.length})
            </button>
            <button
              onClick={() => setActiveTab("faculty")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition ${
                activeTab === "faculty"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Users className="h-4 w-4" />
              Faculty Mentors ({course.faculty_members.length})
            </button>
            <button
              onClick={() => setActiveTab("admission")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition ${
                activeTab === "admission"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <CheckCircle2 className="h-4 w-4" />
              Eligibility & Admission
            </button>
          </div>
        </div>
      </nav>

      {/* 3. Main Body Container with Sidebar */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 gap-10 lg:grid-cols-12">
          {/* Main Left Content Column */}
          <div className="lg:col-span-8 space-y-10">
            {/* TAB 1: OVERVIEW */}
            {activeTab === "overview" && (
              <div className="space-y-8 animate-fadeIn">
                <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs space-y-4">
                  <h2 className="text-xl font-bold text-slate-900">Academic Overview</h2>
                  <div className="text-xs sm:text-sm text-slate-600 leading-relaxed whitespace-pre-line space-y-3">
                    {course.overview}
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs space-y-4">
                  <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                    <Compass className="h-5 w-5 text-brand-600" />
                    Career Pathways & Placement Opportunities
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                    {course.career_prospects}
                  </p>
                  <div className="mt-4 rounded-xl bg-slate-50 p-4 border border-slate-100">
                    <div className="text-xs font-bold text-slate-800 mb-2">Key Recruiting Domains:</div>
                    <div className="flex flex-wrap gap-2">
                      <span className="rounded-md bg-white border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-700">
                        Artificial Intelligence & Deep Learning
                      </span>
                      <span className="rounded-md bg-white border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-700">
                        Cloud Native & DevOps Engineering
                      </span>
                      <span className="rounded-md bg-white border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-700">
                        Distributed Enterprise Systems
                      </span>
                      <span className="rounded-md bg-white border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-700">
                        Cyber Security & Systems Auditing
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 2: CURRICULUM */}
            {activeTab === "curriculum" && (
              <div className="space-y-6 animate-fadeIn" id="curriculum">
                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
                    <div>
                      <h2 className="text-xl font-bold text-slate-900">Semester-wise Curriculum Structure</h2>
                      <p className="text-xs text-slate-500 mt-0.5">
                        Outcome-based education framework benchmarked with NBA Tier-1 guidelines.
                      </p>
                    </div>
                    <div className="text-xs font-bold text-brand-700 bg-brand-50 px-3 py-1.5 rounded-lg w-fit">
                      Total Credits: 180+
                    </div>
                  </div>

                  <div className="space-y-4">
                    {course.curricula.map((curr) => {
                      const isExpanded = expandedSemesters[curr.semester_number] ?? false;
                      return (
                        <div
                          key={curr.id}
                          className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-2xs"
                        >
                          <button
                            type="button"
                            onClick={() => toggleSemester(curr.semester_number)}
                            className="flex w-full items-center justify-between bg-slate-50/80 px-5 py-3.5 text-left text-xs sm:text-sm font-bold text-slate-900 hover:bg-slate-100 transition"
                          >
                            <div className="flex items-center gap-3">
                              <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-brand-600 font-extrabold text-white text-xs">
                                {curr.semester_number}
                              </span>
                              <span>{curr.semester_title}</span>
                              <span className="rounded-md bg-blue-100 px-2 py-0.5 text-[11px] font-bold text-brand-800">
                                {curr.credits} Credits
                              </span>
                            </div>
                            <ChevronDown
                              className={`h-4 w-4 text-slate-500 transition-transform ${
                                isExpanded ? "rotate-180" : ""
                              }`}
                            />
                          </button>

                          {isExpanded && (
                            <div className="p-4 sm:p-5 border-t border-slate-200/60 divide-y divide-slate-100">
                              {curr.subjects.map((sub, sIdx) => (
                                <div
                                  key={sIdx}
                                  className="py-2.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 text-xs"
                                >
                                  <div className="flex items-center gap-3">
                                    <span className="font-mono font-bold text-brand-700 w-16 shrink-0">
                                      {sub.code}
                                    </span>
                                    <span className="font-semibold text-slate-800">{sub.title}</span>
                                  </div>
                                  <div className="flex items-center gap-2 shrink-0">
                                    <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-600">
                                      {sub.type}
                                    </span>
                                    <span className="font-bold text-slate-700">{sub.credits} Credits</span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {/* TAB 3: FACULTY MENTORS */}
            {activeTab === "faculty" && (
              <div className="space-y-6 animate-fadeIn">
                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
                  <h2 className="text-xl font-bold text-slate-900 mb-1">Faculty & Academic Directorate</h2>
                  <p className="text-xs text-slate-500 mb-6">
                    Our programs are led by distinguished professors holding doctoral degrees from premier
                    institutions.
                  </p>

                  <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                    {course.faculty_members.map((fac) => (
                      <div
                        key={fac.id}
                        className="rounded-xl border border-slate-200 bg-slate-50/50 p-5 space-y-3"
                      >
                        <div className="flex items-center gap-3">
                          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-100 text-brand-700 font-extrabold text-base">
                            {fac.faculty_name.charAt(0)}
                          </div>
                          <div>
                            <h4 className="text-sm font-bold text-slate-900">{fac.faculty_name}</h4>
                            <p className="text-xs text-brand-600 font-semibold">{fac.designation}</p>
                          </div>
                        </div>
                        <div className="text-xs text-slate-600 border-t border-slate-200/60 pt-2 space-y-1">
                          <div>
                            <strong className="text-slate-800">Qualifications:</strong> {fac.qualifications}
                          </div>
                          <div>
                            <strong className="text-slate-800">Specialization:</strong> {fac.specialization}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* TAB 4: ELIGIBILITY & ADMISSION */}
            {activeTab === "admission" && (
              <div className="space-y-6 animate-fadeIn">
                <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-slate-900 mb-2">Eligibility Criteria</h2>
                    <div className="rounded-xl bg-blue-50/60 p-4 border border-blue-100 text-xs sm:text-sm text-slate-700 leading-relaxed">
                      {course.eligibility_summary}
                    </div>
                  </div>

                  <div>
                    <h2 className="text-xl font-bold text-slate-900 mb-2">Admission Process & Counseling</h2>
                    <p className="text-xs sm:text-sm text-slate-600 leading-relaxed whitespace-pre-line">
                      {course.admission_process}
                    </p>
                  </div>

                  <div className="border-t border-slate-100 pt-6">
                    <Link
                      to={`/admissions/apply?course=${encodeURIComponent(course.code)}`}
                      className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-6 py-3 text-xs font-bold text-white shadow-md hover:bg-brand-700 transition"
                    >
                      <span>Proceed to Online Application</span>
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Sticky Sidebar Right Column */}
          <div className="lg:col-span-4 space-y-6">
            <div className="sticky top-32 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-6">
              <div className="border-b border-slate-100 pb-4">
                <div className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Annual Fee</div>
                <div className="text-2xl font-extrabold text-slate-900 mt-1">{course.annual_fee}</div>
                {course.total_fee && (
                  <div className="text-xs text-slate-500 mt-0.5">Total Estimated Course Fee: {course.total_fee}</div>
                )}
              </div>

              <div className="space-y-3 text-xs">
                <div className="flex justify-between border-b border-slate-100 pb-2">
                  <span className="text-slate-500">Degree Level</span>
                  <span className="font-semibold text-slate-800">{course.degree_level}</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-2">
                  <span className="text-slate-500">Duration</span>
                  <span className="font-semibold text-slate-800">{course.duration}</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-2">
                  <span className="text-slate-500">Mode</span>
                  <span className="font-semibold text-slate-800">{course.study_mode}</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-2">
                  <span className="text-slate-500">Intake Seats</span>
                  <span className="font-semibold text-slate-800">{course.seats_intake}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Admissions Status</span>
                  <span className="font-bold text-emerald-600">Open for 2026-27</span>
                </div>
              </div>

              <div className="space-y-2.5 pt-2">
                <Link
                  to={`/admissions/apply?course=${encodeURIComponent(course.code)}`}
                  className="block w-full text-center rounded-xl bg-brand-600 px-4 py-3 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
                >
                  Apply for Admission
                </Link>

                <Link
                  to="/contact"
                  className="block w-full text-center rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
                >
                  Request Program Syllabus
                </Link>
              </div>

              <div className="rounded-xl bg-slate-50 p-4 border border-slate-100 text-[11px] text-slate-500 space-y-1">
                <div className="font-bold text-slate-700">Need Guidance?</div>
                <div>Contact Admissions Helpline at Indore campus:</div>
                <div className="font-mono text-brand-600 font-bold">+91 (0731) 4900-100</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
