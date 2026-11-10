import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  AlertCircle,
  Megaphone,
  ExternalLink,
  ChevronRight,
  Flame,
  Volume2,
} from "lucide-react";
import { WebsiteTickerItem } from "@/types/website.types";

interface PublicLiveTickerProps {
  items: WebsiteTickerItem[];
}

export const PublicLiveTicker: React.FC<PublicLiveTickerProps> = ({ items }) => {
  const [isPaused, setIsPaused] = useState(false);

  if (!items || items.length === 0) {
    return null;
  }

  // Check if any emergency notice exists
  const hasEmergency = items.some((item) => item.is_emergency);

  return (
    <div
      className={`relative z-30 flex h-10 w-full items-center border-b text-xs font-medium transition-colors ${
        hasEmergency
          ? "border-rose-300 bg-rose-600 text-white"
          : "border-brand-100 bg-brand-50/95 text-slate-800 backdrop-blur-md"
      }`}
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      role="region"
      aria-label="Live Institutional Updates"
    >
      <div className="mx-auto flex h-full w-full max-w-7xl items-center px-4 sm:px-6 lg:px-8">
        {/* Static Left Label Badge */}
        <div
          className={`flex shrink-0 items-center gap-1.5 rounded-lg px-2.5 py-1 text-[11px] font-bold tracking-wider uppercase shadow-2xs ${
            hasEmergency
              ? "bg-white text-rose-700 animate-pulse"
              : "bg-brand-600 text-white"
          }`}
        >
          {hasEmergency ? (
            <Flame className="h-3.5 w-3.5" />
          ) : (
            <Megaphone className="h-3.5 w-3.5" />
          )}
          <span>{hasEmergency ? "Emergency Alert" : "Live Updates"}</span>
        </div>

        {/* Marquee Ticker Track */}
        <div className="relative ml-4 flex-1 overflow-hidden">
          <div
            className={`flex w-max items-center gap-8 ${
              isPaused ? "animate-none" : "animate-marquee"
            }`}
            style={{
              animation: isPaused
                ? "none"
                : `marquee ${Math.max(25, items.length * 8)}s linear infinite`,
            }}
          >
            {/* Duplicated list to create infinite seamless scrolling loop */}
            {[...items, ...items].map((item, idx) => {
              const Content = (
                <span className="flex items-center gap-2 transition hover:underline">
                  <span
                    className={`inline-block rounded px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider ${
                      item.is_emergency
                        ? "bg-rose-800 text-rose-100"
                        : "bg-brand-200/80 text-brand-900"
                    }`}
                  >
                    {item.category}
                  </span>
                  <span className="font-semibold text-slate-800">{item.title}</span>
                  {item.is_external ? (
                    <ExternalLink className="h-3 w-3 text-slate-500" />
                  ) : (
                    <ChevronRight className="h-3 w-3 text-slate-500" />
                  )}
                </span>
              );

              return (
                <div key={`${item.id}-${idx}`} className="flex items-center">
                  {item.link_url ? (
                    item.is_external ? (
                      <a
                        href={item.link_url}
                        target={item.open_new_tab ? "_blank" : "_self"}
                        rel="noreferrer"
                        className="cursor-pointer"
                      >
                        {Content}
                      </a>
                    ) : (
                      <Link to={item.link_url} className="cursor-pointer">
                        {Content}
                      </Link>
                    )
                  ) : (
                    Content
                  )}
                  <span className="ml-8 text-slate-300">•</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
