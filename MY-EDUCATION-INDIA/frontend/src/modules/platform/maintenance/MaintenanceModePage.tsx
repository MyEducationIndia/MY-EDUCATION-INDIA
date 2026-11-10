import React from "react";
import { Construction, Bell, Users, Clock } from "lucide-react";

export const MaintenanceModePage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Maintenance Windows & Traffic Routing</h1>
      <p className="text-sm text-gray-500">Schedule maintenance downtime, broadcast custom notice banners, and whitelist emergency administrator IPs</p>
    </div>
  );
};
