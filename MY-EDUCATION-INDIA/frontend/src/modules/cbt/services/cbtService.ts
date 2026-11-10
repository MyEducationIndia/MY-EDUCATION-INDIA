import { apiClient } from "@/lib/api/apiClient";
import {
  CandidateSession,
  CBTDashboardSummary,
  CBTSession,
  ExamTemplate,
  LiveCandidateStatus,
  QuestionBank,
  QuestionVersion,
} from "../types/cbt.types";

export const cbtService = {
  // Dashboard
  getDashboardSummary: async (instituteId: string): Promise<CBTDashboardSummary> => {
    const res = await apiClient.get<CBTDashboardSummary>("/cbt/dashboard", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  // Question Bank
  getQuestionBanks: async (instituteId: string): Promise<QuestionBank[]> => {
    const res = await apiClient.get<QuestionBank[]>("/cbt/question-bank", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  createQuestionBank: async (payload: { institute_id: string; code: string; name: string; description?: string }): Promise<QuestionBank> => {
    const res = await apiClient.post<QuestionBank>("/cbt/question-bank", payload);
    return res.data;
  },

  createQuestion: async (payload: any): Promise<QuestionVersion> => {
    const res = await apiClient.post<QuestionVersion>("/cbt/questions", payload);
    return res.data;
  },

  // Exam Templates & Sessions
  createTemplate: async (payload: any): Promise<ExamTemplate> => {
    const res = await apiClient.post<ExamTemplate>("/cbt/templates", payload);
    return res.data;
  },

  createSession: async (payload: any): Promise<CBTSession> => {
    const res = await apiClient.post<CBTSession>("/cbt/sessions", payload);
    return res.data;
  },

  // Candidate Delivery
  startCandidateExam: async (payload: { cbt_session_id: string; student_id: string; device_fingerprint?: string }): Promise<CandidateSession> => {
    const res = await apiClient.post<CandidateSession>("/cbt/delivery/start", payload);
    return res.data;
  },

  autosaveAnswers: async (candidateSessionId: string, answers: any[]): Promise<any> => {
    const res = await apiClient.post("/cbt/delivery/autosave", answers, {
      params: { candidate_session_id: candidateSessionId },
    });
    return res.data;
  },

  submitExam: async (candidateSessionId: string): Promise<CandidateSession> => {
    const res = await apiClient.post<CandidateSession>("/cbt/delivery/submit", null, {
      params: { candidate_session_id: candidateSessionId },
    });
    return res.data;
  },

  // Offline Sync
  syncOfflineBatch: async (payload: { candidate_session_id: string; answers: any[]; checksum: string }): Promise<any> => {
    const res = await apiClient.post("/cbt/offline-sync", payload);
    return res.data;
  },
};
