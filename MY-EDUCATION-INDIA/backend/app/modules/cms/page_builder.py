from typing import Any, Dict, List
from app.modules.cms.models import Page, PageSection

SUPPORTED_BLOCK_TYPES = {
    "HERO": "Full-width hero banner with title, CTA buttons, and background asset",
    "HEADING": "SEO-friendly declarative heading (H1-H6)",
    "PARAGRAPH": "Rich formatted text paragraph",
    "BUTTON": "Interactive primary or secondary action link",
    "CARD": "Card container with image, header, and badge",
    "GALLERY": "Responsive image grid with lightbox support",
    "SLIDER": "Auto-playing carousel slider",
    "ACCORDION": "Collapsible FAQ or syllabus section",
    "COUNTER": "Animated statistical metric counter",
    "TIMELINE": "Chronological history or event milestone stream",
    "TABLE": "Tabular fee schedule or curriculum table",
    "TESTIMONIAL": "Student, parent, and recruiter review block",
    "MAP": "Embedded interactive campus map",
    "CONTACT_FORM": "Direct enquiry and callback request form",
    "ADMISSION_FORM": "Online student registration and intake form",
    "COURSE_LIST": "Dynamic grid of available academic programs",
    "NEWS_GRID": "Dynamic press release and announcements stream",
    "DOWNLOADS": "Direct syllabus, timetable, and prospectus download cards",
    "HTML": "Sanitized custom HTML markup block",
}


class PageBuilderCompiler:
    """Validates and compiles visual page builder blocks into dynamic frontend structures."""

    @staticmethod
    def sanitize_block_payload(block_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = payload.copy()
        # Prevent arbitrary script execution in standard HTML blocks
        if block_type == "HTML" and "html_content" in cleaned:
            content = str(cleaned["html_content"])
            # Remove dangerous script tags for safety
            content = content.replace("<script", "&lt;script").replace("</script>", "&lt;/script&gt;")
            cleaned["html_content"] = content
        return cleaned

    @staticmethod
    def build_default_homepage_sections(page_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "section_key": "hero_primary",
                "block_type": "HERO",
                "display_order": 0,
                "container_width": "FULL_WIDTH",
                "content_payload": {
                    "heading": "Empowering India's Next Generation of Leaders",
                    "subheading": "Admissions Open for Academic Session 2026-27 across Engineering, Management, Healthcare & Computing.",
                    "primary_cta_text": "Apply for Admission",
                    "primary_cta_url": "/admissions",
                    "secondary_cta_text": "Explore Courses",
                    "secondary_cta_url": "/courses",
                    "badge_text": "NAAC A++ Accredited • 100% Placement Record",
                },
            },
            {
                "section_key": "metrics_counter",
                "block_type": "COUNTER",
                "display_order": 1,
                "container_width": "BOXED",
                "content_payload": {
                    "counters": [
                        {"label": "Enrolled Scholars", "value": "15,000+"},
                        {"label": "Placement Ratio", "value": "98.4%"},
                        {"label": "Corporate Recruiters", "value": "350+"},
                        {"label": "National Awards", "value": "42+"},
                    ]
                },
            },
            {
                "section_key": "featured_courses",
                "block_type": "COURSE_LIST",
                "display_order": 2,
                "container_width": "BOXED",
                "content_payload": {
                    "title": "Popular Academic Disciplines",
                    "subtitle": "Industry-aligned curricula with hands-on lab infrastructure",
                },
            },
            {
                "section_key": "quick_admission_enquiry",
                "block_type": "ADMISSION_FORM",
                "display_order": 3,
                "container_width": "BOXED",
                "content_payload": {
                    "form_title": "Take the First Step: Request Academic Counseling",
                    "enquiry_type": "ADMISSION",
                },
            },
        ]
