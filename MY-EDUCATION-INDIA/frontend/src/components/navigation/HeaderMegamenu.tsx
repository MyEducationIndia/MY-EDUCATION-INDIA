import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  ChevronDown,
  Sparkles,
  BookOpen,
  GraduationCap,
  Briefcase,
  Calendar,
  Layers,
  ArrowRight,
  ExternalLink,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import { NavigationMenuItem } from "@/types/website.types";

interface HeaderMegamenuProps {
  onMobileItemClick?: () => void;
  isMobile?: boolean;
}

export const HeaderMegamenu: React.FC<HeaderMegamenuProps> = ({
  onMobileItemClick,
  isMobile = false,
}) => {
  const location = useLocation();
  const [activeMenuId, setActiveMenuId] = useState<string | null>(null);

  const { data: menuItems = [] } = useQuery<NavigationMenuItem[]>({
    queryKey: ["public_megamenu_tree"],
    queryFn: async () => {
      return await websiteService.getPublicMegamenu("HEADER_MAIN");
    },
    staleTime: 5 * 60 * 1000,
  });

  // Fallback default navigation if database seed is loading
  const defaultNav: NavigationMenuItem[] = [
    {
      id: "nav-about",
      institute_id: "default",
      menu_location: "HEADER_MAIN",
      title: "About",
      path: "/about",
      icon_name: null,
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: true,
      display_order: 1,
      is_active: true,
      children: [
        {
          id: "about-1",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Overview & Leadership",
          path: "/about",
          icon_name: null,
          badge_text: "Vision",
          description: "Statutory governance, Chancellor vision, and mission",
          parent_id: "nav-about",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 1,
          is_active: true,
          children: [],
        },
        {
          id: "about-2",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Accreditations & NAAC",
          path: "/about",
          icon_name: null,
          badge_text: "Grade A+",
          description: "Autonomous NIRF and NBA quality rankings",
          parent_id: "nav-about",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 2,
          is_active: true,
          children: [],
        },
        {
          id: "about-3",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Campus Infrastructure",
          path: "/about",
          icon_name: null,
          badge_text: "Indore HQ",
          description: "Research laboratories, sports complex, and hostels",
          parent_id: "nav-about",
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
      id: "nav-academics",
      institute_id: "default",
      menu_location: "HEADER_MAIN",
      title: "Academics",
      path: "/courses",
      icon_name: null,
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: true,
      display_order: 2,
      is_active: true,
      children: [
        {
          id: "acad-1",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "All Degree Programs",
          path: "/courses",
          icon_name: null,
          badge_text: "UG / PG",
          description: "Industry-aligned undergraduate and master courses",
          parent_id: "nav-academics",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 1,
          is_active: true,
          children: [],
        },
        {
          id: "acad-2",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "B.Tech Computer Science",
          path: "/courses",
          icon_name: null,
          badge_text: "AICTE",
          description: "Four-year flagship engineering curriculum",
          parent_id: "nav-academics",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 2,
          is_active: true,
          children: [],
        },
        {
          id: "acad-3",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "M.Tech Cloud & AI",
          path: "/courses",
          icon_name: null,
          badge_text: "New",
          description: "Specialized postgraduate engineering cohort",
          parent_id: "nav-academics",
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
      id: "nav-admissions",
      institute_id: "default",
      menu_location: "HEADER_MAIN",
      title: "Admissions",
      path: "/admissions",
      icon_name: null,
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: true,
      display_order: 3,
      is_active: true,
      children: [
        {
          id: "adm-1",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Admissions 2026-27",
          path: "/admissions",
          icon_name: null,
          badge_text: "Open",
          description: "Online application form, counseling, and seat matrix",
          parent_id: "nav-admissions",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 1,
          is_active: true,
          children: [],
        },
        {
          id: "adm-2",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Fee Structures",
          path: "/admissions",
          icon_name: null,
          description: "Semester fee breakdowns and installment schedules",
          parent_id: "nav-admissions",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 2,
          is_active: true,
          children: [],
        },
        {
          id: "adm-3",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Scholarships",
          path: "/admissions",
          icon_name: null,
          badge_text: "Up to 100%",
          description: "Merit-based fee waivers and defense grants",
          parent_id: "nav-admissions",
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
      id: "nav-faculty",
      institute_id: "default",
      menu_location: "HEADER_MAIN",
      title: "Faculty",
      path: "/faculty",
      icon_name: null,
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: false,
      display_order: 4,
      is_active: true,
      children: [],
    },
    {
      id: "nav-placements",
      institute_id: "default",
      menu_location: "HEADER_MAIN",
      title: "Placements",
      path: "/placements",
      icon_name: null,
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: true,
      display_order: 5,
      is_active: true,
      children: [
        {
          id: "pl-1",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Placement Records",
          path: "/placements",
          icon_name: null,
          badge_text: "₹52 LPA",
          description: "Annual packages, median salary, and placement audits",
          parent_id: "nav-placements",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 1,
          is_active: true,
          children: [],
        },
        {
          id: "pl-2",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Recruiting Partners",
          path: "/recruiters",
          icon_name: null,
          description: "250+ Fortune 500 tech companies and corporate tie-ups",
          parent_id: "nav-placements",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 2,
          is_active: true,
          children: [],
        },
        {
          id: "pl-3",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Alumni Stories",
          path: "/stories",
          icon_name: null,
          description: "Graduates working across top global organizations",
          parent_id: "nav-placements",
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
      id: "nav-campus",
      institute_id: "default",
      menu_location: "HEADER_MAIN",
      title: "Campus Life",
      path: "/events",
      icon_name: null,
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: true,
      display_order: 6,
      is_active: true,
      children: [
        {
          id: "cl-1",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Events & Seminars",
          path: "/events",
          icon_name: null,
          description: "Hackathons, cultural fests, and expert workshops",
          parent_id: "nav-campus",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 1,
          is_active: true,
          children: [],
        },
        {
          id: "cl-2",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Notices & Circulars",
          path: "/notices",
          icon_name: null,
          badge_text: "Live",
          description: "Examination timetables and academic registrar notices",
          parent_id: "nav-campus",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 2,
          is_active: true,
          children: [],
        },
        {
          id: "cl-3",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Campus Media Gallery",
          path: "/gallery",
          icon_name: null,
          description: "Campus photographs and laboratory facilities",
          parent_id: "nav-campus",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 3,
          is_active: true,
          children: [],
        },
        {
          id: "cl-4",
          institute_id: "default",
          menu_location: "HEADER_MAIN",
          title: "Downloads & Forms",
          path: "/downloads",
          icon_name: null,
          badge_text: "PDF",
          description: "Official prospectuses, syllabus, and administrative forms",
          parent_id: "nav-campus",
          is_external: false,
          open_new_tab: false,
          is_mega_menu: false,
          display_order: 4,
          is_active: true,
          children: [],
        },
      ],
    },
    {
      id: "nav-contact",
      institute_id: "default",
      menu_location: "HEADER_MAIN",
      title: "Contact",
      path: "/contact",
      icon_name: null,
      parent_id: null,
      is_external: false,
      open_new_tab: false,
      is_mega_menu: false,
      display_order: 7,
      is_active: true,
      children: [],
    },
  ];

  const itemsToRender = menuItems.length > 0 ? menuItems : defaultNav;

  // Mobile Render
  if (isMobile) {
    return (
      <div className="space-y-1 py-2">
        {itemsToRender.map((item) => {
          const hasChildren = item.children && item.children.length > 0;
          const isExpanded = activeMenuId === item.id;
          const isActive = location.pathname === item.path;

          return (
            <div key={item.id} className="border-b border-slate-100 last:border-b-0">
              <div className="flex items-center justify-between">
                <Link
                  to={item.path}
                  onClick={onMobileItemClick}
                  className={`flex-1 px-4 py-3 text-sm font-bold transition flex items-center gap-2 ${
                    isActive
                      ? "text-indigo-600 bg-indigo-50/50"
                      : "text-slate-700 hover:text-indigo-600"
                  }`}
                >
                  {item.title}
                  {item.badge_text && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-amber-100 text-amber-800">
                      {item.badge_text}
                    </span>
                  )}
                </Link>
                {hasChildren && (
                  <button
                    onClick={() => setActiveMenuId(isExpanded ? null : item.id)}
                    className="p-3 text-slate-400 hover:text-slate-600"
                  >
                    <ChevronDown
                      className={`w-4 h-4 transition-transform duration-200 ${
                        isExpanded ? "rotate-180 text-indigo-600" : ""
                      }`}
                    />
                  </button>
                )}
              </div>

              {hasChildren && isExpanded && (
                <div className="bg-slate-50 px-4 py-2 space-y-2 border-t border-slate-100">
                  {item.children.map((child) => (
                    <Link
                      key={child.id}
                      to={child.path}
                      onClick={onMobileItemClick}
                      className="block p-2 rounded-lg hover:bg-white text-xs font-semibold text-slate-700 hover:text-indigo-600 transition"
                    >
                      <div className="flex items-center justify-between">
                        <span>{child.title}</span>
                        {child.badge_text && (
                          <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-indigo-100 text-indigo-700">
                            {child.badge_text}
                          </span>
                        )}
                      </div>
                      {child.description && (
                        <p className="text-[11px] text-slate-400 font-normal mt-0.5 line-clamp-1">
                          {child.description}
                        </p>
                      )}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  }

  // Desktop Hover Megamenu
  return (
    <nav className="hidden lg:flex items-center gap-1">
      {itemsToRender.map((item) => {
        const hasChildren = item.children && item.children.length > 0;
        const isActive =
          location.pathname === item.path ||
          (hasChildren &&
            item.children.some((c) => location.pathname === c.path));

        return (
          <div
            key={item.id}
            className="relative"
            onMouseEnter={() => hasChildren && setActiveMenuId(item.id)}
            onMouseLeave={() => setActiveMenuId(null)}
          >
            <Link
              to={item.path}
              className={`px-3 py-2 rounded-lg text-sm font-bold transition inline-flex items-center gap-1.5 ${
                isActive
                  ? "text-indigo-600 bg-indigo-50/80"
                  : "text-slate-700 hover:text-indigo-600 hover:bg-slate-50"
              }`}
            >
              <span>{item.title}</span>
              {item.badge_text && (
                <span className="px-1.5 py-0.2 rounded text-[10px] font-extrabold uppercase bg-amber-100 text-amber-800">
                  {item.badge_text}
                </span>
              )}
              {hasChildren && (
                <ChevronDown
                  className={`w-3.5 h-3.5 transition-transform duration-200 ${
                    activeMenuId === item.id ? "rotate-180 text-indigo-600" : "text-slate-400"
                  }`}
                />
              )}
            </Link>

            {/* Desktop Megamenu Card Dropdown */}
            {hasChildren && activeMenuId === item.id && (
              <div className="absolute top-full left-0 pt-2 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
                <div className="bg-white rounded-2xl shadow-2xl border border-slate-200/80 p-5 w-80 sm:w-96 space-y-2 backdrop-blur-md">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                      {item.title} Portals
                    </span>
                    <Link
                      to={item.path}
                      className="text-xs text-indigo-600 hover:text-indigo-800 font-bold flex items-center gap-1"
                    >
                      View Hub <ArrowRight className="w-3 h-3" />
                    </Link>
                  </div>

                  <div className="space-y-1.5 pt-1">
                    {item.children.map((child) => (
                      <Link
                        key={child.id}
                        to={child.path}
                        className="p-2.5 rounded-xl hover:bg-indigo-50/70 transition group block"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-slate-800 group-hover:text-indigo-900 transition flex items-center gap-1.5">
                            {child.title}
                          </span>
                          {child.badge_text && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-indigo-100 text-indigo-700">
                              {child.badge_text}
                            </span>
                          )}
                        </div>
                        {child.description && (
                          <p className="text-[11px] text-slate-500 font-normal line-clamp-1 mt-0.5 group-hover:text-slate-600">
                            {child.description}
                          </p>
                        )}
                      </Link>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </nav>
  );
};
