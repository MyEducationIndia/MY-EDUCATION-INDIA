import React from "react";
import { Users, UserPlus } from "lucide-react";

export const LibraryMembersPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Library Members Directory</h1>
      <p className="text-sm text-gray-500">Configure member borrowing allowances, issue validity periods, and membership passes</p>
    </div>
  );
};
