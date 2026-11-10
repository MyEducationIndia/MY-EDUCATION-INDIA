import React from "react";
import { Flag, Sliders, ToggleLeft, ToggleRight, Users } from "lucide-react";

export const FeatureFlagsPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dynamic Feature Flags & Canary Rollouts</h1>
      <p className="text-sm text-gray-500">Enable or disable module capabilities dynamically by percentage rollout, user roles, or branch clusters</p>
    </div>
  );
};
