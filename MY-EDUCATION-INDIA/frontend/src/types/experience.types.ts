export interface PortalItem {
  portal_type: string;
  display_title: string;
  default_route: string;
  allowed_roles: string[];
  accent_color: string;
  tagline: string;
  icon: string;
}

export interface RootOwnerOverview {
  owner_username: string;
  emergency_lockdown_active: boolean;
  developer_mode_enabled: boolean;
  license_tier: string;
  total_institutes_active: number;
  campus_name: string;
  campus_location: string;
  total_modules_licensed: number;
  complete_blueprint_verified: boolean;
}

export interface NotificationItem {
  id: string;
  title: string;
  category: string;
  message: string;
  timestamp: string;
  priority: "LOW" | "MEDIUM" | "HIGH";
  is_read: boolean;
}

export interface ErpMasterModule {
  id: number;
  key: string;
  name: string;
  subdomain: string;
  category: string;
  status: string;
}

export interface ModulesRegistryResponse {
  total_modules: number;
  completion_percentage: number;
  blueprint: string;
  modules: ErpMasterModule[];
}

export interface PortalProfileResponse {
  portal: PortalItem;
  user_preference: {
    dark_mode: boolean;
    accent_color: string;
    sidebar_collapsed: boolean;
    notifications_enabled: boolean;
  };
  allowed_subsystems: string[];
}
