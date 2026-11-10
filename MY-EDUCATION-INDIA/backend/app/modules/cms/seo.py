from typing import Any, Dict, List
from app.modules.cms.models import Page, WebsiteSettings


class SEOGenerator:
    """Generates Schema.org JSON-LD, OpenGraph, Twitter Cards, Sitemap, and Robots.txt."""

    @staticmethod
    def generate_schema_org_jsonld(page: Page, settings: WebsiteSettings) -> Dict[str, Any]:
        return {
            "@context": "https://schema.org",
            "@type": "EducationalOrganization",
            "name": settings.website_title,
            "description": settings.tagline,
            "url": f"https://myeducationindia.edu.in/{page.slug if not page.is_homepage else ''}",
            "logo": settings.logo_url or "https://res.cloudinary.com/mei/logo.png",
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": settings.contact_phone,
                "contactType": "Admissions & Student Helpline",
                "areaServed": "IN",
                "availableLanguage": ["English", "Hindi"],
            },
            "sameAs": list(settings.social_links.values()) if settings.social_links else [],
        }

    @staticmethod
    def generate_sitemap_xml(pages: List[Page], base_url: str = "https://myeducationindia.edu.in") -> str:
        xml_entries = []
        for p in pages:
            loc = base_url if p.is_homepage else f"{base_url}/{p.slug}"
            lastmod = p.updated_at.strftime("%Y-%m-%d")
            xml_entries.append(
                f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{'1.0' if p.is_homepage else '0.8'}</priority>\n  </url>"
            )

        return (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
            + "\n".join(xml_entries)
            + "\n</urlset>"
        )

    @staticmethod
    def generate_robots_txt(base_url: str = "https://myeducationindia.edu.in") -> str:
        return (
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /admin/\n"
            "Disallow: /api/\n"
            f"Sitemap: {base_url}/sitemap.xml\n"
        )
