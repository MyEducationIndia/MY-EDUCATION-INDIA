import { httpClient } from "@/api/httpClient";
import {
  BatchRecord,
  CourseRecord,
  DepartmentRecord,
  ProgramRecord,
  SubjectRecord,
  TimetableRecord,
  TimetableSlotRecord,
} from "../types/academic.types";

export const academicService = {
  async listDepartments(): Promise<DepartmentRecord[]> {
    const res = await httpClient.get<DepartmentRecord[]>("/academics/departments");
    return res.data;
  },

  async createDepartment(payload: any): Promise<DepartmentRecord> {
    const res = await httpClient.post<DepartmentRecord>("/academics/departments", payload);
    return res.data;
  },

  async listPrograms(): Promise<ProgramRecord[]> {
    const res = await httpClient.get<ProgramRecord[]>("/academics/programs");
    return res.data;
  },

  async createProgram(payload: any): Promise<ProgramRecord> {
    const res = await httpClient.post<ProgramRecord>("/academics/programs", payload);
    return res.data;
  },

  async listCourses(): Promise<CourseRecord[]> {
    const res = await httpClient.get<CourseRecord[]>("/academics/courses");
    return res.data;
  },

  async createCourse(payload: any): Promise<CourseRecord> {
    const res = await httpClient.post<CourseRecord>("/academics/courses", payload);
    return res.data;
  },

  async listSubjects(): Promise<SubjectRecord[]> {
    const res = await httpClient.get<SubjectRecord[]>("/academics/subjects");
    return res.data;
  },

  async createSubject(payload: any): Promise<SubjectRecord> {
    const res = await httpClient.post<SubjectRecord>("/academics/subjects", payload);
    return res.data;
  },

  async listBatches(): Promise<BatchRecord[]> {
    const res = await httpClient.get<BatchRecord[]>("/academics/batches");
    return res.data;
  },

  async createBatch(payload: any): Promise<BatchRecord> {
    const res = await httpClient.post<BatchRecord>("/academics/batches", payload);
    return res.data;
  },

  async getTimetable(batchId: string, sectionId: string): Promise<TimetableRecord | null> {
    const res = await httpClient.get<TimetableRecord | null>("/academics/timetable", {
      params: { batch_id: batchId, section_id: sectionId },
    });
    return res.data;
  },

  async addTimetableSlot(payload: any): Promise<TimetableSlotRecord> {
    const res = await httpClient.post<TimetableSlotRecord>("/academics/timetable/slots", payload);
    return res.data;
  },
};
