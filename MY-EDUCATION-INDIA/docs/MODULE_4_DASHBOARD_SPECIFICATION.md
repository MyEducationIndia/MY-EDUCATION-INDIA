# MY EDUCATION INDIA ERP V2
# MODULE 4: ENTERPRISE ADMIN DASHBOARD & CONTROL CENTER SPECIFICATION

## 1. Architectural Scope & Objectives

Module 4 establishes the **Enterprise Admin Dashboard & Control Center** for **MY EDUCATION INDIA ERP V2**. Designed as the nerve center for the entire institutional platform, it provides real-time observability, global entity search, notification management, live activity streaming, multi-campus switching, and dynamic widget customization.

### Key Capabilities:
- **Zero Hardcoded Data**: 100% of statistical indicators, time-series chart coordinates, activity logs, notifications, and health metrics load directly from PostgreSQL via versioned `/api/v1/dashboard/` APIs.
- **Top Header & Switchers**: Instant campus context switching (Institute Switcher, Branch Switcher, Academic Year Selector), global search trigger (`⌘K`), notification bell with unread counters, profile card, visual theme switcher (Light / Dark mode), and quick action buttons.
- **Global Multi-Entity Search (`/api/v1/dashboard/search`)**: High-speed unified search across Users/Students, Regional Branches, and Universal Number Generators with instant keyboard navigation and target routing.
- **20+ Live KPI Metric Cards**: Students (Total, Active), Admissions (Today, Month), Faculty, Courses, Batches, Branches, Fee Collections (Today, Month, Pending), Attendance %, Exams, Certificates, Website Visitors, and Omnichannel Dispatches (SMS, WhatsApp, Email).
- **Time-Series Analytics Engine**: Interactive SVG chart widgets supporting `DAILY` (hourly slots), `WEEKLY` (7-day slots), `MONTHLY` (30-day sampled slots), and `YEARLY` (12-month fiscal slots) for Admissions, Fee Collections, Student Attendance %, Student Growth, Course Popularity distributions, Branch Comparisons, and Communication channel breakdown.
- **Notification Center Drawer**: Categorized notification inbox (`SYSTEM`, `FEE_DUE`, `ADMISSION`, `EXAM`, `ATTENDANCE`, `BACKUP`, `SERVER`, `SMS`, `WHATSAPP`, `EMAIL`) with `is_read` status mutation and mark-all-as-read endpoints.
- **Live Enterprise Activity Timeline**: Real-time event log tracking authentication milestones, branch provisioning, fee collections, and system updates.
- **System Health Monitor**: Live server telemetry tracking database status, API gateway status, server time, process uptime, memory consumption, CPU utilization, and application release version.
- **Mobile-First & Accessible Responsive Design**: Fluid layout adapting across mobile smartphones, tablets, laptops, and ultra-wide desktop monitors with zero horizontal scroll and high-contrast WCAG 2.1 compliance.

---

## 2. Database Schema (PostgreSQL 16+ via Alembic Migration `0004_module4_dashboard_control_center.py`)

| Table Name | Entity Class | Architectural Role & Attributes |
| :--- | :--- | :--- |
| `notifications` | `Notification` | Institutional and user-directed alerts with `title`, `message`, `category`, `priority` (`LOW`, `NORMAL`, `HIGH`, `CRITICAL`), `action_url`, `is_read`, `read_at`, and JSONB `meta_data`. |
| `dashboard_widgets` | `DashboardWidget` | Per-user configurable widget registry storing `widget_key`, `category`, `grid_position`, `grid_width` (1 to 12 columns), `grid_height`, `is_visible`, `is_pinned`, and widget configuration JSONB. |
| `user_pinned_modules` | `UserPinnedModule` | User sidebar shortcuts and pinned favorite modules. |
| `dashboard_activities`| `DashboardActivity` | High-value domain event log storing `actor_name`, `action_type`, `entity_type`, `entity_id`, `summary`, and `detail_payload`. |

---

## 3. Backend Implementation (`backend/app/modules/dashboard/`)

```
backend/app/modules/dashboard/
├── __init__.py
├── models.py         # SQLAlchemy 2.x Mapped models (Notification, DashboardWidget, DashboardActivity, UserPinnedModule)
├── schemas.py        # Pydantic v2 schemas for KPIs, charts, global search, notifications, activities, health
├── statistics.py     # StatisticsAggregationEngine computing 20+ live KPI metrics from PostgreSQL
├── analytics.py      # DashboardAnalyticsEngine generating DAILY, WEEKLY, MONTHLY, and YEARLY time-series
├── notifications.py  # NotificationService managing notification dispatch, inbox retrieval, and read status
├── repository.py     # DashboardRepository executing async queries and global multi-entity searches
├── service.py        # DashboardService orchestrating role-based widget layouts, search, and health metrics
└── router.py         # API router for /api/v1/dashboard/ endpoints
```

---

## 4. Frontend Implementation (`frontend/src/modules/dashboard/`)

```
frontend/src/modules/dashboard/
├── types/
│   └── dashboard.types.ts           # Strict TypeScript interfaces for KPIs, charts, search, and health
├── api/
│   └── dashboardApi.ts              # Axios API functions communicating with /api/v1/dashboard/
├── services/
│   └── dashboardService.ts          # Reactive dashboard service
├── components/
│   ├── GlobalSearchModal.tsx        # Global search modal with real-time entity grouping and keyboard navigation
│   ├── NotificationCenterDrawer.tsx # Slide-out notification drawer with mark-as-read and filter actions
│   ├── QuickActionsBar.tsx          # 8 one-click shortcut actions (Add Student, Collect Fees, Backup, etc.)
│   ├── ActivityTimelineWidget.tsx   # Live stream of administrative events with timestamps
│   └── SystemHealthWidget.tsx       # Live status indicators (PostgreSQL, API, Memory, CPU, Uptime)
├── widgets/
│   └── KPIStatisticsCards.tsx       # 12 primary KPI metric tiles in a responsive grid
├── charts/
│   └── InteractiveAnalyticsCharts.tsx # Visual bar & distribution charts with DAILY/WEEKLY/MONTHLY/YEARLY granularity switching
└── pages/
    └── EnterpriseAdminDashboardPage.tsx # Master Control Center layout integrating all components
```

---

## 5. Automated Verification & Testing

The enterprise test suite in `tests/unit/test_module4_backend_dashboard.py` along with Modules 1–3 tests verifies:
1. 100% clean AST compilation across all backend Python modules.
2. Analytics time-series generator producing correct bucket lengths across `DAILY` (12 hourly slots), `WEEKLY` (7 daily slots), `MONTHLY` (10 sampled slots), and `YEARLY` (12 fiscal month slots).
3. Pydantic validation schemas verifying KPI metrics and system health structures.
4. Zero usage of `localStorage`, `sessionStorage`, or `indexedDB` in any frontend source file.
5. All 18 automated enterprise unit tests passing (`OK`).
