import { EventsNewsManagementPanel } from "@/pages/admin/EventsNewsManagementPanel";
import { GalleryManagementPanel } from "@/pages/admin/GalleryManagementPanel";
import { DownloadsManagementPanel } from "@/pages/admin/DownloadsManagementPanel";
import { PlacementCellManagementPanel } from "@/pages/admin/PlacementCellManagementPanel";
import { TestimonialsModerationPanel } from "@/pages/admin/TestimonialsModerationPanel";
import { ContactInquiriesManagementPanel } from "@/pages/admin/ContactInquiriesManagementPanel";
import { NavigationSitemapManagementPanel } from "@/pages/admin/NavigationSitemapManagementPanel";
import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import {
  Compass,
  Mail,
  Globe,
  Sliders,
  Megaphone,
  MessageSquare,
  Layout,
  Palette,
  Search,
  CheckCircle2,
  Plus,
  Trash2,
  Edit2,
  ExternalLink,
  ShieldAlert,
  ArrowRight,
  Save,
  Tv,
  Activity,
  BookOpen,
  Calendar,
  Camera,
  Download,
  Users,
  Award,
  ShieldCheck,
  Building2,
  Briefcase,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsAlumniSuccessStory,
  CmsPlacementStat,
  CmsRecruiterPartner,
  CmsFacultyMemberCreateRequest,
  CmsFacultyMemberSummary,
  CmsStaffMember,
  CmsStaffMemberCreateRequest,
  CmsAdmissionApplication,
  CmsAdmissionEnquiry,
  CmsAdmissionStep,
  CmsFeeStructure,
  CmsScholarship,
  CmsCourseCategory,
  CmsCourseSummary,
  CmsAccreditation,
  CmsCampusInfrastructure,
  CmsFeaturedProgram,
  CmsHeroSlide,
  CmsLeadershipMessage,
  CmsMilestone,
  CmsStatCounter,
  NavigationMenuItem,
  WebsiteSettings,
  WebsiteTheme,
  WebsiteTickerItem,
} from "@/types/website.types";

export const WebsiteManagementPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<
    | "settings"
    | "ticker"
    | "menus"
    | "theme"
    | "hero_slides"
    | "stats"
    | "programs"
    | "milestones"
    | "leadership"
    | "accreditations"
    | "infrastructure"
    | "course_categories"
    | "courses"
    | "admission_steps"
    | "fee_structures"
    | "scholarships"
    | "applications"
    | "enquiries"
    | "faculty_members"
    | "staff_directory"
    | "placement_stats"
    | "recruiter_partners"
    | "alumni_stories"
    | "events_news"
    | "gallery"
    | "downloads"
    | "placement_cell"
    | "testimonials_moderation"
    | "contact_inquiries"
    | "navigation_sitemap"
  >("settings");
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Queries
  const { data: settings } = useQuery({
    queryKey: ["admin-website-settings"],
    queryFn: websiteService.getSettings,
  });

  const { data: theme } = useQuery({
    queryKey: ["admin-website-theme"],
    queryFn: websiteService.getTheme,
  });

  const { data: tickerItems = [] } = useQuery({
    queryKey: ["admin-website-ticker"],
    queryFn: websiteService.listTickerItems,
  });

  const { data: menuItems = [] } = useQuery({
    queryKey: ["admin-website-menus"],
    queryFn: () => websiteService.listMenus("HEADER_MAIN"),
  });

  // Module 2 Queries
  const { data: heroSlides = [] } = useQuery({
    queryKey: ["admin-home-slides"],
    queryFn: websiteService.listHeroSlides,
  });

  const { data: statCounters = [] } = useQuery({
    queryKey: ["admin-home-counters"],
    queryFn: websiteService.listStatCounters,
  });

  const { data: featuredPrograms = [] } = useQuery({
    queryKey: ["admin-home-programs"],
    queryFn: websiteService.listFeaturedPrograms,
  });

  // Module 3 Queries
  const { data: milestones = [] } = useQuery({
    queryKey: ["admin-about-milestones"],
    queryFn: websiteService.listMilestones,
  });

  const { data: leadershipMessages = [] } = useQuery({
    queryKey: ["admin-about-leadership"],
    queryFn: websiteService.listLeadershipMessages,
  });

  const { data: accreditations = [] } = useQuery({
    queryKey: ["admin-about-accreditations"],
    queryFn: websiteService.listAccreditations,
  });

  const { data: campusInfrastructure = [] } = useQuery({
    queryKey: ["admin-about-infrastructure"],
    queryFn: websiteService.listCampusInfrastructure,
  });

  // Module 4 Course Management Queries
  const { data: courseCategories = [] } = useQuery({
    queryKey: ["admin-course-categories"],
    queryFn: websiteService.listAdminCategories,
  });

  const { data: adminCourses = [] } = useQuery({
    queryKey: ["admin-courses-list"],
    queryFn: () => websiteService.listAdminCourses(),
  });

  // Module 5 Admission System Queries
  const { data: adminSteps = [] } = useQuery({
    queryKey: ["admin-admission-steps"],
    queryFn: websiteService.listAdminSteps,
  });

  const { data: adminFees = [] } = useQuery({
    queryKey: ["admin-fee-structures"],
    queryFn: websiteService.listAdminFeeStructures,
  });

  const { data: adminScholarships = [] } = useQuery({
    queryKey: ["admin-scholarships"],
    queryFn: websiteService.listAdminScholarships,
  });

  const { data: adminApplications = [] } = useQuery({
    queryKey: ["admin-admission-applications"],
    queryFn: () => websiteService.listAdminApplications(),
  });

  const { data: adminEnquiries = [] } = useQuery({
    queryKey: ["admin-admission-enquiries"],
    queryFn: () => websiteService.listAdminEnquiries(),
  });

  // Module 6 Faculty & Staff Queries
  const { data: adminFaculty = [] } = useQuery({
    queryKey: ["admin-faculty-list"],
    queryFn: websiteService.listAdminFaculty,
  });

  const { data: adminStaff = [] } = useQuery({
    queryKey: ["admin-staff-list"],
    queryFn: websiteService.listAdminStaff,
  });

  // Module 7 Placements Queries
  const { data: adminPlacementStats = [] } = useQuery({
    queryKey: ["admin-placements-stats"],
    queryFn: websiteService.listAdminPlacementStats,
  });

  const { data: adminRecruiters = [] } = useQuery({
    queryKey: ["admin-recruiters-list"],
    queryFn: websiteService.listAdminRecruiters,
  });

  const { data: adminStories = [] } = useQuery({
    queryKey: ["admin-stories-list"],
    queryFn: websiteService.listAdminStories,
  });

  // Mutations
  const updateSettingsMutation = useMutation({
    mutationFn: websiteService.updateSettings,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-website-settings"] });
      void queryClient.invalidateQueries({ queryKey: ["public-website-bundle"] });
      setStatusMessage("Website settings updated successfully.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const updateThemeMutation = useMutation({
    mutationFn: websiteService.updateTheme,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-website-theme"] });
      void queryClient.invalidateQueries({ queryKey: ["public-website-bundle"] });
      setStatusMessage("Theme preferences saved.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createTickerMutation = useMutation({
    mutationFn: websiteService.createTickerItem,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-website-ticker"] });
      void queryClient.invalidateQueries({ queryKey: ["public-website-bundle"] });
      setStatusMessage("Live ticker announcement published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteTickerMutation = useMutation({
    mutationFn: websiteService.deleteTickerItem,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-website-ticker"] });
      void queryClient.invalidateQueries({ queryKey: ["public-website-bundle"] });
      setStatusMessage("Ticker item removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createMenuMutation = useMutation({
    mutationFn: websiteService.createMenu,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-website-menus"] });
      void queryClient.invalidateQueries({ queryKey: ["public-website-bundle"] });
      setStatusMessage("Menu item created.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteMenuMutation = useMutation({
    mutationFn: websiteService.deleteMenu,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-website-menus"] });
      void queryClient.invalidateQueries({ queryKey: ["public-website-bundle"] });
      setStatusMessage("Menu item deleted.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Module 2 Mutations
  const createHeroSlideMutation = useMutation({
    mutationFn: websiteService.createHeroSlide,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-home-slides"] });
      void queryClient.invalidateQueries({ queryKey: ["public-home-bundle"] });
      setStatusMessage("Hero slide published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteHeroSlideMutation = useMutation({
    mutationFn: websiteService.deleteHeroSlide,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-home-slides"] });
      void queryClient.invalidateQueries({ queryKey: ["public-home-bundle"] });
      setStatusMessage("Hero slide removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createStatCounterMutation = useMutation({
    mutationFn: websiteService.createStatCounter,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-home-counters"] });
      void queryClient.invalidateQueries({ queryKey: ["public-home-bundle"] });
      setStatusMessage("Stat counter added.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteStatCounterMutation = useMutation({
    mutationFn: websiteService.deleteStatCounter,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-home-counters"] });
      void queryClient.invalidateQueries({ queryKey: ["public-home-bundle"] });
      setStatusMessage("Stat counter removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createProgramMutation = useMutation({
    mutationFn: websiteService.createFeaturedProgram,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-home-programs"] });
      void queryClient.invalidateQueries({ queryKey: ["public-home-bundle"] });
      setStatusMessage("Featured degree program published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteProgramMutation = useMutation({
    mutationFn: websiteService.deleteFeaturedProgram,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-home-programs"] });
      void queryClient.invalidateQueries({ queryKey: ["public-home-bundle"] });
      setStatusMessage("Featured program removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Module 3 Mutations
  const createMilestoneMutation = useMutation({
    mutationFn: websiteService.createMilestone,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-about-milestones"] });
      void queryClient.invalidateQueries({ queryKey: ["public-about-bundle"] });
      setStatusMessage("Milestone published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteMilestoneMutation = useMutation({
    mutationFn: websiteService.deleteMilestone,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-about-milestones"] });
      void queryClient.invalidateQueries({ queryKey: ["public-about-bundle"] });
      setStatusMessage("Milestone removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createLeadershipMutation = useMutation({
    mutationFn: websiteService.createLeadershipMessage,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-about-leadership"] });
      void queryClient.invalidateQueries({ queryKey: ["public-about-bundle"] });
      setStatusMessage("Leadership message published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteLeadershipMutation = useMutation({
    mutationFn: websiteService.deleteLeadershipMessage,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-about-leadership"] });
      void queryClient.invalidateQueries({ queryKey: ["public-about-bundle"] });
      setStatusMessage("Leadership message removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createAccreditationMutation = useMutation({
    mutationFn: websiteService.createAccreditation,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-about-accreditations"] });
      void queryClient.invalidateQueries({ queryKey: ["public-about-bundle"] });
      setStatusMessage("Accreditation published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteAccreditationMutation = useMutation({
    mutationFn: websiteService.deleteAccreditation,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-about-accreditations"] });
      void queryClient.invalidateQueries({ queryKey: ["public-about-bundle"] });
      setStatusMessage("Accreditation removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createInfrastructureMutation = useMutation({
    mutationFn: websiteService.createCampusInfrastructure,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-about-infrastructure"] });
      void queryClient.invalidateQueries({ queryKey: ["public-about-bundle"] });
      setStatusMessage("Campus facility published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteInfrastructureMutation = useMutation({
    mutationFn: websiteService.deleteCampusInfrastructure,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-about-infrastructure"] });
      void queryClient.invalidateQueries({ queryKey: ["public-about-bundle"] });
      setStatusMessage("Campus facility removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Module 4 Course Management Mutations
  const createCourseCategoryMutation = useMutation({
    mutationFn: websiteService.createAdminCategory,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-course-categories"] });
      void queryClient.invalidateQueries({ queryKey: ["public-courses-bundle"] });
      setStatusMessage("Course category created.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteCourseCategoryMutation = useMutation({
    mutationFn: websiteService.deleteAdminCategory,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-course-categories"] });
      void queryClient.invalidateQueries({ queryKey: ["public-courses-bundle"] });
      setStatusMessage("Course category removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createCourseMutation = useMutation({
    mutationFn: websiteService.createAdminCourse,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-courses-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-courses-bundle"] });
      setStatusMessage("Degree course published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteCourseMutation = useMutation({
    mutationFn: websiteService.deleteAdminCourse,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-courses-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-courses-bundle"] });
      setStatusMessage("Degree course deleted.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Module 5 Mutations
  const createStepMutation = useMutation({
    mutationFn: websiteService.createAdminStep,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-admission-steps"] });
      void queryClient.invalidateQueries({ queryKey: ["public-admissions-bundle"] });
      setStatusMessage("Admission step published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteStepMutation = useMutation({
    mutationFn: websiteService.deleteAdminStep,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-admission-steps"] });
      void queryClient.invalidateQueries({ queryKey: ["public-admissions-bundle"] });
      setStatusMessage("Admission step deleted.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createFeeMutation = useMutation({
    mutationFn: websiteService.createAdminFeeStructure,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-fee-structures"] });
      void queryClient.invalidateQueries({ queryKey: ["public-admissions-bundle"] });
      setStatusMessage("Fee schedule created.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteFeeMutation = useMutation({
    mutationFn: websiteService.deleteAdminFeeStructure,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-fee-structures"] });
      void queryClient.invalidateQueries({ queryKey: ["public-admissions-bundle"] });
      setStatusMessage("Fee schedule removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createScholMutation = useMutation({
    mutationFn: websiteService.createAdminScholarship,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-scholarships"] });
      void queryClient.invalidateQueries({ queryKey: ["public-admissions-bundle"] });
      setStatusMessage("Scholarship scheme published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteScholMutation = useMutation({
    mutationFn: websiteService.deleteAdminScholarship,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-scholarships"] });
      void queryClient.invalidateQueries({ queryKey: ["public-admissions-bundle"] });
      setStatusMessage("Scholarship scheme removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const updateAppStatusMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: { status: string; remarks?: string } }) =>
      websiteService.updateApplicationStatus(id, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-admission-applications"] });
      setStatusMessage("Application status updated.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const updateEnqStatusMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: { status: string; counselor_notes?: string } }) =>
      websiteService.updateEnquiryStatus(id, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-admission-enquiries"] });
      setStatusMessage("Enquiry status updated.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Module 6 Mutations
  const createFacultyMutation = useMutation({
    mutationFn: websiteService.createAdminFaculty,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-faculty-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-faculty-bundle"] });
      setStatusMessage("Faculty profile published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteFacultyMutation = useMutation({
    mutationFn: websiteService.deleteAdminFaculty,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-faculty-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-faculty-bundle"] });
      setStatusMessage("Faculty profile removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createStaffMutation = useMutation({
    mutationFn: websiteService.createAdminStaff,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-staff-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-staff-bundle"] });
      setStatusMessage("Staff record added.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteStaffMutation = useMutation({
    mutationFn: websiteService.deleteAdminStaff,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-staff-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-staff-bundle"] });
      setStatusMessage("Staff record removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Module 7 Mutations
  const createStatMutation = useMutation({
    mutationFn: websiteService.createAdminPlacementStat,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-placements-stats"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placements-bundle"] });
      setStatusMessage("Placement track record saved.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteStatMutation = useMutation({
    mutationFn: websiteService.deleteAdminPlacementStat,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-placements-stats"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placements-bundle"] });
      setStatusMessage("Placement track record removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createRecruiterMutation = useMutation({
    mutationFn: websiteService.createAdminRecruiter,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-recruiters-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placements-bundle"] });
      setStatusMessage("Recruiter partner added.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteRecruiterMutation = useMutation({
    mutationFn: websiteService.deleteAdminRecruiter,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-recruiters-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placements-bundle"] });
      setStatusMessage("Recruiter partner removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const createStoryMutation = useMutation({
    mutationFn: websiteService.createAdminStory,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-stories-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placements-bundle"] });
      setStatusMessage("Alumni success story published.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  const deleteStoryMutation = useMutation({
    mutationFn: websiteService.deleteAdminStory,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-stories-list"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placements-bundle"] });
      setStatusMessage("Alumni success story removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Forms
  const { register: registerSettings, handleSubmit: handleSaveSettings } = useForm<Partial<WebsiteSettings>>({
    values: settings,
  });

  const { register: registerTheme, handleSubmit: handleSaveTheme } = useForm<Partial<WebsiteTheme>>({
    values: theme,
  });

  // Ticker form state
  const [newTickerTitle, setNewTickerTitle] = useState("");
  const [newTickerCategory, setNewTickerCategory] = useState("Admission");
  const [newTickerLink, setNewTickerLink] = useState("");
  const [newTickerEmergency, setNewTickerEmergency] = useState(false);

  // Menu form state
  const [newMenuTitle, setNewMenuTitle] = useState("");
  const [newMenuPath, setNewMenuPath] = useState("");

  // Module 2 Form States
  const [newSlideBadge, setNewSlideBadge] = useState("");
  const [newSlideTitle, setNewSlideTitle] = useState("");
  const [newSlideSubtitle, setNewSlideSubtitle] = useState("");
  const [newSlideCtaText, setNewSlideCtaText] = useState("Apply Now");
  const [newSlideCtaLink, setNewSlideCtaLink] = useState("/admissions/apply");

  const [newCounterValue, setNewCounterValue] = useState("");
  const [newCounterLabel, setNewCounterLabel] = useState("");
  const [newCounterSubtext, setNewCounterSubtext] = useState("");

  const [newProgTitle, setNewProgTitle] = useState("");
  const [newProgCode, setNewProgCode] = useState("");
  const [newProgCategory, setNewProgCategory] = useState("Engineering & Technology");
  const [newProgFee, setNewProgFee] = useState("₹95,000 / Year");
  const [newProgSummary, setNewProgSummary] = useState("");

  // Module 3 Form States
  const [newMilestoneYear, setNewMilestoneYear] = useState("");
  const [newMilestoneTitle, setNewMilestoneTitle] = useState("");
  const [newMilestoneDesc, setNewMilestoneDesc] = useState("");

  const [newLeaderName, setNewLeaderName] = useState("");
  const [newLeaderDesig, setNewLeaderDesig] = useState("");
  const [newLeaderRole, setNewLeaderRole] = useState("DIRECTOR");
  const [newLeaderSalutation, setNewLeaderSalutation] = useState("");
  const [newLeaderMsg, setNewLeaderMsg] = useState("");

  const [newAccredBody, setNewAccredBody] = useState("");
  const [newAccredTitle, setNewAccredTitle] = useState("");
  const [newAccredRef, setNewAccredRef] = useState("");
  const [newAccredValidFrom, setNewAccredValidFrom] = useState("2024");
  const [newAccredValidUpto, setNewAccredValidUpto] = useState("2029");

  const [newFacilName, setNewFacilName] = useState("");
  const [newFacilCat, setNewFacilCat] = useState("ACADEMIC");
  const [newFacilCap, setNewFacilCap] = useState("");
  const [newFacilLoc, setNewFacilLoc] = useState("");
  const [newFacilDesc, setNewFacilDesc] = useState("");

  // Module 4 Form States
  const [newCourseCatName, setNewCourseCatName] = useState("");
  const [newCourseCatSlug, setNewCourseCatSlug] = useState("");
  const [newCourseCatDesc, setNewCourseCatDesc] = useState("");

  const [newCourseCode, setNewCourseCode] = useState("");
  const [newCourseSlug, setNewCourseSlug] = useState("");
  const [newCourseTitle, setNewCourseTitle] = useState("");
  const [newCourseShort, setNewCourseShort] = useState("");
  const [newCourseCatId, setNewCourseCatId] = useState("");
  const [newCourseLevel, setNewCourseLevel] = useState("UNDERGRADUATE");
  const [newCourseDuration, setNewCourseDuration] = useState("4 Years (8 Semesters)");
  const [newCourseFee, setNewCourseFee] = useState("₹1,25,000 / Year");
  const [newCourseSeats, setNewCourseSeats] = useState(60);
  const [newCourseElig, setNewCourseElig] = useState("");
  const [newCourseSummary, setNewCourseSummary] = useState("");
  const [newCourseOverview, setNewCourseOverview] = useState("");

  // Module 5 Form States
  const [newStepNum, setNewStepNum] = useState(1);
  const [newStepTitle, setNewStepTitle] = useState("");
  const [newStepDesc, setNewStepDesc] = useState("");
  const [newStepBadge, setNewStepBadge] = useState("");

  const [newFeeProgName, setNewFeeProgName] = useState("");
  const [newFeeProgCode, setNewFeeProgCode] = useState("");
  const [newFeeAdm, setNewFeeAdm] = useState("₹15,000");
  const [newFeeTuit, setNewFeeTuit] = useState("₹55,000");
  const [newFeeTot, setNewFeeTot] = useState("₹1,25,000 / Year");

  const [newScholTitle, setNewScholTitle] = useState("");
  const [newScholCat, setNewScholCat] = useState("MERIT");
  const [newScholElig, setNewScholElig] = useState("");
  const [newScholBen, setNewScholBen] = useState("");
  const [newScholWaiv, setNewScholWaiv] = useState(50);

  // Module 6 Form States
  const [newFacName, setNewFacName] = useState("");
  const [newFacDept, setNewFacDept] = useState("Computer Science & Engineering");
  const [newFacDesig, setNewFacDesig] = useState("Professor");
  const [newFacQual, setNewFacQual] = useState("Ph.D.");
  const [newFacSpec, setNewFacSpec] = useState("");
  const [newFacEmail, setNewFacEmail] = useState("");
  const [newFacBio, setNewFacBio] = useState("");
  const [newFacExp, setNewFacExp] = useState(8);
  const [newFacRoom, setNewFacRoom] = useState("Faculty Block A, Room 302");
  const [newFacInterests, setNewFacInterests] = useState("");
  const [newFacCourses, setNewFacCourses] = useState("");
  const [newFacScholar, setNewFacScholar] = useState("");

  const [newStaffName, setNewStaffName] = useState("");
  const [newStaffDiv, setNewStaffDiv] = useState("Registrar Directorate");
  const [newStaffDesig, setNewStaffDesig] = useState("Assistant Registrar");
  const [newStaffRoom, setNewStaffRoom] = useState("Admin Block, Room 105");
  const [newStaffEmail, setNewStaffEmail] = useState("");
  const [newStaffExt, setNewStaffExt] = useState("Ext 105");

  // Module 7 Form States
  const [newStatYear, setNewStatYear] = useState("2026-2027");
  const [newStatHigh, setNewStatHigh] = useState("₹52.0 LPA");
  const [newStatAvg, setNewStatAvg] = useState("₹12.8 LPA");
  const [newStatMed, setNewStatMed] = useState("₹10.5 LPA");
  const [newStatOffers, setNewStatOffers] = useState(1450);
  const [newStatPct, setNewStatPct] = useState(98.5);

  const [newRecName, setNewRecName] = useState("");
  const [newRecSector, setNewRecSector] = useState("IT & Software");
  const [newRecTier, setNewRecTier] = useState("TIER_1");
  const [newRecPkg, setNewRecPkg] = useState("₹24.0 LPA");
  const [newRecHq, setNewRecHq] = useState("Bangalore");

  const [newStoryName, setNewStoryName] = useState("");
  const [newStoryProg, setNewStoryProg] = useState("B.Tech Computer Science");
  const [newStoryYear, setNewStoryYear] = useState(2024);
  const [newStoryComp, setNewStoryComp] = useState("");
  const [newStoryRole, setNewStoryRole] = useState("");
  const [newStoryPkg, setNewStoryPkg] = useState("₹32.0 LPA");
  const [newStoryQuote, setNewStoryQuote] = useState("");

  const handleAddTicker = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTickerTitle.trim()) return;
    await createTickerMutation.mutateAsync({
      title: newTickerTitle.trim(),
      category: newTickerCategory,
      link_url: newTickerLink.trim() || null,
      is_emergency: newTickerEmergency,
      is_external: newTickerLink.startsWith("http"),
      open_new_tab: false,
      priority_level: newTickerEmergency ? 3 : 1,
      display_order: tickerItems.length + 1,
      is_active: true,
      publish_at: new Date().toISOString(),
      expire_at: null,
    });
    setNewTickerTitle("");
    setNewTickerLink("");
    setNewTickerEmergency(false);
  };

  const handleAddMenu = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMenuTitle.trim() || !newMenuPath.trim()) return;
    await createMenuMutation.mutateAsync({
      menu_location: "HEADER_MAIN",
      title: newMenuTitle.trim(),
      path: newMenuPath.trim(),
      is_external: newMenuPath.startsWith("http"),
      open_new_tab: false,
      is_mega_menu: false,
      display_order: menuItems.length + 1,
      is_active: true,
    });
    setNewMenuTitle("");
    setNewMenuPath("");
  };

  const handleAddSlide = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSlideTitle.trim() || !newSlideSubtitle.trim()) return;
    await createHeroSlideMutation.mutateAsync({
      badge_text: newSlideBadge.trim() || null,
      title: newSlideTitle.trim(),
      subtitle: newSlideSubtitle.trim(),
      primary_cta_text: newSlideCtaText.trim(),
      primary_cta_link: newSlideCtaLink.trim(),
      secondary_cta_text: null,
      secondary_cta_link: null,
      background_image_url: null,
      video_url: null,
      display_order: heroSlides.length + 1,
      is_active: true,
    });
    setNewSlideBadge("");
    setNewSlideTitle("");
    setNewSlideSubtitle("");
  };

  const handleAddCounter = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCounterValue.trim() || !newCounterLabel.trim()) return;
    await createStatCounterMutation.mutateAsync({
      metric_value: newCounterValue.trim(),
      label: newCounterLabel.trim(),
      subtext: newCounterSubtext.trim() || null,
      numeric_target: null,
      icon_name: "Activity",
      display_order: statCounters.length + 1,
      is_active: true,
    });
    setNewCounterValue("");
    setNewCounterLabel("");
    setNewCounterSubtext("");
  };

  const handleAddProgram = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProgTitle.trim() || !newProgCode.trim() || !newProgSummary.trim()) return;
    await createProgramMutation.mutateAsync({
      title: newProgTitle.trim(),
      code: newProgCode.trim(),
      category: newProgCategory,
      degree_level: "Undergraduate",
      duration: "4 Years (8 Semesters)",
      annual_fee: newProgFee.trim(),
      eligibility_summary: "10+2 with PCM >= 60%",
      summary: newProgSummary.trim(),
      image_url: null,
      syllabus_url: null,
      is_admissions_open: true,
      display_order: featuredPrograms.length + 1,
      is_active: true,
    });
    setNewProgTitle("");
    setNewProgCode("");
    setNewProgSummary("");
  };

  const handleAddMilestone = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMilestoneYear.trim() || !newMilestoneTitle.trim() || !newMilestoneDesc.trim()) return;
    await createMilestoneMutation.mutateAsync({
      year: newMilestoneYear.trim(),
      title: newMilestoneTitle.trim(),
      description: newMilestoneDesc.trim(),
      image_url: null,
      icon_name: "Calendar",
      display_order: milestones.length + 1,
      is_active: true,
    });
    setNewMilestoneYear("");
    setNewMilestoneTitle("");
    setNewMilestoneDesc("");
  };

  const handleAddLeadership = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newLeaderName.trim() || !newLeaderDesig.trim() || !newLeaderMsg.trim()) return;
    await createLeadershipMutation.mutateAsync({
      leader_name: newLeaderName.trim(),
      leader_designation: newLeaderDesig.trim(),
      role_category: newLeaderRole,
      salutation_title: newLeaderSalutation.trim() || "Institutional Address",
      message_body: newLeaderMsg.trim(),
      portrait_image_url: null,
      signature_image_url: null,
      video_address_url: null,
      display_order: leadershipMessages.length + 1,
      is_active: true,
    });
    setNewLeaderName("");
    setNewLeaderDesig("");
    setNewLeaderSalutation("");
    setNewLeaderMsg("");
  };

  const handleAddAccreditation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAccredBody.trim() || !newAccredTitle.trim() || !newAccredRef.trim()) return;
    await createAccreditationMutation.mutateAsync({
      accrediting_body: newAccredBody.trim(),
      title: newAccredTitle.trim(),
      approval_reference_number: newAccredRef.trim(),
      valid_from: newAccredValidFrom.trim() || null,
      valid_upto: newAccredValidUpto.trim() || null,
      certificate_pdf_url: null,
      logo_badge_url: null,
      display_order: accreditations.length + 1,
      is_active: true,
    });
    setNewAccredBody("");
    setNewAccredTitle("");
    setNewAccredRef("");
  };

  const handleAddInfrastructure = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFacilName.trim() || !newFacilCap.trim() || !newFacilDesc.trim()) return;
    await createInfrastructureMutation.mutateAsync({
      facility_name: newFacilName.trim(),
      category: newFacilCat,
      capacity_metric: newFacilCap.trim(),
      description: newFacilDesc.trim(),
      floor_or_location: newFacilLoc.trim() || null,
      image_url: null,
      display_order: campusInfrastructure.length + 1,
      is_active: true,
    });
    setNewFacilName("");
    setNewFacilCap("");
    setNewFacilLoc("");
    setNewFacilDesc("");
  };

  const handleAddCourseCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCourseCatName.trim() || !newCourseCatSlug.trim()) return;
    await createCourseCategoryMutation.mutateAsync({
      name: newCourseCatName.trim(),
      slug: newCourseCatSlug.trim().toLowerCase(),
      description: newCourseCatDesc.trim() || null,
      icon_name: "BookOpen",
      display_order: courseCategories.length + 1,
      is_active: true,
    });
    setNewCourseCatName("");
    setNewCourseCatSlug("");
    setNewCourseCatDesc("");
  };

  const handleAddCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCourseCode.trim() || !newCourseTitle.trim() || !newCourseCatId) return;
    await createCourseMutation.mutateAsync({
      category_id: newCourseCatId,
      code: newCourseCode.trim().toUpperCase(),
      slug: newCourseSlug.trim().toLowerCase() || newCourseTitle.toLowerCase().replace(/[^a-z0-9]+/g, "-"),
      title: newCourseTitle.trim(),
      short_name: newCourseShort.trim() || newCourseCode.trim(),
      degree_level: newCourseLevel,
      duration: newCourseDuration.trim(),
      study_mode: "Full-Time On-Campus",
      annual_fee: newCourseFee.trim(),
      seats_intake: Number(newCourseSeats) || 60,
      eligibility_summary: newCourseElig.trim() || "10+2 with minimum 60% aggregate.",
      admission_process: "Centralized counseling and direct merit admission.",
      career_prospects: "Professional industry roles, research, and higher academics.",
      summary: newCourseSummary.trim() || newCourseTitle.trim(),
      overview: newCourseOverview.trim() || newCourseSummary.trim() || newCourseTitle.trim(),
      is_admissions_open: true,
      is_featured: false,
      display_order: adminCourses.length + 1,
      is_active: true,
    });
    setNewCourseCode("");
    setNewCourseSlug("");
    setNewCourseTitle("");
    setNewCourseShort("");
    setNewCourseElig("");
    setNewCourseSummary("");
    setNewCourseOverview("");
  };

  const handleAddAdmissionStep = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newStepTitle.trim() || !newStepDesc.trim()) return;
    await createStepMutation.mutateAsync({
      step_number: Number(newStepNum) || 1,
      title: newStepTitle.trim(),
      description: newStepDesc.trim(),
      icon_name: "CheckCircle2",
      timeline_badge: newStepBadge.trim() || null,
      display_order: Number(newStepNum) || 1,
      is_active: true,
    });
    setNewStepTitle("");
    setNewStepDesc("");
    setNewStepBadge("");
  };

  const handleAddFeeStructure = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFeeProgName.trim() || !newFeeProgCode.trim()) return;
    await createFeeMutation.mutateAsync({
      program_name: newFeeProgName.trim(),
      program_code: newFeeProgCode.trim().toUpperCase(),
      academic_year: "2026-2027",
      admission_fee: newFeeAdm.trim(),
      tuition_fee_per_semester: newFeeTuit.trim(),
      development_fee: "₹10,000",
      examination_fee: "₹5,000",
      caution_deposit_refundable: "₹10,000 (Refundable)",
      total_annual_fee: newFeeTot.trim(),
      display_order: adminFees.length + 1,
      is_active: true,
    });
    setNewFeeProgName("");
    setNewFeeProgCode("");
  };

  const handleAddScholarship = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newScholTitle.trim() || !newScholElig.trim()) return;
    await createScholMutation.mutateAsync({
      title: newScholTitle.trim(),
      category: newScholCat,
      eligibility_criteria: newScholElig.trim(),
      benefit_summary: newScholBen.trim() || `${newScholWaiv}% Tuition Waiver`,
      waiver_percentage: Number(newScholWaiv) || 50,
      validity_period: "Academic Year 2026-27",
      display_order: adminScholarships.length + 1,
      is_active: true,
    });
    setNewScholTitle("");
    setNewScholElig("");
    setNewScholBen("");
  };

  const handleAddFaculty = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFacName.trim() || !newFacEmail.trim()) return;
    const parts = newFacName.trim().split(" ");
    const firstName = parts[0] || "Professor";
    const lastName = parts.slice(1).join(" ") || "Faculty";
    const slug = newFacName.toLowerCase().replace(/[^a-z0-9]+/g, "-");

    await createFacultyMutation.mutateAsync({
      first_name: firstName,
      last_name: lastName,
      full_name: newFacName.trim(),
      slug,
      department: newFacDept,
      designation: newFacDesig.trim(),
      qualifications: newFacQual.trim(),
      specialization: newFacSpec.trim() || "Higher Education & Research",
      email: newFacEmail.trim(),
      bio: newFacBio.trim() || "Distinguished faculty member at MY EDUCATION INDIA Indore campus.",
      experience_years: Number(newFacExp) || 8,
      office_location: newFacRoom.trim() || "Faculty Block A, Room 302",
      research_interests: newFacInterests.trim() || newFacSpec.trim(),
      teaching_courses: newFacCourses.trim() || null,
      google_scholar_url: newFacScholar.trim() || null,
      display_order: adminFaculty.length + 1,
      is_active: true,
    });
    setNewFacName("");
    setNewFacEmail("");
    setNewFacSpec("");
    setNewFacBio("");
  };

  const handleAddStaff = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newStaffName.trim() || !newStaffEmail.trim()) return;
    await createStaffMutation.mutateAsync({
      full_name: newStaffName.trim(),
      division: newStaffDiv,
      designation: newStaffDesig.trim(),
      office_room_number: newStaffRoom.trim(),
      official_email: newStaffEmail.trim(),
      extension_number: newStaffExt.trim(),
      visiting_hours: "Mon–Fri (2:00 PM – 4:30 PM)",
      display_order: adminStaff.length + 1,
      is_active: true,
    });
    setNewStaffName("");
    setNewStaffEmail("");
  };

  const handleAddPlacementStat = async (e: React.FormEvent) => {
    e.preventDefault();
    await createStatMutation.mutateAsync({
      academic_year: newStatYear.trim(),
      highest_package_lpa: newStatHigh.trim(),
      average_package_lpa: newStatAvg.trim(),
      median_package_lpa: newStatMed.trim(),
      total_offers: Number(newStatOffers) || 1000,
      placement_percentage: Number(newStatPct) || 95.0,
      participating_companies: 250,
      display_order: adminPlacementStats.length + 1,
      is_active: true,
    });
  };

  const handleAddRecruiter = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newRecName.trim()) return;
    const slug = newRecName.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    await createRecruiterMutation.mutateAsync({
      company_name: newRecName.trim(),
      slug,
      sector: newRecSector,
      tier: newRecTier,
      highest_package_lpa: newRecPkg.trim(),
      headquarters: newRecHq.trim(),
      display_order: adminRecruiters.length + 1,
      is_active: true,
    });
    setNewRecName("");
  };

  const handleAddStory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newStoryName.trim() || !newStoryComp.trim() || !newStoryQuote.trim()) return;
    await createStoryMutation.mutateAsync({
      alumni_name: newStoryName.trim(),
      degree_program: newStoryProg.trim(),
      graduation_year: Number(newStoryYear) || 2024,
      company_name: newStoryComp.trim(),
      designation: newStoryRole.trim() || "Software Engineer",
      package_lpa: newStoryPkg.trim(),
      testimonial_quote: newStoryQuote.trim(),
      is_featured: true,
      display_order: adminStories.length + 1,
      is_active: true,
    });
    setNewStoryName("");
    setNewStoryComp("");
    setNewStoryRole("");
    setNewStoryQuote("");
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600 shadow-xs">
              <Globe className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">Website Management Center</h1>
              <p className="mt-0.5 text-xs text-slate-500">
                Configure Module 1 (Foundation, Sticky Header, Live Ticker, Menus, Theme) & Module 2 (Hero Slider, Stats, Featured Programs).
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <a
              href="/"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 transition"
            >
              <span>View Live Website</span>
              <ExternalLink className="h-3.5 w-3.5 text-slate-400" />
            </a>
          </div>
        </div>

        {statusMessage && (
          <div className="mt-4 flex items-center gap-2 rounded-xl bg-emerald-50 border border-emerald-200 p-3 text-xs font-semibold text-emerald-800">
            <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
            <span>{statusMessage}</span>
          </div>
        )}

        {/* Tab Controls (Module 1 + Module 2 Tabs) */}
        <div className="mt-6 flex flex-wrap gap-2 border-t border-slate-100 pt-4">
          <button
            type="button"
            onClick={() => setActiveTab("settings")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "settings"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Sliders className="h-3.5 w-3.5" />
            <span>Header & General Settings</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("hero_slides")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "hero_slides"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Tv className="h-3.5 w-3.5" />
            <span>Hero Slider (M2)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {heroSlides.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("stats")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "stats"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Activity className="h-3.5 w-3.5" />
            <span>Stats Counters (M2)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {statCounters.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("programs")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "programs"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <BookOpen className="h-3.5 w-3.5" />
            <span>Featured Programs (M2)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {featuredPrograms.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("ticker")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "ticker"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Megaphone className="h-3.5 w-3.5" />
            <span>Live Ticker Manager</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {tickerItems.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("menus")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "menus"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Layout className="h-3.5 w-3.5" />
            <span>Navigation Menu Tree</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {menuItems.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("milestones")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "milestones"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Calendar className="h-3.5 w-3.5" />
            <span>Milestones (M3)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {milestones.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("leadership")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "leadership"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Users className="h-3.5 w-3.5" />
            <span>Leadership (M3)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {leadershipMessages.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("accreditations")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "accreditations"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <ShieldCheck className="h-3.5 w-3.5" />
            <span>Accreditations (M3)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {accreditations.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("infrastructure")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "infrastructure"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Building2 className="h-3.5 w-3.5" />
            <span>Infrastructure (M3)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {campusInfrastructure.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("course_categories")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "course_categories"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <BookOpen className="h-3.5 w-3.5" />
            <span>Course Categories (M4)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {courseCategories.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("courses")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "courses"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <GraduationCap className="h-3.5 w-3.5" />
            <span>Degree Courses (M4)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminCourses.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("admission_steps")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "admission_steps"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <CheckCircle2 className="h-3.5 w-3.5" />
            <span>Admission Steps (M5)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminSteps.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("fee_structures")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "fee_structures"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <IndianRupee className="h-3.5 w-3.5" />
            <span>Fee Schedules (M5)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminFees.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("scholarships")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "scholarships"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Award className="h-3.5 w-3.5" />
            <span>Scholarships (M5)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminScholarships.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("applications")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "applications"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <FileText className="h-3.5 w-3.5" />
            <span>Applications (M5)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminApplications.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("enquiries")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "enquiries"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <HelpCircle className="h-3.5 w-3.5" />
            <span>Inquiry Leads (M5)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminEnquiries.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("faculty_members")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "faculty_members"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Users className="h-3.5 w-3.5" />
            <span>Faculty Members (M6)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminFaculty.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("staff_directory")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "staff_directory"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Building2 className="h-3.5 w-3.5" />
            <span>Staff Directory (M6)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminStaff.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("placement_stats")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "placement_stats"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Award className="h-3.5 w-3.5" />
            <span>Placement Scorecard (M7)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminPlacementStats.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("recruiter_partners")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "recruiter_partners"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Building2 className="h-3.5 w-3.5" />
            <span>Recruiting Partners (M7)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminRecruiters.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("alumni_stories")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "alumni_stories"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <GraduationCap className="h-3.5 w-3.5" />
            <span>Alumni Stories (M7)</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {adminStories.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("theme")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "theme"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Palette className="h-3.5 w-3.5" />
            <span>Theme & Colors</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("navigation_sitemap")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "navigation_sitemap"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Compass className="h-3.5 w-3.5" />
            <span>Navigation & Search (M15)</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("contact_inquiries")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "contact_inquiries"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Mail className="h-3.5 w-3.5" />
            <span>Inquiries & Helpdesk (M14)</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("testimonials_moderation")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "testimonials_moderation"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <MessageSquare className="h-3.5 w-3.5" />
            <span>Reviews & Moderation (M13)</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("placement_cell")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "placement_cell"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Briefcase className="h-3.5 w-3.5" />
            <span>Placement Cell (M12)</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("downloads")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "downloads"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Download className="h-3.5 w-3.5" />
            <span>Downloads Center (M10)</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("gallery")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "gallery"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Camera className="h-3.5 w-3.5" />
            <span>Media Gallery (M9)</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("events_news")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "events_news"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Calendar className="h-3.5 w-3.5" />
            <span>Events & News Hub (M8)</span>
          </button>

        </div>
      </div>

      {/* ===================================================================
          MODULE 2: TAB 1 - HERO SLIDER MANAGER
      ==================================================================== */}
      {activeTab === "hero_slides" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Hero Slide
            </h2>
            <form onSubmit={handleAddSlide} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Badge Callout (Optional)</label>
                <input
                  type="text"
                  value={newSlideBadge}
                  onChange={(e) => setNewSlideBadge(e.target.value)}
                  placeholder="e.g. Admissions Open 2026-27"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Slide Main Headline</label>
                <textarea
                  rows={2}
                  required
                  value={newSlideTitle}
                  onChange={(e) => setNewSlideTitle(e.target.value)}
                  placeholder="e.g. Empowering Next-Generation Leaders in Technology"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Slide Subtitle / Paragraph</label>
                <textarea
                  rows={3}
                  required
                  value={newSlideSubtitle}
                  onChange={(e) => setNewSlideSubtitle(e.target.value)}
                  placeholder="Detailed academic mission statement..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Primary Button</label>
                  <input
                    type="text"
                    value={newSlideCtaText}
                    onChange={(e) => setNewSlideCtaText(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Target Route</label>
                  <input
                    type="text"
                    value={newSlideCtaLink}
                    onChange={(e) => setNewSlideCtaLink(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={createHeroSlideMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Hero Slide</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Published Hero Slides ({heroSlides.length})
            </h2>

            <div className="mt-4 space-y-3.5">
              {heroSlides.length > 0 ? (
                heroSlides.map((slide) => (
                  <div key={slide.id} className="rounded-xl border border-slate-200 bg-slate-50/50 p-4 flex items-start justify-between gap-4">
                    <div className="space-y-1 flex-1">
                      {slide.badge_text && (
                        <span className="rounded bg-brand-100 px-2 py-0.5 text-[10px] font-bold text-brand-800">
                          {slide.badge_text}
                        </span>
                      )}
                      <h3 className="text-sm font-bold text-slate-900">{slide.title}</h3>
                      <p className="text-xs text-slate-600 line-clamp-2">{slide.subtitle}</p>
                      <div className="flex items-center gap-2 pt-1 text-[11px] text-slate-500 font-mono">
                        <span>CTA: {slide.primary_cta_text} ({slide.primary_cta_link})</span>
                      </div>
                    </div>

                    <button
                      type="button"
                      onClick={() => deleteHeroSlideMutation.mutate(slide.id)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition"
                      title="Delete slide"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))
              ) : (
                <p className="py-8 text-center text-xs text-slate-500">No hero slides found.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 2: TAB 2 - STAT COUNTERS MANAGER
      ==================================================================== */}
      {activeTab === "stats" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Stat Counter
            </h2>
            <form onSubmit={handleAddCounter} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Metric Value Display</label>
                <input
                  type="text"
                  required
                  value={newCounterValue}
                  onChange={(e) => setNewCounterValue(e.target.value)}
                  placeholder="e.g. 15,000+ or 100%"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Metric Label</label>
                <input
                  type="text"
                  required
                  value={newCounterLabel}
                  onChange={(e) => setNewCounterLabel(e.target.value)}
                  placeholder="e.g. Scholars & Alumni"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Subtext Description</label>
                <input
                  type="text"
                  value={newCounterSubtext}
                  onChange={(e) => setNewCounterSubtext(e.target.value)}
                  placeholder="e.g. Empowered Across National Industry"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createStatCounterMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Stat Counter</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Configured Stat Counters ({statCounters.length})
            </h2>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
              {statCounters.map((counter) => (
                <div key={counter.id} className="rounded-xl border border-slate-200 bg-slate-50/50 p-4 flex items-start justify-between">
                  <div>
                    <p className="text-2xl font-black text-brand-600">{counter.metric_value}</p>
                    <p className="text-xs font-bold text-slate-900 mt-1">{counter.label}</p>
                    {counter.subtext && <p className="text-[11px] text-slate-500 mt-0.5">{counter.subtext}</p>}
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteStatCounterMutation.mutate(counter.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 2: TAB 3 - FEATURED PROGRAMS MANAGER
      ==================================================================== */}
      {activeTab === "programs" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Featured Program
            </h2>
            <form onSubmit={handleAddProgram} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Program Title</label>
                <input
                  type="text"
                  required
                  value={newProgTitle}
                  onChange={(e) => setNewProgTitle(e.target.value)}
                  placeholder="e.g. B.Tech Computer Science & Engineering"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Program Code</label>
                  <input
                    type="text"
                    required
                    value={newProgCode}
                    onChange={(e) => setNewProgCode(e.target.value)}
                    placeholder="BTECH-CSE"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Annual Fee</label>
                  <input
                    type="text"
                    value={newProgFee}
                    onChange={(e) => setNewProgFee(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Program Summary</label>
                <textarea
                  rows={3}
                  required
                  value={newProgSummary}
                  onChange={(e) => setNewProgSummary(e.target.value)}
                  placeholder="Overview of curriculum and careers..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createProgramMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Program Card</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Featured Programs on Homepage ({featuredPrograms.length})
            </h2>

            <div className="mt-4 space-y-3">
              {featuredPrograms.map((prog) => (
                <div key={prog.id} className="rounded-xl border border-slate-200 bg-slate-50/50 p-4 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded bg-brand-100 px-1.5 py-0.5 text-[9px] font-bold text-brand-800">
                        {prog.category}
                      </span>
                      <span className="font-mono text-xs text-slate-400">{prog.code}</span>
                      {prog.annual_fee && (
                        <span className="text-xs font-bold text-emerald-700">{prog.annual_fee}</span>
                      )}
                    </div>
                    <h3 className="text-sm font-bold text-slate-900">{prog.title}</h3>
                    <p className="text-xs text-slate-600 line-clamp-2">{prog.summary}</p>
                  </div>

                  <button
                    type="button"
                    onClick={() => deleteProgramMutation.mutate(prog.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 1: SETTINGS TAB
      ==================================================================== */}
      {activeTab === "settings" && (
        <form onSubmit={handleSaveSettings((data) => updateSettingsMutation.mutate(data))}>
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
              <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
                Main Header Configuration
              </h2>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Institutional Site Title</label>
                <input
                  type="text"
                  {...registerSettings("site_title")}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Tagline / Subheading</label>
                <input
                  type="text"
                  {...registerSettings("tagline")}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="space-y-3 pt-2">
                <label className="flex items-center gap-2.5 text-xs font-semibold text-slate-800 cursor-pointer">
                  <input
                    type="checkbox"
                    {...registerSettings("header_is_sticky")}
                    className="h-4 w-4 rounded text-brand-600 focus:ring-brand-500"
                  />
                  <span>Sticky Header (Remains fixed at top during scrolling)</span>
                </label>

                <label className="flex items-center gap-2.5 text-xs font-semibold text-slate-800 cursor-pointer">
                  <input
                    type="checkbox"
                    {...registerSettings("header_show_search")}
                    className="h-4 w-4 rounded text-brand-600 focus:ring-brand-500"
                  />
                  <span>Enable Global Search Button in Header</span>
                </label>

                <label className="flex items-center gap-2.5 text-xs font-semibold text-slate-800 cursor-pointer">
                  <input
                    type="checkbox"
                    {...registerSettings("header_show_login")}
                    className="h-4 w-4 rounded text-brand-600 focus:ring-brand-500"
                  />
                  <span>Show Single Universal Login Button</span>
                </label>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-2">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Login Button Label</label>
                  <input
                    type="text"
                    {...registerSettings("header_login_button_text")}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Login Target Route</label>
                  <input
                    type="text"
                    {...registerSettings("header_login_route")}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
              <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
                Contact Coordinates & SEO
              </h2>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Official Helpline Phone</label>
                <input
                  type="text"
                  {...registerSettings("contact_phone")}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Official Admissions Email</label>
                <input
                  type="email"
                  {...registerSettings("contact_email")}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Campus Physical Address</label>
                <textarea
                  rows={2}
                  {...registerSettings("contact_address")}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Meta Description (SEO)</label>
                <textarea
                  rows={2}
                  {...registerSettings("meta_description")}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  disabled={updateSettingsMutation.isPending}
                  className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
                >
                  <Save className="h-4 w-4" />
                  <span>Save Website Settings</span>
                </button>
              </div>
            </div>
          </div>
        </form>
      )}

      {/* ===================================================================
          MODULE 1: LIVE TICKER TAB
      ==================================================================== */}
      {activeTab === "ticker" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Ticker Announcement
            </h2>
            <form onSubmit={handleAddTicker} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Announcement Headline</label>
                <textarea
                  rows={2}
                  required
                  value={newTickerTitle}
                  onChange={(e) => setNewTickerTitle(e.target.value)}
                  placeholder="e.g. National Entrance Exam 2026-27 Registrations Open"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Category Tag</label>
                  <select
                    value={newTickerCategory}
                    onChange={(e) => setNewTickerCategory(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    {[
                      "Admission",
                      "Examination",
                      "Result",
                      "Holiday",
                      "Circular",
                      "Event",
                      "News",
                      "Placement",
                      "Scholarship",
                      "Emergency",
                      "Important Notice",
                    ].map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">Target URL / Route</label>
                  <input
                    type="text"
                    value={newTickerLink}
                    onChange={(e) => setNewTickerLink(e.target.value)}
                    placeholder="/admissions/apply"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <label className="flex items-center gap-2 text-xs font-bold text-rose-700 cursor-pointer pt-1">
                <input
                  type="checkbox"
                  checked={newTickerEmergency}
                  onChange={(e) => setNewTickerEmergency(e.target.checked)}
                  className="h-4 w-4 rounded text-rose-600 focus:ring-rose-500"
                />
                <span>Emergency Notice (Turns entire banner red)</span>
              </label>

              <button
                type="submit"
                disabled={createTickerMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish to Live Ticker</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Active Ticker Announcements ({tickerItems.length})
            </h2>

            <div className="mt-4 divide-y divide-slate-100">
              {tickerItems.length > 0 ? (
                tickerItems.map((item) => (
                  <div key={item.id} className="flex items-start justify-between py-3.5 gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span
                          className={`rounded px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-wider ${
                            item.is_emergency
                              ? "bg-rose-100 text-rose-800"
                              : "bg-brand-100 text-brand-800"
                          }`}
                        >
                          {item.category}
                        </span>
                        {item.is_emergency && (
                          <span className="rounded bg-rose-600 px-1.5 py-0.5 text-[9px] font-bold text-white">
                            EMERGENCY
                          </span>
                        )}
                        <span className="text-[11px] text-slate-400">Order #{item.display_order}</span>
                      </div>
                      <p className="text-xs font-bold text-slate-900">{item.title}</p>
                      {item.link_url && (
                        <p className="text-[11px] font-mono text-brand-600">{item.link_url}</p>
                      )}
                    </div>

                    <button
                      type="button"
                      onClick={() => deleteTickerMutation.mutate(item.id)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))
              ) : (
                <p className="py-8 text-center text-xs text-slate-500">No active ticker items found.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 1: NAVIGATION MENUS TAB
      ==================================================================== */}
      {activeTab === "menus" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Menu Link
            </h2>
            <form onSubmit={handleAddMenu} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Menu Label</label>
                <input
                  type="text"
                  required
                  value={newMenuTitle}
                  onChange={(e) => setNewMenuTitle(e.target.value)}
                  placeholder="e.g. Research & Innovation"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Link Path / URL</label>
                <input
                  type="text"
                  required
                  value={newMenuPath}
                  onChange={(e) => setNewMenuPath(e.target.value)}
                  placeholder="/research or https://..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createMenuMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Add to Main Navigation</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Header Navigation Items & Submenus ({menuItems.length})
            </h2>

            <div className="mt-4 space-y-3">
              {menuItems.map((item) => (
                <div key={item.id} className="rounded-xl border border-slate-200 bg-slate-50/50 p-3.5">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-xs font-bold text-slate-900">{item.title}</span>
                      <span className="ml-2 font-mono text-[11px] text-slate-500">{item.path}</span>
                      {item.children && item.children.length > 0 && (
                        <span className="ml-2 rounded-md bg-brand-100 px-1.5 py-0.5 text-[10px] font-bold text-brand-800">
                          {item.children.length} submenus
                        </span>
                      )}
                    </div>
                    <button
                      type="button"
                      onClick={() => deleteMenuMutation.mutate(item.id)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>

                  {item.children && item.children.length > 0 && (
                    <div className="mt-2.5 ml-4 border-l-2 border-brand-200 pl-3 space-y-1.5">
                      {item.children.map((child) => (
                        <div key={child.id} className="flex items-center justify-between py-1 text-xs">
                          <span className="font-medium text-slate-700">{child.title}</span>
                          <span className="font-mono text-[10px] text-slate-400">{child.path}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 1: THEME TAB
      ==================================================================== */}
      {activeTab === "theme" && (
        <form onSubmit={handleSaveTheme((data) => updateThemeMutation.mutate(data))}>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-6">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Brand Color Palette & Styling
            </h2>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Primary Color</label>
                <div className="mt-1.5 flex items-center gap-3">
                  <input
                    type="color"
                    {...registerTheme("primary_color")}
                    className="h-10 w-12 cursor-pointer rounded-lg border border-slate-300 p-1"
                  />
                  <input
                    type="text"
                    {...registerTheme("primary_color")}
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-mono uppercase text-slate-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Secondary Accent</label>
                <div className="mt-1.5 flex items-center gap-3">
                  <input
                    type="color"
                    {...registerTheme("secondary_color")}
                    className="h-10 w-12 cursor-pointer rounded-lg border border-slate-300 p-1"
                  />
                  <input
                    type="text"
                    {...registerTheme("secondary_color")}
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-mono uppercase text-slate-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Border Radius</label>
                <select
                  {...registerTheme("border_radius")}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  <option value="0.375rem">Subtle (6px)</option>
                  <option value="0.75rem">Rounded (12px - Default)</option>
                  <option value="1rem">Pill / Soft (16px)</option>
                </select>
              </div>
            </div>

            <div className="border-t border-slate-100 pt-4">
              <button
                type="submit"
                disabled={updateThemeMutation.isPending}
                className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Save className="h-4 w-4" />
                <span>Save Theme Palette</span>
              </button>
            </div>
          </div>
        </form>
      )}

      {/* ===================================================================
          MODULE 3: MILESTONES TIMELINE TAB
      ==================================================================== */}
      {activeTab === "milestones" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Timeline Milestone
            </h2>
            <form onSubmit={handleAddMilestone} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Year</label>
                <input
                  type="text"
                  required
                  value={newMilestoneYear}
                  onChange={(e) => setNewMilestoneYear(e.target.value)}
                  placeholder="e.g. 2026"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Milestone Title</label>
                <input
                  type="text"
                  required
                  value={newMilestoneTitle}
                  onChange={(e) => setNewMilestoneTitle(e.target.value)}
                  placeholder="e.g. NAAC Grade A+ Accreditation"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Description</label>
                <textarea
                  rows={3}
                  required
                  value={newMilestoneDesc}
                  onChange={(e) => setNewMilestoneDesc(e.target.value)}
                  placeholder="Detailed institutional significance..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createMilestoneMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Milestone</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Institutional History Milestones ({milestones.length})
            </h2>
            <div className="mt-4 space-y-3">
              {milestones.map((m) => (
                <div key={m.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-brand-100 px-2.5 py-0.5 text-xs font-extrabold text-brand-800">
                        {m.year}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{m.title}</h4>
                    </div>
                    <p className="text-xs text-slate-600">{m.description}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteMilestoneMutation.mutate(m.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 3: LEADERSHIP MESSAGES TAB
      ==================================================================== */}
      {activeTab === "leadership" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Executive Leader Message
            </h2>
            <form onSubmit={handleAddLeadership} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Leader Full Name</label>
                <input
                  type="text"
                  required
                  value={newLeaderName}
                  onChange={(e) => setNewLeaderName(e.target.value)}
                  placeholder="e.g. Prof. (Dr.) A. K. Sharma"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Official Designation</label>
                <input
                  type="text"
                  required
                  value={newLeaderDesig}
                  onChange={(e) => setNewLeaderDesig(e.target.value)}
                  placeholder="e.g. Director General & Principal"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Role Category</label>
                <select
                  value={newLeaderRole}
                  onChange={(e) => setNewLeaderRole(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  <option value="CHAIRMAN">Chairman & Chancellor</option>
                  <option value="DIRECTOR">Director General</option>
                  <option value="PRINCIPAL">Principal</option>
                  <option value="DEAN">Dean of Academics</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Salutation / Headline</label>
                <input
                  type="text"
                  value={newLeaderSalutation}
                  onChange={(e) => setNewLeaderSalutation(e.target.value)}
                  placeholder="e.g. Empowering Next-Generation Pioneers"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Message Body</label>
                <textarea
                  rows={4}
                  required
                  value={newLeaderMsg}
                  onChange={(e) => setNewLeaderMsg(e.target.value)}
                  placeholder="Enter full institutional message text..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createLeadershipMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Message</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Leadership Messages ({leadershipMessages.length})
            </h2>
            <div className="mt-4 space-y-4">
              {leadershipMessages.map((lm) => (
                <div key={lm.id} className="rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="rounded-md bg-purple-100 px-2 py-0.5 text-[10px] font-bold text-purple-800 uppercase">
                        {lm.role_category}
                      </span>
                      <h4 className="text-sm font-bold text-slate-900 mt-1">{lm.leader_name}</h4>
                      <p className="text-xs text-slate-500">{lm.leader_designation}</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => deleteLeadershipMutation.mutate(lm.id)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                  <p className="mt-2 text-xs font-semibold text-slate-700">{lm.salutation_title}</p>
                  <p className="mt-1 text-xs text-slate-600 line-clamp-3">{lm.message_body}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 3: ACCREDITATIONS & APPROVALS TAB
      ==================================================================== */}
      {activeTab === "accreditations" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Accreditation Record
            </h2>
            <form onSubmit={handleAddAccreditation} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Accrediting Body</label>
                <input
                  type="text"
                  required
                  value={newAccredBody}
                  onChange={(e) => setNewAccredBody(e.target.value)}
                  placeholder="e.g. AICTE, UGC, NAAC, NBA"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Accreditation Title</label>
                <input
                  type="text"
                  required
                  value={newAccredTitle}
                  onChange={(e) => setNewAccredTitle(e.target.value)}
                  placeholder="e.g. Grade A+ Institutional Accreditation"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Order / Reference Number</label>
                <input
                  type="text"
                  required
                  value={newAccredRef}
                  onChange={(e) => setNewAccredRef(e.target.value)}
                  placeholder="e.g. NAAC/A&A/2024/IND-0821"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Valid From</label>
                  <input
                    type="text"
                    value={newAccredValidFrom}
                    onChange={(e) => setNewAccredValidFrom(e.target.value)}
                    placeholder="2024"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Valid Upto</label>
                  <input
                    type="text"
                    value={newAccredValidUpto}
                    onChange={(e) => setNewAccredValidUpto(e.target.value)}
                    placeholder="2029"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={createAccreditationMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Accreditation</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Institutional Accreditations & Recognitions ({accreditations.length})
            </h2>
            <div className="mt-4 space-y-3">
              {accreditations.map((acc) => (
                <div key={acc.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-extrabold text-emerald-800">
                        {acc.accrediting_body}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{acc.title}</h4>
                    </div>
                    <div className="text-[11px] text-slate-500 font-mono">
                      Ref: {acc.approval_reference_number} • Validity: {acc.valid_from || "Start"} - {acc.valid_upto || "Perpetual"}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteAccreditationMutation.mutate(acc.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 3: CAMPUS INFRASTRUCTURE TAB
      ==================================================================== */}
      {activeTab === "infrastructure" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Campus Facility
            </h2>
            <form onSubmit={handleAddInfrastructure} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Facility Name</label>
                <input
                  type="text"
                  required
                  value={newFacilName}
                  onChange={(e) => setNewFacilName(e.target.value)}
                  placeholder="e.g. Central Digital Library"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Category</label>
                <select
                  value={newFacilCat}
                  onChange={(e) => setNewFacilCat(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  <option value="ACADEMIC">Academic Complex</option>
                  <option value="EXAMINATION">CBT & Examination Lab</option>
                  <option value="RESEARCH">R&D & Innovation Center</option>
                  <option value="SPORTS">Sports & Athletics</option>
                  <option value="RESIDENTIAL">Hostels & Dining</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Capacity / Specs Metric</label>
                <input
                  type="text"
                  required
                  value={newFacilCap}
                  onChange={(e) => setNewFacilCap(e.target.value)}
                  placeholder="e.g. 500 Biometric Exam Terminals"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Location / Floor</label>
                <input
                  type="text"
                  value={newFacilLoc}
                  onChange={(e) => setNewFacilLoc(e.target.value)}
                  placeholder="e.g. Technology Tower, 3rd Floor"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Description</label>
                <textarea
                  rows={3}
                  required
                  value={newFacilDesc}
                  onChange={(e) => setNewFacilDesc(e.target.value)}
                  placeholder="Facility specifications and research capabilities..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createInfrastructureMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Facility</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Campus Facilities & Infrastructure ({campusInfrastructure.length})
            </h2>
            <div className="mt-4 space-y-3">
              {campusInfrastructure.map((inf) => (
                <div key={inf.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-blue-100 px-2 py-0.5 text-xs font-extrabold text-brand-800">
                        {inf.category}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{inf.facility_name}</h4>
                    </div>
                    <div className="text-xs font-semibold text-brand-600">{inf.capacity_metric}</div>
                    <p className="text-xs text-slate-600">{inf.description}</p>
                    {inf.floor_or_location && (
                      <div className="text-[11px] text-slate-400">Location: {inf.floor_or_location}</div>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteInfrastructureMutation.mutate(inf.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 4: COURSE CATEGORIES TAB
      ==================================================================== */}
      {activeTab === "course_categories" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Course Category / Faculty
            </h2>
            <form onSubmit={handleAddCourseCategory} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Category Name</label>
                <input
                  type="text"
                  required
                  value={newCourseCatName}
                  onChange={(e) => {
                    setNewCourseCatName(e.target.value);
                    if (!newCourseCatSlug) {
                      setNewCourseCatSlug(e.target.value.toLowerCase().replace(/[^a-z0-9]+/g, "-"));
                    }
                  }}
                  placeholder="e.g. Computer Science & AI"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">URL Slug</label>
                <input
                  type="text"
                  required
                  value={newCourseCatSlug}
                  onChange={(e) => setNewCourseCatSlug(e.target.value)}
                  placeholder="e.g. computer-science-ai"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-mono text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Description</label>
                <textarea
                  rows={3}
                  value={newCourseCatDesc}
                  onChange={(e) => setNewCourseCatDesc(e.target.value)}
                  placeholder="Academic and departmental focus..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createCourseCategoryMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Category</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Course Categories & Departments ({courseCategories.length})
            </h2>
            <div className="mt-4 space-y-3">
              {courseCategories.map((cat) => (
                <div key={cat.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-brand-100 px-2 py-0.5 text-xs font-bold text-brand-800">
                        {cat.name}
                      </span>
                      <span className="font-mono text-[11px] text-slate-400">/{cat.slug}</span>
                    </div>
                    {cat.description && (
                      <p className="text-xs text-slate-600">{cat.description}</p>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteCourseCategoryMutation.mutate(cat.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 4: DEGREE COURSES TAB
      ==================================================================== */}
      {activeTab === "courses" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Degree Course
            </h2>
            <form onSubmit={handleAddCourse} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Course Category</label>
                <select
                  required
                  value={newCourseCatId}
                  onChange={(e) => setNewCourseCatId(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  <option value="">Select Category...</option>
                  {courseCategories.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Course Code</label>
                  <input
                    type="text"
                    required
                    value={newCourseCode}
                    onChange={(e) => setNewCourseCode(e.target.value)}
                    placeholder="e.g. BTECH-CSE"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-mono uppercase text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Degree Level</label>
                  <select
                    value={newCourseLevel}
                    onChange={(e) => setNewCourseLevel(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="UNDERGRADUATE">Undergraduate (UG)</option>
                    <option value="POSTGRADUATE">Postgraduate (PG)</option>
                    <option value="DOCTORAL">Doctoral (Ph.D.)</option>
                    <option value="DIPLOMA">Diploma</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Course Full Title</label>
                <input
                  type="text"
                  required
                  value={newCourseTitle}
                  onChange={(e) => {
                    setNewCourseTitle(e.target.value);
                    if (!newCourseSlug) {
                      setNewCourseSlug(e.target.value.toLowerCase().replace(/[^a-z0-9]+/g, "-"));
                    }
                  }}
                  placeholder="e.g. B.Tech in Computer Science & Engineering (AI & ML)"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">URL Slug</label>
                <input
                  type="text"
                  required
                  value={newCourseSlug}
                  onChange={(e) => setNewCourseSlug(e.target.value)}
                  placeholder="e.g. b-tech-computer-science-engineering"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-mono text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Duration</label>
                  <input
                    type="text"
                    required
                    value={newCourseDuration}
                    onChange={(e) => setNewCourseDuration(e.target.value)}
                    placeholder="4 Years (8 Semesters)"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Annual Tuition Fee</label>
                  <input
                    type="text"
                    required
                    value={newCourseFee}
                    onChange={(e) => setNewCourseFee(e.target.value)}
                    placeholder="₹1,25,000 / Year"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Eligibility Summary</label>
                <input
                  type="text"
                  value={newCourseElig}
                  onChange={(e) => setNewCourseElig(e.target.value)}
                  placeholder="10+2 with PCM (min 60%) + valid JEE score"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Course Summary</label>
                <textarea
                  rows={2}
                  value={newCourseSummary}
                  onChange={(e) => setNewCourseSummary(e.target.value)}
                  placeholder="Brief headline description..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createCourseMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Degree Course</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Published Degree Courses ({adminCourses.length})
            </h2>
            <div className="mt-4 space-y-4">
              {adminCourses.map((c) => (
                <div key={c.id} className="rounded-xl border border-slate-200 bg-slate-50/50 p-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-brand-100 px-2.5 py-0.5 text-xs font-mono font-bold text-brand-800">
                        {c.code}
                      </span>
                      <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800 uppercase">
                        {c.degree_level}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{c.title}</h4>
                    </div>
                    <button
                      type="button"
                      onClick={() => deleteCourseMutation.mutate(c.id)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-[11px] text-slate-500 bg-white p-2.5 rounded-lg border border-slate-100">
                    <div>Duration: <strong className="text-slate-800">{c.duration}</strong></div>
                    <div>Annual Fee: <strong className="text-emerald-700">{c.annual_fee}</strong></div>
                    <div>Seats Intake: <strong className="text-slate-800">{c.seats_intake}</strong></div>
                  </div>
                  <p className="text-xs text-slate-600 line-clamp-2">{c.summary}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 5: ADMISSION STEPS TAB
      ==================================================================== */}
      {activeTab === "admission_steps" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Admission Step
            </h2>
            <form onSubmit={handleAddAdmissionStep} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Step Number</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  required
                  value={newStepNum}
                  onChange={(e) => setNewStepNum(Number(e.target.value))}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Step Title</label>
                <input
                  type="text"
                  required
                  value={newStepTitle}
                  onChange={(e) => setNewStepTitle(e.target.value)}
                  placeholder="e.g. Document Verification"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Timeline / Stage Badge</label>
                <input
                  type="text"
                  value={newStepBadge}
                  onChange={(e) => setNewStepBadge(e.target.value)}
                  placeholder="e.g. Step 2: Scrutiny"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Description</label>
                <textarea
                  rows={3}
                  required
                  value={newStepDesc}
                  onChange={(e) => setNewStepDesc(e.target.value)}
                  placeholder="Workflow instructions for candidate..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createStepMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Step</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Admission Process Steps ({adminSteps.length})
            </h2>
            <div className="mt-4 space-y-3">
              {adminSteps.map((s) => (
                <div key={s.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="flex h-6 w-6 items-center justify-center rounded-lg bg-brand-600 text-white font-extrabold text-xs">
                        {s.step_number}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{s.title}</h4>
                      {s.timeline_badge && (
                        <span className="rounded-md bg-blue-100 px-2 py-0.5 text-[10px] font-bold text-brand-800">
                          {s.timeline_badge}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-600">{s.description}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteStepMutation.mutate(s.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 5: FEE STRUCTURES TAB
      ==================================================================== */}
      {activeTab === "fee_structures" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Program Fee Schedule
            </h2>
            <form onSubmit={handleAddFeeStructure} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Program Title</label>
                <input
                  type="text"
                  required
                  value={newFeeProgName}
                  onChange={(e) => setNewFeeProgName(e.target.value)}
                  placeholder="e.g. B.Tech Computer Science"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Program Code</label>
                <input
                  type="text"
                  required
                  value={newFeeProgCode}
                  onChange={(e) => setNewFeeProgCode(e.target.value)}
                  placeholder="e.g. BTECH-CSE"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-mono uppercase text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Admission Fee</label>
                  <input
                    type="text"
                    required
                    value={newFeeAdm}
                    onChange={(e) => setNewFeeAdm(e.target.value)}
                    placeholder="₹15,000"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Tuition / Sem</label>
                  <input
                    type="text"
                    required
                    value={newFeeTuit}
                    onChange={(e) => setNewFeeTuit(e.target.value)}
                    placeholder="₹55,000"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Total Annual Fee</label>
                <input
                  type="text"
                  required
                  value={newFeeTot}
                  onChange={(e) => setNewFeeTot(e.target.value)}
                  placeholder="₹1,25,000 / Year"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createFeeMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Fee Schedule</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Official Program Fee Schedules ({adminFees.length})
            </h2>
            <div className="mt-4 space-y-3">
              {adminFees.map((f) => (
                <div key={f.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-brand-100 px-2 py-0.5 text-xs font-mono font-bold text-brand-800">
                        {f.program_code}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{f.program_name}</h4>
                    </div>
                    <div className="text-xs text-slate-600">
                      Admission: <strong>{f.admission_fee}</strong> • Tuition/Sem: <strong>{f.tuition_fee_per_semester}</strong> • Total Annual: <strong className="text-emerald-700">{f.total_annual_fee}</strong>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteFeeMutation.mutate(f.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 5: SCHOLARSHIPS TAB
      ==================================================================== */}
      {activeTab === "scholarships" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Scholarship Scheme
            </h2>
            <form onSubmit={handleAddScholarship} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Scheme Title</label>
                <input
                  type="text"
                  required
                  value={newScholTitle}
                  onChange={(e) => setNewScholTitle(e.target.value)}
                  placeholder="e.g. Merit Fellowship"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Category</label>
                  <select
                    value={newScholCat}
                    onChange={(e) => setNewScholCat(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="MERIT">Academic Merit</option>
                    <option value="WOMEN_IN_TECH">Women in Tech</option>
                    <option value="SPORTS">Sports & Athletics</option>
                    <option value="DEFENSE">Armed Forces Ward</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">Waiver %</label>
                  <input
                    type="number"
                    min="1"
                    max="100"
                    required
                    value={newScholWaiv}
                    onChange={(e) => setNewScholWaiv(Number(e.target.value))}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Eligibility Criteria</label>
                <textarea
                  rows={2}
                  required
                  value={newScholElig}
                  onChange={(e) => setNewScholElig(e.target.value)}
                  placeholder="Criteria for award..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createScholMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Scholarship</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Institutional Scholarships ({adminScholarships.length})
            </h2>
            <div className="mt-4 space-y-3">
              {adminScholarships.map((s) => (
                <div key={s.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-purple-100 px-2 py-0.5 text-xs font-bold text-purple-800">
                        {s.category}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{s.title}</h4>
                      <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-extrabold text-emerald-800">
                        {s.waiver_percentage}% Waiver
                      </span>
                    </div>
                    <p className="text-xs text-slate-600">{s.eligibility_criteria}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteScholMutation.mutate(s.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 5: CANDIDATE APPLICATIONS TAB
      ==================================================================== */}
      {activeTab === "applications" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-100 pb-4 gap-2">
            <div>
              <h2 className="text-sm font-bold text-slate-900">
                Submitted Candidate Applications ({adminApplications.length})
              </h2>
              <p className="text-xs text-slate-500">Review candidate profiles, entrance scores, and update admission review statuses.</p>
            </div>
          </div>

          {adminApplications.length === 0 ? (
            <div className="p-12 text-center text-xs text-slate-400">
              No online candidate applications received yet.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/80 text-[11px] font-bold text-slate-700 uppercase tracking-wider">
                    <th className="p-3">Application No</th>
                    <th className="p-3">Candidate & Contact</th>
                    <th className="p-3">Preferred Program</th>
                    <th className="p-3">Academic Score</th>
                    <th className="p-3">Status</th>
                    <th className="p-3 text-right">Review Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {adminApplications.map((app) => (
                    <tr key={app.id} className="hover:bg-slate-50/50 transition">
                      <td className="p-3 font-mono font-bold text-brand-700">{app.application_number}</td>
                      <td className="p-3">
                        <div className="font-bold text-slate-900">{app.applicant_name}</div>
                        <div className="text-[11px] text-slate-500">{app.email} • {app.phone}</div>
                      </td>
                      <td className="p-3 font-medium text-slate-800">{app.preferred_course_name}</td>
                      <td className="p-3">
                        <div>{app.qualifying_exam}</div>
                        <strong className="text-slate-900">{app.qualifying_percentage}%</strong>
                      </td>
                      <td className="p-3">
                        <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800 uppercase">
                          {app.status}
                        </span>
                      </td>
                      <td className="p-3 text-right">
                        <select
                          value={app.status}
                          onChange={(e) =>
                            updateAppStatusMutation.mutate({
                              id: app.id,
                              payload: { status: e.target.value, remarks: `Status updated to ${e.target.value}` },
                            })
                          }
                          className="rounded-lg border border-slate-300 px-2 py-1 text-xs font-semibold text-slate-700"
                        >
                          <option value="SUBMITTED">SUBMITTED</option>
                          <option value="UNDER_REVIEW">UNDER REVIEW</option>
                          <option value="DOCUMENTS_VERIFIED">DOCS VERIFIED</option>
                          <option value="PROVISIONAL_OFFER">PROVISIONAL OFFER</option>
                          <option value="CONFIRMED">CONFIRMED</option>
                          <option value="REJECTED">REJECTED</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* ===================================================================
          MODULE 5: INQUIRY LEADS TAB
      ==================================================================== */}
      {activeTab === "enquiries" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div className="border-b border-slate-100 pb-3">
            <h2 className="text-sm font-bold text-slate-900">
              Admission Inquiry Leads ({adminEnquiries.length})
            </h2>
            <p className="text-xs text-slate-500">Incoming inquiries from prospective candidates seeking counseling.</p>
          </div>

          {adminEnquiries.length === 0 ? (
            <div className="p-12 text-center text-xs text-slate-400">
              No inquiry leads logged yet.
            </div>
          ) : (
            <div className="space-y-3">
              {adminEnquiries.map((enq) => (
                <div key={enq.id} className="flex flex-col sm:flex-row sm:items-center sm:justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4 gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900 text-xs">{enq.full_name}</span>
                      <span className="text-[11px] text-slate-500">({enq.city})</span>
                      <span className="rounded-md bg-blue-100 px-2 py-0.5 text-[10px] font-bold text-brand-800">
                        {enq.program_interest}
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-500">{enq.email} • {enq.phone}</div>
                    <p className="text-xs text-slate-700 italic">&ldquo;{enq.message}&rdquo;</p>
                  </div>

                  <div className="shrink-0 flex items-center gap-2">
                    <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                      {enq.status}
                    </span>
                    <select
                      value={enq.status}
                      onChange={(e) =>
                        updateEnqStatusMutation.mutate({
                          id: enq.id,
                          payload: { status: e.target.value },
                        })
                      }
                      className="rounded-lg border border-slate-300 px-2 py-1 text-xs font-semibold text-slate-700"
                    >
                      <option value="NEW">NEW</option>
                      <option value="CONTACTED">CONTACTED</option>
                      <option value="COUNSELING_SCHEDULED">COUNSELING SCHEDULED</option>
                      <option value="CONVERTED">CONVERTED</option>
                      <option value="CLOSED">CLOSED</option>
                    </select>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ===================================================================
          MODULE 6: FACULTY MEMBERS TAB
      ==================================================================== */}
      {activeTab === "faculty_members" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Faculty Profile
            </h2>
            <form onSubmit={handleAddFaculty} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Full Name</label>
                <input
                  type="text"
                  required
                  value={newFacName}
                  onChange={(e) => setNewFacName(e.target.value)}
                  placeholder="e.g. Prof. (Dr.) Arvind Mehta"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Department</label>
                <select
                  value={newFacDept}
                  onChange={(e) => setNewFacDept(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  <option value="Computer Science & Engineering">Computer Science & Engineering</option>
                  <option value="Electronics & Communication Engineering">Electronics & Communication</option>
                  <option value="Management Studies">Management Studies</option>
                  <option value="Applied Sciences">Applied Sciences</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Designation</label>
                  <input
                    type="text"
                    required
                    value={newFacDesig}
                    onChange={(e) => setNewFacDesig(e.target.value)}
                    placeholder="Professor & HOD"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Qualifications</label>
                  <input
                    type="text"
                    required
                    value={newFacQual}
                    onChange={(e) => setNewFacQual(e.target.value)}
                    placeholder="Ph.D. (IIT Bombay)"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Specialization</label>
                <input
                  type="text"
                  required
                  value={newFacSpec}
                  onChange={(e) => setNewFacSpec(e.target.value)}
                  placeholder="AI, Distributed Systems"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Official Email</label>
                <input
                  type="email"
                  required
                  value={newFacEmail}
                  onChange={(e) => setNewFacEmail(e.target.value)}
                  placeholder="faculty@myeducation.in"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Years of Experience</label>
                  <input
                    type="number"
                    min={1}
                    value={newFacExp}
                    onChange={(e) => setNewFacExp(Number(e.target.value))}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Office Room Number</label>
                  <input
                    type="text"
                    value={newFacRoom}
                    onChange={(e) => setNewFacRoom(e.target.value)}
                    placeholder="Block A, Room 302"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Research Focus Areas</label>
                <input
                  type="text"
                  value={newFacInterests}
                  onChange={(e) => setNewFacInterests(e.target.value)}
                  placeholder="e.g. Deep Learning, Autonomous Robotics, Edge AI"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Teaching Course Allocations</label>
                <input
                  type="text"
                  value={newFacCourses}
                  onChange={(e) => setNewFacCourses(e.target.value)}
                  placeholder="e.g. CS601 (Machine Learning), CS605L (AI Lab)"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createFacultyMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Faculty Member</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Academic Faculty Profiles ({adminFaculty.length})
            </h2>
            <div className="mt-4 space-y-3">
              {adminFaculty.map((f) => (
                <div key={f.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-brand-100 px-2 py-0.5 text-xs font-bold text-brand-800">
                        {f.department}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{f.full_name}</h4>
                    </div>
                    <div className="text-xs text-slate-600">
                      {f.designation} • {f.qualifications} • {f.email}
                    </div>
                    <div className="text-[11px] text-slate-500 font-medium">
                      Specialization: {f.specialization}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteFacultyMutation.mutate(f.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 6: STAFF DIRECTORY TAB
      ==================================================================== */}
      {activeTab === "staff_directory" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Staff Record
            </h2>
            <form onSubmit={handleAddStaff} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Full Name</label>
                <input
                  type="text"
                  required
                  value={newStaffName}
                  onChange={(e) => setNewStaffName(e.target.value)}
                  placeholder="e.g. Mr. Sudhir K. Tiwari"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Division / Office</label>
                <select
                  value={newStaffDiv}
                  onChange={(e) => setNewStaffDiv(e.target.value)}
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                >
                  <option value="Registrar Directorate">Registrar Directorate</option>
                  <option value="Finance & Accounts">Finance & Accounts</option>
                  <option value="Examination & CBT Cell">Examination & CBT Cell</option>
                  <option value="Library & Information Science">Library & Information Science</option>
                  <option value="Student Affairs & Hostel">Student Affairs & Hostel</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Designation</label>
                <input
                  type="text"
                  required
                  value={newStaffDesig}
                  onChange={(e) => setNewStaffDesig(e.target.value)}
                  placeholder="Deputy Registrar"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Room / Office</label>
                  <input
                    type="text"
                    required
                    value={newStaffRoom}
                    onChange={(e) => setNewStaffRoom(e.target.value)}
                    placeholder="Admin Block, Room 101"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Extension</label>
                  <input
                    type="text"
                    required
                    value={newStaffExt}
                    onChange={(e) => setNewStaffExt(e.target.value)}
                    placeholder="Ext 101"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Official Email</label>
                <input
                  type="email"
                  required
                  value={newStaffEmail}
                  onChange={(e) => setNewStaffEmail(e.target.value)}
                  placeholder="staff@myeducation.in"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createStaffMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Staff Member</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Administrative & Support Staff ({adminStaff.length})
            </h2>
            <div className="mt-4 space-y-3">
              {adminStaff.map((s) => (
                <div key={s.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-blue-100 px-2 py-0.5 text-xs font-bold text-brand-800">
                        {s.division}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{s.full_name}</h4>
                      <span className="font-mono text-xs text-slate-400">({s.extension_number})</span>
                    </div>
                    <div className="text-xs text-slate-600">
                      {s.designation} • {s.office_room_number} • {s.official_email}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteStaffMutation.mutate(s.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 7: PLACEMENT STATS TAB
      ==================================================================== */}
      {activeTab === "placement_stats" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Annual Placement Record
            </h2>
            <form onSubmit={handleAddPlacementStat} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Academic Year</label>
                <input
                  type="text"
                  required
                  value={newStatYear}
                  onChange={(e) => setNewStatYear(e.target.value)}
                  placeholder="2026-2027"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Highest Package</label>
                  <input
                    type="text"
                    required
                    value={newStatHigh}
                    onChange={(e) => setNewStatHigh(e.target.value)}
                    placeholder="₹52.0 LPA"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Average Package</label>
                  <input
                    type="text"
                    required
                    value={newStatAvg}
                    onChange={(e) => setNewStatAvg(e.target.value)}
                    placeholder="₹12.8 LPA"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Total Offers</label>
                  <input
                    type="number"
                    required
                    value={newStatOffers}
                    onChange={(e) => setNewStatOffers(Number(e.target.value))}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Placement %</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={newStatPct}
                    onChange={(e) => setNewStatPct(Number(e.target.value))}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={createStatMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Placement Stats</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Annual Placement Track Records ({adminPlacementStats.length})
            </h2>
            <div className="mt-4 space-y-3">
              {adminPlacementStats.map((st) => (
                <div key={st.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-brand-100 px-2 py-0.5 text-xs font-bold text-brand-800">
                        Session {st.academic_year}
                      </span>
                      <span className="font-extrabold text-emerald-700 text-xs">Highest: {st.highest_package_lpa}</span>
                    </div>
                    <div className="text-xs text-slate-600">
                      Average: <strong>{st.average_package_lpa}</strong> • Placement Rate: <strong className="text-emerald-700">{st.placement_percentage}%</strong> • Offers: <strong>{st.total_offers}</strong>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteStatMutation.mutate(st.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 7: RECRUITER PARTNERS TAB
      ==================================================================== */}
      {activeTab === "recruiter_partners" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Add Corporate Partner
            </h2>
            <form onSubmit={handleAddRecruiter} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Company Name</label>
                <input
                  type="text"
                  required
                  value={newRecName}
                  onChange={(e) => setNewRecName(e.target.value)}
                  placeholder="e.g. Google Cloud"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Sector</label>
                  <select
                    value={newRecSector}
                    onChange={(e) => setNewRecSector(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="IT & Software">IT & Software</option>
                    <option value="AI & Hardware">AI & Hardware</option>
                    <option value="Cloud & Distributed Systems">Cloud & Systems</option>
                    <option value="Core Engineering">Core Engineering</option>
                    <option value="Consulting & Analytics">Consulting & Analytics</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">Tier</label>
                  <select
                    value={newRecTier}
                    onChange={(e) => setNewRecTier(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="DAY_0">Day 0</option>
                    <option value="TIER_1">Tier 1</option>
                    <option value="REGULAR">Regular</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Maximum Package</label>
                <input
                  type="text"
                  value={newRecPkg}
                  onChange={(e) => setNewRecPkg(e.target.value)}
                  placeholder="₹48.0 LPA"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createRecruiterMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Save Corporate Partner</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Corporate Recruiting Partners ({adminRecruiters.length})
            </h2>
            <div className="mt-4 space-y-3">
              {adminRecruiters.map((r) => (
                <div key={r.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-purple-100 px-2 py-0.5 text-xs font-bold text-purple-800">
                        {r.tier.replace("_", " ")}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{r.company_name}</h4>
                      <span className="text-[11px] text-slate-500">({r.sector})</span>
                    </div>
                    {r.highest_package_lpa && (
                      <div className="text-xs text-emerald-700 font-bold">Max CTC: {r.highest_package_lpa}</div>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteRecruiterMutation.mutate(r.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================================
          MODULE 7: ALUMNI SUCCESS STORIES TAB
      ==================================================================== */}
      {activeTab === "alumni_stories" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Publish Alumni Story
            </h2>
            <form onSubmit={handleAddStory} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Alumni Name</label>
                <input
                  type="text"
                  required
                  value={newStoryName}
                  onChange={(e) => setNewStoryName(e.target.value)}
                  placeholder="e.g. Aarushi Jain"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Degree Program</label>
                <input
                  type="text"
                  required
                  value={newStoryProg}
                  onChange={(e) => setNewStoryProg(e.target.value)}
                  placeholder="B.Tech Computer Science"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Hiring Company</label>
                  <input
                    type="text"
                    required
                    value={newStoryComp}
                    onChange={(e) => setNewStoryComp(e.target.value)}
                    placeholder="Google Cloud"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Package</label>
                  <input
                    type="text"
                    required
                    value={newStoryPkg}
                    onChange={(e) => setNewStoryPkg(e.target.value)}
                    placeholder="₹48.0 LPA"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Testimonial Quote</label>
                <textarea
                  rows={3}
                  required
                  value={newStoryQuote}
                  onChange={(e) => setNewStoryQuote(e.target.value)}
                  placeholder="Alumni reflection on academic preparation..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createStoryMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Success Story</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
              Published Success Stories ({adminStories.length})
            </h2>
            <div className="mt-4 space-y-3">
              {adminStories.map((st) => (
                <div key={st.id} className="flex items-start justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h4 className="text-xs font-bold text-slate-900">{st.alumni_name}</h4>
                      <span className="font-semibold text-brand-600 text-xs">({st.company_name})</span>
                      <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-extrabold text-emerald-800">
                        {st.package_lpa}
                      </span>
                    </div>
                    <div className="text-xs text-slate-500">{st.degree_program} • Class of {st.graduation_year}</div>
                    <p className="text-xs text-slate-600 italic line-clamp-2">&ldquo;{st.testimonial_quote}&rdquo;</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => deleteStoryMutation.mutate(st.id)}
                    className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
          {/* ===================================================================
          MODULE 8: EVENTS, NEWS, NOTICES & ACHIEVEMENTS MANAGEMENT
      ==================================================================== */}
      {activeTab === "events_news" && (
        <EventsNewsManagementPanel />
      )}

      {activeTab === "gallery" && (
        <GalleryManagementPanel />
      )}

      {activeTab === "downloads" && (
        <DownloadsManagementPanel />
      )}

      {activeTab === "placement_cell" && (
        <PlacementCellManagementPanel />
      )}

      {activeTab === "testimonials_moderation" && (
        <TestimonialsModerationPanel />
      )}

      {activeTab === "contact_inquiries" && (
        <ContactInquiriesManagementPanel />
      )}

      {activeTab === "navigation_sitemap" && (
        <NavigationSitemapManagementPanel />
      )}








    </div>
  );
};
