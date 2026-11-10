import React from "react";
import { ShieldCheck, Lock, Key, AlertTriangle, UserX } from "lucide-react";

export const SecurityCenterPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Platform Security & Access Governance</h1>
      <p className="text-sm text-gray-500">Enforce enterprise password complexity, failed login lockouts, IP CIDR restrictions, and session idle timeouts</p>
    </div>
  );
};
