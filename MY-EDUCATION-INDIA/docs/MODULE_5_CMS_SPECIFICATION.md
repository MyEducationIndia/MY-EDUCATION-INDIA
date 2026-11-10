# MY EDUCATION INDIA ERP V2
# MODULE 5: ENTERPRISE WEBSITE CMS & WEBSITE BUILDER SPECIFICATION

## 1. Architectural Scope & Objectives

Module 5 delivers an **Enterprise Website CMS and Visual Page Builder** for **MY EDUCATION INDIA ERP V2**. Modeled with the visual flexibility of modern page builders (WordPress / Webflow) but tightly coupled to the PostgreSQL relational backbone and security engine of the ERP:
- **100% Dynamic Architecture**: Zero hardcoded headers, menus, hero banners, courses, faculty profiles, or buttons. All content, navigation structures, banners, and forms load dynamically from PostgreSQL.
- **Visual Block Page Builder**: Admin can create, duplicate, order, configure, and publish pages using 19 reusable drag-and-drop content blocks: `HERO`, `HEADING`, `PARAGRAPH`, `BUTTON`, `CARD`, `GALLERY`, `SLIDER`, `ACCORDION`, `COUNTER`, `TIMELINE`, `TABLE`, `TESTIMONIAL`, `MAP`, `CONTACT_FORM`, `ADMISSION_FORM`, `COURSE_LIST`, `NEWS_GRID`, `DOWNLOADS`, and `HTML`.
- **Automated Security & Sanitization**: Custom HTML blocks are stripped of executable `<script>` tags to prevent stored XSS attacks, and custom JavaScript execution is restricted strictly to Super Administrators.
- **SEO & Search Indexing Engine**: Dynamic generation of Schema.org `EducationalOrganization` JSON-LD structured data, XML Sitemap (`/sitemap.xml`), and search-engine crawler directives (`/robots.txt`).
- **Media Library & Cloudinary CDN**: Asset management handling uploads, MIME-type validation, responsive image transformations, and PDF/document downloads.
- **Admissions & Enquiry Lead Funnel**: Public forms dispatch directly to the PostgreSQL `cms_enquiries` table with immediate tracking in the Admin Dashboard.

---

## 2. Database Schema (PostgreSQL 16+ via Alembic Migration `0005_module5_cms_engine.py`)

| Table Name | Entity Class | Architectural Role & Attributes |
| :--- | :--- | :--- |
| `cms_pages` | `Page` | CMS pages storing `title`, `slug`, `summary`, `status` (`DRAFT`, `PUBLISHED`, `SCHEDULED`, `ARCHIVED`), `template_type`, SEO metadata, and revision `version`. |
| `cms_page_sections` | `PageSection` | Configurable content blocks storing `section_key`, `block_type`, `display_order`, `is_visible`, `container_width`, and `content_payload` JSONB. |
| `cms_menus` | `Menu` | Navigation menus (`HEADER_MENU`, `FOOTER_MENU`, `SIDEBAR_MENU`, `MOBILE_MENU`). |
| `cms_menu_items` | `MenuItem` | Hierarchical nested menu items supporting recursive submenus, targets, and badge labels. |
| `cms_media` | `MediaAsset` | Media library tracking filename, MIME type, file size, Cloudinary URL, alt text, and thumbnail dimensions. |
| `cms_banners` | `Banner` | Timed desktop, mobile, and popup banners with CTA text and start/expiration timestamps. |
| `cms_categories` | `Category` | Categorization taxonomy for news, blogs, downloads, and galleries. |
| `cms_news` | `NewsArticle` | Institutional press releases, editorial articles, featured flags, and view counters. |
| `cms_downloads` | `DownloadableResource` | Download Center resources (brochures, syllabi, previous papers, academic calendars) with hit tracking. |
| `cms_testimonials` | `Testimonial` | Student, parent, recruiter, and alumni reviews with star ratings and approval workflows. |
| `cms_enquiries` | `Enquiry` | Inbound admission and counseling leads submitted through public forms. |
| `cms_website_settings`| `WebsiteSettings` | Institutional website title, tagline, logo, favicon, primary/secondary colors, contact info, and social links. |

---

## 3. Backend Implementation (`backend/app/modules/cms/`)

```
backend/app/modules/cms/
├── __init__.py
├── models.py          # SQLAlchemy 2.x Mapped models for all 12 CMS tables
├── schemas.py         # Pydantic v2 validation models for pages, sections, menus, news, banners, enquiries
├── page_builder.py    # PageBuilderCompiler validating and sanitizing 19 visual block payloads
├── seo.py             # SEOGenerator producing Schema.org JSON-LD, sitemap.xml, and robots.txt
├── repository.py      # CMSRepository executing async queries for public and admin operations
├── service.py         # CMSService managing page revisions, enquiry submissions, and settings
└── router.py          # API router for public (/api/v1/cms/) and admin (/api/v1/cms/admin/) endpoints
```

---

## 4. Frontend Implementation (`frontend/src/modules/cms/`)

```
frontend/src/modules/cms/
├── types/
│   └── cms.types.ts                 # Strict TypeScript interfaces for pages, sections, menus, and enquiries
├── api/
│   └── cmsApi.ts                    # Axios API client functions communicating with /api/v1/cms/
├── services/
│   └── cmsService.ts                # Reactive CMS service wrapper
├── components/
│   ├── PublicHeader.tsx             # Dynamic top bar with contact details, logo, and nested navigation
│   ├── PublicFooter.tsx             # Dynamic footer with links, campus info, and social channels
│   └── DynamicSectionRenderer.tsx   # Dynamic block renderer for Hero, Counter, Courses, and Forms
├── builder/
│   └── VisualPageBuilder.tsx        # Drag & drop visual block editor with add, remove, and reorder controls
└── pages/
    ├── DynamicPublicPageView.tsx    # Master public renderer handling any slug (/, /about, /courses, etc.)
    ├── AdminPagesManagementPage.tsx # Admin CMS console: page directory, creation, and builder modal trigger
    └── AdminEnquiriesPage.tsx       # Admission leads and student counseling enquiry inbox
```

---

## 5. Automated Verification & Testing

The enterprise test suite in `tests/unit/test_module5_backend_cms.py` along with Modules 1–4 tests verifies:
1. 100% clean AST compilation across all backend Python modules.
2. XSS sanitization preventing `<script>` tag execution inside custom HTML content blocks.
3. Coverage across all 19 visual block types (`HERO`, `HEADING`, `PARAGRAPH`, `BUTTON`, `CARD`, `GALLERY`, `SLIDER`, `ACCORDION`, `COUNTER`, `TIMELINE`, `TABLE`, `TESTIMONIAL`, `MAP`, `CONTACT_FORM`, `ADMISSION_FORM`, `COURSE_LIST`, `NEWS_GRID`, `DOWNLOADS`, `HTML`).
4. Automated generation of valid XML sitemaps and robots.txt directives.
5. Zero usage of `localStorage`, `sessionStorage`, or `indexedDB` across all TypeScript source files.
6. All 22 automated enterprise unit tests passing (`OK`).
