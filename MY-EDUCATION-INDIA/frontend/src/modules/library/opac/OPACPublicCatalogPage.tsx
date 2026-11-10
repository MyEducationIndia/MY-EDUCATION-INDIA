import React, { useState } from "react";
import { Search, BookOpen, MapPin } from "lucide-react";

export const OPACPublicCatalogPage: React.FC = () => {
  const [query, setQuery] = useState("");
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight sm:text-4xl">
            Online Public Access Catalog (OPAC)
          </h1>
          <p className="mt-3 text-lg text-gray-500">
            Search physical books, eBooks, and research publications across institute libraries
          </p>
        </div>

        <div className="bg-white p-4 rounded-2xl shadow-md border border-gray-200">
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Search by Title, Author, Subject or ISBN..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button className="px-6 py-3 bg-indigo-600 text-white rounded-xl font-medium text-sm hover:bg-indigo-700 flex items-center gap-2">
              <Search className="w-4 h-4" /> Search Catalog
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
