export interface PageSectionItem {
  id?: string;
  section_key: string;
  block_type: string;
  display_order: number;
  is_visible: boolean;
  container_width: "BOXED" | "FULL_WIDTH";
  background_color?: string | null;
  background_image_url?: string | null;
  padding_top: number;
  padding_bottom: number;
  content_payload: Record<string, any>;
}

export interface DynamicPageItem {
  id: string;
  institute_id: string;
  title: string;
  slug: string;
  summary?: string | null;
  featured_image_url?: string | null;
  status: "DRAFT" | "PUBLISHED" | "SCHEDULED" | "ARCHIVED";
  published_at?: string | null;
  is_homepage: boolean;
  template_type: string;
  meta_title?: string | null;
  meta_description?: string | null;
  meta_keywords?: string | null;
  view_count: number;
  version: number;
  sections: PageSectionItem[];
  created_at: string;
  updated_at: string;
}

export interface MenuItemNode {
  id: string;
  menu_id: string;
  title: string;
  url: string;
  target: string;
  icon_name?: string | null;
  badge_label?: string | null;
  display_order: number;
  is_active: boolean;
  children: MenuItemNode[];
}

export interface MenuStructure {
  id: string;
  institute_id: string;
  code: string;
  name: string;
  location: string;
  is_active: boolean;
  items: MenuItemNode[];
}

export interface MediaItem {
  id: string;
  filename: string;
  original_filename: string;
  file_type: string;
  mime_type: string;
  file_size_bytes: number;
  url: string;
  thumbnail_url?: string | null;
  alt_text?: string | null;
  created_at: string;
}

export interface BannerItem {
  id: string;
  title: string;
  subtitle?: string | null;
  banner_type: string;
  image_url: string;
  mobile_image_url?: string | null;
  cta_text?: string | null;
  cta_url?: string | null;
  display_order: number;
  is_active: boolean;
}

export interface NewsItem {
  id: string;
  title: string;
  slug: string;
  content: string;
  excerpt?: string | null;
  author_name: string;
  featured_image_url?: string | null;
  is_featured: boolean;
  is_trending: boolean;
  published_at: string;
  view_count: number;
}

export interface TestimonialItem {
  id: string;
  author_name: string;
  author_role: string;
  avatar_url?: string | null;
  content: string;
  rating_stars: number;
  company_or_course?: string | null;
}

export interface DownloadItem {
  id: string;
  title: string;
  resource_type: string;
  file_url: string;
  file_size_formatted: string;
  download_count: number;
}

export interface EnquiryRecord {
  id: string;
  full_name: string;
  email: string;
  phone_number: string;
  enquiry_type: string;
  course_interested?: string | null;
  message: string;
  status: string;
  created_at: string;
}

export interface WebsiteSettingsRecord {
  id: string;
  website_title: string;
  tagline: string;
  logo_url?: string | null;
  favicon_url?: string | null;
  primary_color: string;
  secondary_color: string;
  contact_phone: string;
  contact_email: string;
  whatsapp_number?: string | null;
  address_display: string;
  social_links: Record<string, string>;
  footer_text: string;
}
