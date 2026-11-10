# MY EDUCATION INDIA – Root Owner Sovereign Operations Manual

**Role:** Sovereign Platform Root Owner  
**Authority Level:** Tier-0 Sovereign Authority (Above Super Admin)  
**Campus Scope:** Autonomous Campus `MEI-HQ`, Indore, Madhya Pradesh

---

## 1. Feature Control Center (Master Switch)

The Feature Control Center (`/root/feature-control`) gives the Root Owner sovereign capability to enable, disable, hide, or restrict any of the 85 platform features across 6 categories without modifying code or redeploying.

### Operational Controls Supported Per Feature:
* **Master Enable/Disable:** Completely turns the feature on or off globally.
* **Hide / Show:** Hides the navigation menu item and direct links while maintaining API access for testing.
* **Maintenance Mode:** Renders an informative maintenance banner for users attempting to access the page or endpoint.
* **Read-Only Mode:** Prevents mutations (POST, PUT, DELETE) while allowing GET requests for audit or archival.
* **Role Restrictions:** Whitelists specific role sets allowed to access the feature (e.g. only `ROOT_ADMIN` or `FACULTY`).
* **Institute Scoping:** Scopes features to specific multi-tenant campus nodes (default: `MEI-HQ`).

### Dependency Safety Protection:
The platform evaluates prerequisite dependency trees before toggling:
* *Example:* If the Root Owner attempts to disable **Question Bank** (`cbt_question_bank`), the system flags that **Exam Paper Builder** (`cbt_exam_builder`) and **Live Exam Engine** (`cbt_exam_engine`) depend on it.
* An interactive modal warns the operator before any disruption occurs.

---

## 2. Login Security & Authentication Governance

* **Strict Single Auth Vector:** The platform enforces User ID + Password exclusively.
* **Prohibited Methods:** Email login, mobile/SMS login, OTP authentication, Social logins (Google, Microsoft, GitHub), and Magic links are permanently removed.
* **Password Policy:** Configure minimum/maximum lengths (default: 10–64 characters), uppercase, lowercase, numeric, and special character mandates, 90-day expiry intervals, and 5-password history depth.
* **Configurable "Forgot Password":** The public self-service forgot password toggle is disabled by default in the security policy.

---

## 3. Session Management & Sovereign System Lockdown

### Session Lifecycle Management:
* **Session Max Timeout:** 60 minutes default.
* **Idle Timeout:** 15 minutes default.
* **Concurrent Device Limit:** 1 device per User ID.
* **Single Device Login:** When a user logs in from a new workstation, any prior active session is automatically terminated.

### System Lockdown Master Switches:
In the event of an institutional emergency or infrastructure maintenance:
1. **Disable Entire Platform:** 1-click global kill switch that freezes all public and internal web access.
2. **Disable Logins:** Disallows all non-Root user authentications while keeping active sessions read-only.
3. **Allow Only Super Admin / Maintenance:** Restricts platform access strictly to authorized DevOps engineers.
4. **Emergency Mode:** Broadcasts a persistent campus alert banner across all portals.
5. **Lockdown Message Broadcast:** Allows the Root Owner to broadcast real-time instructions to campus users.

---

## 4. Immutable Append-Only Audit Trail

Every feature modification, security policy update, system lockdown toggle, and administrator password reset is committed to an immutable append-only ledger in PostgreSQL:
* **Audit Metadata Captured:** Audit ID, target feature/user, administrator ID, previous value snapshot (JSONB), new value snapshot (JSONB), IP address, device user-agent, mandatory justification, and ISO-8601 timestamp.
* **Immutability:** Audit records cannot be modified or deleted through any API or administrative screen.
