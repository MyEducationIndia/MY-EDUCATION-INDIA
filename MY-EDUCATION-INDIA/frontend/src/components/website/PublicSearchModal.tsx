import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Search,
  X,
  FileText,
  Calendar,
  Award,
  BookOpen,
  ArrowRight,
  Clock,
  ExternalLink,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import { SearchResultItem } from "@/types/website.types";

interface PublicSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const PublicSearchModal: React.FC<PublicSearchModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      setQuery("");
      setResults([]);
      setHasSearched(false);
      return;
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  // Debounced search trigger
  useEffect(() => {
    if (query.trim().length < 2) {
      setResults([]);
      setHasSearched(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      try {
        const data = await websiteService.search(query.trim(), 15);
        setResults(data.results || []);
        setHasSearched(true);
      } catch (err) {
        console.error("Search failed:", err);
      } finally {
        setIsLoading(false);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [query]);

  if (!isOpen) return null;

  const getEntityIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case "course":
        return <BookOpen className="h-4 w-4 text-blue-600" />;
      case "notice":
      case "circular":
        return <FileText className="h-4 w-4 text-amber-600" />;
      case "event":
        return <Calendar className="h-4 w-4 text-purple-600" />;
      case "news":
      case "achievement":
        return <Award className="h-4 w-4 text-emerald-600" />;
      default:
        return <FileText className="h-4 w-4 text-slate-500" />;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4" role="dialog" aria-modal="true">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal Dialog */}
      <div className="relative w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl animate-in zoom-in-95 duration-150">
        {/* Search Input Bar */}
        <div className="flex items-center gap-3 border-b border-slate-200 pb-3.5">
          <Search className="h-5 w-5 text-slate-400" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search across programs, notices, faculty, admissions..."
            className="w-full text-sm font-medium outline-hidden placeholder:text-slate-400 text-slate-900"
          />
          {query && (
            <button
              type="button"
              onClick={() => setQuery("")}
              className="text-xs font-semibold text-slate-400 hover:text-slate-600"
            >
              Clear
            </button>
          )}
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
            aria-label="Close search"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Results Container */}
        <div className="mt-4 max-h-96 overflow-y-auto space-y-2">
          {isLoading && (
            <div className="py-8 text-center text-xs font-semibold text-slate-500">
              Searching institutional knowledge catalog...
            </div>
          )}

          {!isLoading && hasSearched && results.length === 0 && (
            <div className="py-10 text-center">
              <p className="text-sm font-bold text-slate-800">No matching results found</p>
              <p className="text-xs text-slate-500 mt-1">
                Try searching for general keywords like "engineering", "admissions", or "scholarship".
              </p>
            </div>
          )}

          {!isLoading && results.length > 0 && (
            <div className="space-y-1.5">
              <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-2 pb-1">
                Results ({results.length})
              </p>
              {results.map((res) => (
                <Link
                  key={res.id}
                  to={res.target_url}
                  onClick={onClose}
                  className="group flex items-start gap-3 rounded-xl p-3 hover:bg-brand-50/60 transition border border-transparent hover:border-brand-200"
                >
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-100 group-hover:bg-white group-hover:shadow-xs transition">
                    {getEntityIcon(res.entity_type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="text-xs font-bold text-slate-900 group-hover:text-brand-700 truncate">
                        {res.title}
                      </p>
                      <span className="rounded bg-slate-100 px-1.5 py-0.5 text-[9px] font-bold uppercase text-slate-600">
                        {res.entity_type}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">
                      {res.summary}
                    </p>
                  </div>
                  <ArrowRight className="h-4 w-4 text-slate-300 group-hover:text-brand-600 shrink-0 self-center transition-transform group-hover:translate-x-0.5" />
                </Link>
              ))}
            </div>
          )}

          {!query && (
            <div className="py-6 px-3">
              <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                Quick Suggested Searches
              </p>
              <div className="flex flex-wrap gap-2">
                {["Computer Science", "Entrance Exam", "Scholarship", "Verification", "Admissions"].map(
                  (tag) => (
                    <button
                      key={tag}
                      type="button"
                      onClick={() => setQuery(tag)}
                      className="rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs font-medium text-slate-700 hover:border-brand-300 hover:bg-brand-50 hover:text-brand-700 transition"
                    >
                      {tag}
                    </button>
                  )
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
