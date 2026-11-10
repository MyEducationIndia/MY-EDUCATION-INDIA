import React, { useState, useEffect } from "react";
import { Link, useOutletContext } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import {
  BookOpen,
  Award,
  GraduationCap,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Building2,
  Users,
  ChevronLeft,
  ChevronRight,
  Star,
  Layers,
  FileText,
  IndianRupee,
  Clock,
  Sparkles,
  ExternalLink,
  Mail,
  Send,
  HelpCircle,
  TrendingUp,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  PublicHomePageBundle,
  PublicWebsiteFrameworkBundle,
} from "@/types/website.types";

interface ContextType {
  bundle?: PublicWebsiteFrameworkBundle;
}

const FALLBACK_HOME_BUNDLE: PublicHomePageBundle = {
  hero_slides: [
    {
      id: "slide-1",
      institute_id: "default-inst",
      badge_text: "National Entrance Examination 2026",
      title: "Shaping Global Leaders in Technology, Management & Sciences",
      subtitle:
        "Join India's premier autonomous flagship institution at Indore. Accredited curricula, AI-powered CBT examinations, and verified digital credentials.",
      background_image_url: null,
      video_url: null,
      primary_cta_text: "Apply for Admission 2026",
      primary_cta_link: "/admissions/apply",
      secondary_cta_text: "Explore Degree Programs",
      secondary_cta_link: "/courses",
      display_order: 1,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "slide-2",
      institute_id: "default-inst",
      badge_text: "Autonomous Research Excellence",
      title: "World-Class Infrastructure & Innovation Labs",
      subtitle:
        "Experience high-performance computing, advanced research incubation, and seamless student-lifecycle administration on a modern digital campus.",
      background_image_url: null,
      video_url: null,
      primary_cta_text: "Take Virtual Campus Tour",
      primary_cta_link: "/about",
      secondary_cta_text: "Placement Records",
      secondary_cta_link: "/placements",
      display_order: 2,
      is_active: true,
      created_at: new Date().toISOString(),
    },
  ],
  stat_counters: [
    {
      id: "stat-1",
      institute_id: "default-inst",
      metric_value: "37+",
      numeric_target: 37,
      label: "Integrated Subsystems",
      subtext: "Real-Time Cloud ERP Architecture",
      icon_name: "Layers",
      display_order: 1,
      is_active: true,
    },
    {
      id: "stat-2",
      institute_id: "default-inst",
      metric_value: "100%",
      numeric_target: 100,
      label: "Placement Assistance",
      subtext: "Top Multinational Corporate Recruiters",
      icon_name: "Award",
      display_order: 2,
      is_active: true,
    },
    {
      id: "stat-3",
      institute_id: "default-inst",
      metric_value: "15,000+",
      numeric_target: 15000,
      label: "Scholars & Alumni",
      subtext: "Empowered Across National Industry",
      icon_name: "Users",
      display_order: 3,
      is_active: true,
    },
    {
      id: "stat-4",
      institute_id: "default-inst",
      metric_value: "A+",
      numeric_target: null,
      label: "Autonomous Governance",
      subtext: "Flagship Campus at Indore, MP",
      icon_name: "ShieldCheck",
      display_order: 4,
      is_active: true,
    },
  ],
  quick_links: [
    {
      id: "ql-1",
      institute_id: "default-inst",
      title: "Online Admissions 2026",
      description: "Submit 2026 degree application with document scrutiny",
      path: "/admissions/apply",
      icon_name: "FileText",
      badge_label: "Open",
      is_external: false,
      display_order: 1,
      is_active: true,
    },
    {
      id: "ql-2",
      institute_id: "default-inst",
      title: "Online Fee Settlement",
      description: "Instant UPI/Card payment with GST tax invoice download",
      path: "/pay-online",
      icon_name: "IndianRupee",
      badge_label: "Secure",
      is_external: false,
      display_order: 2,
      is_active: true,
    },
    {
      id: "ql-3",
      institute_id: "default-inst",
      title: "Examination Portal",
      description: "Examination schedules, hall tickets & CBT test bank",
      path: "/admin/exams",
      icon_name: "Award",
      badge_label: "Live",
      is_external: false,
      display_order: 3,
      is_active: true,
    },
    {
      id: "ql-4",
      institute_id: "default-inst",
      title: "Document Verification",
      description: "Cryptographic QR credential validation ledger",
      path: "/verify",
      icon_name: "ShieldCheck",
      badge_label: "Zero Login",
      is_external: false,
      display_order: 4,
      is_active: true,
    },
  ],
  featured_programs: [
    {
      id: "prog-1",
      institute_id: "default-inst",
      title: "B.Tech Computer Science & Engineering",
      code: "BTECH-CSE",
      category: "Engineering & Technology",
      degree_level: "Undergraduate",
      duration: "4 Years (8 Semesters)",
      annual_fee: "₹95,000 / Year",
      eligibility_summary: "10+2 with PCM >= 60%",
      summary:
        "Specialization in Artificial Intelligence, Cloud Computing, Full-Stack Architecture, and Autonomous Systems with modern lab access.",
      image_url: null,
      syllabus_url: null,
      is_admissions_open: true,
      display_order: 1,
      is_active: true,
    },
    {
      id: "prog-2",
      institute_id: "default-inst",
      title: "Master of Business Administration (Executive MBA)",
      code: "MBA-EXEC",
      category: "Management Studies",
      degree_level: "Postgraduate",
      duration: "2 Years (4 Semesters)",
      annual_fee: "₹1,20,000 / Year",
      eligibility_summary: "Bachelor Degree >= 50%",
      summary:
        "Advanced institutional management degree focusing on Corporate Strategy, Financial Analytics, Supply Chain, and Global Business Leadership.",
      image_url: null,
      syllabus_url: null,
      is_admissions_open: true,
      display_order: 2,
      is_active: true,
    },
    {
      id: "prog-3",
      institute_id: "default-inst",
      title: "Bachelor of Computer Applications (BCA)",
      code: "BCA-HONS",
      category: "Computer Applications",
      degree_level: "Undergraduate",
      duration: "3 Years (6 Semesters)",
      annual_fee: "₹65,000 / Year",
      eligibility_summary: "10+2 Any Stream >= 50%",
      summary:
        "Comprehensive software development curriculum covering Cloud DevOps, Database Administration, Web Technologies, and Cyber Security.",
      image_url: null,
      syllabus_url: null,
      is_admissions_open: true,
      display_order: 3,
      is_active: true,
    },
  ],
  recruiters: [
    {
      id: "rec-1",
      institute_id: "default-inst",
      company_name: "Microsoft",
      tier: "Tier 1",
      highest_package_lpa: "44.0 LPA",
      logo_url: null,
      website_url: "https://microsoft.com",
      display_order: 1,
      is_active: true,
    },
    {
      id: "rec-2",
      institute_id: "default-inst",
      company_name: "Amazon",
      tier: "Tier 1",
      highest_package_lpa: "38.5 LPA",
      logo_url: null,
      website_url: "https://amazon.com",
      display_order: 2,
      is_active: true,
    },
    {
      id: "rec-3",
      institute_id: "default-inst",
      company_name: "Tata Consultancy Services",
      tier: "Regular",
      highest_package_lpa: "9.5 LPA",
      logo_url: null,
      website_url: "https://tcs.com",
      display_order: 3,
      is_active: true,
    },
    {
      id: "rec-4",
      institute_id: "default-inst",
      company_name: "Infosys",
      tier: "Regular",
      highest_package_lpa: "8.5 LPA",
      logo_url: null,
      website_url: "https://infosys.com",
      display_order: 4,
      is_active: true,
    },
    {
      id: "rec-5",
      institute_id: "default-inst",
      company_name: "Deloitte",
      tier: "Tier 1",
      highest_package_lpa: "14.0 LPA",
      logo_url: null,
      website_url: "https://deloitte.com",
      display_order: 5,
      is_active: true,
    },
    {
      id: "rec-6",
      institute_id: "default-inst",
      company_name: "HCL Technologies",
      tier: "Regular",
      highest_package_lpa: "7.5 LPA",
      logo_url: null,
      website_url: "https://hcltech.com",
      display_order: 6,
      is_active: true,
    },
  ],
  testimonials: [
    {
      id: "test-1",
      institute_id: "default-inst",
      author_name: "Aarav Sharma",
      author_role: "B.Tech CSE, Batch 2024 (Placed at Microsoft)",
      author_category: "Student",
      rating_stars: 5,
      quote:
        "The autonomous curriculum and real-time CBT testing platform at MY EDUCATION INDIA prepared me for the rigorous interviews of top global tech firms. The faculty mentorship was extraordinary.",
      avatar_url: null,
      video_url: null,
      display_order: 1,
      is_active: true,
    },
    {
      id: "test-2",
      institute_id: "default-inst",
      author_name: "Priya Patel",
      author_role: "MBA Executive, Batch 2023 (Consultant at Deloitte)",
      author_category: "Alumni",
      rating_stars: 5,
      quote:
        "From campus case study competitions to corporate leadership seminars in Indore, the institute's emphasis on practical management disciplines gave my career an incredible leap.",
      avatar_url: null,
      video_url: null,
      display_order: 2,
      is_active: true,
    },
  ],
};

export const PublicHomePage: React.FC = () => {
  const { bundle: frameworkBundle } = useOutletContext<ContextType>() || {};
  const settings = frameworkBundle?.settings;

  // Real-time API query for Module 2 Home Page Bundle
  const { data: homeBundle = FALLBACK_HOME_BUNDLE } = useQuery({
    queryKey: ["public-home-bundle"],
    queryFn: websiteService.getPublicHomeBundle,
    staleTime: 60000,
  });

  const {
    hero_slides,
    stat_counters,
    quick_links,
    featured_programs,
    recruiters,
    testimonials,
  } = homeBundle;

  // Hero Slider State
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);

  useEffect(() => {
    if (!hero_slides || hero_slides.length <= 1) return;
    const interval = setInterval(() => {
      setCurrentSlideIndex((prev) => (prev + 1) % hero_slides.length);
    }, 6500);
    return () => clearInterval(interval);
  }, [hero_slides]);

  const activeSlide = hero_slides[currentSlideIndex] || hero_slides[0];

  // Testimonial Carousel State
  const [currentTestimonialIndex, setCurrentTestimonialIndex] = useState(0);
  const activeTestimonial =
    testimonials[currentTestimonialIndex] || testimonials[0];

  // Newsletter Subscription Form State
  const [newsletterEmail, setNewsletterEmail] = useState("");
  const [newsletterStatus, setNewsletterStatus] = useState<string | null>(null);

  const newsletterMutation = useMutation({
    mutationFn: websiteService.subscribeNewsletter,
    onSuccess: (data) => {
      setNewsletterStatus(data.message);
      setNewsletterEmail("");
      setTimeout(() => setNewsletterStatus(null), 4000);
    },
    onError: () => {
      setNewsletterStatus("Unable to register subscription. Please verify your email.");
      setTimeout(() => setNewsletterStatus(null), 4000);
    },
  });

  const handleNewsletterSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newsletterEmail.trim()) return;
    newsletterMutation.mutate(newsletterEmail.trim());
  };

  return (
    <div className="space-y-0 font-sans">
      {/* =====================================================================
          1. DYNAMIC HERO SLIDER SECTION
      ====================================================================== */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-brand-950 to-slate-900 py-24 sm:py-32 text-white">
        {/* Subtle geometric grid background */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b15_1px,transparent_1px),linear-gradient(to_bottom,#1e293b15_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-30 pointer-events-none" />

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            {activeSlide?.badge_text && (
              <div className="inline-flex items-center gap-2 rounded-full border border-brand-400/30 bg-brand-900/60 px-4 py-1.5 text-xs font-bold text-brand-200 shadow-inner mb-6 backdrop-blur-xs">
                <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                <span>{activeSlide.badge_text}</span>
              </div>
            )}

            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl leading-tight">
              {activeSlide?.title}
            </h1>

            <p className="mt-6 text-base leading-relaxed text-slate-300 sm:text-lg max-w-2xl mx-auto">
              {activeSlide?.subtitle}
            </p>

            <div className="mt-9 flex flex-wrap items-center justify-center gap-4">
              <Link
                to={activeSlide?.primary_cta_link || "/admissions/apply"}
                className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-7 py-3.5 text-sm font-bold text-white shadow-xl shadow-brand-600/30 hover:bg-brand-500 transition-all hover:scale-102"
              >
                <span>{activeSlide?.primary_cta_text || "Apply Now"}</span>
                <ArrowRight className="h-4 w-4" />
              </Link>

              {activeSlide?.secondary_cta_text && (
                <Link
                  to={activeSlide.secondary_cta_link || "/courses"}
                  className="inline-flex items-center gap-2 rounded-xl border border-slate-700 bg-slate-800/80 px-6 py-3.5 text-sm font-bold text-slate-200 hover:bg-slate-800 hover:text-white transition backdrop-blur-xs"
                >
                  <span>{activeSlide.secondary_cta_text}</span>
                </Link>
              )}
            </div>

            {/* Slider Dots Indicator */}
            {hero_slides && hero_slides.length > 1 && (
              <div className="mt-12 flex items-center justify-center gap-2.5">
                {hero_slides.map((_, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setCurrentSlideIndex(idx)}
                    className={`h-2.5 rounded-full transition-all ${
                      currentSlideIndex === idx
                        ? "w-8 bg-brand-500"
                        : "w-2.5 bg-slate-700 hover:bg-slate-600"
                    }`}
                    aria-label={`Jump to slide ${idx + 1}`}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* =====================================================================
          2. KEY STATISTICS COUNTERS BAR
      ====================================================================== */}
      <section className="border-y border-slate-200 bg-white py-10 shadow-xs">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-6 md:grid-cols-4 text-center">
            {stat_counters.map((stat) => (
              <div key={stat.id} className="space-y-1">
                <p className="text-3xl font-black text-brand-600 sm:text-4xl">
                  {stat.metric_value}
                </p>
                <p className="text-xs font-bold uppercase tracking-wider text-slate-800">
                  {stat.label}
                </p>
                {stat.subtext && (
                  <p className="text-[11px] text-slate-500 hidden sm:block">
                    {stat.subtext}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* =====================================================================
          3. QUICK ACCESS TILES SECTION
      ====================================================================== */}
      <section className="py-14 bg-slate-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-xl mx-auto mb-8">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-700">
              Immediate Institutional Access
            </span>
            <h2 className="mt-1 text-2xl font-bold text-slate-900">
              Direct Student & Applicant Services
            </h2>
          </div>

          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {quick_links.map((link) => (
              <Link
                key={link.id}
                to={link.path}
                className="group relative flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-5 shadow-xs transition hover:border-brand-400 hover:shadow-md"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600 group-hover:bg-brand-600 group-hover:text-white transition-colors">
                      <FileText className="h-5 w-5" />
                    </div>
                    {link.badge_label && (
                      <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800">
                        {link.badge_label}
                      </span>
                    )}
                  </div>
                  <h3 className="text-sm font-bold text-slate-900 group-hover:text-brand-700 transition-colors">
                    {link.title}
                  </h3>
                  {link.description && (
                    <p className="mt-1 text-xs text-slate-500 leading-relaxed">
                      {link.description}
                    </p>
                  )}
                </div>
                <div className="mt-4 flex items-center gap-1.5 text-xs font-bold text-brand-600">
                  <span>Access Service</span>
                  <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* =====================================================================
          4. FEATURED ACADEMIC PROGRAMS SHOWCASE
      ====================================================================== */}
      <section id="programs" className="py-20 bg-white border-t border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-12">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-brand-700">
                Accredited Curricula
              </span>
              <h2 className="mt-1 text-3xl font-extrabold text-slate-900">
                Featured Academic Degree Programs
              </h2>
              <p className="mt-2 text-xs text-slate-500 max-w-xl">
                Industry-aligned degree courses integrated with continuous assessment and CBT testing platforms.
              </p>
            </div>
            <Link
              to="/courses"
              className="inline-flex items-center gap-2 rounded-xl border border-slate-200 px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 transition"
            >
              <span>View All Programs</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            {featured_programs.map((prog) => (
              <div
                key={prog.id}
                className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs transition hover:shadow-lg hover:border-brand-300"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="rounded-md bg-brand-50 px-2 py-0.5 text-[11px] font-bold text-brand-700">
                      {prog.category}
                    </span>
                    <span className="text-[11px] font-mono text-slate-400">
                      {prog.code}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-slate-900 leading-snug">
                    {prog.title}
                  </h3>

                  <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500">
                    <span>⏱ {prog.duration}</span>
                    {prog.annual_fee && (
                      <span className="font-semibold text-emerald-700">
                        💳 {prog.annual_fee}
                      </span>
                    )}
                  </div>

                  <p className="mt-3 text-xs leading-relaxed text-slate-600 line-clamp-3">
                    {prog.summary}
                  </p>

                  <div className="mt-4 rounded-xl bg-slate-50 p-2.5 text-[11px] text-slate-600 border border-slate-100">
                    <strong className="text-slate-800">Eligibility:</strong>{" "}
                    {prog.eligibility_summary}
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                  <Link
                    to="/admissions/apply"
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 hover:text-brand-800"
                  >
                    <span>Apply Online</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Link>

                  <Link
                    to="/courses"
                    className="text-xs font-medium text-slate-500 hover:text-slate-800"
                  >
                    Syllabus Details
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* =====================================================================
          5. CORPORATE RECRUITER PARTNERS SHOWCASE
      ====================================================================== */}
      <section className="py-16 bg-slate-50 border-t border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-700">
            Career Pathways & Placements
          </span>
          <h2 className="mt-1 text-2xl font-bold text-slate-900">
            Trusted by Global Enterprise Recruiters
          </h2>
          <p className="mt-2 text-xs text-slate-500 max-w-lg mx-auto">
            Annual campus recruitment drives offering highest CTCs up to ₹45.0 LPA.
          </p>

          <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-6">
            {recruiters.map((rec) => (
              <div
                key={rec.id}
                className="flex flex-col items-center justify-center rounded-2xl border border-slate-200 bg-white p-5 shadow-2xs hover:border-brand-400 transition"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-700 font-extrabold text-xs mb-2">
                  {rec.company_name.slice(0, 2).toUpperCase()}
                </div>
                <p className="text-xs font-bold text-slate-800 truncate w-full">
                  {rec.company_name}
                </p>
                {rec.highest_package_lpa && (
                  <span className="mt-1 rounded-sm bg-emerald-50 px-1.5 py-0.5 text-[10px] font-bold text-emerald-800">
                    Up to {rec.highest_package_lpa}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* =====================================================================
          6. STUDENT & ALUMNI TESTIMONIALS CAROUSEL
      ====================================================================== */}
      <section className="py-20 bg-white border-t border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-700">
              Verified Social Proof
            </span>
            <h2 className="mt-1 text-3xl font-extrabold text-slate-900">
              Scholar & Alumni Success Stories
            </h2>

            {activeTestimonial && (
              <div className="mt-10 rounded-3xl border border-slate-200 bg-slate-50/70 p-8 sm:p-10 shadow-xs relative">
                {/* 5-Star Rating */}
                <div className="flex justify-center gap-1 mb-6 text-amber-500">
                  {Array.from({ length: activeTestimonial.rating_stars }).map(
                    (_, i) => (
                      <Star key={i} className="h-5 w-5 fill-amber-400" />
                    )
                  )}
                </div>

                <p className="text-base sm:text-lg italic text-slate-700 leading-relaxed max-w-2xl mx-auto">
                  "{activeTestimonial.quote}"
                </p>

                <div className="mt-8">
                  <p className="text-sm font-bold text-slate-900">
                    {activeTestimonial.author_name}
                  </p>
                  <p className="text-xs text-brand-700 font-medium mt-0.5">
                    {activeTestimonial.author_role}
                  </p>
                </div>

                {/* Carousel Navigation Buttons */}
                {testimonials.length > 1 && (
                  <div className="mt-8 flex justify-center gap-3">
                    <button
                      type="button"
                      onClick={() =>
                        setCurrentTestimonialIndex(
                          (prev) => (prev - 1 + testimonials.length) % testimonials.length
                        )
                      }
                      className="rounded-full border border-slate-200 bg-white p-2 text-slate-600 hover:bg-slate-100 transition shadow-2xs"
                      aria-label="Previous testimonial"
                    >
                      <ChevronLeft className="h-4 w-4" />
                    </button>
                    <button
                      type="button"
                      onClick={() =>
                        setCurrentTestimonialIndex(
                          (prev) => (prev + 1) % testimonials.length
                        )
                      }
                      className="rounded-full border border-slate-200 bg-white p-2 text-slate-600 hover:bg-slate-100 transition shadow-2xs"
                      aria-label="Next testimonial"
                    >
                      <ChevronRight className="h-4 w-4" />
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* =====================================================================
          7. NEWSLETTER SUBSCRIPTION & CAMPUS INQUIRIES
      ====================================================================== */}
      <section className="py-16 bg-slate-900 text-white border-t border-slate-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <span className="rounded-full bg-brand-900/60 border border-brand-500/40 px-3 py-1 text-xs font-bold text-brand-300">
              Institutional Bulletin
            </span>
            <h2 className="mt-3 text-2xl font-bold sm:text-3xl">
              Stay Updated on Entrance Exams & Admissions
            </h2>
            <p className="mt-2 text-xs text-slate-400">
              Subscribe directly to official circulars, examination date sheets, and scholarship announcements.
            </p>

            <form
              onSubmit={handleNewsletterSubmit}
              className="mt-6 flex flex-col sm:flex-row gap-2.5 max-w-md mx-auto"
            >
              <input
                type="email"
                required
                value={newsletterEmail}
                onChange={(e) => setNewsletterEmail(e.target.value)}
                placeholder="Enter your institutional or personal email..."
                className="flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:border-brand-500 focus:outline-hidden"
              />
              <button
                type="submit"
                disabled={newsletterMutation.isPending}
                className="inline-flex items-center justify-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-xs font-bold text-white hover:bg-brand-500 transition shadow-xs"
              >
                <span>Subscribe</span>
                <Send className="h-3 w-3" />
              </button>
            </form>

            {newsletterStatus && (
              <p className="mt-3 text-xs font-semibold text-emerald-400 animate-in fade-in">
                {newsletterStatus}
              </p>
            )}
          </div>
        </div>
      </section>
    </div>
  );
};
