# MY EDUCATION INDIA ERP V2 — MODULE 18 SPECIFICATION
## ENTERPRISE REPORTS, ANALYTICS & BUSINESS INTELLIGENCE (BI)

### 1. Executive Summary & Architectural Overview
Module 18 serves as the **Centralized Institutional Intelligence Engine and Reporting Platform** for MY EDUCATION INDIA ERP V2. Rather than each administrative subsystem implementing fragmented reporting silos, Module 18 unifies all 17 upstream ERP modules into a single cross-domain analytics warehouse and visual report designer.

#### Key Architectural Highlights
- **Single Source of Truth**: All modules (SIMS, Academics, Finance, Attendance, Examinations, CBT, Certificates, Library, LXP, CRM, and Integrations) route tabular facts and time-series metrics through Module 18.
- **Executive KPI Command Center**: Cross-institutional scorecard delivering real-time institutional health indices:
  $$	ext{Institute Health Score} = (	ext{Attendance}\% 	imes 0.25) + (	ext{Fee Collection}\% 	imes 0.35) + (	ext{Exam Pass}\% 	imes 0.25) + (	ext{Lead Conversion}\% 	imes 0.15)$$
- **Zero-Code Drag & Drop Report Builder (`report_engine.py`)**: Enables administrators to compose complex custom tabular and pivot reports with calculated columns, joins, grouping, and aggregations (SUM, AVG, COUNT, MIN, MAX) without SQL knowledge.
- **Apache ECharts Visualization Studio (`chart_engine.py`)**: Native declarative configuration for 14 chart styles: Bar, Line, Area, Pie, Donut, Stacked Bar, Radar, Scatter, Heatmap, Gauge, Funnel, Treemap, and Timelines.
- **Automated Report Scheduler**: Cron-based scheduled report generation (Daily, Weekly, Monthly, Quarterly, Yearly) with automated dispatches via Module 16 Communication Center (Email, WhatsApp).
- **Universal Multi-Format Export Center (`export_engine.py`)**: Instant exports to PDF, Excel (.xlsx), CSV, Word (.docx), and JSON, including password-protected confidential ledgers.
- **Infrastructure & Cluster Health Monitor (`system_health.py`)**: Real-time telemetry for PostgreSQL query latency, background queue workers, notification brokers, and storage pools.
- **Zero Client-Side Storage**: 100% compliant with zero usage of `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 2. Database Schema (14 Enterprise Relational Tables)
Provisioned via Alembic revision `0018_bi_platform`:
1. `report_definitions`: Report catalog, source tables, selected fields, filter predicates, aggregations, and access permissions.
2. `report_templates`: Pre-built statutory and operational templates (Tabular, Pivot, Summary, Executive Brief).
3. `report_schedules`: Cron triggers, frequency rules, export formats, and recipient distribution lists.
4. `saved_reports`: Versioned snapshot instances with cached row counts and execution timestamps.
5. `dashboard_widgets`: Modular metric cards, KPI gauges, chart containers, and data query pointers.
6. `dashboard_layouts`: User-customized grid tile positions for Executive, Academic, and Financial viewports.
7. `kpi_definitions`: Formula-based objectives, target values, warning thresholds, critical thresholds, and trend arrows.
8. `analytics_snapshots`: Time-series rollups across Enrollment, Revenue, Attendance, and Academic Performance.
9. `system_health_logs`: Infrastructure telemetry capturing component status, latency in milliseconds, and error rates.
10. `audit_reports`: Statutory audit trail of report access, exports, schedules, and user IP addresses.
11. `export_history`: Download history, file sizes, row counts, and password-protection status flags.
12. `chart_definitions`: Reusable Apache ECharts options configurations and visual styling themes.
13. `widget_settings`: Viewport positioning coordinates (X, Y, Width, Height) and visibility flags.
14. `bi_settings`: Caching durations, query execution limits, pre-aggregation schedules, and fiscal calendar alignments.

---

### 3. Business Logic & Calculation Engines
- **Universal Report Query Engine (`report_engine.py`)**:
  - In-memory multi-predicate filtering (`==`, `!=`, `>`, `<`, `in`).
  - Aggregation calculations (`SUM`, `AVG`, `COUNT`, `MAX`, `MIN`).
- **Predictive Analytics & Health Score Engine (`analytics_engine.py`)**:
  - Moving average trend forecasting across custom window intervals.
  - Institutional composite health score calculation (0–100 scale).
- **Apache ECharts Option Builder (`chart_engine.py`)**:
  - Declarative generation of Apache ECharts options for Bar, Pie, Gauge, Radar, and Heatmap series.
- **KPI Evaluation Engine (`kpi_engine.py`)**:
  - Multi-tier threshold status classifier: `NORMAL` (Safe), `WARNING` (Amber Alert), `CRITICAL` (Action Required).
- **Data Export Engine (`export_engine.py`)**:
  - Streaming tabular conversion for CSV and structured JSON records.

---

### 4. Frontend & Navigation Architecture
- **Path**: `frontend/src/modules/bi/`
- **13 Submodules Delivered**:
  - `dashboard/ExecutiveDashboardPage.tsx`: Executive command center (₹8.45 Cr Revenue, 1,420 Admissions, 91.5% Attendance, 94.8% Pass Rate, 92.4 Health Score).
  - `reports/ReportsDirectoryPage.tsx`: Centralized report master with statutory templates and saved queries.
  - `report-builder/ReportBuilderPage.tsx`: Visual drag & drop report builder with multi-table field selection.
  - `charts/ChartStudioPage.tsx`: Apache ECharts visualization lab with 14 chart formats.
  - `analytics/CrossModuleAnalyticsPage.tsx`: Longitudinal trend lines, moving averages, and cross-module correlations.
  - `widgets/DashboardWidgetsPage.tsx`: Widget gallery and viewport layout customizer.
  - `kpis/KpiManagementPage.tsx`: Strategic KPI formula engine with status thresholds.
  - `exports/ExportCenterPage.tsx`: Multi-format export hub (PDF, Excel, CSV, DOCX, JSON).
  - `system-health/SystemHealthDashboardPage.tsx`: Infrastructure cluster health monitor for DB, workers, and queues.
  - `audit/AuditReportsPage.tsx`: Statutory audit trail of report access and exports.
  - `settings/BiSettingsPage.tsx`: Cache duration settings and query quotas.
  - `types/bi.types.ts` & `services/biService.ts`: TypeScript contracts and HTTP API client.
- **Routing**: Mounted under `/admin/bi/*` in `AppRoutes.tsx` with navigation item `Reports & BI` (`PieChart` icon).

---

### 5. Verification & Testing
- Unit test suite `tests/unit/test_module18_backend_bi.py` executed with 100% pass rate:
  - Clean AST syntax across all 14 Python files in `backend/app/modules/bi/`.
  - Pydantic schema validation for reports, schedules, KPIs, and chart definitions.
  - Chart type validation across all 12 formats, export format validation, and cron syntax checks.
  - UniversalReportQueryEngine in-memory filtering and field aggregation calculations.
  - Moving average trend forecasting and composite institutional health score computation.
  - Apache ECharts option builder for bar and pie series.
  - Data export CSV formatting and KPI status threshold evaluation (`NORMAL`, `WARNING`, `CRITICAL`).
  - Zero browser storage audit: 0 instances of `localStorage`, `sessionStorage`, or `indexedDB`.
