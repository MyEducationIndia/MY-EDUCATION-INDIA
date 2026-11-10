import React from "react";
import { Link, useLocation } from "react-router-dom";
import { ChevronRight, Home } from "lucide-react";

interface RouteTitleMap {
  [key: string]: string;
}

const ROUTE_LABELS: RouteTitleMap = {
  about: "About Institute",
  courses: "Academic Courses",
  admissions: "Admissions 2026",
  faculty: "Faculty Directory",
  staff: "Administrative Staff",
  placements: "Corporate Placements",
  recruiters: "Recruiting Partners",
  stories: "Alumni Success Stories",
  events: "Campus Events",
  news: "News & Media",
  notices: "Circulars & Notices",
  gallery: "Campus Gallery",
  downloads: "Downloads & Forms",
  testimonials: "Student Reviews",
  contact: "Contact Desk",
  search: "Global Search",
  sitemap: "Sitemap Index",
  login: "Universal Login",
};

export const BreadcrumbNav: React.FC = () => {
  const location = useLocation();
  const pathnames = location.pathname.split("/").filter((x) => x);

  // Don't show on root home page
  if (pathnames.length === 0) {
    return null;
  }

  // Format slug or parameter to readable text
  const formatSegment = (segment: string): string => {
    if (ROUTE_LABELS[segment]) {
      return ROUTE_LABELS[segment];
    }
    return segment
      .replace(/-/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  return (
    <nav
      aria-label="Breadcrumb"
      className="bg-slate-50 border-b border-slate-200/80 py-2.5 px-4 sm:px-6 lg:px-8 text-xs text-slate-500"
    >
      <div className="max-w-7xl mx-auto flex items-center space-x-2 overflow-x-auto no-scrollbar">
        <Link
          to="/"
          className="inline-flex items-center gap-1 text-slate-600 hover:text-indigo-600 transition font-medium"
        >
          <Home className="w-3.5 h-3.5 text-slate-400" />
          <span>Home</span>
        </Link>

        {pathnames.map((value, index) => {
          const to = `/${pathnames.slice(0, index + 1).join("/")}`;
          const isLast = index === pathnames.length - 1;
          const label = formatSegment(value);

          return (
            <React.Fragment key={to}>
              <ChevronRight className="w-3 h-3 text-slate-400 shrink-0" />
              {isLast ? (
                <span className="font-bold text-slate-900 truncate max-w-[200px] sm:max-w-md">
                  {label}
                </span>
              ) : (
                <Link
                  to={to}
                  className="hover:text-indigo-600 transition font-medium text-slate-600 truncate max-w-[150px]"
                >
                  {label}
                </Link>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </nav>
  );
};
