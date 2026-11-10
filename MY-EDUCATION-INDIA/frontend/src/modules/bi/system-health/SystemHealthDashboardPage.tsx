import React from "react";
import { Server, Database, Cpu, HardDrive, CheckCircle2 } from "lucide-react";

export const SystemHealthDashboardPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">ERP Cluster Infrastructure & Health Monitor</h1>
      <p className="text-sm text-gray-500">Real-time status of PostgreSQL query latency, background queue workers, notification brokers, and storage pools</p>
    </div>
  );
};
