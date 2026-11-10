import { httpClient } from "@/services/httpClient";
import {
  PortalItem,
  RootOwnerOverview,
  NotificationItem,
  ModulesRegistryResponse,
  PortalProfileResponse,
} from "@/types/experience.types";

export const experienceService = {
  // Root Owner & Health
  async getHealth(): Promise<any> {
    const res = await httpClient.get("/experience/health");
    return res.data;
  },

  async getRootOverview(): Promise<RootOwnerOverview> {
    const res = await httpClient.get<RootOwnerOverview>("/experience/root-owner/overview");
    return res.data;
  },

  async toggleLockdown(active?: boolean): Promise<any> {
    const res = await httpClient.post("/experience/root-owner/lockdown", { active });
    return res.data;
  },

  // Portals
  async listPortals(): Promise<PortalItem[]> {
    const res = await httpClient.get<PortalItem[]>("/experience/portals");
    return res.data;
  },

  async getPortalProfile(portalType: string): Promise<PortalProfileResponse> {
    const res = await httpClient.get<PortalProfileResponse>(`/experience/portals/${portalType}/profile`);
    return res.data;
  },

  // Notifications
  async listNotifications(): Promise<NotificationItem[]> {
    const res = await httpClient.get<NotificationItem[]>("/experience/notifications");
    return res.data;
  },

  async broadcastNotification(payload: { title: string; category: string; message: string; priority: string }): Promise<NotificationItem> {
    const res = await httpClient.post<NotificationItem>("/experience/notifications/broadcast", payload);
    return res.data;
  },

  // 20-Module Blueprint Registry
  async getModulesRegistry(): Promise<ModulesRegistryResponse> {
    const res = await httpClient.get<ModulesRegistryResponse>("/experience/modules/registry");
    return res.data;
  },
};
