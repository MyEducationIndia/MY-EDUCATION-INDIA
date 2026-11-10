import React, { useState } from "react";
import { Plus, Filter, CheckCircle2, Shield, Settings, Play } from "lucide-react";

export const ProviderDirectoryPage: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");
  const categories = ["ALL", "SMS", "WHATSAPP", "EMAIL", "PUSH", "PAYMENT", "VIDEO", "STORAGE", "AI", "MAPS", "OTP"];

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">API Provider Registry</h1>
          <p className="text-sm text-gray-500">Configure external cloud gateways without code changes. Select default and failover routing.</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium">
          <Plus className="w-4 h-4" /> Connect New Provider
        </button>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
              selectedCategory === cat
                ? "bg-indigo-600 text-white"
                : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>
    </div>
  );
};
