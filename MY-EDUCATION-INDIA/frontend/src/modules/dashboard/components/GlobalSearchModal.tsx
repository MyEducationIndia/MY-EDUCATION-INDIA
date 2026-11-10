import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Search, X, User, GitBranch, Binary, ArrowRight } from "lucide-react";
import { dashboardApi } from "../api/dashboardApi";
import { GlobalSearchData } from "../types/dashboard.types";

interface GlobalSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const GlobalSearchModal: React.FC<GlobalSearchModalProps> = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [results, setResults] = useState<GlobalSearchData | null>(null);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    if (!searchTerm.trim() || searchTerm.length < 2) {
      setResults(null);
      return;
    }

    const timer = setTimeout(() => {
      setIsSearching(true);
      dashboardApi
        .searchGlobal(searchTerm.trim())
        .then(setResults)
        .finally(() => setIsSearching(false));
    }, 250);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center bg-slate-950/70 p-4 pt-16 backdrop-blur-xs">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-4 shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <div className="relative flex items-center border-b border-slate-200 pb-3 dark:border-slate-800">
          <Search className="h-5 w-5 text-slate-400" />
          <input
            type="search"
            autoFocus
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Global ERP Search (Students, Faculty, Branches, Roll No, Invoices...)"
            className="w-full bg-transparent px-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-hidden dark:text-white"
          />
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800 dark:hover:text-white"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="max-h-96 overflow-y-auto py-2">
          {isSearching && (
            <p className="py-6 text-center text-xs text-slate-500">Searching PostgreSQL records...</p>
          )}

          {!isSearching && results && results.total_results === 0 && (
            <p className="py-6 text-center text-xs text-slate-500">No matching records found for "{searchTerm}".</p>
          )}

          {!isSearching && results && results.total_results > 0 && (
            <div className="space-y-4">
              {Object.entries(results.grouped_results).map(([group, items]) => (
                <div key={group}>
                  <p className="px-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">{group}</p>
                  <div className="mt-1 space-y-1">
                    {items.map((item, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => {
                          onClose();
                          navigate(item.target_url);
                        }}
                        className="flex w-full items-center justify-between rounded-xl px-3 py-2 text-left transition hover:bg-slate-100 dark:hover:bg-slate-800"
                      >
                        <div className="flex items-center gap-3">
                          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-400">
                            {item.entity_type === "branch" ? <GitBranch className="h-4 w-4" /> : item.entity_type === "number_generator" ? <Binary className="h-4 w-4" /> : <User className="h-4 w-4" />}
                          </div>
                          <div>
                            <p className="text-xs font-bold text-slate-900 dark:text-white">{item.title}</p>
                            {item.subtitle && <p className="text-[11px] text-slate-500">{item.subtitle}</p>}
                          </div>
                        </div>
                        <ArrowRight className="h-4 w-4 text-slate-400" />
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
