import {
  SearchResponse,
  SearchSuggestionItem,
  WebsiteQuickLink,
  SitemapResponse,
  SearchAnalyticsSummary,
  CmsContactInquiry,
  CmsDepartmentContact,
  CmsDepartmentContactCreateRequest,
  CmsFaqItem,
  CmsFaqItemCreateRequest,
  CmsSupportFeedback,
  PublicContactBundle,
  PublicContactInquiryCreateRequest,
  PublicSupportFeedbackCreateRequest,

  PublicTestimonialSubmitRequest,
  PublicTestimonialsBundle,
  CmsTestimonialCreateRequest,

  CmsInternshipOpportunity,
  CmsInternshipOpportunityCreateRequest,
  CmsPlacementDrive,
  CmsPlacementDriveCreateRequest,
  CmsTrainingProgram,
  CmsTrainingProgramCreateRequest,
  PublicPlacementCellBundle,

  CmsDownloadCategory,
  CmsDownloadCategoryCreateRequest,
  CmsDownloadCategoryWithDocs,
  CmsDownloadDocument,
  CmsDownloadDocumentCreateRequest,
  PublicDownloadsBundle,

  CmsGalleryAlbum,
  CmsGalleryAlbumCreateRequest,
  CmsGalleryAlbumDetail,
  CmsGalleryMedia,
  CmsGalleryMediaCreateRequest,
  PublicGalleryBundle,
 httpClient } from "@/api/httpClient";
import {
  CmsCourseCategory,
  CmsCourseCategoryCreateRequest,
  CmsCourseCurriculum,
  CmsCourseCurriculumCreateRequest,
  CmsCourseDetail,
  CmsCourseFaculty,
  CmsCourseFacultyCreateRequest,
  CmsCourseSummary,
  CmsCourseCreateRequest,
  PublicCoursesBundle,
  CmsAchievement,
  CmsAchievementCreateRequest,
  CmsEvent,
  CmsEventCreateRequest,
  CmsNewsArticle,
  CmsNewsArticleCreateRequest,
  CmsNoticeCircular,
  CmsNoticeCircularCreateRequest,
  PublicEventsNewsBundle,
  CmsAlumniSuccessStory,
  CmsAlumniSuccessStoryCreateRequest,
  CmsPlacementStat,
  CmsPlacementStatCreateRequest,
  CmsRecruiterPartner,
  CmsRecruiterPartnerCreateRequest,
  PublicPlacementsBundle,
  CmsFacultyMemberCreateRequest,
  CmsFacultyMemberDetail,
  CmsFacultyMemberSummary,
  CmsResearchPublication,
  CmsResearchPublicationCreateRequest,
  CmsStaffMember,
  CmsStaffMemberCreateRequest,
  PublicFacultyBundle,
  PublicStaffBundle,
  CmsAdmissionApplication,
  CmsAdmissionApplicationCreateRequest,
  CmsAdmissionEnquiry,
  CmsAdmissionEnquiryCreateRequest,
  CmsAdmissionStep,
  CmsAdmissionStepCreateRequest,
  CmsFeeStructure,
  CmsFeeStructureCreateRequest,
  CmsScholarship,
  CmsScholarshipCreateRequest,
  PublicAdmissionBundle,
  CmsAccreditation,
  CmsAccreditationCreateRequest,
  CmsCampusInfrastructure,
  CmsCampusInfrastructureCreateRequest,
  CmsFeaturedProgram,
  CmsHeroSlide,
  CmsLeadershipMessage,
  CmsLeadershipMessageCreateRequest,
  CmsMilestone,
  CmsMilestoneCreateRequest,
  CmsQuickLink,
  CmsRecruiterLogo,
  CmsStatCounter,
  CmsTestimonial,
  NavigationMenuItem,
  PublicAboutInstituteBundle,
  PublicHomePageBundle,
  PublicWebsiteFrameworkBundle,
  SearchResponse,
  WebsiteSettings,
  WebsiteTheme,
  WebsiteTickerItem,
} from "@/types/website.types";

export const websiteService = {
  // Public Framework Bundle
  async getPublicFrameworkBundle(): Promise<PublicWebsiteFrameworkBundle> {
    const res = await httpClient.get<PublicWebsiteFrameworkBundle>(
      "/public/website/framework-bundle"
    );
    return res.data;
  },

  // Public Home Page Bundle (Module 2)
  async getPublicHomeBundle(): Promise<PublicHomePageBundle> {
    const res = await httpClient.get<PublicHomePageBundle>("/public/home/bundle");
    return res.data;
  },

  // Public Newsletter Subscription (Module 2)
  async subscribeNewsletter(email: string): Promise<{ success: boolean; message: string }> {
    const res = await httpClient.post<{ success: boolean; message: string }>(
      "/public/home/newsletter/subscribe",
      { email }
    );
    return res.data;
  },

  // Public About Institute Bundle (Module 3)
  async getPublicAboutBundle(): Promise<PublicAboutInstituteBundle> {
    const res = await httpClient.get<PublicAboutInstituteBundle>("/public/about/bundle");
    return res.data;
  },

  // Public Global Search
  async search(query: string, limit: number = 15): Promise<SearchResponse> {
    const res = await httpClient.get<SearchResponse>("/public/website/search", {
      params: { q: query, limit },
    });
    return res.data;
  },

  // Admin Settings
  async getSettings(): Promise<WebsiteSettings> {
    const res = await httpClient.get<WebsiteSettings>("/admin/website/settings");
    return res.data;
  },

  async updateSettings(payload: Partial<WebsiteSettings>): Promise<WebsiteSettings> {
    const res = await httpClient.patch<WebsiteSettings>(
      "/admin/website/settings",
      payload
    );
    return res.data;
  },

  // Admin Theme
  async getTheme(): Promise<WebsiteTheme> {
    const res = await httpClient.get<WebsiteTheme>("/admin/website/theme");
    return res.data;
  },

  async updateTheme(payload: Partial<WebsiteTheme>): Promise<WebsiteTheme> {
    const res = await httpClient.patch<WebsiteTheme>(
      "/admin/website/theme",
      payload
    );
    return res.data;
  },

  // Admin Ticker
  async listTickerItems(): Promise<WebsiteTickerItem[]> {
    const res = await httpClient.get<WebsiteTickerItem[]>("/admin/website/ticker");
    return res.data;
  },

  async createTickerItem(
    payload: Omit<WebsiteTickerItem, "id" | "institute_id" | "created_at">
  ): Promise<WebsiteTickerItem> {
    const res = await httpClient.post<WebsiteTickerItem>(
      "/admin/website/ticker",
      payload
    );
    return res.data;
  },

  async updateTickerItem(
    itemId: string,
    payload: Partial<WebsiteTickerItem>
  ): Promise<WebsiteTickerItem> {
    const res = await httpClient.patch<WebsiteTickerItem>(
      `/admin/website/ticker/${itemId}`,
      payload
    );
    return res.data;
  },

  async deleteTickerItem(itemId: string): Promise<void> {
    await httpClient.delete(`/admin/website/ticker/${itemId}`);
  },

  // Admin Navigation Menus
  async listMenus(location: string = "HEADER_MAIN"): Promise<NavigationMenuItem[]> {
    const res = await httpClient.get<NavigationMenuItem[]>("/admin/website/menus", {
      params: { location },
    });
    return res.data;
  },

  async createMenu(
    payload: Partial<NavigationMenuItem>
  ): Promise<NavigationMenuItem> {
    const res = await httpClient.post<NavigationMenuItem>(
      "/admin/website/menus",
      payload
    );
    return res.data;
  },

  async updateMenu(
    menuId: string,
    payload: Partial<NavigationMenuItem>
  ): Promise<NavigationMenuItem> {
    const res = await httpClient.patch<NavigationMenuItem>(
      `/admin/website/menus/${menuId}`,
      payload
    );
    return res.data;
  },

  async deleteMenu(menuId: string): Promise<void> {
    await httpClient.delete(`/admin/website/menus/${menuId}`);
  },

  // =========================================================================
  // MODULE 2: HOME PAGE CMS ADMIN APIs
  // =========================================================================
  // Hero Slides
  async listHeroSlides(): Promise<CmsHeroSlide[]> {
    const res = await httpClient.get<CmsHeroSlide[]>("/admin/home/slides");
    return res.data;
  },

  async createHeroSlide(
    payload: Omit<CmsHeroSlide, "id" | "institute_id" | "created_at">
  ): Promise<CmsHeroSlide> {
    const res = await httpClient.post<CmsHeroSlide>("/admin/home/slides", payload);
    return res.data;
  },

  async updateHeroSlide(
    slideId: string,
    payload: Partial<CmsHeroSlide>
  ): Promise<CmsHeroSlide> {
    const res = await httpClient.patch<CmsHeroSlide>(
      `/admin/home/slides/${slideId}`,
      payload
    );
    return res.data;
  },

  async deleteHeroSlide(slideId: string): Promise<void> {
    await httpClient.delete(`/admin/home/slides/${slideId}`);
  },

  // Stat Counters
  async listStatCounters(): Promise<CmsStatCounter[]> {
    const res = await httpClient.get<CmsStatCounter[]>("/admin/home/counters");
    return res.data;
  },

  async createStatCounter(
    payload: Omit<CmsStatCounter, "id" | "institute_id">
  ): Promise<CmsStatCounter> {
    const res = await httpClient.post<CmsStatCounter>("/admin/home/counters", payload);
    return res.data;
  },

  async updateStatCounter(
    counterId: string,
    payload: Partial<CmsStatCounter>
  ): Promise<CmsStatCounter> {
    const res = await httpClient.patch<CmsStatCounter>(
      `/admin/home/counters/${counterId}`,
      payload
    );
    return res.data;
  },

  async deleteStatCounter(counterId: string): Promise<void> {
    await httpClient.delete(`/admin/home/counters/${counterId}`);
  },

  // Featured Programs
  async listFeaturedPrograms(): Promise<CmsFeaturedProgram[]> {
    const res = await httpClient.get<CmsFeaturedProgram[]>("/admin/home/programs");
    return res.data;
  },

  async createFeaturedProgram(
    payload: Omit<CmsFeaturedProgram, "id" | "institute_id">
  ): Promise<CmsFeaturedProgram> {
    const res = await httpClient.post<CmsFeaturedProgram>("/admin/home/programs", payload);
    return res.data;
  },

  async updateFeaturedProgram(
    progId: string,
    payload: Partial<CmsFeaturedProgram>
  ): Promise<CmsFeaturedProgram> {
    const res = await httpClient.patch<CmsFeaturedProgram>(
      `/admin/home/programs/${progId}`,
      payload
    );
    return res.data;
  },

  async deleteFeaturedProgram(progId: string): Promise<void> {
    await httpClient.delete(`/admin/home/programs/${progId}`);
  },

  // =========================================================================
  // MODULE 3: ABOUT INSTITUTE CMS ADMIN APIs
  // =========================================================================
  // Milestones Timeline
  async listMilestones(): Promise<CmsMilestone[]> {
    const res = await httpClient.get<CmsMilestone[]>("/admin/about/milestones");
    return res.data;
  },

  async createMilestone(payload: CmsMilestoneCreateRequest): Promise<CmsMilestone> {
    const res = await httpClient.post<CmsMilestone>("/admin/about/milestones", payload);
    return res.data;
  },

  async updateMilestone(
    id: string,
    payload: Partial<CmsMilestoneCreateRequest>
  ): Promise<CmsMilestone> {
    const res = await httpClient.patch<CmsMilestone>(
      `/admin/about/milestones/${id}`,
      payload
    );
    return res.data;
  },

  async deleteMilestone(id: string): Promise<void> {
    await httpClient.delete(`/admin/about/milestones/${id}`);
  },

  // Leadership Messages
  async listLeadershipMessages(): Promise<CmsLeadershipMessage[]> {
    const res = await httpClient.get<CmsLeadershipMessage[]>("/admin/about/leadership");
    return res.data;
  },

  async createLeadershipMessage(
    payload: CmsLeadershipMessageCreateRequest
  ): Promise<CmsLeadershipMessage> {
    const res = await httpClient.post<CmsLeadershipMessage>(
      "/admin/about/leadership",
      payload
    );
    return res.data;
  },

  async updateLeadershipMessage(
    id: string,
    payload: Partial<CmsLeadershipMessageCreateRequest>
  ): Promise<CmsLeadershipMessage> {
    const res = await httpClient.patch<CmsLeadershipMessage>(
      `/admin/about/leadership/${id}`,
      payload
    );
    return res.data;
  },

  async deleteLeadershipMessage(id: string): Promise<void> {
    await httpClient.delete(`/admin/about/leadership/${id}`);
  },

  // Accreditations
  async listAccreditations(): Promise<CmsAccreditation[]> {
    const res = await httpClient.get<CmsAccreditation[]>("/admin/about/accreditations");
    return res.data;
  },

  async createAccreditation(
    payload: CmsAccreditationCreateRequest
  ): Promise<CmsAccreditation> {
    const res = await httpClient.post<CmsAccreditation>(
      "/admin/about/accreditations",
      payload
    );
    return res.data;
  },

  async updateAccreditation(
    id: string,
    payload: Partial<CmsAccreditationCreateRequest>
  ): Promise<CmsAccreditation> {
    const res = await httpClient.patch<CmsAccreditation>(
      `/admin/about/accreditations/${id}`,
      payload
    );
    return res.data;
  },

  async deleteAccreditation(id: string): Promise<void> {
    await httpClient.delete(`/admin/about/accreditations/${id}`);
  },

  // Campus Infrastructure
  async listCampusInfrastructure(): Promise<CmsCampusInfrastructure[]> {
    const res = await httpClient.get<CmsCampusInfrastructure[]>(
      "/admin/about/infrastructure"
    );
    return res.data;
  },

  async createCampusInfrastructure(
    payload: CmsCampusInfrastructureCreateRequest
  ): Promise<CmsCampusInfrastructure> {
    const res = await httpClient.post<CmsCampusInfrastructure>(
      "/admin/about/infrastructure",
      payload
    );
    return res.data;
  },

  async updateCampusInfrastructure(
    id: string,
    payload: Partial<CmsCampusInfrastructureCreateRequest>
  ): Promise<CmsCampusInfrastructure> {
    const res = await httpClient.patch<CmsCampusInfrastructure>(
      `/admin/about/infrastructure/${id}`,
      payload
    );
    return res.data;
  },

  async deleteCampusInfrastructure(id: string): Promise<void> {
    await httpClient.delete(`/admin/about/infrastructure/${id}`);
  },

  // =========================================================================
  // MODULE 4: COURSE MANAGEMENT SYSTEM (CMS) APIs
  // =========================================================================
  // Public Course Catalog Bundle
  async getPublicCoursesBundle(params?: {
    category_slug?: string;
    degree_level?: string;
    q?: string;
  }): Promise<PublicCoursesBundle> {
    const res = await httpClient.get<PublicCoursesBundle>("/public/courses/bundle", {
      params,
    });
    return res.data;
  },

  // Public Course Detail View
  async getPublicCourseDetail(slug: string): Promise<CmsCourseDetail> {
    const res = await httpClient.get<CmsCourseDetail>(`/public/courses/detail/${slug}`);
    return res.data;
  },

  // Admin Course Categories
  async listAdminCategories(): Promise<CmsCourseCategory[]> {
    const res = await httpClient.get<CmsCourseCategory[]>("/admin/courses/categories");
    return res.data;
  },

  async createAdminCategory(
    payload: CmsCourseCategoryCreateRequest
  ): Promise<CmsCourseCategory> {
    const res = await httpClient.post<CmsCourseCategory>(
      "/admin/courses/categories",
      payload
    );
    return res.data;
  },

  async updateAdminCategory(
    id: string,
    payload: Partial<CmsCourseCategoryCreateRequest>
  ): Promise<CmsCourseCategory> {
    const res = await httpClient.patch<CmsCourseCategory>(
      `/admin/courses/categories/${id}`,
      payload
    );
    return res.data;
  },

  async deleteAdminCategory(id: string): Promise<void> {
    await httpClient.delete(`/admin/courses/categories/${id}`);
  },

  // Admin Courses
  async listAdminCourses(categoryId?: string): Promise<CmsCourseSummary[]> {
    const res = await httpClient.get<CmsCourseSummary[]>("/admin/courses/", {
      params: categoryId ? { category_id: categoryId } : undefined,
    });
    return res.data;
  },

  async getAdminCourseDetail(id: string): Promise<CmsCourseDetail> {
    const res = await httpClient.get<CmsCourseDetail>(`/admin/courses/${id}`);
    return res.data;
  },

  async createAdminCourse(payload: CmsCourseCreateRequest): Promise<CmsCourseDetail> {
    const res = await httpClient.post<CmsCourseDetail>("/admin/courses/", payload);
    return res.data;
  },

  async updateAdminCourse(
    id: string,
    payload: Partial<CmsCourseCreateRequest>
  ): Promise<CmsCourseDetail> {
    const res = await httpClient.patch<CmsCourseDetail>(`/admin/courses/${id}`, payload);
    return res.data;
  },

  async deleteAdminCourse(id: string): Promise<void> {
    await httpClient.delete(`/admin/courses/${id}`);
  },

  // Admin Curriculum & Faculty Sub-items
  async addCourseCurriculum(
    courseId: string,
    payload: CmsCourseCurriculumCreateRequest
  ): Promise<CmsCourseCurriculum> {
    const res = await httpClient.post<CmsCourseCurriculum>(
      `/admin/courses/${courseId}/curricula`,
      payload
    );
    return res.data;
  },

  async deleteCourseCurriculum(curriculumId: string): Promise<void> {
    await httpClient.delete(`/admin/courses/curricula/${curriculumId}`);
  },

  async addCourseFaculty(
    courseId: string,
    payload: CmsCourseFacultyCreateRequest
  ): Promise<CmsCourseFaculty> {
    const res = await httpClient.post<CmsCourseFaculty>(
      `/admin/courses/${courseId}/faculty`,
      payload
    );
    return res.data;
  },

  async deleteCourseFaculty(facultyId: string): Promise<void> {
    await httpClient.delete(`/admin/courses/faculty/${facultyId}`);
  },

  // =========================================================================
  // MODULE 5: ADMISSION SYSTEM APIs
  // =========================================================================
  // Public Admission Bundle (Steps, Fee Structure, Scholarships)
  async getPublicAdmissionBundle(): Promise<PublicAdmissionBundle> {
    const res = await httpClient.get<PublicAdmissionBundle>("/public/admissions/bundle");
    return res.data;
  },

  // Online Application Submission
  async submitOnlineApplication(
    payload: CmsAdmissionApplicationCreateRequest
  ): Promise<CmsAdmissionApplication> {
    const res = await httpClient.post<CmsAdmissionApplication>(
      "/public/admissions/apply",
      payload
    );
    return res.data;
  },

  // Application Tracking
  async trackApplicationStatus(
    applicationNumber: string,
    identifier: string
  ): Promise<CmsAdmissionApplication> {
    const res = await httpClient.get<CmsAdmissionApplication>("/public/admissions/track", {
      params: {
        application_number: applicationNumber,
        identifier,
      },
    });
    return res.data;
  },

  // Public Admission Enquiry / Helpdesk Lead
  async submitAdmissionEnquiry(
    payload: CmsAdmissionEnquiryCreateRequest
  ): Promise<CmsAdmissionEnquiry> {
    const res = await httpClient.post<CmsAdmissionEnquiry>(
      "/public/admissions/enquiry",
      payload
    );
    return res.data;
  },

  // Admin Admission Steps
  async listAdminSteps(): Promise<CmsAdmissionStep[]> {
    const res = await httpClient.get<CmsAdmissionStep[]>("/admin/admissions/steps");
    return res.data;
  },

  async createAdminStep(payload: CmsAdmissionStepCreateRequest): Promise<CmsAdmissionStep> {
    const res = await httpClient.post<CmsAdmissionStep>("/admin/admissions/steps", payload);
    return res.data;
  },

  async updateAdminStep(
    id: string,
    payload: Partial<CmsAdmissionStepCreateRequest>
  ): Promise<CmsAdmissionStep> {
    const res = await httpClient.patch<CmsAdmissionStep>(`/admin/admissions/steps/${id}`, payload);
    return res.data;
  },

  async deleteAdminStep(id: string): Promise<void> {
    await httpClient.delete(`/admin/admissions/steps/${id}`);
  },

  // Admin Fee Structures
  async listAdminFeeStructures(): Promise<CmsFeeStructure[]> {
    const res = await httpClient.get<CmsFeeStructure[]>("/admin/admissions/fees");
    return res.data;
  },

  async createAdminFeeStructure(
    payload: CmsFeeStructureCreateRequest
  ): Promise<CmsFeeStructure> {
    const res = await httpClient.post<CmsFeeStructure>("/admin/admissions/fees", payload);
    return res.data;
  },

  async updateAdminFeeStructure(
    id: string,
    payload: Partial<CmsFeeStructureCreateRequest>
  ): Promise<CmsFeeStructure> {
    const res = await httpClient.patch<CmsFeeStructure>(`/admin/admissions/fees/${id}`, payload);
    return res.data;
  },

  async deleteAdminFeeStructure(id: string): Promise<void> {
    await httpClient.delete(`/admin/admissions/fees/${id}`);
  },

  // Admin Scholarships
  async listAdminScholarships(): Promise<CmsScholarship[]> {
    const res = await httpClient.get<CmsScholarship[]>("/admin/admissions/scholarships");
    return res.data;
  },

  async createAdminScholarship(
    payload: CmsScholarshipCreateRequest
  ): Promise<CmsScholarship> {
    const res = await httpClient.post<CmsScholarship>("/admin/admissions/scholarships", payload);
    return res.data;
  },

  async updateAdminScholarship(
    id: string,
    payload: Partial<CmsScholarshipCreateRequest>
  ): Promise<CmsScholarship> {
    const res = await httpClient.patch<CmsScholarship>(`/admin/admissions/scholarships/${id}`, payload);
    return res.data;
  },

  async deleteAdminScholarship(id: string): Promise<void> {
    await httpClient.delete(`/admin/admissions/scholarships/${id}`);
  },

  // Admin Applications Review
  async listAdminApplications(status?: string): Promise<CmsAdmissionApplication[]> {
    const res = await httpClient.get<CmsAdmissionApplication[]>("/admin/admissions/applications", {
      params: status ? { status } : undefined,
    });
    return res.data;
  },

  async updateApplicationStatus(
    id: string,
    payload: { status: string; remarks?: string; payment_status?: string }
  ): Promise<CmsAdmissionApplication> {
    const res = await httpClient.patch<CmsAdmissionApplication>(
      `/admin/admissions/applications/${id}/status`,
      payload
    );
    return res.data;
  },

  // Admin Enquiries Leads
  async listAdminEnquiries(status?: string): Promise<CmsAdmissionEnquiry[]> {
    const res = await httpClient.get<CmsAdmissionEnquiry[]>("/admin/admissions/enquiries", {
      params: status ? { status } : undefined,
    });
    return res.data;
  },

  async updateEnquiryStatus(
    id: string,
    payload: { status: string; counselor_notes?: string }
  ): Promise<CmsAdmissionEnquiry> {
    const res = await httpClient.patch<CmsAdmissionEnquiry>(
      `/admin/admissions/enquiries/${id}/status`,
      payload
    );
    return res.data;
  },

  // =========================================================================
  // MODULE 6: FACULTY & STAFF DIRECTORY APIs
  // =========================================================================
  // Public Faculty Bundle
  async getPublicFacultyBundle(params?: {
    department?: string;
    q?: string;
  }): Promise<PublicFacultyBundle> {
    const res = await httpClient.get<PublicFacultyBundle>("/public/faculty/bundle", {
      params,
    });
    return res.data;
  },

  // Public Faculty Detail
  async getPublicFacultyDetail(slug: string): Promise<CmsFacultyMemberDetail> {
    const res = await httpClient.get<CmsFacultyMemberDetail>(`/public/faculty/detail/${slug}`);
    return res.data;
  },

  // Public Staff Bundle
  async getPublicStaffBundle(params?: {
    division?: string;
    q?: string;
  }): Promise<PublicStaffBundle> {
    const res = await httpClient.get<PublicStaffBundle>("/public/faculty/staff/bundle", {
      params,
    });
    return res.data;
  },

  // Admin Faculty
  async listAdminFaculty(): Promise<CmsFacultyMemberSummary[]> {
    const res = await httpClient.get<CmsFacultyMemberSummary[]>("/admin/faculty/");
    return res.data;
  },

  async createAdminFaculty(
    payload: CmsFacultyMemberCreateRequest
  ): Promise<CmsFacultyMemberSummary> {
    const res = await httpClient.post<CmsFacultyMemberSummary>("/admin/faculty/", payload);
    return res.data;
  },

  async updateAdminFaculty(
    id: string,
    payload: Partial<CmsFacultyMemberCreateRequest>
  ): Promise<CmsFacultyMemberSummary> {
    const res = await httpClient.patch<CmsFacultyMemberSummary>(`/admin/faculty/${id}`, payload);
    return res.data;
  },

  async deleteAdminFaculty(id: string): Promise<void> {
    await httpClient.delete(`/admin/faculty/${id}`);
  },

  // Admin Research Publications
  async addFacultyPublication(
    facultyId: string,
    payload: CmsResearchPublicationCreateRequest
  ): Promise<CmsResearchPublication> {
    const res = await httpClient.post<CmsResearchPublication>(
      `/admin/faculty/${facultyId}/publications`,
      payload
    );
    return res.data;
  },

  async deleteFacultyPublication(publicationId: string): Promise<void> {
    await httpClient.delete(`/admin/faculty/publications/${publicationId}`);
  },

  // Admin Staff
  async listAdminStaff(): Promise<CmsStaffMember[]> {
    const res = await httpClient.get<CmsStaffMember[]>("/admin/faculty/staff");
    return res.data;
  },

  async createAdminStaff(payload: CmsStaffMemberCreateRequest): Promise<CmsStaffMember> {
    const res = await httpClient.post<CmsStaffMember>("/admin/faculty/staff", payload);
    return res.data;
  },

  async updateAdminStaff(
    id: string,
    payload: Partial<CmsStaffMemberCreateRequest>
  ): Promise<CmsStaffMember> {
    const res = await httpClient.patch<CmsStaffMember>(`/admin/faculty/staff/${id}`, payload);
    return res.data;
  },

  async deleteAdminStaff(id: string): Promise<void> {
    await httpClient.delete(`/admin/faculty/staff/${id}`);
  },

  // =========================================================================
  // MODULE 7: PLACEMENTS, RECRUITERS & SUCCESS STORIES APIs
  // =========================================================================
  // Public Placements Bundle
  async getPublicPlacementsBundle(): Promise<PublicPlacementsBundle> {
    const res = await httpClient.get<PublicPlacementsBundle>("/public/placements/bundle");
    return res.data;
  },

  // Public Recruiters Directory
  async listPublicRecruiters(params?: {
    sector?: string;
    tier?: string;
    q?: string;
  }): Promise<CmsRecruiterPartner[]> {
    const res = await httpClient.get<CmsRecruiterPartner[]>("/public/placements/recruiters", {
      params,
    });
    return res.data;
  },

  // Public Success Stories
  async listPublicSuccessStories(featuredOnly: boolean = false): Promise<CmsAlumniSuccessStory[]> {
    const res = await httpClient.get<CmsAlumniSuccessStory[]>("/public/placements/success-stories", {
      params: { featured_only: featuredOnly },
    });
    return res.data;
  },

  // Admin Placement Stats
  async listAdminPlacementStats(): Promise<CmsPlacementStat[]> {
    const res = await httpClient.get<CmsPlacementStat[]>("/admin/placements/stats");
    return res.data;
  },

  async createAdminPlacementStat(
    payload: CmsPlacementStatCreateRequest
  ): Promise<CmsPlacementStat> {
    const res = await httpClient.post<CmsPlacementStat>("/admin/placements/stats", payload);
    return res.data;
  },

  async updateAdminPlacementStat(
    id: string,
    payload: Partial<CmsPlacementStatCreateRequest>
  ): Promise<CmsPlacementStat> {
    const res = await httpClient.patch<CmsPlacementStat>(`/admin/placements/stats/${id}`, payload);
    return res.data;
  },

  async deleteAdminPlacementStat(id: string): Promise<void> {
    await httpClient.delete(`/admin/placements/stats/${id}`);
  },

  // Admin Recruiter Partners
  async listAdminRecruiters(): Promise<CmsRecruiterPartner[]> {
    const res = await httpClient.get<CmsRecruiterPartner[]>("/admin/placements/recruiters");
    return res.data;
  },

  async createAdminRecruiter(
    payload: CmsRecruiterPartnerCreateRequest
  ): Promise<CmsRecruiterPartner> {
    const res = await httpClient.post<CmsRecruiterPartner>("/admin/placements/recruiters", payload);
    return res.data;
  },

  async updateAdminRecruiter(
    id: string,
    payload: Partial<CmsRecruiterPartnerCreateRequest>
  ): Promise<CmsRecruiterPartner> {
    const res = await httpClient.patch<CmsRecruiterPartner>(`/admin/placements/recruiters/${id}`, payload);
    return res.data;
  },

  async deleteAdminRecruiter(id: string): Promise<void> {
    await httpClient.delete(`/admin/placements/recruiters/${id}`);
  },

  // Admin Alumni Success Stories
  async listAdminStories(): Promise<CmsAlumniSuccessStory[]> {
    const res = await httpClient.get<CmsAlumniSuccessStory[]>("/admin/placements/stories");
    return res.data;
  },

  async createAdminStory(
    payload: CmsAlumniSuccessStoryCreateRequest
  ): Promise<CmsAlumniSuccessStory> {
    const res = await httpClient.post<CmsAlumniSuccessStory>("/admin/placements/stories", payload);
    return res.data;
  },

  async updateAdminStory(
    id: string,
    payload: Partial<CmsAlumniSuccessStoryCreateRequest>
  ): Promise<CmsAlumniSuccessStory> {
    const res = await httpClient.patch<CmsAlumniSuccessStory>(`/admin/placements/stories/${id}`, payload);
    return res.data;
  },

  async deleteAdminStory(id: string): Promise<void> {
    await httpClient.delete(`/admin/placements/stories/${id}`);
  },

  // =========================================================================
  // MODULE 8: EVENTS, NEWS, NOTICES & ACHIEVEMENTS APIs
  // =========================================================================
  // Public Events & News Bundle
  async getPublicEventsNewsBundle(): Promise<PublicEventsNewsBundle> {
    const res = await httpClient.get<PublicEventsNewsBundle>("/public/events-news/bundle");
    return res.data;
  },

  // Admin Events
  async listAdminEvents(): Promise<CmsEvent[]> {
    const res = await httpClient.get<CmsEvent[]>("/admin/events-news/events");
    return res.data;
  },

  async createAdminEvent(payload: CmsEventCreateRequest): Promise<CmsEvent> {
    const res = await httpClient.post<CmsEvent>("/admin/events-news/events", payload);
    return res.data;
  },

  async updateAdminEvent(id: string, payload: Partial<CmsEventCreateRequest>): Promise<CmsEvent> {
    const res = await httpClient.patch<CmsEvent>(`/admin/events-news/events/${id}`, payload);
    return res.data;
  },

  async deleteAdminEvent(id: string): Promise<void> {
    await httpClient.delete(`/admin/events-news/events/${id}`);
  },

  // Admin News
  async listAdminNews(): Promise<CmsNewsArticle[]> {
    const res = await httpClient.get<CmsNewsArticle[]>("/admin/events-news/news");
    return res.data;
  },

  async createAdminNews(payload: CmsNewsArticleCreateRequest): Promise<CmsNewsArticle> {
    const res = await httpClient.post<CmsNewsArticle>("/admin/events-news/news", payload);
    return res.data;
  },

  async updateAdminNews(id: string, payload: Partial<CmsNewsArticleCreateRequest>): Promise<CmsNewsArticle> {
    const res = await httpClient.patch<CmsNewsArticle>(`/admin/events-news/news/${id}`, payload);
    return res.data;
  },

  async deleteAdminNews(id: string): Promise<void> {
    await httpClient.delete(`/admin/events-news/news/${id}`);
  },

  // Admin Notices
  async listAdminNotices(): Promise<CmsNoticeCircular[]> {
    const res = await httpClient.get<CmsNoticeCircular[]>("/admin/events-news/notices");
    return res.data;
  },

  async createAdminNotice(payload: CmsNoticeCircularCreateRequest): Promise<CmsNoticeCircular> {
    const res = await httpClient.post<CmsNoticeCircular>("/admin/events-news/notices", payload);
    return res.data;
  },

  async updateAdminNotice(id: string, payload: Partial<CmsNoticeCircularCreateRequest>): Promise<CmsNoticeCircular> {
    const res = await httpClient.patch<CmsNoticeCircular>(`/admin/events-news/notices/${id}`, payload);
    return res.data;
  },

  async deleteAdminNotice(id: string): Promise<void> {
    await httpClient.delete(`/admin/events-news/notices/${id}`);
  },

  // Admin Achievements
  async listAdminAchievements(): Promise<CmsAchievement[]> {
    const res = await httpClient.get<CmsAchievement[]>("/admin/events-news/achievements");
    return res.data;
  },

  async createAdminAchievement(payload: CmsAchievementCreateRequest): Promise<CmsAchievement> {
    const res = await httpClient.post<CmsAchievement>("/admin/events-news/achievements", payload);
    return res.data;
  },

  async deleteAdminAchievement(id: string): Promise<void> {
    await httpClient.delete(`/admin/events-news/achievements/${id}`);
  },

  // =========================================================================
  // MODULE 9: GALLERY MANAGEMENT CMS APIs
  // =========================================================================
  async getPublicGalleryBundle(params?: {
    category?: string;
    q?: string;
  }): Promise<PublicGalleryBundle> {
    const res = await httpClient.get<PublicGalleryBundle>("/public/gallery/bundle", { params });
    return res.data;
  },

  async getPublicAlbumDetail(slug: string): Promise<CmsGalleryAlbumDetail> {
    const res = await httpClient.get<CmsGalleryAlbumDetail>(`/public/gallery/albums/${slug}`);
    return res.data;
  },

  // Admin Albums
  async listAdminGalleryAlbums(): Promise<CmsGalleryAlbum[]> {
    const res = await httpClient.get<CmsGalleryAlbum[]>("/admin/gallery/albums");
    return res.data;
  },

  async createAdminGalleryAlbum(payload: CmsGalleryAlbumCreateRequest): Promise<CmsGalleryAlbum> {
    const res = await httpClient.post<CmsGalleryAlbum>("/admin/gallery/albums", payload);
    return res.data;
  },

  async updateAdminGalleryAlbum(id: string, payload: Partial<CmsGalleryAlbumCreateRequest>): Promise<CmsGalleryAlbum> {
    const res = await httpClient.patch<CmsGalleryAlbum>(`/admin/gallery/albums/${id}`, payload);
    return res.data;
  },

  async deleteAdminGalleryAlbum(id: string): Promise<void> {
    await httpClient.delete(`/admin/gallery/albums/${id}`);
  },

  // Admin Media
  async listAdminGalleryMedia(albumId: string): Promise<CmsGalleryMedia[]> {
    const res = await httpClient.get<CmsGalleryMedia[]>(`/admin/gallery/albums/${albumId}/media`);
    return res.data;
  },

  async createAdminGalleryMedia(payload: CmsGalleryMediaCreateRequest): Promise<CmsGalleryMedia> {
    const res = await httpClient.post<CmsGalleryMedia>("/admin/gallery/media", payload);
    return res.data;
  },

  async updateAdminGalleryMedia(id: string, payload: Partial<CmsGalleryMediaCreateRequest>): Promise<CmsGalleryMedia> {
    const res = await httpClient.patch<CmsGalleryMedia>(`/admin/gallery/media/${id}`, payload);
    return res.data;
  },

  async deleteAdminGalleryMedia(id: string): Promise<void> {
    await httpClient.delete(`/admin/gallery/media/${id}`);
  },

  // =========================================================================
  // MODULE 10: DOWNLOADS CMS APIs
  // =========================================================================
  async getPublicDownloadsBundle(params?: {
    category_slug?: string;
    program?: string;
    q?: string;
  }): Promise<PublicDownloadsBundle> {
    const res = await httpClient.get<PublicDownloadsBundle>("/public/downloads/bundle", { params });
    return res.data;
  },

  async recordDocumentDownload(documentId: string): Promise<CmsDownloadDocument> {
    const res = await httpClient.post<CmsDownloadDocument>(`/public/downloads/${documentId}/download`);
    return res.data;
  },

  // Admin Categories
  async listAdminDownloadCategories(): Promise<CmsDownloadCategory[]> {
    const res = await httpClient.get<CmsDownloadCategory[]>("/admin/downloads/categories");
    return res.data;
  },

  async createAdminDownloadCategory(payload: CmsDownloadCategoryCreateRequest): Promise<CmsDownloadCategory> {
    const res = await httpClient.post<CmsDownloadCategory>("/admin/downloads/categories", payload);
    return res.data;
  },

  async updateAdminDownloadCategory(id: string, payload: Partial<CmsDownloadCategoryCreateRequest>): Promise<CmsDownloadCategory> {
    const res = await httpClient.patch<CmsDownloadCategory>(`/admin/downloads/categories/${id}`, payload);
    return res.data;
  },

  async deleteAdminDownloadCategory(id: string): Promise<void> {
    await httpClient.delete(`/admin/downloads/categories/${id}`);
  },

  // Admin Documents
  async listAdminDownloadDocuments(categoryId?: string): Promise<CmsDownloadDocument[]> {
    const res = await httpClient.get<CmsDownloadDocument[]>("/admin/downloads/documents", {
      params: categoryId ? { category_id: categoryId } : undefined,
    });
    return res.data;
  },

  async createAdminDownloadDocument(payload: CmsDownloadDocumentCreateRequest): Promise<CmsDownloadDocument> {
    const res = await httpClient.post<CmsDownloadDocument>("/admin/downloads/documents", payload);
    return res.data;
  },

  async updateAdminDownloadDocument(id: string, payload: Partial<CmsDownloadDocumentCreateRequest>): Promise<CmsDownloadDocument> {
    const res = await httpClient.patch<CmsDownloadDocument>(`/admin/downloads/documents/${id}`, payload);
    return res.data;
  },

  async deleteAdminDownloadDocument(id: string): Promise<void> {
    await httpClient.delete(`/admin/downloads/documents/${id}`);
  },

  // =========================================================================
  // MODULE 12: PLACEMENT CELL CMS APIs
  // =========================================================================
  async getPublicPlacementCellBundle(): Promise<PublicPlacementCellBundle> {
    const res = await httpClient.get<PublicPlacementCellBundle>("/public/placements/cell-bundle");
    return res.data;
  },

  // Admin Placement Drives
  async listAdminPlacementDrives(): Promise<CmsPlacementDrive[]> {
    const res = await httpClient.get<CmsPlacementDrive[]>("/admin/placements/drives");
    return res.data;
  },

  async createAdminPlacementDrive(payload: CmsPlacementDriveCreateRequest): Promise<CmsPlacementDrive> {
    const res = await httpClient.post<CmsPlacementDrive>("/admin/placements/drives", payload);
    return res.data;
  },

  async updateAdminPlacementDrive(id: string, payload: Partial<CmsPlacementDriveCreateRequest>): Promise<CmsPlacementDrive> {
    const res = await httpClient.patch<CmsPlacementDrive>(`/admin/placements/drives/${id}`, payload);
    return res.data;
  },

  async deleteAdminPlacementDrive(id: string): Promise<void> {
    await httpClient.delete(`/admin/placements/drives/${id}`);
  },

  // Admin Training Programs
  async listAdminTrainingPrograms(): Promise<CmsTrainingProgram[]> {
    const res = await httpClient.get<CmsTrainingProgram[]>("/admin/placements/training");
    return res.data;
  },

  async createAdminTrainingProgram(payload: CmsTrainingProgramCreateRequest): Promise<CmsTrainingProgram> {
    const res = await httpClient.post<CmsTrainingProgram>("/admin/placements/training", payload);
    return res.data;
  },

  async deleteAdminTrainingProgram(id: string): Promise<void> {
    await httpClient.delete(`/admin/placements/training/${id}`);
  },

  // Admin Internships
  async listAdminInternships(): Promise<CmsInternshipOpportunity[]> {
    const res = await httpClient.get<CmsInternshipOpportunity[]>("/admin/placements/internships");
    return res.data;
  },

  async createAdminInternship(payload: CmsInternshipOpportunityCreateRequest): Promise<CmsInternshipOpportunity> {
    const res = await httpClient.post<CmsInternshipOpportunity>("/admin/placements/internships", payload);
    return res.data;
  },

  async deleteAdminInternship(id: string): Promise<void> {
    await httpClient.delete(`/admin/placements/internships/${id}`);
  },

  // =========================================================================
  // MODULE 13: TESTIMONIALS CMS APIs
  // =========================================================================
  async getPublicTestimonialsBundle(params?: {
    category?: string;
    min_rating?: number;
    has_video?: boolean;
  }): Promise<PublicTestimonialsBundle> {
    const res = await httpClient.get<PublicTestimonialsBundle>("/public/testimonials/bundle", { params });
    return res.data;
  },

  async submitPublicTestimonial(payload: PublicTestimonialSubmitRequest): Promise<CmsTestimonial> {
    const res = await httpClient.post<CmsTestimonial>("/public/testimonials/submit", payload);
    return res.data;
  },

  // Admin Testimonials & Moderation
  async listAdminTestimonials(params?: {
    moderation_status?: string;
    category?: string;
  }): Promise<CmsTestimonial[]> {
    const res = await httpClient.get<CmsTestimonial[]>("/admin/testimonials/reviews", { params });
    return res.data;
  },

  async approveTestimonial(id: string): Promise<CmsTestimonial> {
    const res = await httpClient.post<CmsTestimonial>(`/admin/testimonials/reviews/${id}/approve`);
    return res.data;
  },

  async rejectTestimonial(id: string): Promise<CmsTestimonial> {
    const res = await httpClient.post<CmsTestimonial>(`/admin/testimonials/reviews/${id}/reject`);
    return res.data;
  },

  async createAdminTestimonial(payload: CmsTestimonialCreateRequest): Promise<CmsTestimonial> {
    const res = await httpClient.post<CmsTestimonial>("/admin/testimonials/reviews", payload);
    return res.data;
  },

  async updateAdminTestimonial(id: string, payload: Partial<CmsTestimonialCreateRequest>): Promise<CmsTestimonial> {
    const res = await httpClient.patch<CmsTestimonial>(`/admin/testimonials/reviews/${id}`, payload);
    return res.data;
  },

  async deleteAdminTestimonial(id: string): Promise<void> {
    await httpClient.delete(`/admin/testimonials/reviews/${id}`);
  },

  // =========================================================================
  // MODULE 14: CONTACT & INQUIRY CMS APIs
  // =========================================================================
  async getPublicContactBundle(params?: { q?: string }): Promise<PublicContactBundle> {
    const res = await httpClient.get<PublicContactBundle>("/public/contact/bundle", { params });
    return res.data;
  },

  async submitContactInquiry(payload: PublicContactInquiryCreateRequest): Promise<CmsContactInquiry> {
    const res = await httpClient.post<CmsContactInquiry>("/public/contact/inquiry", payload);
    return res.data;
  },

  async submitSupportFeedback(payload: PublicSupportFeedbackCreateRequest): Promise<CmsSupportFeedback> {
    const res = await httpClient.post<CmsSupportFeedback>("/public/contact/feedback", payload);
    return res.data;
  },

  // Admin Inquiries
  async listAdminInquiries(params?: { status_filter?: string; category?: string }): Promise<CmsContactInquiry[]> {
    const res = await httpClient.get<CmsContactInquiry[]>("/admin/contact/inquiries", { params });
    return res.data;
  },

  async updateAdminInquiry(id: string, payload: { status?: string; admin_notes?: string }): Promise<CmsContactInquiry> {
    const res = await httpClient.patch<CmsContactInquiry>(`/admin/contact/inquiries/${id}`, payload);
    return res.data;
  },

  async deleteAdminInquiry(id: string): Promise<void> {
    await httpClient.delete(`/admin/contact/inquiries/${id}`);
  },

  // Admin Department Contacts
  async listAdminDepartments(): Promise<CmsDepartmentContact[]> {
    const res = await httpClient.get<CmsDepartmentContact[]>("/admin/contact/departments");
    return res.data;
  },

  async createAdminDepartment(payload: CmsDepartmentContactCreateRequest): Promise<CmsDepartmentContact> {
    const res = await httpClient.post<CmsDepartmentContact>("/admin/contact/departments", payload);
    return res.data;
  },

  async updateAdminDepartment(id: string, payload: Partial<CmsDepartmentContactCreateRequest>): Promise<CmsDepartmentContact> {
    const res = await httpClient.patch<CmsDepartmentContact>(`/admin/contact/departments/${id}`, payload);
    return res.data;
  },

  async deleteAdminDepartment(id: string): Promise<void> {
    await httpClient.delete(`/admin/contact/departments/${id}`);
  },

  // Admin FAQs
  async listAdminFaqs(params?: { category?: string }): Promise<CmsFaqItem[]> {
    const res = await httpClient.get<CmsFaqItem[]>("/admin/contact/faqs", { params });
    return res.data;
  },

  async createAdminFaq(payload: CmsFaqItemCreateRequest): Promise<CmsFaqItem> {
    const res = await httpClient.post<CmsFaqItem>("/admin/contact/faqs", payload);
    return res.data;
  },

  async updateAdminFaq(id: string, payload: Partial<CmsFaqItemCreateRequest>): Promise<CmsFaqItem> {
    const res = await httpClient.patch<CmsFaqItem>(`/admin/contact/faqs/${id}`, payload);
    return res.data;
  },

  async deleteAdminFaq(id: string): Promise<void> {
    await httpClient.delete(`/admin/contact/faqs/${id}`);
  },

  // Admin Feedbacks
  async listAdminFeedbacks(params?: { status_filter?: string }): Promise<CmsSupportFeedback[]> {
    const res = await httpClient.get<CmsSupportFeedback[]>("/admin/contact/feedbacks", { params });
    return res.data;
  },

  // =========================================================================
  // MODULE 15: SEARCH & NAVIGATION ENGINE APIs
  // =========================================================================
  // Public Megamenu & Quick Links
  async getPublicMegamenu(location: string = "HEADER_MAIN"): Promise<NavigationMenuItem[]> {
    const res = await httpClient.get<NavigationMenuItem[]>("/public/navigation/megamenu", {
      params: { location },
    });
    return res.data;
  },

  async getPublicQuickLinks(): Promise<WebsiteQuickLink[]> {
    const res = await httpClient.get<WebsiteQuickLink[]>("/public/navigation/quick-links");
    return res.data;
  },

  // Public Multi-Entity Search & Autocomplete
  async globalSiteSearch(params: {
    q: string;
    category?: string;
    limit?: number;
  }): Promise<SearchResponse> {
    const res = await httpClient.get<SearchResponse>("/public/search", { params });
    return res.data;
  },

  async getSearchSuggestions(q: string, limit: number = 8): Promise<SearchSuggestionItem[]> {
    const res = await httpClient.get<SearchSuggestionItem[]>("/public/search/suggestions", {
      params: { q, limit },
    });
    return res.data;
  },

  // Public Sitemap
  async getPublicSitemapJson(): Promise<SitemapResponse> {
    const res = await httpClient.get<SitemapResponse>("/public/sitemap/json");
    return res.data;
  },

  // Admin Navigation Management
  async listAdminNavigationMenus(location?: string): Promise<NavigationMenuItem[]> {
    const res = await httpClient.get<NavigationMenuItem[]>("/admin/navigation/menus", {
      params: location ? { location } : undefined,
    });
    return res.data;
  },

  async createAdminNavigationMenu(payload: Partial<NavigationMenuItem>): Promise<NavigationMenuItem> {
    const res = await httpClient.post<NavigationMenuItem>("/admin/navigation/menus", payload);
    return res.data;
  },

  async updateAdminNavigationMenu(id: string, payload: Partial<NavigationMenuItem>): Promise<NavigationMenuItem> {
    const res = await httpClient.patch<NavigationMenuItem>(`/admin/navigation/menus/${id}`, payload);
    return res.data;
  },

  async deleteAdminNavigationMenu(id: string): Promise<void> {
    await httpClient.delete(`/admin/navigation/menus/${id}`);
  },

  // Admin Quick Links Management
  async listAdminQuickLinks(): Promise<WebsiteQuickLink[]> {
    const res = await httpClient.get<WebsiteQuickLink[]>("/admin/navigation/quick-links");
    return res.data;
  },

  async createAdminQuickLink(payload: Partial<WebsiteQuickLink>): Promise<WebsiteQuickLink> {
    const res = await httpClient.post<WebsiteQuickLink>("/admin/navigation/quick-links", payload);
    return res.data;
  },

  async updateAdminQuickLink(id: string, payload: Partial<WebsiteQuickLink>): Promise<WebsiteQuickLink> {
    const res = await httpClient.patch<WebsiteQuickLink>(`/admin/navigation/quick-links/${id}`, payload);
    return res.data;
  },

  async deleteAdminQuickLink(id: string): Promise<void> {
    await httpClient.delete(`/admin/navigation/quick-links/${id}`);
  },

  // Admin Search Catalog Re-indexing & Analytics
  async reindexSearchCatalog(): Promise<{ status: string; indexed_items: number }> {
    const res = await httpClient.post<{ status: string; indexed_items: number }>("/admin/navigation/reindex-search");
    return res.data;
  },

  async getAdminSearchAnalytics(): Promise<SearchAnalyticsSummary> {
    const res = await httpClient.get<SearchAnalyticsSummary>("/admin/navigation/search-analytics");
    return res.data;
  },
};
