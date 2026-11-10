export interface WebsiteSettings {
  id: string;
  institute_id: string;
  site_title: string;
  tagline: string;
  header_logo_url: string | null;
  footer_logo_url: string | null;
  favicon_url: string | null;

  header_is_sticky: boolean;
  header_show_search: boolean;
  header_show_login: boolean;
  header_login_button_text: string;
  header_login_route: string;

  contact_phone: string;
  contact_email: string;
  contact_address: string;

  meta_description: string;
  meta_keywords: string;
  og_image_url: string | null;
  google_analytics_id: string | null;

  is_maintenance_mode: boolean;
  maintenance_message: string | null;
  custom_css: string | null;
  custom_head_scripts: string | null;
  updated_at: string;
}

export interface WebsiteTheme {
  id: string;
  institute_id: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  background_color: string;
  surface_color: string;
  text_primary_color: string;
  text_secondary_color: string;

  font_family: string;
  heading_font_family: string;
  border_radius: string;
  button_style: string;
  shadow_style: string;
  animation_enabled: boolean;
  updated_at: string;
}

export interface WebsiteTickerItem {
  id: string;
  institute_id: string;
  title: string;
  category: string;
  link_url: string | null;
  is_external: boolean;
  open_new_tab: boolean;
  is_emergency: boolean;
  priority_level: number;
  publish_at: string;
  expire_at: string | null;
  is_active: boolean;
  display_order: number;
  created_at: string;
}

export interface NavigationMenuItem {
  id: string;
  institute_id: string;
  menu_location: string;
  title: string;
  path: string;
  icon_name: string | null;
  badge_text?: string | null;
  description?: string | null;
  category?: string | null;
  parent_id: string | null;
  is_external: boolean;
  open_new_tab: boolean;
  is_mega_menu: boolean;
  display_order: number;
  is_active: boolean;
  children: NavigationMenuItem[];
}

export interface WebsiteQuickLink {
  id: string;
  institute_id: string;
  title: string;
  path: string;
  icon_name: string | null;
  badge_text: string | null;
  target_type: string;
  is_highlighted: boolean;
  display_order: number;
  is_active: boolean;
}

export interface WebsiteSocialLink {
  id: string;
  institute_id: string;
  platform: string;
  url: string;
  display_order: number;
  is_active: boolean;
}

export interface SearchResultItem {
  id: string;
  entity_type: string;
  category: string;
  title: string;
  summary: string;
  target_url: string;
  badge_text?: string | null;
  metadata_json?: Record<string, any> | null;
}

export interface SearchSuggestionItem {
  title: string;
  category: string;
  target_url: string;
  entity_type: string;
  badge_text?: string | null;
}

export interface SearchResponse {
  query: string;
  category_filter: string | null;
  total_results: number;
  results: SearchResultItem[];
  category_counts: Record<string, number>;
}

export interface SitemapItem {
  loc: string;
  lastmod: string | null;
  changefreq: string;
  priority: number;
  title: string;
  category: string;
}

export interface SitemapResponse {
  generated_at: string;
  total_urls: number;
  urls: SitemapItem[];
}

export interface SearchAnalyticsSummary {
  total_searches: number;
  top_queries: { query: string; count: number }[];
  zero_result_queries: { query: string; count: number }[];
  category_distribution: Record<string, number>;
}

export interface SearchResponse {
  query: string;
  total_results: number;
  results: SearchResultItem[];
}

export interface PublicWebsiteFrameworkBundle {
  settings: WebsiteSettings;
  theme: WebsiteTheme;
  header_navigation: NavigationMenuItem[];
  ticker_announcements: WebsiteTickerItem[];
  social_links: WebsiteSocialLink[];
}

// =============================================================================
// MODULE 2: HOME PAGE CMS TYPES
// =============================================================================
export interface CmsHeroSlide {
  id: string;
  institute_id: string;
  badge_text: string | null;
  title: string;
  subtitle: string;
  background_image_url: string | null;
  video_url: string | null;
  primary_cta_text: string;
  primary_cta_link: string;
  secondary_cta_text: string | null;
  secondary_cta_link: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsStatCounter {
  id: string;
  institute_id: string;
  metric_value: string;
  numeric_target: number | null;
  label: string;
  subtext: string | null;
  icon_name: string | null;
  display_order: number;
  is_active: boolean;
}

export interface CmsQuickLink {
  id: string;
  institute_id: string;
  title: string;
  description: string | null;
  path: string;
  icon_name: string | null;
  badge_label: string | null;
  is_external: boolean;
  display_order: number;
  is_active: boolean;
}

export interface CmsFeaturedProgram {
  id: string;
  institute_id: string;
  title: string;
  code: string;
  category: string;
  degree_level: string;
  duration: string;
  annual_fee: string | null;
  eligibility_summary: string;
  summary: string;
  image_url: string | null;
  syllabus_url: string | null;
  is_admissions_open: boolean;
  display_order: number;
  is_active: boolean;
}

export interface CmsRecruiterLogo {
  id: string;
  institute_id: string;
  company_name: string;
  tier: string;
  highest_package_lpa: string | null;
  logo_url: string | null;
  website_url: string | null;
  display_order: number;
  is_active: boolean;
}

export interface CmsTestimonial {
  id: string;
  institute_id: string;
  author_name: string;
  author_role: string;
  author_category: string;
  rating_stars: number;
  quote: string;
  company_or_institution?: string | null;
  batch_year?: string | null;
  avatar_url: string | null;
  video_url: string | null;
  video_thumbnail_url?: string | null;
  video_embed_id?: string | null;
  moderation_status: "PENDING" | "APPROVED" | "REJECTED";
  is_featured: boolean;
  display_order: number;
  is_active: boolean;
  created_at?: string;
}

export interface PublicTestimonialSubmitRequest {
  author_name: string;
  author_role: string;
  author_category: string;
  rating_stars: number;
  quote: string;
  company_or_institution?: string | null;
  batch_year?: string | null;
  avatar_url?: string | null;
  video_url?: string | null;
}

export interface CmsTestimonialCreateRequest {
  author_name: string;
  author_role: string;
  author_category: string;
  rating_stars: number;
  quote: string;
  company_or_institution?: string | null;
  batch_year?: string | null;
  avatar_url?: string | null;
  video_url?: string | null;
  video_thumbnail_url?: string | null;
  video_embed_id?: string | null;
  moderation_status?: "PENDING" | "APPROVED" | "REJECTED";
  is_featured?: boolean;
  display_order?: number;
  is_active?: boolean;
}

export interface PublicTestimonialsBundle {
  testimonials: CmsTestimonial[];
  featured_testimonials: CmsTestimonial[];
  video_testimonials: CmsTestimonial[];
  categories: string[];
  average_rating: number;
  total_reviews: number;
  category_counts: Record<string, number>;
}

export interface PublicHomePageBundle {
  hero_slides: CmsHeroSlide[];
  stat_counters: CmsStatCounter[];
  quick_links: CmsQuickLink[];
  featured_programs: CmsFeaturedProgram[];
  recruiters: CmsRecruiterLogo[];
  testimonials: CmsTestimonial[];
}


// ==========================================
// Phase 1 Module 3: About Institute CMS Types
// ==========================================

export interface CmsMilestone {
  id: string;
  institute_id: string;
  year: string;
  title: string;
  description: string;
  image_url: string | null;
  icon_name: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsMilestoneCreateRequest {
  year: string;
  title: string;
  description: string;
  image_url?: string | null;
  icon_name?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsLeadershipMessage {
  id: string;
  institute_id: string;
  leader_name: string;
  leader_designation: string;
  role_category: string; // CHAIRMAN, DIRECTOR, PRINCIPAL, DEAN
  salutation_title: string;
  message_body: string;
  portrait_image_url: string | null;
  signature_image_url: string | null;
  video_address_url: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsLeadershipMessageCreateRequest {
  leader_name: string;
  leader_designation: string;
  role_category: string;
  salutation_title: string;
  message_body: string;
  portrait_image_url?: string | null;
  signature_image_url?: string | null;
  video_address_url?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsAccreditation {
  id: string;
  institute_id: string;
  accrediting_body: string;
  title: string;
  approval_reference_number: string;
  valid_from: string | null;
  valid_upto: string | null;
  certificate_pdf_url: string | null;
  logo_badge_url: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsAccreditationCreateRequest {
  accrediting_body: string;
  title: string;
  approval_reference_number: string;
  valid_from?: string | null;
  valid_upto?: string | null;
  certificate_pdf_url?: string | null;
  logo_badge_url?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsCampusInfrastructure {
  id: string;
  institute_id: string;
  facility_name: string;
  category: string;
  capacity_metric: string;
  description: string;
  image_url: string | null;
  floor_or_location: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsCampusInfrastructureCreateRequest {
  facility_name: string;
  category: string;
  capacity_metric: string;
  description: string;
  image_url?: string | null;
  floor_or_location?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface PublicAboutInstituteBundle {
  milestones: CmsMilestone[];
  leadership_messages: CmsLeadershipMessage[];
  accreditations: CmsAccreditation[];
  infrastructure: CmsCampusInfrastructure[];
}


// ==========================================
// Phase 1 Module 4: Course Management CMS Types
// ==========================================

export interface CmsCourseCategory {
  id: string;
  institute_id: string;
  name: string;
  slug: string;
  description: string | null;
  icon_name: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsCourseCategoryCreateRequest {
  name: string;
  slug: string;
  description?: string | null;
  icon_name?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsCourseSubject {
  code: string;
  title: string;
  credits: number;
  type: string; // Core, Lab, Elective, Project
  hours_per_week?: number;
}

export interface CmsCourseCurriculum {
  id: string;
  course_id: string;
  semester_number: number;
  semester_title: string;
  credits: number;
  subjects: CmsCourseSubject[];
  display_order: number;
  created_at: string;
}

export interface CmsCourseCurriculumCreateRequest {
  semester_number: number;
  semester_title: string;
  credits?: number;
  subjects: CmsCourseSubject[];
  display_order?: number;
}

export interface CmsCourseFaculty {
  id: string;
  course_id: string;
  faculty_name: string;
  designation: string;
  qualifications: string;
  specialization: string;
  avatar_url: string | null;
  display_order: number;
  created_at: string;
}

export interface CmsCourseFacultyCreateRequest {
  faculty_name: string;
  designation: string;
  qualifications: string;
  specialization: string;
  avatar_url?: string | null;
  display_order?: number;
}

export interface CmsCourseSummary {
  id: string;
  institute_id: string;
  category_id: string;
  code: string;
  slug: string;
  title: string;
  short_name: string;
  degree_level: string; // UNDERGRADUATE, POSTGRADUATE, DIPLOMA, DOCTORAL
  duration: string;
  study_mode: string;
  annual_fee: string;
  total_fee: string | null;
  seats_intake: number;
  eligibility_summary: string;
  summary: string;
  image_url: string | null;
  is_admissions_open: boolean;
  is_featured: boolean;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsCourseDetail extends CmsCourseSummary {
  category?: CmsCourseCategory;
  admission_process: string;
  career_prospects: string;
  overview: string;
  brochure_pdf_url: string | null;
  syllabus_pdf_url: string | null;
  curricula: CmsCourseCurriculum[];
  faculty_members: CmsCourseFaculty[];
}

export interface CmsCourseCreateRequest {
  category_id: string;
  code: string;
  slug: string;
  title: string;
  short_name: string;
  degree_level: string;
  duration: string;
  study_mode?: string;
  annual_fee: string;
  total_fee?: string | null;
  seats_intake?: number;
  eligibility_summary: string;
  admission_process: string;
  career_prospects: string;
  summary: string;
  overview: string;
  image_url?: string | null;
  brochure_pdf_url?: string | null;
  syllabus_pdf_url?: string | null;
  is_admissions_open?: boolean;
  is_featured?: boolean;
  display_order?: number;
  is_active?: boolean;
}

export interface PublicCoursesBundle {
  categories: CmsCourseCategory[];
  courses: CmsCourseSummary[];
  featured_courses: CmsCourseSummary[];
  total_courses: number;
}


// ==========================================
// Phase 1 Module 5: Admission System CMS Types
// ==========================================

export interface CmsAdmissionStep {
  id: string;
  institute_id: string;
  step_number: number;
  title: string;
  description: string;
  icon_name: string | null;
  timeline_badge: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsAdmissionStepCreateRequest {
  step_number: number;
  title: string;
  description: string;
  icon_name?: string | null;
  timeline_badge?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsFeeStructure {
  id: string;
  institute_id: string;
  course_id: string | null;
  program_name: string;
  program_code: string;
  academic_year: string;
  admission_fee: string;
  tuition_fee_per_semester: string;
  development_fee: string;
  examination_fee: string;
  caution_deposit_refundable: string;
  total_annual_fee: string;
  notes: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsFeeStructureCreateRequest {
  course_id?: string | null;
  program_name: string;
  program_code: string;
  academic_year?: string;
  admission_fee: string;
  tuition_fee_per_semester: string;
  development_fee: string;
  examination_fee: string;
  caution_deposit_refundable?: string;
  total_annual_fee: string;
  notes?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsScholarship {
  id: string;
  institute_id: string;
  title: string;
  category: string; // MERIT, WOMEN_IN_TECH, SPORTS, DEFENSE, NEED_BASED
  eligibility_criteria: string;
  benefit_summary: string;
  waiver_percentage: number;
  seats_available: number | null;
  validity_period: string;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsScholarshipCreateRequest {
  title: string;
  category: string;
  eligibility_criteria: string;
  benefit_summary: string;
  waiver_percentage?: number;
  seats_available?: number | null;
  validity_period?: string;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsAdmissionApplication {
  id: string;
  institute_id: string;
  application_number: string;
  applicant_name: string;
  email: string;
  phone: string;
  course_id: string | null;
  preferred_course_name: string;
  date_of_birth: string;
  gender: string;
  father_or_guardian_name: string;
  address_city: string;
  address_state: string;
  qualifying_exam: string;
  qualifying_percentage: number;
  entrance_exam_name: string | null;
  entrance_score_or_rank: string | null;
  status: string; // SUBMITTED, UNDER_REVIEW, DOCUMENTS_VERIFIED, PROVISIONAL_OFFER, CONFIRMED, REJECTED
  remarks: string | null;
  documents_uploaded: Array<{ document_type: string; file_name: string; file_url?: string; status: string }>;
  payment_status: string;
  payment_transaction_id: string | null;
  created_at: string;
}

export interface CmsAdmissionApplicationCreateRequest {
  applicant_name: string;
  email: string;
  phone: string;
  course_id?: string | null;
  preferred_course_name: string;
  date_of_birth: string;
  gender: string;
  father_or_guardian_name: string;
  address_city: string;
  address_state: string;
  qualifying_exam: string;
  qualifying_percentage: number;
  entrance_exam_name?: string | null;
  entrance_score_or_rank?: string | null;
}

export interface CmsAdmissionEnquiry {
  id: string;
  institute_id: string;
  full_name: string;
  email: string;
  phone: string;
  program_interest: string;
  city: string;
  message: string;
  status: string; // NEW, CONTACTED, COUNSELING_SCHEDULED, CONVERTED, CLOSED
  counselor_notes: string | null;
  created_at: string;
}

export interface CmsAdmissionEnquiryCreateRequest {
  full_name: string;
  email: string;
  phone: string;
  program_interest: string;
  city: string;
  message: string;
}

export interface PublicAdmissionBundle {
  steps: CmsAdmissionStep[];
  fee_structures: CmsFeeStructure[];
  scholarships: CmsScholarship[];
}


// ==========================================
// Phase 1 Module 6: Faculty & Staff CMS Types
// ==========================================

export interface CmsResearchPublication {
  id: string;
  faculty_id: string;
  title: string;
  journal_or_conference: string;
  publication_year: number;
  doi_or_url: string | null;
  citation_count: number;
  indexing: string;
  created_at: string;
}

export interface CmsResearchPublicationCreateRequest {
  title: string;
  journal_or_conference: string;
  publication_year: number;
  doi_or_url?: string | null;
  citation_count?: number;
  indexing?: string;
}

export interface CmsFacultyMemberSummary {
  id: string;
  institute_id: string;
  first_name: string;
  last_name: string;
  full_name: string;
  slug: string;
  department: string;
  designation: string;
  qualifications: string;
  specialization: string;
  email: string;
  phone: string | null;
  bio: string;
  avatar_url: string | null;
  google_scholar_url: string | null;
  orcid_id: string | null;
  linkedin_url: string | null;
  researchgate_url?: string | null;
  experience_years?: number;
  office_location?: string | null;
  research_interests?: string | null;
  teaching_courses?: string | null;
  total_citations: number;
  h_index: number;
  patents_count: number;
  is_head_of_department: boolean;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsFacultyMemberDetail extends CmsFacultyMemberSummary {
  publications: CmsResearchPublication[];
}

export interface CmsFacultyMemberCreateRequest {
  first_name: string;
  last_name: string;
  full_name: string;
  slug: string;
  department: string;
  designation: string;
  qualifications: string;
  specialization: string;
  email: string;
  phone?: string | null;
  bio: string;
  avatar_url?: string | null;
  google_scholar_url?: string | null;
  orcid_id?: string | null;
  linkedin_url?: string | null;
  researchgate_url?: string | null;
  experience_years?: number;
  office_location?: string | null;
  research_interests?: string | null;
  teaching_courses?: string | null;
  total_citations?: number;
  h_index?: number;
  patents_count?: number;
  is_head_of_department?: boolean;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsStaffMember {
  id: string;
  institute_id: string;
  full_name: string;
  division: string;
  designation: string;
  office_room_number: string;
  official_email: string;
  extension_number: string;
  visiting_hours: string;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsStaffMemberCreateRequest {
  full_name: string;
  division: string;
  designation: string;
  office_room_number: string;
  official_email: string;
  extension_number: string;
  visiting_hours?: string;
  display_order?: number;
  is_active?: boolean;
}

export interface PublicFacultyBundle {
  departments: string[];
  faculty: CmsFacultyMemberSummary[];
  total_faculty: number;
}

export interface PublicStaffBundle {
  divisions: string[];
  staff: CmsStaffMember[];
  total_staff: number;
}


// ==========================================
// Phase 1 Module 7: Placements & Recruiters CMS Types
// ==========================================

export interface CmsPlacementStat {
  id: string;
  institute_id: string;
  academic_year: string;
  highest_package_lpa: string;
  average_package_lpa: string;
  median_package_lpa: string;
  total_offers: number;
  placement_percentage: number;
  participating_companies: number;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsPlacementStatCreateRequest {
  academic_year: string;
  highest_package_lpa: string;
  average_package_lpa: string;
  median_package_lpa: string;
  total_offers: number;
  placement_percentage: number;
  participating_companies?: number;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsRecruiterPartner {
  id: string;
  institute_id: string;
  company_name: string;
  slug: string;
  sector: string; // IT & Software, Core Engineering, Management & Finance, Analytics & Consulting
  tier: string; // DAY_0, TIER_1, TIER_2, REGULAR
  highest_package_lpa: string | null;
  logo_url: string | null;
  website_url: string | null;
  headquarters: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsRecruiterPartnerCreateRequest {
  company_name: string;
  slug: string;
  sector: string;
  tier?: string;
  highest_package_lpa?: string | null;
  logo_url?: string | null;
  website_url?: string | null;
  headquarters?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsAlumniSuccessStory {
  id: string;
  institute_id: string;
  alumni_name: string;
  degree_program: string;
  graduation_year: number;
  company_name: string;
  designation: string;
  package_lpa: string;
  testimonial_quote: string;
  avatar_url: string | null;
  linkedin_url: string | null;
  video_story_url: string | null;
  is_featured: boolean;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsAlumniSuccessStoryCreateRequest {
  alumni_name: string;
  degree_program: string;
  graduation_year: number;
  company_name: string;
  designation: string;
  package_lpa: string;
  testimonial_quote: string;
  avatar_url?: string | null;
  linkedin_url?: string | null;
  video_story_url?: string | null;
  is_featured?: boolean;
  display_order?: number;
  is_active?: boolean;
}

export interface PublicPlacementsBundle {
  latest_stats: CmsPlacementStat | null;
  historical_stats: CmsPlacementStat[];
  top_recruiters: CmsRecruiterPartner[];
  featured_stories: CmsAlumniSuccessStory[];
  sectors: string[];
  total_companies: number;
  total_alumni_placed: number;
}


// ==========================================
// Phase 1 Module 8: Events, News & Notices Types
// ==========================================

export interface CmsEvent {
  id: string;
  institute_id: string;
  title: string;
  slug: string;
  category: string; // ACADEMIC, HACKATHON, CULTURAL, SPORTS, CONVOCATION
  start_date: string;
  end_date: string | null;
  time_window: string;
  venue: string;
  summary: string;
  registration_link: string | null;
  image_url: string | null;
  is_flagship: boolean;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsEventCreateRequest {
  title: string;
  slug: string;
  category: string;
  start_date: string;
  end_date?: string | null;
  time_window?: string;
  venue: string;
  summary: string;
  registration_link?: string | null;
  image_url?: string | null;
  is_flagship?: boolean;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsNewsArticle {
  id: string;
  institute_id: string;
  headline: string;
  slug: string;
  category: string;
  publish_date: string;
  summary: string;
  content: string;
  image_url: string | null;
  author_name: string;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsNewsArticleCreateRequest {
  headline: string;
  slug: string;
  category?: string;
  publish_date: string;
  summary: string;
  content: string;
  image_url?: string | null;
  author_name?: string;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsNoticeCircular {
  id: string;
  institute_id: string;
  circular_number: string;
  title: string;
  category: string; // EXAMINATION, ACADEMIC, FEE, HOLIDAY, EMERGENCY
  publish_date: string;
  description: string;
  document_pdf_url: string | null;
  is_urgent: boolean;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsNoticeCircularCreateRequest {
  circular_number: string;
  title: string;
  category: string;
  publish_date: string;
  description: string;
  document_pdf_url?: string | null;
  is_urgent?: boolean;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsAchievement {
  id: string;
  institute_id: string;
  title: string;
  category: string; // INSTITUTIONAL, FACULTY, STUDENT, SPORTS, RESEARCH
  awarding_body: string;
  award_year: string;
  description: string;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsAchievementCreateRequest {
  title: string;
  category: string;
  awarding_body: string;
  award_year: string;
  description: string;
  display_order?: number;
  is_active?: boolean;
}

export interface PublicEventsNewsBundle {
  events: CmsEvent[];
  flagship_events: CmsEvent[];
  news: CmsNewsArticle[];
  notices: CmsNoticeCircular[];
  achievements: CmsAchievement[];
  event_categories: string[];
}

// =========================================================================
// MODULE 9: GALLERY MANAGEMENT CMS TYPES
// =========================================================================
export interface CmsGalleryMedia {
  id: string;
  album_id: string;
  media_type: "IMAGE" | "VIDEO";
  title: string;
  caption?: string | null;
  url: string;
  thumbnail_url?: string | null;
  video_provider?: "YOUTUBE" | "VIMEO" | "SELF_HOSTED" | null;
  video_embed_id?: string | null;
  duration_seconds?: number | null;
  aspect_ratio?: string | null;
  tags?: string[] | null;
  display_order: number;
  is_cover: boolean;
  is_active: boolean;
  created_at: string;
}

export interface CmsGalleryAlbum {
  id: string;
  title: string;
  slug: string;
  category: string; // CAMPUS_LIFE, CONVOCATION, HACKATHON, SPORTS, CULTURAL, RESEARCH
  description: string;
  cover_image_url: string;
  academic_year: string;
  event_date?: string | null;
  item_count: number;
  is_featured: boolean;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsGalleryAlbumDetail extends CmsGalleryAlbum {
  media_items: CmsGalleryMedia[];
}

export interface PublicGalleryBundle {
  albums: CmsGalleryAlbum[];
  featured_albums: CmsGalleryAlbum[];
  recent_media: CmsGalleryMedia[];
  categories: string[];
  total_albums: number;
  total_photos: number;
  total_videos: number;
}

export interface CmsGalleryAlbumCreateRequest {
  title: string;
  slug: string;
  category: string;
  description: string;
  cover_image_url: string;
  academic_year?: string;
  event_date?: string | null;
  is_featured?: boolean;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsGalleryMediaCreateRequest {
  album_id: string;
  media_type?: "IMAGE" | "VIDEO";
  title: string;
  caption?: string | null;
  url: string;
  thumbnail_url?: string | null;
  video_provider?: string | null;
  video_embed_id?: string | null;
  duration_seconds?: number | null;
  aspect_ratio?: string | null;
  tags?: string[] | null;
  display_order?: number;
  is_cover?: boolean;
  is_active?: boolean;
}

// =========================================================================
// MODULE 10: DOWNLOADS CMS TYPES
// =========================================================================
export interface CmsDownloadDocument {
  id: string;
  category_id: string;
  institute_id: string;
  title: string;
  slug: string;
  description: string;
  target_audience: string; // ALL, PROSPECTIVE, STUDENTS, FACULTY
  applicable_program: string;
  academic_year: string;
  file_url: string;
  file_size_formatted: string;
  file_format: string; // PDF, DOCX, XLSX
  version: string;
  download_count: number;
  is_pinned: boolean;
  is_featured: boolean;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsDownloadCategory {
  id: string;
  institute_id: string;
  name: string;
  slug: string;
  description?: string | null;
  icon_name: string;
  display_order: number;
  is_active: boolean;
  document_count: number;
  created_at: string;
}

export interface CmsDownloadCategoryWithDocs extends CmsDownloadCategory {
  documents: CmsDownloadDocument[];
}

export interface PublicDownloadsBundle {
  categories: CmsDownloadCategoryWithDocs[];
  pinned_documents: CmsDownloadDocument[];
  featured_documents: CmsDownloadDocument[];
  total_documents: number;
  total_downloads: number;
}

export interface CmsDownloadCategoryCreateRequest {
  name: string;
  slug: string;
  description?: string | null;
  icon_name?: string;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsDownloadDocumentCreateRequest {
  category_id: string;
  title: string;
  slug: string;
  description: string;
  target_audience?: string;
  applicable_program?: string;
  academic_year?: string;
  file_url: string;
  file_size_formatted?: string;
  file_format?: string;
  version?: string;
  is_pinned?: boolean;
  is_featured?: boolean;
  display_order?: number;
  is_active?: boolean;
}

// =========================================================================
// MODULE 12: PLACEMENT CELL CMS TYPES
// =========================================================================
export interface CmsPlacementDrive {
  id: string;
  institute_id: string;
  company_name: string;
  slug: string;
  job_role: string;
  package_ctc: string;
  drive_date: string;
  registration_deadline: string;
  eligible_branches: string;
  selection_process: string;
  job_location: string;
  drive_status: "UPCOMING" | "ONGOING" | "COMPLETED";
  registration_link?: string | null;
  company_logo_url?: string | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsPlacementDriveCreateRequest {
  company_name: string;
  slug: string;
  job_role: string;
  package_ctc: string;
  drive_date: string;
  registration_deadline: string;
  eligible_branches: string;
  selection_process: string;
  job_location?: string;
  drive_status?: string;
  registration_link?: string | null;
  company_logo_url?: string | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsTrainingProgram {
  id: string;
  institute_id: string;
  title: string;
  slug: string;
  training_type: string;
  trainer_name: string;
  duration_weeks: number;
  start_date: string;
  end_date?: string | null;
  syllabus_highlights: string;
  batch_eligibility: string;
  mode: "OFFLINE" | "ONLINE" | "HYBRID";
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsTrainingProgramCreateRequest {
  title: string;
  slug: string;
  training_type: string;
  trainer_name: string;
  duration_weeks?: number;
  start_date: string;
  end_date?: string | null;
  syllabus_highlights: string;
  batch_eligibility?: string;
  mode?: string;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsInternshipOpportunity {
  id: string;
  institute_id: string;
  company_name: string;
  slug: string;
  role_title: string;
  stipend_monthly: string;
  duration_months: number;
  location: string;
  application_deadline: string;
  eligibility_criteria: string;
  apply_url: string;
  is_featured: boolean;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsInternshipOpportunityCreateRequest {
  company_name: string;
  slug: string;
  role_title: string;
  stipend_monthly: string;
  duration_months?: number;
  location?: string;
  application_deadline: string;
  eligibility_criteria: string;
  apply_url: string;
  is_featured?: boolean;
  display_order?: number;
  is_active?: boolean;
}

export interface PublicPlacementCellBundle {
  upcoming_drives: CmsPlacementDrive[];
  training_programs: CmsTrainingProgram[];
  internship_opportunities: CmsInternshipOpportunity[];
  top_recruiters: CmsRecruiterPartner[];
  latest_stats?: CmsPlacementStat | null;
  featured_stories: CmsAlumniSuccessStory[];
  total_drives: number;
  total_internships: number;
}

// =========================================================================
// MODULE 14: CONTACT & INQUIRY CMS TYPES
// =========================================================================
export interface CmsContactInquiry {
  id: string;
  institute_id: string;
  full_name: string;
  email: string;
  phone: string;
  subject: string;
  category: string; // ADMISSION, ACADEMIC, EXAMINATION, HOSTEL, FEE_FINANCE, GENERAL
  message: string;
  status: "NEW" | "IN_PROGRESS" | "RESPONDED" | "CLOSED";
  admin_notes?: string | null;
  responded_by_id?: string | null;
  responded_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface PublicContactInquiryCreateRequest {
  full_name: string;
  email: string;
  phone: string;
  subject: string;
  category?: string;
  message: string;
}

export interface CmsDepartmentContact {
  id: string;
  institute_id: string;
  department_name: string;
  slug: string;
  contact_person: string;
  email: string;
  phone_numbers: string;
  office_location: string;
  operating_hours: string;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface CmsDepartmentContactCreateRequest {
  department_name: string;
  slug: string;
  contact_person: string;
  email: string;
  phone_numbers: string;
  office_location: string;
  operating_hours?: string;
  display_order?: number;
  is_active?: boolean;
}

export interface CmsFaqItem {
  id: string;
  institute_id: string;
  category: string; // ADMISSION, ACADEMICS, EXAMINATIONS, CAMPUS_HOSTEL, FEES_SCHOLARSHIPS, GENERAL
  question: string;
  answer: string;
  display_order: number;
  is_featured: boolean;
  is_active: boolean;
  created_at: string;
}

export interface CmsFaqItemCreateRequest {
  category?: string;
  question: string;
  answer: string;
  display_order?: number;
  is_featured?: boolean;
  is_active?: boolean;
}

export interface CmsSupportFeedback {
  id: string;
  institute_id: string;
  user_type: string;
  name: string;
  email: string;
  feedback_type: string;
  description: string;
  rating_satisfaction: number;
  status: "OPEN" | "INVESTIGATING" | "RESOLVED";
  resolution_notes?: string | null;
  created_at: string;
}

export interface PublicSupportFeedbackCreateRequest {
  user_type?: string;
  name: string;
  email: string;
  feedback_type?: string;
  description: string;
  rating_satisfaction?: number;
}

export interface PublicContactBundle {
  departments: CmsDepartmentContact[];
  featured_faqs: CmsFaqItem[];
  all_faqs: CmsFaqItem[];
  faq_categories: string[];
  campus_address: string;
  campus_city: string;
  campus_state: string;
  campus_pincode: string;
  google_maps_embed_url: string;
  primary_email: string;
  admissions_hotline: string;
  emergency_contact: string;
}
