import { httpClient } from "@/api/httpClient";
import { LibraryBook, LibraryDashboardMetrics, DigitalResource } from "../types/library.types";

export const libraryService = {
  getDashboardMetrics: async (): Promise<LibraryDashboardMetrics> => {
    const res = await httpClient.get<LibraryDashboardMetrics>("/library/dashboard/metrics");
    return res.data;
  },

  listBooks: async (search?: string): Promise<LibraryBook[]> => {
    const res = await httpClient.get<LibraryBook[]>("/library/books", { params: { search } });
    return res.data;
  },

  publicOpacSearch: async (query: string) => {
    const res = await httpClient.get("/library/opac/search", { params: { query } });
    return res.data;
  }
};
