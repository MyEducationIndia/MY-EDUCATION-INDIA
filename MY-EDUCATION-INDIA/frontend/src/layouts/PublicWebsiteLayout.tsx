import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { websiteService } from "@/services/websiteService";
import { PublicMainHeader } from "@/components/website/PublicMainHeader";
import { PublicLiveTicker } from "@/components/website/PublicLiveTicker";
import { PublicFooter } from "@/components/website/PublicFooter";
import { GlobalSearchModal } from "@/components/search/GlobalSearchModal";
import { BreadcrumbNav } from "@/components/navigation/BreadcrumbNav";
import { PublicMobileDrawer } from "@/components/website/PublicMobileDrawer";
import { PublicWebsiteFrameworkBundle } from "@/types/website.types";

const FALLBACK_BUNDLE: PublicWebsiteFrameworkBundle = {
  settings: {
    id: "default-settings",
    institute_id: "default-inst",
    site_title: "MY EDUCATION INDIA",
    tagline: "National Flagship Higher Education Institution",
    header_logo_url: null,
    footer_logo_url: null,
    favicon_url: null,
    header_is_sticky: true,
    header_show_search: true,
    header_show_login: true,
    header_login_button_text: "Login",
    header_login_route: "/login",
    contact_phone: "+91 731 245 6789",
    contact_email: "admissions@myeducation.in",
    contact_address: "Campus Square, Institutional Sector, Indore, Madhya Pradesh 452001",
    meta_description: "Official Portal of MY EDUCATION INDIA. Autonomous Higher Education & Research Campus.",
    meta_keywords: "higher education, degrees, indore, engineering, management, cbt, admissions",
    og_image_url: null,
    google_analytics_id: null,
    is_maintenance_mode: false,
    maintenance_message: null,
    custom_css: null,
    custom_head_scripts: null,
    updated_at: new Date().toISOString(),
  },
  theme: {
    id: "default-theme",
    institute_id: "default-inst",
    primary_color: "#1E40AF",
    secondary_color: "#0D9488",
    accent_color: "#F59E0B",
    background_color: "#F8FAFC",
    surface_color: "#FFFFFF",
    text_primary_color: "#0F172A",
    text_secondary_color: "#475569",
    font_family: "Inter, system-ui, sans-serif",
    heading_font_family: "Inter, system-ui, sans-serif",
    border_radius: "0.75rem",
    button_style: "rounded",
    shadow_style: "soft",
    animation_enabled: true,
    updated_at: new Date().toISOString(),
  },
  header_navigation: [
    {
      id: "nav-1",
      institute_id: "default-inst",
      menu_location: "HEADER_MAIN",
      title: "Home",
      path: "/",
      icon_name: "Home",
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: false,
      display_order: 1,
      is_active: true,
      children: [],
    },
    {
      id: "nav-2",
      institute_id: "default-inst",
      menu_location: "HEADER_MAIN",
      title: "About",
      path: "/about",
      icon_name: "Building2",
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: true,
      display_order: 2,
      children: [
        {
          id: "nav-2-1",
          institute_id: "default-inst",
          menu_location: "HEADER_MAIN",
          title: "Vision & Mission",
          path: "/about/vision-mission",
          icon_name: null,
          parent_id: "nav-2",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 1,
          is_active: true,
          children: [],
        },
        {
          id: "nav-2-2",
          institute_id: "default-inst",
          menu_location: "HEADER_MAIN",
          title: "Director's Message",
          path: "/about/directors-message",
          icon_name: null,
          parent_id: "nav-2",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 2,
          is_active: true,
          children: [],
        },
      ],
    },
    {
      id: "nav-3",
      institute_id: "default-inst",
      menu_location: "HEADER_MAIN",
      title: "Academics",
      path: "/courses",
      icon_name: "BookOpen",
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: true,
      display_order: 3,
      children: [
        {
          id: "nav-3-1",
          institute_id: "default-inst",
          menu_location: "HEADER_MAIN",
          title: "Undergraduate Degrees",
          path: "/courses",
          icon_name: null,
          parent_id: "nav-3",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 1,
          is_active: true,
          children: [],
        },
        {
          id: "nav-3-2",
          institute_id: "default-inst",
          menu_location: "HEADER_MAIN",
          title: "Postgraduate Degrees",
          path: "/courses",
          icon_name: null,
          parent_id: "nav-3",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 2,
          is_active: true,
          children: [],
        },
      ],
    },
    {
      id: "nav-4",
      institute_id: "default-inst",
      menu_location: "HEADER_MAIN",
      title: "Admissions",
      path: "/admissions",
      icon_name: "ClipboardList",
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: true,
      display_order: 4,
      children: [
        {
          id: "nav-4-1",
          institute_id: "default-inst",
          menu_location: "HEADER_MAIN",
          title: "Admission Process",
          path: "/admissions/process",
          icon_name: null,
          parent_id: "nav-4",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 1,
          is_active: true,
          children: [],
        },
        {
          id: "nav-4-2",
          institute_id: "default-inst",
          menu_location: "HEADER_MAIN",
          title: "Eligibility Criteria",
          path: "/admissions/eligibility",
          icon_name: null,
          parent_id: "nav-4",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 2,
          is_active: true,
          children: [],
        },
        {
          id: "nav-4-3",
          institute_id: "default-inst",
          menu_location: "HEADER_MAIN",
          title: "Fee Structure",
          path: "/admissions/fees",
          icon_name: null,
          parent_id: "nav-4",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 3,
          is_active: true,
          children: [],
        },
      ],
    },
    {
      id: "nav-5",
      institute_id: "default-inst",
      menu_location: "HEADER_MAIN",
      title: "Verification",
      path: "/verify",
      icon_name: "FileBadge",
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: false,
      display_order: 5,
      children: [],
    },
    {
      id: "nav-6",
      institute_id: "default-inst",
      menu_location: "HEADER_MAIN",
      title: "Contact",
      path: "/contact",
      icon_name: "Phone",
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: false,
      display_order: 6,
      children: [],
    },
  ],
  ticker_announcements: [
    {
      id: "t-1",
      institute_id: "default-inst",
      title: "National Entrance Examination 2026-27 Registrations Open Now — Apply Online",
      category: "Admission",
      link_url: "/admissions/apply",
      is_external: false,
      open_new_tab: false,
      is_emergency: false,
      priority_level: 1,
      publish_at: new Date().toISOString(),
      expire_at: null,
      is_active: true,
      display_order: 1,
      created_at: new Date().toISOString(),
    },
    {
      id: "t-2",
      institute_id: "default-inst",
      title: "End-Term Semester Examination Timetable & Seating Chart Released",
      category: "Examination",
      link_url: "/admin/exams",
      is_external: false,
      open_new_tab: false,
      is_emergency: false,
      priority_level: 2,
      publish_at: new Date().toISOString(),
      expire_at: null,
      is_active: true,
      display_order: 2,
      created_at: new Date().toISOString(),
    },
    {
      id: "t-3",
      institute_id: "default-inst",
      title: "Merit-cum-Means Scholarships 2026 Application Window Extended to Nov 30",
      category: "Scholarship",
      link_url: "/admissions/scholarships",
      is_external: false,
      open_new_tab: false,
      is_emergency: false,
      priority_level: 3,
      publish_at: new Date().toISOString(),
      expire_at: null,
      is_active: true,
      display_order: 3,
      created_at: new Date().toISOString(),
    },
  ],
  social_links: [
    {
      id: "s-1",
      institute_id: "default-inst",
      platform: "linkedin",
      url: "https://linkedin.com/company/myeducationindia",
      display_order: 1,
      is_active: true,
    },
    {
      id: "s-2",
      institute_id: "default-inst",
      platform: "twitter",
      url: "https://twitter.com/myeducationin",
      display_order: 2,
      is_active: true,
    },
    {
      id: "s-3",
      institute_id: "default-inst",
      platform: "youtube",
      url: "https://youtube.com/@myeducationindia",
      display_order: 3,
      is_active: true,
    },
  ],
};

export const PublicWebsiteLayout: React.FC = () => {
  const [searchModalOpen, setSearchModalOpen] = useState(false);
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  // High-speed API fetch for website bundle with immediate fallback
  const { data: bundle = FALLBACK_BUNDLE } = useQuery({
    queryKey: ["public-website-bundle"],
    queryFn: websiteService.getPublicFrameworkBundle,
    staleTime: 60000,
  });

  const { settings, header_navigation, ticker_announcements, social_links, theme } = bundle;

  return (
    <div
      className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans"
      style={{
        // Dynamic theme variable injection directly from database
        ["--brand-primary" as any]: theme.primary_color,
        ["--brand-secondary" as any]: theme.secondary_color,
      }}
    >
      {/* 1. STICKY MAIN HEADER */}
      <PublicMainHeader
        settings={settings}
        navigation={header_navigation}
        onOpenSearch={() => setSearchModalOpen(true)}
        onOpenMobileMenu={() => setMobileDrawerOpen(true)}
      />

      {/* 2. STICKY LIVE UPDATE TICKER (Immediately below main header) */}
      <PublicLiveTicker items={ticker_announcements} />

      {/* 2B. DYNAMIC BREADCRUMB NAVIGATION */}
      <BreadcrumbNav />

      {/* 3. DYNAMIC CONTENT VIEWPORT */}
      <main className="flex-1">
        <Outlet context={{ bundle }} />
      </main>

      {/* 4. FOOTER FOUNDATION */}
      <PublicFooter settings={settings} socialLinks={social_links} />

      {/* 5. ENHANCED GLOBAL SEARCH MODAL (Triggered via Header or Ctrl+K) */}
      <GlobalSearchModal
        isOpen={searchModalOpen}
        onClose={() => setSearchModalOpen(false)}
      />

      {/* 6. MOBILE NAVIGATION DRAWER */}
      <PublicMobileDrawer
        isOpen={mobileDrawerOpen}
        onClose={() => setMobileDrawerOpen(false)}
        settings={settings}
        navigation={header_navigation}
        onOpenSearch={() => setSearchModalOpen(true)}
      />
    </div>
  );
};
