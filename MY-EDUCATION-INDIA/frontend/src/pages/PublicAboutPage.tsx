import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  Award,
  Building2,
  Calendar,
  CheckCircle2,
  ChevronRight,
  Compass,
  FileBadge,
  FileCheck2,
  GraduationCap,
  HeartHandshake,
  Lightbulb,
  MapPin,
  Maximize2,
  Quote,
  Shield,
  ShieldCheck,
  Sparkles,
  Target,
  Trophy,
  Users,
  Video,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsAccreditation,
  CmsCampusInfrastructure,
  CmsLeadershipMessage,
  CmsMilestone,
  PublicAboutInstituteBundle,
} from "@/types/website.types";

const FALLBACK_ABOUT_BUNDLE: PublicAboutInstituteBundle = {
  milestones: [
    {
      id: "m-1",
      institute_id: "default-inst",
      year: "2010",
      title: "Foundation of MY EDUCATION INDIA",
      description:
        "Established in Indore, Madhya Pradesh as an autonomous pioneering institute dedicated to technical excellence, modern engineering, and management disciplines.",
      image_url: null,
      icon_name: "Building2",
      display_order: 1,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "m-2",
      institute_id: "default-inst",
      year: "2014",
      title: "Statutory AICTE & UGC Approvals",
      description:
        "Secured statutory recognition under AICTE and University Grants Commission with an expanded 50-acre flagship research campus.",
      image_url: null,
      icon_name: "ShieldCheck",
      display_order: 2,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "m-3",
      institute_id: "default-inst",
      year: "2018",
      title: "NBA Tier-1 Accreditation Granted",
      description:
        "Core computer engineering, electrical, and management postgraduate programs received prestigious NBA Tier-1 outcome-based accreditation.",
      image_url: null,
      icon_name: "Award",
      display_order: 3,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "m-4",
      institute_id: "default-inst",
      year: "2021",
      title: "State-of-the-Art CBT Platform Launch",
      description:
        "Commissioned a dedicated 500-seat biometric high-density Computer-Based Testing center for secure university and national competitive exams.",
      image_url: null,
      icon_name: "Lightbulb",
      display_order: 4,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "m-5",
      institute_id: "default-inst",
      year: "2024",
      title: "NAAC A+ Accreditation (CGPA 3.68/4.0)",
      description:
        "Achieved Grade A+ institutional accreditation by the National Assessment and Accreditation Council for stellar academic rigor and research output.",
      image_url: null,
      icon_name: "Trophy",
      display_order: 5,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "m-6",
      institute_id: "default-inst",
      year: "2026",
      title: "ERP V2 Unified Autonomous Digital Campus",
      description:
        "Full rollout of Enterprise Cloud ERP V2, integrating zero-login public portals, digital verified credentials, and high-frequency CBT pipelines.",
      image_url: null,
      icon_name: "Sparkles",
      display_order: 6,
      is_active: true,
      created_at: new Date().toISOString(),
    },
  ],
  leadership_messages: [
    {
      id: "lead-1",
      institute_id: "default-inst",
      leader_name: "Dr. Rajeshwar Sharma",
      leader_designation: "Chairman & Chancellor",
      role_category: "CHAIRMAN",
      salutation_title: "Fostering Intellectual Rigor, Ethical Leadership & Global Impact",
      message_body:
        "Welcome to MY EDUCATION INDIA. Since our inception in 2010 at Indore, we have stood firm in our conviction that higher education must bridge academic discovery with transformative real-world impact. We believe in providing an ecosystem where students are empowered to question orthodoxies, develop technological breakthroughs, and conduct themselves with unwavering integrity. Our investments in world-class research infrastructure, advanced CBT centers, and industry alliances ensure that every scholar graduating from our portals is primed to lead on global stages.",
      portrait_image_url: null,
      signature_image_url: null,
      video_address_url: null,
      display_order: 1,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "lead-2",
      institute_id: "default-inst",
      leader_name: "Prof. (Dr.) Sunita Deshmukh",
      leader_designation: "Director General & Principal",
      role_category: "DIRECTOR",
      salutation_title: "Empowering Next-Generation Pioneers Through Innovation & Practice",
      message_body:
        "At MY EDUCATION INDIA, academic excellence is not an aspiration—it is our daily operating standard. Our outcome-based curricula are mapped directly to industry paradigms and international standards. Through our integrated ERP platform, continuous evaluation protocols, and hands-on laboratory experiences, we provide learners with a multidisciplinary launchpad. Whether you are pursuing technology, management, or applied sciences, our distinguished faculty mentors and research laboratories will nurture your potential every step of the way.",
      portrait_image_url: null,
      signature_image_url: null,
      video_address_url: null,
      display_order: 2,
      is_active: true,
      created_at: new Date().toISOString(),
    },
  ],
  accreditations: [
    {
      id: "acc-1",
      institute_id: "default-inst",
      accrediting_body: "AICTE",
      title: "All India Council for Technical Education",
      approval_reference_number: "F.No. Central/1-931829102/2025/EOA",
      valid_from: "2010",
      valid_upto: "2027",
      certificate_pdf_url: null,
      logo_badge_url: null,
      display_order: 1,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "acc-2",
      institute_id: "default-inst",
      accrediting_body: "UGC",
      title: "University Grants Commission (Autonomous Status)",
      approval_reference_number: "UGC/AUTONOMY/MP-INDORE/2022-28",
      valid_from: "2014",
      valid_upto: "2028",
      certificate_pdf_url: null,
      logo_badge_url: null,
      display_order: 2,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "acc-3",
      institute_id: "default-inst",
      accrediting_body: "NAAC",
      title: "National Assessment & Accreditation Council - Grade A+ (3.68 CGPA)",
      approval_reference_number: "NAAC/A&A/2024/IND-0821",
      valid_from: "2024",
      valid_upto: "2029",
      certificate_pdf_url: null,
      logo_badge_url: null,
      display_order: 3,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "acc-4",
      institute_id: "default-inst",
      accrediting_body: "NBA",
      title: "National Board of Accreditation (Tier-1 Programs)",
      approval_reference_number: "NBA/TIER1/CSE-IT-ECE/2023-26",
      valid_from: "2018",
      valid_upto: "2026",
      certificate_pdf_url: null,
      logo_badge_url: null,
      display_order: 4,
      is_active: true,
      created_at: new Date().toISOString(),
    },
  ],
  infrastructure: [
    {
      id: "inf-1",
      institute_id: "default-inst",
      facility_name: "Dr. APJ Abdul Kalam Central Digital Library",
      category: "ACADEMIC",
      capacity_metric: "150,000+ Print & E-Volumes • 600 Seating",
      description:
        "A 4-tier fully automated hybrid library equipped with RFID issue kiosks, IEEE/Springer digital repository access, and 24/7 dedicated doctoral research carrels.",
      image_url: null,
      floor_or_location: "Academic Block A, Ground & 1st Floor",
      display_order: 1,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "inf-2",
      institute_id: "default-inst",
      facility_name: "High-Density CBT Computer-Based Testing Complex",
      category: "EXAMINATION",
      capacity_metric: "500 Biometric Exam Terminals • Dual Gigabit Line",
      description:
        "National-grade high-security CBT center with redundant fiber lines, localized offline backup servers, biometric check-in pods, and proctoring telemetry.",
      image_url: null,
      floor_or_location: "Technology Tower, 3rd Floor",
      display_order: 2,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "inf-3",
      institute_id: "default-inst",
      facility_name: "Center for Artificial Intelligence & Robotics Innovation",
      category: "RESEARCH",
      capacity_metric: "40 GPU Compute Workstations • NVIDIA DGX Pod",
      description:
        "Advanced industrial computing laboratory housing high-performance GPU nodes, industrial 6-axis robotic arms, and autonomous IoT sensory testbeds.",
      image_url: null,
      floor_or_location: "Innovation Hub, Ground Floor",
      display_order: 3,
      is_active: true,
      created_at: new Date().toISOString(),
    },
    {
      id: "inf-4",
      institute_id: "default-inst",
      facility_name: "Olympic Standard Sports Arena & Aquatic Complex",
      category: "SPORTS",
      capacity_metric: "2,000 Spectator Pavilion • FIFA Synthetic Turf",
      description:
        "Comprehensive athletics hub featuring an Olympic-sized swimming pool, floodlit synthetic turf football pitch, wooden indoor badminton courts, and gym.",
      image_url: null,
      floor_or_location: "West Campus Sports Enclave",
      display_order: 4,
      is_active: true,
      created_at: new Date().toISOString(),
    },
  ],
};

export const PublicAboutPage: React.FC = () => {
  const location = useLocation();
  const [activeTab, setActiveTab] = useState<
    "overview" | "vision-mission" | "leadership" | "accreditations" | "infrastructure"
  >("overview");

  // Synchronize active tab with URL path
  useEffect(() => {
    if (location.pathname.includes("vision-mission")) {
      setActiveTab("vision-mission");
    } else if (location.pathname.includes("directors-message") || location.pathname.includes("leadership")) {
      setActiveTab("leadership");
    } else if (location.pathname.includes("accreditations")) {
      setActiveTab("accreditations");
    } else if (location.pathname.includes("infrastructure")) {
      setActiveTab("infrastructure");
    } else {
      setActiveTab("overview");
    }
  }, [location.pathname]);

  const { data: aboutData } = useQuery<PublicAboutInstituteBundle>({
    queryKey: ["public-about-bundle"],
    queryFn: websiteService.getPublicAboutBundle,
    staleTime: 1000 * 60 * 5,
  });

  const bundle = aboutData || FALLBACK_ABOUT_BUNDLE;

  return (
    <div className="min-h-screen bg-slate-50">
      {/* 1. Institutional Hero Header Banner */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-brand-950 to-blue-900 text-white py-16 lg:py-24">
        <div className="absolute inset-0 opacity-15">
          <div className="absolute -top-40 -right-40 h-96 w-96 rounded-full bg-blue-500 blur-3xl pointer-events-none" />
          <div className="absolute -bottom-40 -left-40 h-96 w-96 rounded-full bg-brand-400 blur-3xl pointer-events-none" />
        </div>

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-300 mb-4">
            <Link to="/" className="hover:text-white transition-colors">
              Home
            </Link>
            <ChevronRight className="h-3 w-3" />
            <span>Institutional Governance</span>
            <ChevronRight className="h-3 w-3" />
            <span className="text-white">About Institute</span>
          </div>

          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-blue-400/30 bg-blue-500/10 px-3.5 py-1 text-xs font-semibold text-blue-200 mb-6 backdrop-blur-xs">
              <Sparkles className="h-3.5 w-3.5 text-blue-300" />
              <span>Autonomous Flagship Campus • Indore, Madhya Pradesh</span>
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl lg:text-5xl text-white">
              Pioneering Academic Rigor, Technological Innovation & Research
            </h1>
            <p className="mt-4 text-base sm:text-lg text-slate-300 leading-relaxed">
              Established in 2010, MY EDUCATION INDIA has evolved into one of central India&apos;s foremost
              autonomous centers of higher learning, accredited with NAAC Grade A+ and NBA Tier-1 recognitions.
            </p>
          </div>

          {/* Quick Metrics Bar */}
          <div className="mt-12 grid grid-cols-2 gap-4 border-t border-white/10 pt-8 sm:grid-cols-4">
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold text-blue-300">2010</div>
              <div className="text-xs sm:text-sm text-slate-400">Year Established</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold text-blue-300">50+ Acres</div>
              <div className="text-xs sm:text-sm text-slate-400">Smart Eco-Campus</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold text-blue-300">Grade A+</div>
              <div className="text-xs sm:text-sm text-slate-400">NAAC Accreditation</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold text-blue-300">500+ Seat</div>
              <div className="text-xs sm:text-sm text-slate-400">National CBT Center</div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Interactive Navigation Sub-Menu */}
      <nav className="sticky top-16 z-20 border-b border-slate-200 bg-white/95 backdrop-blur-md shadow-xs">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1 overflow-x-auto py-2.5 no-scrollbar">
            <button
              onClick={() => setActiveTab("overview")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition-all ${
                activeTab === "overview"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Building2 className="h-4 w-4" />
              History & Milestones
            </button>
            <button
              onClick={() => setActiveTab("vision-mission")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition-all ${
                activeTab === "vision-mission"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Target className="h-4 w-4" />
              Vision, Mission & Values
            </button>
            <button
              onClick={() => setActiveTab("leadership")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition-all ${
                activeTab === "leadership"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Users className="h-4 w-4" />
              Leadership Messages
            </button>
            <button
              onClick={() => setActiveTab("accreditations")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition-all ${
                activeTab === "accreditations"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <ShieldCheck className="h-4 w-4" />
              Accreditations & Approvals
            </button>
            <button
              onClick={() => setActiveTab("infrastructure")}
              className={`flex shrink-0 items-center gap-2 rounded-lg px-4 py-2 text-xs font-bold transition-all ${
                activeTab === "infrastructure"
                  ? "bg-brand-50 text-brand-700 shadow-2xs border border-brand-200"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Compass className="h-4 w-4" />
              Campus Infrastructure
            </button>
          </div>
        </div>
      </nav>

      {/* 3. Main Content Container */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12 space-y-16">
        {/* ========================================================================= */}
        {/* TAB 1: OVERVIEW & HISTORICAL MILESTONES TIMELINE */}
        {/* ========================================================================= */}
        {activeTab === "overview" && (
          <section className="space-y-12 animate-fadeIn">
            <div className="grid grid-cols-1 gap-10 lg:grid-cols-12 items-center">
              <div className="lg:col-span-7 space-y-4">
                <div className="inline-flex items-center gap-2 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
                  <Building2 className="h-3.5 w-3.5" />
                  <span>Institutional Legacy & Growth</span>
                </div>
                <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
                  Sixteen Years of Autonomous Educational Leadership in Central India
                </h2>
                <p className="text-sm sm:text-base text-slate-600 leading-relaxed">
                  Founded in 2010 under the aegis of the MEI Educational Foundation, MY EDUCATION INDIA was
                  conceived as an institute of distinction designed to transcend conventional classroom pedagogy.
                  Located in the thriving technological and financial hub of Indore, Madhya Pradesh, the campus
                  serves as an incubator for advanced engineering, applied computer sciences, and executive
                  business administration.
                </p>
                <p className="text-sm sm:text-base text-slate-600 leading-relaxed">
                  With autonomous academic privileges granted by the University Grants Commission (UGC) and
                  comprehensive accreditation by NAAC (Grade A+) and NBA Tier-1, the institute empowers more than
                  4,500 enrolled scholars with experiential problem-solving and rigorous industry mentorship.
                </p>
              </div>

              <div className="lg:col-span-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <ShieldCheck className="h-5 w-5 text-brand-600" />
                  Statutory Institutional Profile
                </h3>
                <dl className="space-y-3 text-xs sm:text-sm">
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <dt className="text-slate-500">Legal Name</dt>
                    <dd className="font-semibold text-slate-900">MY EDUCATION INDIA ERP V2</dd>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <dt className="text-slate-500">Campus Code</dt>
                    <dd className="font-semibold text-slate-900">MEI-HQ-INDORE (01)</dd>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <dt className="text-slate-500">Jurisdiction</dt>
                    <dd className="font-semibold text-slate-900">Indore, Madhya Pradesh, India</dd>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <dt className="text-slate-500">Affiliation & Autonomy</dt>
                    <dd className="font-semibold text-brand-600">Autonomous Institute (UGC/AICTE)</dd>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <dt className="text-slate-500">Institutional NAAC Rating</dt>
                    <dd className="font-semibold text-emerald-600">Grade A+ (CGPA 3.68/4.0)</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-slate-500">Examination Modality</dt>
                    <dd className="font-semibold text-slate-900">High-Security Hybrid CBT + Outcome Based</dd>
                  </div>
                </dl>
              </div>
            </div>

            {/* Milestones Timeline */}
            <div className="space-y-6 pt-6">
              <div className="text-center max-w-2xl mx-auto">
                <h3 className="text-xl sm:text-2xl font-bold text-slate-900">
                  Institutional Timeline of Excellence (2010 – 2026)
                </h3>
                <p className="mt-2 text-xs sm:text-sm text-slate-500">
                  A chronicle of transformative growth, milestone accreditations, and digital innovations.
                </p>
              </div>

              <div className="relative mt-10">
                {/* Vertical timeline spine */}
                <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gradient-to-b from-brand-600 via-blue-400 to-emerald-500 sm:left-1/2 -ml-px" />

                <div className="space-y-8">
                  {bundle.milestones
                    .filter((m) => m.is_active)
                    .sort((a, b) => a.display_order - b.display_order)
                    .map((milestone, idx) => {
                      const isEven = idx % 2 === 0;
                      return (
                        <div
                          key={milestone.id}
                          className="relative flex flex-col sm:flex-row items-start sm:items-center"
                        >
                          {/* Left column (Desktop) */}
                          <div
                            className={`w-full sm:w-1/2 pl-12 sm:pl-0 ${
                              isEven ? "sm:pr-10 sm:text-right" : "sm:order-2 sm:pl-10 sm:text-left"
                            }`}
                          >
                            <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-xs hover:shadow-md transition-shadow">
                              <span className="inline-block rounded-md bg-brand-50 px-2.5 py-1 text-xs font-extrabold text-brand-700 mb-2">
                                Year {milestone.year}
                              </span>
                              <h4 className="text-base font-bold text-slate-900">{milestone.title}</h4>
                              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                                {milestone.description}
                              </p>
                            </div>
                          </div>

                          {/* Center Node Badge */}
                          <div className="absolute left-1.5 sm:left-1/2 -ml-3.5 flex h-7 w-7 items-center justify-center rounded-full border-2 border-white bg-brand-600 text-white shadow-xs">
                            <Calendar className="h-3.5 w-3.5" />
                          </div>
                        </div>
                      );
                    })}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* ========================================================================= */}
        {/* TAB 2: VISION, MISSION & CORE VALUES */}
        {/* ========================================================================= */}
        {activeTab === "vision-mission" && (
          <section className="space-y-12 animate-fadeIn">
            <div className="text-center max-w-2xl mx-auto space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
                <Target className="h-3.5 w-3.5" />
                <span>Foundational Principles</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
                Guiding Purpose, Strategic Vision & Core Values
              </h2>
              <p className="text-sm text-slate-600">
                The philosophical commitments guiding every academic curriculum, research initiative, and
                governance decision at MY EDUCATION INDIA.
              </p>
            </div>

            {/* Vision & Mission Grid */}
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
              {/* Vision Card */}
              <div className="relative overflow-hidden rounded-2xl border border-brand-200 bg-gradient-to-br from-blue-900 to-brand-950 p-8 text-white shadow-md">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-500/20 text-blue-300 mb-6 backdrop-blur-xs">
                  <Compass className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Our Institutional Vision</h3>
                <p className="text-sm text-slate-200 leading-relaxed">
                  &ldquo;To be recognized as a premier globally competitive autonomous institute of education,
                  celebrated for excellence in research-driven instruction, ethical technological advancement,
                  and nurturing principled innovators who enrich society and drive national development.&rdquo;
                </p>
                <div className="mt-8 border-t border-white/10 pt-4 flex items-center gap-3 text-xs text-blue-200">
                  <Sparkles className="h-4 w-4 text-blue-300" />
                  <span>Aligned to National Education Policy (NEP) 2020 Framework</span>
                </div>
              </div>

              {/* Mission Card */}
              <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-xs">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 mb-6">
                  <Target className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">Our Mission Mandate</h3>
                <ul className="space-y-4 text-xs sm:text-sm text-slate-600">
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5" />
                    <span>
                      <strong>Rigor & Practice:</strong> Deliver cutting-edge outcome-based curricula benchmarked
                      with global standards across engineering, sciences, and management.
                    </span>
                  </li>
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5" />
                    <span>
                      <strong>Technological Leadership:</strong> Maintain state-of-the-art computational infrastructure,
                      AI testbeds, and national CBT examination pipelines.
                    </span>
                  </li>
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5" />
                    <span>
                      <strong>Ethical Citizenship:</strong> Instill professional ethics, social accountability,
                      and lifelong inquiry in every student scholar.
                    </span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Core Values Grid */}
            <div className="space-y-6 pt-4">
              <h3 className="text-lg font-bold text-slate-900 text-center">Institutional Core Values</h3>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-xs text-center">
                  <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-brand-600 mb-3">
                    <Shield className="h-5 w-5" />
                  </div>
                  <h4 className="text-sm font-bold text-slate-900">Integrity & Governance</h4>
                  <p className="mt-1 text-xs text-slate-500">
                    Transparent administrative systems, zero compromise on evaluation, and ethical accountability.
                  </p>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-xs text-center">
                  <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-lg bg-purple-50 text-purple-600 mb-3">
                    <Lightbulb className="h-5 w-5" />
                  </div>
                  <h4 className="text-sm font-bold text-slate-900">Innovation & Inquiry</h4>
                  <p className="mt-1 text-xs text-slate-500">
                    Encouraging independent research, patented prototypes, and multidisciplinary exploration.
                  </p>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-xs text-center">
                  <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-600 mb-3">
                    <GraduationCap className="h-5 w-5" />
                  </div>
                  <h4 className="text-sm font-bold text-slate-900">Student Centricity</h4>
                  <p className="mt-1 text-xs text-slate-500">
                    Holistic student development with counseling, merit scholarships, and global placement support.
                  </p>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-xs text-center">
                  <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-600 mb-3">
                    <HeartHandshake className="h-5 w-5" />
                  </div>
                  <h4 className="text-sm font-bold text-slate-900">Social Responsibility</h4>
                  <p className="mt-1 text-xs text-slate-500">
                    Community engagement, rural outreach programs, and sustainable green campus practices.
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* ========================================================================= */}
        {/* TAB 3: LEADERSHIP MESSAGES */}
        {/* ========================================================================= */}
        {activeTab === "leadership" && (
          <section className="space-y-12 animate-fadeIn">
            <div className="text-center max-w-2xl mx-auto space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
                <Users className="h-3.5 w-3.5" />
                <span>Executive Leadership</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
                Messages from the Directorate & Chancellor
              </h2>
              <p className="text-sm text-slate-600">
                Hear directly from our visionary leaders shaping the strategic roadmap, institutional culture,
                and academic standards of MY EDUCATION INDIA.
              </p>
            </div>

            <div className="space-y-10">
              {bundle.leadership_messages
                .filter((l) => l.is_active)
                .sort((a, b) => a.display_order - b.display_order)
                .map((leader) => (
                  <div
                    key={leader.id}
                    className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xs"
                  >
                    <div className="grid grid-cols-1 lg:grid-cols-12">
                      {/* Portrait & Profile Column */}
                      <div className="lg:col-span-4 bg-slate-900 p-8 text-white flex flex-col justify-between">
                        <div>
                          <div className="inline-block rounded-full bg-brand-500/20 px-3 py-1 text-[11px] font-bold text-brand-300 uppercase tracking-wider mb-6">
                            {leader.role_category}
                          </div>
                          <div className="h-36 w-36 rounded-2xl border-2 border-brand-500/40 bg-slate-800 flex items-center justify-center text-brand-300 font-extrabold text-3xl mb-4 overflow-hidden">
                            {leader.portrait_image_url ? (
                              <img
                                src={leader.portrait_image_url}
                                alt={leader.leader_name}
                                className="h-full w-full object-cover"
                              />
                            ) : (
                              <Users className="h-16 w-16 text-slate-600" />
                            )}
                          </div>
                          <h3 className="text-xl font-bold text-white">{leader.leader_name}</h3>
                          <p className="text-xs font-semibold text-blue-300 mt-0.5">
                            {leader.leader_designation}
                          </p>
                        </div>

                        <div className="mt-8 border-t border-slate-800 pt-4 text-[11px] text-slate-400">
                          MY EDUCATION INDIA Governing Directorate • Indore, MP
                        </div>
                      </div>

                      {/* Message Body Column */}
                      <div className="lg:col-span-8 p-8 flex flex-col justify-between">
                        <div className="space-y-4">
                          <div className="flex items-center gap-2 text-brand-600">
                            <Quote className="h-6 w-6 rotate-180" />
                          </div>
                          <h4 className="text-lg sm:text-xl font-bold text-slate-900 leading-snug">
                            {leader.salutation_title}
                          </h4>
                          <div className="text-xs sm:text-sm text-slate-600 leading-relaxed whitespace-pre-line space-y-3">
                            {leader.message_body}
                          </div>
                        </div>

                        <div className="mt-8 border-t border-slate-100 pt-4 flex items-center justify-between">
                          <div className="text-xs text-slate-500">
                            Official Endorsement • Verified Digital Record
                          </div>
                          {leader.video_address_url && (
                            <a
                              href={leader.video_address_url}
                              target="_blank"
                              rel="noreferrer"
                              className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 hover:text-brand-800"
                            >
                              <Video className="h-4 w-4" />
                              Watch Address
                            </a>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </section>
        )}

        {/* ========================================================================= */}
        {/* TAB 4: ACCREDITATIONS & STATUTORY RECOGNITIONS */}
        {/* ========================================================================= */}
        {activeTab === "accreditations" && (
          <section className="space-y-12 animate-fadeIn">
            <div className="text-center max-w-2xl mx-auto space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
                <ShieldCheck className="h-3.5 w-3.5" />
                <span>Statutory Compliance & Standards</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
                National Accreditations, Affiliations & Gazetted Approvals
              </h2>
              <p className="text-sm text-slate-600">
                All degree programs, examinations, and curricula adhere strictly to statutory guidelines
                promulgated by national higher education councils.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              {bundle.accreditations
                .filter((a) => a.is_active)
                .sort((a, b) => a.display_order - b.display_order)
                .map((acc) => (
                  <div
                    key={acc.id}
                    className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs hover:border-brand-300 transition-colors"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-4">
                        <span className="rounded-md bg-blue-50 px-3 py-1 text-xs font-extrabold text-brand-700">
                          {acc.accrediting_body}
                        </span>
                        <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-600">
                          <CheckCircle2 className="h-4 w-4" />
                          <span>Active Statutory Standing</span>
                        </div>
                      </div>

                      <h3 className="text-base font-bold text-slate-900">{acc.title}</h3>

                      <div className="mt-4 rounded-xl bg-slate-50 p-3.5 space-y-2 text-xs">
                        <div className="flex justify-between">
                          <span className="text-slate-500">Order Ref. Number:</span>
                          <span className="font-mono font-semibold text-slate-800">
                            {acc.approval_reference_number}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Validity Period:</span>
                          <span className="font-semibold text-slate-800">
                            {acc.valid_from || "Inception"} &mdash; {acc.valid_upto || "Perpetual"}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="mt-6 border-t border-slate-100 pt-4 flex items-center justify-between text-xs">
                      <span className="text-slate-400">Public Compliance Record</span>
                      {acc.certificate_pdf_url ? (
                        <a
                          href={acc.certificate_pdf_url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 font-bold text-brand-600 hover:underline"
                        >
                          <FileBadge className="h-3.5 w-3.5" />
                          Download Certificate PDF
                        </a>
                      ) : (
                        <span className="text-slate-400 italic">Certificate Available at Registrar Office</span>
                      )}
                    </div>
                  </div>
                ))}
            </div>
          </section>
        )}

        {/* ========================================================================= */}
        {/* TAB 5: CAMPUS INFRASTRUCTURE & FACILITIES */}
        {/* ========================================================================= */}
        {activeTab === "infrastructure" && (
          <section className="space-y-12 animate-fadeIn">
            <div className="text-center max-w-2xl mx-auto space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
                <Building2 className="h-3.5 w-3.5" />
                <span>Smart 50-Acre Campus</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
                World-Class Academic, Research & Living Infrastructure
              </h2>
              <p className="text-sm text-slate-600">
                Explore our high-technology learning environments, specialized research laboratories, and
                student wellness facilities in Indore.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
              {bundle.infrastructure
                .filter((inf) => inf.is_active)
                .sort((a, b) => a.display_order - b.display_order)
                .map((facility) => (
                  <div
                    key={facility.id}
                    className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xs hover:shadow-md transition-shadow flex flex-col justify-between"
                  >
                    <div>
                      {/* Placeholder or actual facility visual banner */}
                      <div className="relative h-48 w-full bg-gradient-to-r from-slate-800 to-slate-900 flex items-center justify-center text-white overflow-hidden">
                        {facility.image_url ? (
                          <img
                            src={facility.image_url}
                            alt={facility.facility_name}
                            className="h-full w-full object-cover"
                          />
                        ) : (
                          <div className="text-center p-4">
                            <Building2 className="mx-auto h-12 w-12 text-blue-400/80 mb-2" />
                            <span className="text-xs font-bold uppercase tracking-wider text-blue-200">
                              {facility.category} Infrastructure
                            </span>
                          </div>
                        )}
                        <span className="absolute top-3 left-3 rounded-md bg-black/60 backdrop-blur-xs px-2.5 py-1 text-[11px] font-bold text-white uppercase tracking-wider">
                          {facility.category}
                        </span>
                      </div>

                      <div className="p-6 space-y-3">
                        <h3 className="text-lg font-bold text-slate-900">{facility.facility_name}</h3>
                        <div className="flex items-center gap-2 text-xs font-semibold text-brand-700 bg-brand-50 px-3 py-1.5 rounded-lg w-fit">
                          <CheckCircle2 className="h-3.5 w-3.5" />
                          <span>{facility.capacity_metric}</span>
                        </div>
                        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                          {facility.description}
                        </p>
                      </div>
                    </div>

                    <div className="border-t border-slate-100 bg-slate-50/50 p-4 px-6 flex items-center justify-between text-xs text-slate-500">
                      <div className="flex items-center gap-1.5">
                        <MapPin className="h-3.5 w-3.5 text-slate-400" />
                        <span>{facility.floor_or_location || "Main Campus, Indore"}</span>
                      </div>
                      <Link
                        to="/contact"
                        className="font-bold text-brand-600 hover:text-brand-800 hover:underline"
                      >
                        Plan Campus Visit &rarr;
                      </Link>
                    </div>
                  </div>
                ))}
            </div>
          </section>
        )}

        {/* 4. Global Bottom Call-To-Action Banner */}
        <section className="rounded-2xl bg-gradient-to-r from-brand-900 via-blue-900 to-indigo-950 p-8 sm:p-12 text-white text-center shadow-lg relative overflow-hidden">
          <div className="relative z-10 max-w-2xl mx-auto space-y-4">
            <h3 className="text-2xl sm:text-3xl font-extrabold text-white">
              Experience the MY EDUCATION INDIA Advantage
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              Admissions for Academic Session 2026–2027 are now open for Undergraduate, Postgraduate, and
              Doctoral degrees. Schedule a guided campus tour or submit your digital application today.
            </p>
            <div className="flex flex-wrap justify-center gap-4 pt-4">
              <Link
                to="/admissions/apply"
                className="rounded-xl bg-white px-6 py-3 text-xs font-bold text-brand-900 shadow-md hover:bg-slate-100 transition-colors"
              >
                Apply for Admission 2026
              </Link>
              <Link
                to="/contact"
                className="rounded-xl border border-white/30 bg-white/10 px-6 py-3 text-xs font-bold text-white hover:bg-white/20 transition-colors backdrop-blur-xs"
              >
                Schedule Campus Visit
              </Link>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};
