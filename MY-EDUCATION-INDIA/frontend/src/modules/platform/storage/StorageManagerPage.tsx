import React from "react";
import { HardDrive, Cloud, Trash2, PieChart } from "lucide-react";

export const StorageManagerPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Object Storage & Media Pool Management</h1>
      <p className="text-sm text-gray-500">Configure local, AWS S3, and Cloudflare R2 object buckets, document retention rules, and automatic log rotation</p>
    </div>
  );
};
