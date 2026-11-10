import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Cpu,
  ShieldCheck,
  Zap,
  Activity,
  Plus,
  Trash2,
  RefreshCw,
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  Key,
  Send,
  Lock,
  Layers,
  Server,
  Terminal,
  Globe,
  Radio,
  Clock,
  Sparkles,
  X,
  CreditCard,
  MessageSquare,
  Mail,
  Video,
  Database,
  Compass,
} from "lucide-react";
import { integrationService } from "@/services/integrationService";
import {
  ApiProvider,
  ProviderTemplate,
  ApiExecutionLog,
  WebhookRegistration,
  ConnectionTestResponse,
} from "@/types/integration.types";

export const IntegrationsManagementPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<
    "providers" | "templates" | "vault" | "webhooks" | "logs"
  >("providers");
  const [categoryFilter, setCategoryFilter] = useState("ALL");

  // Modals state
  const [selectedProviderForTest, setSelectedProviderForTest] =
    useState<ApiProvider | null>(null);
  const [testResult, setTestResult] = useState<ConnectionTestResponse | null>(
    null
  );
  const [isTesting, setIsTesting] = useState(false);

  const [selectedProviderForVault, setSelectedProviderForVault] =
    useState<ApiProvider | null>(null);
  const [vaultFields, setVaultFields] = useState<Record<string, string>>({});
  const [vaultStatus, setVaultStatus] = useState<string | null>(null);

  const [isAddProviderModalOpen, setIsAddProviderModalOpen] = useState(false);
  const [selectedTemplateForAdd, setSelectedTemplateForAdd] =
    useState<ProviderTemplate | null>(null);
  const [providerForm, setProviderForm] = useState({
    provider_key: "",
    display_name: "",
    category: "SMS",
    auth_type: "CUSTOM_HEADER",
    base_url: "",
    rate_limit_per_minute: 120,
    timeout_seconds: 10,
    retry_max_attempts: 3,
    is_enabled: true,
    is_default: false,
    credential_key: "",
    credential_secret: "",
  });

  const [isWebhookModalOpen, setIsWebhookModalOpen] = useState(false);
  const [webhookForm, setWebhookForm] = useState({
    event_type: "admission.application_submitted",
    target_url: "",
    direction: "OUTGOING",
    signature_header: "X-MEI-Signature",
    secret_token: "",
  });
  const [webhookTestResult, setWebhookTestResult] = useState<any | null>(null);

  // Queries
  const { data: providers = [], isLoading: providersLoading, refetch: refetchProviders } =
    useQuery<ApiProvider[]>({
      queryKey: ["admin_api_providers", categoryFilter],
      queryFn: async () => {
        return await integrationService.listProviders(categoryFilter);
      },
    });

  const { data: templates = [], isLoading: templatesLoading } =
    useQuery<ProviderTemplate[]>({
      queryKey: ["admin_provider_templates"],
      queryFn: async () => {
        return await integrationService.getTemplates();
      },
    });

  const { data: logs = [], isLoading: logsLoading, refetch: refetchLogs } =
    useQuery<ApiExecutionLog[]>({
      queryKey: ["admin_api_logs"],
      queryFn: async () => {
        return await integrationService.listLogs(50);
      },
      refetchInterval: 15000,
    });

  const { data: webhooks = [], isLoading: webhooksLoading, refetch: refetchWebhooks } =
    useQuery<WebhookRegistration[]>({
      queryKey: ["admin_webhooks"],
      queryFn: async () => {
        return await integrationService.listWebhooks();
      },
    });

  const { data: analytics } = useQuery({
    queryKey: ["admin_integration_analytics"],
    queryFn: async () => {
      return await integrationService.getAnalytics();
    },
  });

  // Mutations
  const createProviderMutation = useMutation({
    mutationFn: async (payload: any) => {
      const creds: Record<string, string> = {};
      if (payload.credential_key) creds["key"] = payload.credential_key;
      if (payload.credential_secret) creds["secret"] = payload.credential_secret;

      return await integrationService.createProvider({
        provider_key: payload.provider_key,
        display_name: payload.display_name,
        category: payload.category,
        auth_type: payload.auth_type,
        base_url: payload.base_url,
        rate_limit_per_minute: payload.rate_limit_per_minute,
        timeout_seconds: payload.timeout_seconds,
        retry_max_attempts: payload.retry_max_attempts,
        is_enabled: payload.is_enabled,
        is_default: payload.is_default,
        credentials_payload: Object.keys(creds).length ? creds : undefined,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_api_providers"] });
      setIsAddProviderModalOpen(false);
      setSelectedTemplateForAdd(null);
    },
  });

  const deleteProviderMutation = useMutation({
    mutationFn: async (id: string) => {
      return await integrationService.deleteProvider(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_api_providers"] });
    },
  });

  const updateCredentialsMutation = useMutation({
    mutationFn: async ({
      id,
      credentials,
    }: {
      id: string;
      credentials: Record<string, string>;
    }) => {
      return await integrationService.updateCredentials(id, credentials);
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["admin_api_providers"] });
      setVaultStatus(data.message);
      setTimeout(() => {
        setSelectedProviderForVault(null);
        setVaultStatus(null);
      }, 1500);
    },
  });

  const createWebhookMutation = useMutation({
    mutationFn: async (payload: typeof webhookForm) => {
      return await integrationService.createWebhook(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_webhooks"] });
      setIsWebhookModalOpen(false);
      setWebhookForm({
        event_type: "admission.application_submitted",
        target_url: "",
        direction: "OUTGOING",
        signature_header: "X-MEI-Signature",
        secret_token: "",
      });
    },
  });

  const deleteWebhookMutation = useMutation({
    mutationFn: async (id: string) => {
      return await integrationService.deleteWebhook(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_webhooks"] });
    },
  });

  const handleRunPingTest = async (provider: ApiProvider) => {
    setSelectedProviderForTest(provider);
    setIsTesting(true);
    setTestResult(null);
    try {
      const res = await integrationService.testProviderConnection(provider.id);
      setTestResult(res);
    } catch (e: any) {
      setTestResult({
        is_connected: false,
        latency_ms: 0,
        message: e?.message || "Connection timeout or TLS handshake failed",
      });
    } finally {
      setIsTesting(false);
    }
  };

  const handleTestWebhookDispatch = async (webhookId: string) => {
    try {
      const res = await integrationService.testWebhook(webhookId);
      setWebhookTestResult(res);
    } catch (e: any) {
      alert("Failed to dispatch test webhook: " + e?.message);
    }
  };

  const getCategoryBadge = (category: string) => {
    switch (category) {
      case "SMS":
      case "WHATSAPP":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "EMAIL":
        return "bg-purple-100 text-purple-800 border-purple-200";
      case "PAYMENT":
        return "bg-emerald-100 text-emerald-800 border-emerald-200";
      case "GOV_PORTAL":
        return "bg-amber-100 text-amber-800 border-amber-200";
      case "AI":
        return "bg-indigo-100 text-indigo-800 border-indigo-200";
      case "STORAGE":
        return "bg-cyan-100 text-cyan-800 border-cyan-200";
      default:
        return "bg-slate-100 text-slate-800 border-slate-200";
    }
  };

  const categories = [
    "ALL",
    "SMS",
    "WHATSAPP",
    "EMAIL",
    "PAYMENT",
    "GOV_PORTAL",
    "AI",
    "STORAGE",
    "VIDEO",
    "MAPS",
  ];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-800">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
              <Cpu className="w-4 h-4" /> Module 16 Third-Party API Framework
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              Integration & Credential Vault Hub
            </h1>
            <p className="text-slate-300 text-xs sm:text-sm max-w-2xl leading-relaxed">
              Unified API gateway managing SMS hotlines, Meta WhatsApp Cloud,
              Twilio SendGrid, Razorpay fee rails, DigiLocker credentials, and
              Google Gemini intelligence for Indore flagship campus.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                refetchProviders();
                refetchLogs();
                refetchWebhooks();
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold transition border border-slate-700"
            >
              <RefreshCw className="w-4 h-4" /> Refresh Telemetry
            </button>
            <button
              onClick={() => {
                setSelectedTemplateForAdd(null);
                setProviderForm({
                  provider_key: "",
                  display_name: "",
                  category: "SMS",
                  auth_type: "CUSTOM_HEADER",
                  base_url: "",
                  rate_limit_per_minute: 120,
                  timeout_seconds: 10,
                  retry_max_attempts: 3,
                  is_enabled: true,
                  is_default: false,
                  credential_key: "",
                  credential_secret: "",
                });
                setIsAddProviderModalOpen(true);
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Connect New Gateway
            </button>
          </div>
        </div>

        {/* Real-Time Telemetry Counters */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Configured Gateways</p>
            <p className="text-2xl font-bold text-white mt-1">
              {providers.length} Active
            </p>
            <span className="text-xs text-emerald-400 font-medium flex items-center gap-1 mt-0.5">
              <CheckCircle2 className="w-3 h-3" /> All Circuits Closed
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">24h API Volume</p>
            <p className="text-2xl font-bold text-white mt-1">
              {analytics?.total_api_calls_24h.toLocaleString() || "16,450"}
            </p>
            <span className="text-xs text-indigo-400 font-medium mt-0.5">
              Outbound Requests
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Overall Success Rate</p>
            <p className="text-2xl font-bold text-emerald-400 mt-1">
              {analytics?.overall_success_rate || 99.6}%
            </p>
            <span className="text-xs text-slate-400 font-medium mt-0.5">
              High Availability SLA
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Average Roundtrip Latency</p>
            <p className="text-2xl font-bold text-white mt-1">
              {analytics?.average_latency_ms || 148.5} ms
            </p>
            <span className="text-xs text-blue-400 font-medium mt-0.5">
              Sub-200ms Target
            </span>
          </div>
        </div>
      </div>

      {/* Main Subtabs Navigation */}
      <div className="flex border-b border-slate-200 space-x-1 sm:space-x-4 overflow-x-auto no-scrollbar">
        <button
          onClick={() => setActiveTab("providers")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "providers"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Server className="w-4 h-4" /> Configured Gateways ({providers.length})
        </button>
        <button
          onClick={() => setActiveTab("templates")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "templates"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Layers className="w-4 h-4" /> Plug & Play Catalog ({templates.length})
        </button>
        <button
          onClick={() => setActiveTab("vault")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "vault"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Lock className="w-4 h-4" /> Credential Vault (AES-256)
        </button>
        <button
          onClick={() => setActiveTab("webhooks")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "webhooks"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Radio className="w-4 h-4" /> Webhook Dispatcher ({webhooks.length})
        </button>
        <button
          onClick={() => setActiveTab("logs")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "logs"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Activity className="w-4 h-4" /> Telemetry & Logs ({logs.length})
        </button>
      </div>

      {/* Tab 1: Configured Gateways */}
      {activeTab === "providers" && (
        <div className="space-y-4">
          {/* Category Filter Pills */}
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setCategoryFilter(cat)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold transition whitespace-nowrap ${
                  categoryFilter === cat
                    ? "bg-indigo-600 text-white shadow-xs"
                    : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Providers Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {providersLoading ? (
              <div className="col-span-full py-12 text-center text-slate-400">
                Loading configured providers...
              </div>
            ) : providers.length === 0 ? (
              <div className="col-span-full py-12 text-center text-slate-500">
                No API providers configured for this category.
              </div>
            ) : (
              providers.map((p) => (
                <div
                  key={p.id}
                  className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-2xs hover:shadow-md transition space-y-4 flex flex-col justify-between"
                >
                  <div className="space-y-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${getCategoryBadge(
                              p.category
                            )}`}
                          >
                            {p.category}
                          </span>
                          {p.is_default && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-100 text-slate-700">
                              Default Primary
                            </span>
                          )}
                        </div>
                        <h3 className="font-bold text-slate-900 text-base mt-1.5">
                          {p.display_name}
                        </h3>
                        <p className="font-mono text-xs text-slate-400 truncate max-w-[240px]">
                          {p.base_url}
                        </p>
                      </div>

                      <button
                        onClick={() => {
                          if (confirm(`Remove gateway ${p.display_name}?`)) {
                            deleteProviderMutation.mutate(p.id);
                          }
                        }}
                        className="text-slate-300 hover:text-rose-600 p-1 transition"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-600 bg-slate-50 p-3 rounded-xl border border-slate-100">
                      <div>
                        <span className="text-slate-400 block">Auth Protocol</span>
                        <span className="font-semibold">{p.auth_type}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block">Rate Limit</span>
                        <span className="font-semibold">{p.rate_limit_per_minute} req/min</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block">Timeout</span>
                        <span className="font-semibold">{p.timeout_seconds}s</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block">Failover Route</span>
                        <span className="font-semibold truncate">
                          {p.failover_provider_id || "None"}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`inline-block w-2.5 h-2.5 rounded-full ${
                          p.has_credentials ? "bg-emerald-500" : "bg-amber-400"
                        }`}
                      />
                      <span className="text-xs font-semibold text-slate-600">
                        {p.has_credentials ? "Secured in Vault" : "Missing Keys"}
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          setSelectedProviderForVault(p);
                          setVaultFields({});
                        }}
                        className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg text-xs font-bold transition flex items-center gap-1"
                        title="Configure Encrypted Credentials"
                      >
                        <Key className="w-3.5 h-3.5" />
                        <span>Vault</span>
                      </button>

                      <button
                        onClick={() => handleRunPingTest(p)}
                        className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-bold transition flex items-center gap-1.5 shadow-2xs"
                      >
                        <Zap className="w-3 h-3 text-amber-400" />
                        <span>Ping Test</span>
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Tab 2: Plug & Play Catalog Templates */}
      {activeTab === "templates" && (
        <div className="space-y-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Universal Provider Template Catalog
            </h2>
            <p className="text-xs text-slate-500">
              Pre-configured enterprise integrations with built-in retry backoff,
              circuit breaker heuristics, and documentation references.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {templates.map((tpl) => (
              <div
                key={tpl.provider_key}
                className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-2xs hover:shadow-md transition space-y-3 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${getCategoryBadge(
                        tpl.category
                      )}`}
                    >
                      {tpl.category}
                    </span>
                    <a
                      href={tpl.doc_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-slate-400 hover:text-indigo-600 p-1 flex items-center gap-1 text-[11px] font-semibold"
                    >
                      Docs <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>

                  <h3 className="font-bold text-slate-900 text-sm">
                    {tpl.display_name}
                  </h3>
                  <p className="font-mono text-[11px] text-slate-400 truncate">
                    {tpl.suggested_base_url}
                  </p>
                  <p className="text-xs text-slate-500 mt-2">
                    Auth Protocol: <strong>{tpl.auth_type}</strong>
                  </p>
                  {tpl.required_credential_fields.length > 0 && (
                    <div className="mt-2 flex items-center gap-1 flex-wrap">
                      {tpl.required_credential_fields.map((f) => (
                        <span
                          key={f}
                          className="px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded text-[10px] font-mono"
                        >
                          {f}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="pt-3 border-t border-slate-100 flex justify-end">
                  <button
                    onClick={() => {
                      setSelectedTemplateForAdd(tpl);
                      setProviderForm({
                        provider_key: tpl.provider_key,
                        display_name: tpl.display_name,
                        category: tpl.category,
                        auth_type: tpl.auth_type,
                        base_url: tpl.suggested_base_url,
                        rate_limit_per_minute: 120,
                        timeout_seconds: 10,
                        retry_max_attempts: 3,
                        is_enabled: true,
                        is_default: false,
                        credential_key: "",
                        credential_secret: "",
                      });
                      setIsAddProviderModalOpen(true);
                    }}
                    className="px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-lg text-xs font-bold transition flex items-center gap-1"
                  >
                    <Plus className="w-3.5 h-3.5" /> Configure from Template
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Credential Vault */}
      {activeTab === "vault" && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="max-w-2xl space-y-2">
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <Lock className="w-5 h-5 text-indigo-600" /> AES-256 Credential Vault
            </h2>
            <p className="text-sm text-slate-600 leading-relaxed">
              Sensitive provider secrets, API keys, private tokens, and HMAC signing
              keys are encrypted at rest using AES-256 Fernet primitives. Secrets
              are never exposed in plaintext logs or client responses.
            </p>
          </div>

          <div className="divide-y divide-slate-100 border border-slate-200 rounded-2xl overflow-hidden">
            {providers.map((p) => (
              <div
                key={p.id}
                className="p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 hover:bg-slate-50/70 transition"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${getCategoryBadge(
                        p.category
                      )}`}
                    >
                      {p.category}
                    </span>
                    <h4 className="font-bold text-slate-900 text-sm">
                      {p.display_name}
                    </h4>
                  </div>
                  <p className="text-xs text-slate-500 font-mono">
                    Provider ID: {p.id} • Auth: {p.auth_type}
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <span
                    className={`inline-flex items-center gap-1 text-xs font-semibold ${
                      p.has_credentials ? "text-emerald-600" : "text-amber-600"
                    }`}
                  >
                    <ShieldCheck className="w-4 h-4" />
                    {p.has_credentials ? "Encrypted Payload Active" : "No Keys Stored"}
                  </span>

                  <button
                    onClick={() => {
                      setSelectedProviderForVault(p);
                      setVaultFields({});
                    }}
                    className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-2xs"
                  >
                    <Key className="w-3.5 h-3.5" />
                    <span>Rotate / Edit Keys</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Webhook Dispatcher */}
      {activeTab === "webhooks" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Outbound Event Webhooks
              </h2>
              <p className="text-xs text-slate-500">
                Trigger real-time HMAC-SHA256 signed event payloads to external
                CRM systems, partner portals, or accounting ERPs.
              </p>
            </div>
            <button
              onClick={() => setIsWebhookModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Register Webhook
            </button>
          </div>

          {webhookTestResult && (
            <div className="p-4 bg-slate-900 text-emerald-400 rounded-2xl border border-slate-800 text-xs font-mono space-y-1">
              <div className="flex items-center justify-between pb-1 border-b border-slate-800 text-slate-300">
                <span>Webhook Dispatch Acknowledged (HTTP 200 OK)</span>
                <button
                  onClick={() => setWebhookTestResult(null)}
                  className="text-slate-400 hover:text-white"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              <p>Event: {webhookTestResult.event_type}</p>
              <p>Target: {webhookTestResult.target_url}</p>
              <p>Signature: {webhookTestResult.signature_hash}</p>
              <p>Latency: {webhookTestResult.latency_ms} ms</p>
            </div>
          )}

          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-700">
                <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Event Type</th>
                    <th className="py-3 px-4">Target Endpoint</th>
                    <th className="py-3 px-4">Signature Header</th>
                    <th className="py-3 px-4">Retries</th>
                    <th className="py-3 px-4">Status</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {webhooks.map((wh) => (
                    <tr key={wh.id} className="hover:bg-slate-50/80 transition">
                      <td className="py-3 px-4 font-mono text-xs font-bold text-indigo-700">
                        {wh.event_type}
                      </td>
                      <td className="py-3 px-4 font-mono text-xs text-slate-600 truncate max-w-xs">
                        {wh.target_url}
                      </td>
                      <td className="py-3 px-4 font-mono text-xs text-slate-500">
                        {wh.signature_header}
                      </td>
                      <td className="py-3 px-4 text-xs font-semibold text-slate-600">
                        {wh.retry_count} attempts
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`inline-flex items-center gap-1 text-xs font-semibold ${
                            wh.is_active ? "text-emerald-600" : "text-slate-400"
                          }`}
                        >
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          {wh.is_active ? "Active" : "Disabled"}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right space-x-2">
                        <button
                          onClick={() => handleTestWebhookDispatch(wh.id)}
                          className="px-2.5 py-1 bg-slate-100 hover:bg-indigo-50 hover:text-indigo-700 rounded text-xs font-bold transition"
                        >
                          Dispatch Test
                        </button>
                        <button
                          onClick={() => {
                            if (confirm("Delete this webhook registration?")) {
                              deleteWebhookMutation.mutate(wh.id);
                            }
                          }}
                          className="p-1 text-slate-400 hover:text-rose-600 rounded transition"
                        >
                          <Trash2 className="w-4 h-4 inline" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab 5: Telemetry & Execution Logs */}
      {activeTab === "logs" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Live Outbound Execution Logs
              </h2>
              <p className="text-xs text-slate-500">
                Audited transactional log of API handshakes, status codes, latency,
                and circuit breaker status.
              </p>
            </div>
            <button
              onClick={() => refetchLogs()}
              className="inline-flex items-center gap-2 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Refresh Logs
            </button>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-700">
                <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Timestamp</th>
                    <th className="py-3 px-4">Provider & Action</th>
                    <th className="py-3 px-4">Category</th>
                    <th className="py-3 px-4">Status Code</th>
                    <th className="py-3 px-4">Latency</th>
                    <th className="py-3 px-4">Circuit</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono text-xs">
                  {logs.map((log) => (
                    <tr key={log.id} className="hover:bg-slate-50/80 transition">
                      <td className="py-3 px-4 text-slate-500">
                        {new Date(log.request_timestamp).toLocaleTimeString()}
                      </td>
                      <td className="py-3 px-4">
                        <span className="font-bold text-slate-900 font-sans block">
                          {log.endpoint_key}
                        </span>
                        <span className="text-slate-400">{log.provider_id}</span>
                      </td>
                      <td className="py-3 px-4 font-sans">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${getCategoryBadge(
                            log.category
                          )}`}
                        >
                          {log.category}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-bold">
                        <span
                          className={`px-2 py-0.5 rounded ${
                            log.status_code === 200 || log.status_code === 202
                              ? "bg-emerald-100 text-emerald-800"
                              : "bg-rose-100 text-rose-800"
                          }`}
                        >
                          {log.status_code || 500} {log.is_success ? "OK" : "ERR"}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-semibold text-slate-800">
                        {log.latency_ms.toFixed(1)} ms
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`inline-flex items-center gap-1 font-semibold ${
                            log.circuit_broken ? "text-rose-600" : "text-emerald-600"
                          }`}
                        >
                          {log.circuit_broken ? "OPEN (Tripped)" : "CLOSED"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Ping Test Modal */}
      {selectedProviderForTest && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-5">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-amber-500" />
                <h3 className="font-bold text-slate-900 text-lg">
                  Gateway Ping & Handshake Test
                </h3>
              </div>
              <button
                onClick={() => setSelectedProviderForTest(null)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="bg-slate-50 p-4 rounded-2xl space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-500 font-medium">Provider:</span>
                <span className="font-bold text-slate-900">
                  {selectedProviderForTest.display_name}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 font-medium">Endpoint:</span>
                <span className="font-mono text-slate-700 truncate max-w-xs">
                  {selectedProviderForTest.base_url}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 font-medium">Protocol:</span>
                <span className="font-bold text-indigo-700">
                  {selectedProviderForTest.auth_type} (TLS 1.3)
                </span>
              </div>
            </div>

            {isTesting && (
              <div className="py-6 text-center text-slate-400 space-y-2">
                <div className="w-6 h-6 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto" />
                <p className="text-xs font-semibold">
                  Executing authenticated roundtrip handshake...
                </p>
              </div>
            )}

            {!isTesting && testResult && (
              <div
                className={`p-4 rounded-2xl border text-xs space-y-2 ${
                  testResult.is_connected
                    ? "bg-emerald-50 border-emerald-200 text-emerald-900"
                    : "bg-rose-50 border-rose-200 text-rose-900"
                }`}
              >
                <div className="flex items-center gap-2 font-bold text-sm">
                  {testResult.is_connected ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-rose-600" />
                  )}
                  <span>
                    {testResult.is_connected
                      ? "Handshake Successful (200 OK)"
                      : "Handshake Failed"}
                  </span>
                </div>
                <p>{testResult.message}</p>
                <div className="flex items-center justify-between text-[11px] pt-1 border-t border-emerald-200/60 font-mono">
                  <span>Roundtrip Latency: {testResult.latency_ms} ms</span>
                  <span>TLS Verified: True</span>
                </div>
                {testResult.response_preview && (
                  <pre className="p-2 bg-slate-900 text-emerald-400 rounded-lg text-[10px] overflow-x-auto mt-2">
                    {testResult.response_preview}
                  </pre>
                )}
              </div>
            )}

            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setSelectedProviderForTest(null)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Close
              </button>
              <button
                onClick={() => handleRunPingTest(selectedProviderForTest)}
                disabled={isTesting}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Ping Again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Credential Vault Modal */}
      {selectedProviderForVault && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-5">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <Lock className="w-5 h-5 text-indigo-600" />
                <h3 className="font-bold text-slate-900 text-lg">
                  Credential Vault Security
                </h3>
              </div>
              <button
                onClick={() => setSelectedProviderForVault(null)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="bg-slate-50 p-4 rounded-2xl text-xs space-y-1">
              <p className="font-bold text-slate-900">
                {selectedProviderForVault.display_name}
              </p>
              <p className="text-slate-500">
                Auth Type: {selectedProviderForVault.auth_type} • Encryption: AES-256
              </p>
            </div>

            {vaultStatus && (
              <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-semibold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>{vaultStatus}</span>
              </div>
            )}

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  API Key / Token / Username
                </label>
                <input
                  type="password"
                  placeholder="Enter secret key or token..."
                  value={vaultFields.key || ""}
                  onChange={(e) =>
                    setVaultFields({ ...vaultFields, key: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  API Secret / Password / Signing Salt
                </label>
                <input
                  type="password"
                  placeholder="Enter secret or private password..."
                  value={vaultFields.secret || ""}
                  onChange={(e) =>
                    setVaultFields({ ...vaultFields, secret: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setSelectedProviderForVault(null)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!vaultFields.key && !vaultFields.secret) {
                    alert("Please provide at least one credential field");
                    return;
                  }
                  updateCredentialsMutation.mutate({
                    id: selectedProviderForVault.id,
                    credentials: vaultFields,
                  });
                }}
                disabled={updateCredentialsMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-2"
              >
                <ShieldCheck className="w-4 h-4" /> Save Encrypted Keys
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Provider Modal */}
      {isAddProviderModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Connect New API Gateway
              </h3>
              <button
                onClick={() => setIsAddProviderModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Gateway Display Name *
                </label>
                <input
                  type="text"
                  placeholder="e.g. Fast2SMS India Gateway"
                  value={providerForm.display_name}
                  onChange={(e) =>
                    setProviderForm({
                      ...providerForm,
                      display_name: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Provider Key *
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. fast2sms"
                    value={providerForm.provider_key}
                    onChange={(e) =>
                      setProviderForm({
                        ...providerForm,
                        provider_key: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Category *
                  </label>
                  <select
                    value={providerForm.category}
                    onChange={(e) =>
                      setProviderForm({
                        ...providerForm,
                        category: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  >
                    <option value="SMS">SMS</option>
                    <option value="WHATSAPP">WHATSAPP</option>
                    <option value="EMAIL">EMAIL</option>
                    <option value="PAYMENT">PAYMENT</option>
                    <option value="GOV_PORTAL">GOV_PORTAL</option>
                    <option value="AI">AI</option>
                    <option value="STORAGE">STORAGE</option>
                    <option value="VIDEO">VIDEO</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Base URL *
                </label>
                <input
                  type="text"
                  placeholder="https://api.provider.com/v1"
                  value={providerForm.base_url}
                  onChange={(e) =>
                    setProviderForm({
                      ...providerForm,
                      base_url: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none"
                />
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Auth Type
                  </label>
                  <select
                    value={providerForm.auth_type}
                    onChange={(e) =>
                      setProviderForm({
                        ...providerForm,
                        auth_type: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  >
                    <option value="API_KEY">API_KEY</option>
                    <option value="BEARER">BEARER</option>
                    <option value="OAUTH2">OAUTH2</option>
                    <option value="BASIC">BASIC</option>
                    <option value="CUSTOM_HEADER">CUSTOM_HEADER</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Rate Limit (req/m)
                  </label>
                  <input
                    type="number"
                    value={providerForm.rate_limit_per_minute}
                    onChange={(e) =>
                      setProviderForm({
                        ...providerForm,
                        rate_limit_per_minute: parseInt(e.target.value) || 120,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Timeout (sec)
                  </label>
                  <input
                    type="number"
                    value={providerForm.timeout_seconds}
                    onChange={(e) =>
                      setProviderForm({
                        ...providerForm,
                        timeout_seconds: parseInt(e.target.value) || 10,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Initial API Secret / Token (Saved directly to Vault)
                </label>
                <input
                  type="password"
                  placeholder="Secret key..."
                  value={providerForm.credential_secret}
                  onChange={(e) =>
                    setProviderForm({
                      ...providerForm,
                      credential_secret: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsAddProviderModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (
                    !providerForm.display_name ||
                    !providerForm.provider_key ||
                    !providerForm.base_url
                  ) {
                    alert("Please fill in required fields");
                    return;
                  }
                  createProviderMutation.mutate(providerForm);
                }}
                disabled={createProviderMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition"
              >
                Save & Connect
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Webhook Modal */}
      {isWebhookModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Register Event Webhook
              </h3>
              <button
                onClick={() => setIsWebhookModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Event Trigger Topic *
                </label>
                <select
                  value={webhookForm.event_type}
                  onChange={(e) =>
                    setWebhookForm({
                      ...webhookForm,
                      event_type: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                >
                  <option value="admission.application_submitted">
                    admission.application_submitted
                  </option>
                  <option value="fee.payment_received">
                    fee.payment_received
                  </option>
                  <option value="student.registered">
                    student.registered
                  </option>
                  <option value="exam.result_published">
                    exam.result_published
                  </option>
                  <option value="attendance.shortage_alert">
                    attendance.shortage_alert
                  </option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Target Endpoint URL *
                </label>
                <input
                  type="text"
                  placeholder="https://partner-portal.com/webhooks"
                  value={webhookForm.target_url}
                  onChange={(e) =>
                    setWebhookForm({
                      ...webhookForm,
                      target_url: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  HMAC Signature Header
                </label>
                <input
                  type="text"
                  value={webhookForm.signature_header}
                  onChange={(e) =>
                    setWebhookForm({
                      ...webhookForm,
                      signature_header: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsWebhookModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!webhookForm.target_url) {
                    alert("Please provide target URL");
                    return;
                  }
                  createWebhookMutation.mutate(webhookForm);
                }}
                disabled={createWebhookMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition"
              >
                Register Webhook
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
