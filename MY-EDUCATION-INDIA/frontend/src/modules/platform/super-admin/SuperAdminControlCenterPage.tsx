import React from "react";
import { Sliders, Layers, Globe, Shield, Users, Database, LayoutTemplate, CheckCircle2 } from "lucide-react";

export const SuperAdminControlCenterPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Super Admin Master Control Center</h1>
          <p className="text-sm text-gray-500">Universal institutional governance: enable/disable modules, dynamic page builder, and role-based ACL</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-50 text-indigo-600 rounded-lg"><Layers className="w-6 h-6" /></div>
            <div>
              <h3 className="font-semibold text-gray-900">Module Governance</h3>
              <p className="text-xs text-gray-500">20 / 20 Active Modules</p>
            </div>
          </div>
          <p className="text-sm text-gray-600">Install, update, clone, or license modules across institutes without application redeployments.</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-50 text-emerald-600 rounded-lg"><Globe className="w-6 h-6" /></div>
            <div>
              <h3 className="font-semibold text-gray-900">Website CMS Control</h3>
              <p className="text-xs text-gray-500">Full Dynamic Rendering</p>
            </div>
          </div>
          <p className="text-sm text-gray-600">Control visibility, drafts, and scheduled releases for all public website sections and landing pages.</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-purple-50 text-purple-600 rounded-lg"><LayoutTemplate className="w-6 h-6" /></div>
            <div>
              <h3 className="font-semibold text-gray-900">Form & Menu Studio</h3>
              <p className="text-xs text-gray-500">Visual Zero-Code Builder</p>
            </div>
          </div>
          <p className="text-sm text-gray-600">Build custom drag & drop admission forms, approval flows, and nested navigation menus.</p>
        </div>
      </div>
    </div>
  );
};
