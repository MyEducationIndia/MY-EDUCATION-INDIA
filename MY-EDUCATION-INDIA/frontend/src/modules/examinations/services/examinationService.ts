import { apiClient } from "@/lib/api/apiClient";
import {
  ExamDashboardSummary,
  ExamSchedule,
  ExamSession,
  ExamType,
  HallTicket,
  MarkEntry,
  Result,
  Transcript,
} from "../types/examination.types";

export const examinationService = {
  // Dashboard & Analytics
  getDashboardAnalytics: async (instituteId: string): Promise<ExamDashboardSummary> => {
    const res = await apiClient.get<ExamDashboardSummary>("/exams/analytics", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  // Types & Sessions
  getExamTypes: async (instituteId: string): Promise<ExamType[]> => {
    const res = await apiClient.get<ExamType[]>("/exams/types", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  createExamType: async (payload: {
    institute_id: string;
    code: string;
    name: string;
    category?: string;
    default_weightage_pct?: number;
  }): Promise<ExamType> => {
    const res = await apiClient.post<ExamType>("/exams/types", payload);
    return res.data;
  },

  getExamSessions: async (instituteId: string): Promise<ExamSession[]> => {
    const res = await apiClient.get<ExamSession[]>("/exams/sessions", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  createExamSession: async (payload: {
    institute_id: string;
    academic_year_id: string;
    code: string;
    name: string;
    start_date: string;
    end_date: string;
    min_attendance_threshold_pct?: number;
    requires_fee_clearance?: boolean;
  }): Promise<ExamSession> => {
    const res = await apiClient.post<ExamSession>("/exams/sessions", payload);
    return res.data;
  },

  // Schedules
  createSchedule: async (payload: {
    exam_session_id: string;
    course_id: string;
    exam_date: string;
    start_time: string;
    end_time: string;
    subjects?: any[];
  }): Promise<ExamSchedule> => {
    const res = await apiClient.post<ExamSchedule>("/exams/schedules", payload);
    return res.data;
  },

  // Marks Entry
  enterMarks: async (payload: {
    exam_subject_id: string;
    marks: Array<{
      student_id: string;
      internal_marks: number;
      external_marks: number;
      practical_marks?: number;
      grace_marks?: number;
      is_absent?: boolean;
    }>;
  }): Promise<MarkEntry[]> => {
    const res = await apiClient.post<MarkEntry[]>("/exams/marks", payload);
    return res.data;
  },

  // Results Publication
  publishResults: async (sessionId: string): Promise<Result[]> => {
    const res = await apiClient.post<Result[]>("/exams/results/publish", null, {
      params: { session_id: sessionId },
    });
    return res.data;
  },

  // Merit List
  getMeritList: async (examSessionId: string, topN: number = 10): Promise<any[]> => {
    const res = await apiClient.get("/exams/reports/merit-list", {
      params: { exam_session_id: examSessionId, top_n: topN },
    });
    return res.data;
  },
};
