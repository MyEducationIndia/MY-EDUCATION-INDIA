# MY EDUCATION INDIA ERP V2 — FOLDER STRUCTURE GUIDE

```text
my-education-india/
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/               # 20 Alembic schema migrations (0001 - 0020)
│   ├── app/
│   │   ├── api/v1/                 # Master REST API router mounting all 20 modules
│   │   ├── auth/                   # Password hashing, JWT lifecycle, security
│   │   ├── core/                   # Global configuration, exceptions, error handlers
│   │   ├── db/                     # Base SQLAlchemy models, async session engine
│   │   ├── middleware/             # Rate limiting, CSRF, security headers
│   │   ├── models/                 # Core relational database entities
│   │   ├── modules/                # Domain-driven modular monolith packages (Modules 1-20)
│   │   ├── permissions/            # RBAC catalog and permission dependencies
│   │   └── services/               # Shared cross-cutting application services
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/                    # Axios HTTP client with interceptors
│   │   ├── components/             # Reusable UI widgets, navigation sidebar, badges
│   │   ├── layouts/                # SuperAdminLayout and role portal layouts
│   │   ├── modules/                # Domain-specific frontend views for all 20 modules
│   │   ├── routes/                 # AppRoutes.tsx routing tree
│   │   ├── store/                  # In-memory authentication and session state
│   │   └── types/                  # TypeScript interface contracts
│   ├── package.json
│   └── vite.config.ts
├── docs/                           # 9 Comprehensive Enterprise Documentation Guides
├── scripts/                        # Production bootstrap seed and backup automation scripts
└── tests/unit/                     # Unit test suites covering all 20 modules
```
