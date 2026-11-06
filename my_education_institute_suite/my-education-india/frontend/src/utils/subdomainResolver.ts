export type EnterprisePortalSubdomain =
  | "admin"
  | "website"
  | "student"
  | "teacher"
  | "parent"
  | "exam"
  | "cbt"
  | "fees"
  | "attendance"
  | "certificate"
  | "library"
  | "lms"
  | "communication"
  | "api";

const VALID_SUBDOMAINS: ReadonlySet<EnterprisePortalSubdomain> = new Set([
  "admin",
  "website",
  "student",
  "teacher",
  "parent",
  "exam",
  "cbt",
  "fees",
  "attendance",
  "certificate",
  "library",
  "lms",
  "communication",
  "api",
]);

export function resolveCurrentSubdomain(): EnterprisePortalSubdomain {
  const hostname = window.location.hostname.toLowerCase();
  const segments = hostname.split(".");
  if (segments.length >= 3) {
    const candidate = segments[0] as EnterprisePortalSubdomain;
    if (VALID_SUBDOMAINS.has(candidate)) {
      return candidate;
    }
  }
  return "admin";
}
