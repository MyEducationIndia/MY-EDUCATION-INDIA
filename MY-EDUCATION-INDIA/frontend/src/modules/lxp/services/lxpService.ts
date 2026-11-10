import { httpClient } from "@/api/httpClient";
import { LearningCourse, LearningModule, LXPDashboardMetrics } from "../types/lxp.types";

export const lxpService = {
  getDashboardMetrics: async (): Promise<LXPDashboardMetrics> => {
    const res = await httpClient.get<LXPDashboardMetrics>("/lxp/dashboard/metrics");
    return res.data;
  },

  listCourses: async (category?: string): Promise<LearningCourse[]> => {
    const res = await httpClient.get<LearningCourse[]>("/lxp/courses", { params: { category } });
    return res.data;
  },

  getCourseModules: async (courseId: string): Promise<LearningModule[]> => {
    const res = await httpClient.get<LearningModule[]>(`/lxp/courses/${courseId}/modules`);
    return res.data;
  }
};
