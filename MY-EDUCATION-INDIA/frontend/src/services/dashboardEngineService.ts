import { httpClient } from "@/api/httpClient";
import {
  DashboardRoleKey,
  DashboardTask,
  RoleDashboardBundle,
} from "@/types/dashboardEngine.types";

export const dashboardEngineService = {
  async getRoleDashboard(
    roleKey: DashboardRoleKey | string,
    instituteId?: string
  ): Promise<RoleDashboardBundle> {
    const response = await httpClient.get<RoleDashboardBundle>(
      `/dashboard-engine/role/${roleKey}`,
      {
        params: instituteId ? { institute_id: instituteId } : undefined,
      }
    );
    return response.data;
  },

  async createTask(payload: {
    title: string;
    description?: string;
    due_date?: string;
    priority?: string;
    status?: string;
    role_target: string;
    action_url?: string;
  }): Promise<DashboardTask> {
    const response = await httpClient.post<DashboardTask>(
      "/dashboard-engine/tasks",
      payload
    );
    return response.data;
  },
};
