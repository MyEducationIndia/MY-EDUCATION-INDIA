import React from "react";
import { Webhook, Plus, ArrowUpRight, ArrowDownLeft } from "lucide-react";

export const WebhooksManagerPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Webhooks & Event Streams</h1>
      <p className="text-sm text-gray-500">Manage inbound event listeners with HMAC signature verification and outbound dispatches with exponential retry.</p>
    </div>
  );
};
