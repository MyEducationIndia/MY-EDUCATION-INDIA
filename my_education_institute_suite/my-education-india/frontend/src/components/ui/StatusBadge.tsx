import React from "react";

interface StatusBadgeProps {
  active: boolean;
  activeLabel?: string;
  inactiveLabel?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  active,
  activeLabel = "Active",
  inactiveLabel = "Disabled",
}) => {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
        active
          ? "bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-600/20"
          : "bg-slate-100 text-slate-600 ring-1 ring-inset ring-slate-500/20"
      }`}
    >
      <span
        className={`h-1.5 w-1.5 rounded-full ${
          active ? "bg-emerald-600" : "bg-slate-400"
        }`}
      />
      {active ? activeLabel : inactiveLabel}
    </span>
  );
};
