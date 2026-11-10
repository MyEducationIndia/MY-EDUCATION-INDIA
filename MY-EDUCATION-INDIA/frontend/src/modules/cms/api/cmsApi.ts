import { httpClient } from "@/api/httpClient";
import {
  BannerItem,
  DownloadItem,
  DynamicPageItem,
  EnquiryRecord,
  MenuStructure,
  NewsItem,
  TestimonialItem,
  WebsiteSettingsRecord,
} from "../types/cms.types";

export const cmsApi = {
  // Public APIs
  async getPageBySlug(slug: string, instituteId: string): Promise<DynamicPageItem> {
    const res = await httpClient.get<DynamicPageItem>(`/cms/pages/slug/${slug}`, {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  async getHomepage(instituteId: string): Promise<DynamicPageItem> {
    const res = await httpClient.get<DynamicPageItem>("/cms/pages/homepage", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  async getMenu(code: string, instituteId: string): Promise<MenuStructure> {
    const res = await httpClient.get<MenuStructure>(`/cms/menus/${code}`, {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  async listBanners(instituteId: string, bannerType?: string): Promise<BannerItem[]> {
    const res = await httpClient.get<BannerItem[]>("/cms/banners", {
      params: { institute_id: instituteId, banner_type: bannerType },
    });
    return res.data;
  },

  async listNews(instituteId: string): Promise<NewsItem[]> {
    const res = await httpClient.get<NewsItem[]>("/cms/news", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  async listTestimonials(instituteId: string): Promise<TestimonialItem[]> {
    const res = await httpClient.get<TestimonialItem[]>("/cms/testimonials", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  async listDownloads(instituteId: string): Promise<DownloadItem[]> {
    const res = await httpClient.get<DownloadItem[]>("/cms/downloads", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  async submitEnquiry(payload: Partial<EnquiryRecord> & { institute_id: string }): Promise<EnquiryRecord> {
    const res = await httpClient.post<EnquiryRecord>("/cms/enquiries", payload);
    return res.data;
  },

  async getWebsiteSettings(instituteId: string): Promise<WebsiteSettingsRecord> {
    const res = await httpClient.get<WebsiteSettingsRecord>("/cms/settings", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  // Admin CMS APIs
  async listAdminPages(): Promise<DynamicPageItem[]> {
    const res = await httpClient.get<DynamicPageItem[]>("/cms/admin/pages");
    return res.data;
  },

  async createPage(payload: Partial<DynamicPageItem>): Promise<DynamicPageItem> {
    const res = await httpClient.post<DynamicPageItem>("/cms/admin/pages", payload);
    return res.data;
  },

  async updatePage(pageId: string, payload: Partial<DynamicPageItem>): Promise<DynamicPageItem> {
    const res = await httpClient.patch<DynamicPageItem>(`/cms/admin/pages/${pageId}`, payload);
    return res.data;
  },

  async updateWebsiteSettings(payload: Partial<WebsiteSettingsRecord>): Promise<WebsiteSettingsRecord> {
    const res = await httpClient.put<WebsiteSettingsRecord>("/cms/admin/settings", payload);
    return res.data;
  },

  async listAdminEnquiries(): Promise<EnquiryRecord[]> {
    const res = await httpClient.get<EnquiryRecord[]>("/cms/admin/enquiries");
    return res.data;
  },
};
