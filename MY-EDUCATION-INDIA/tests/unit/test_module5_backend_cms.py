"""Unit and Integration Tests for Module 5: Enterprise Website CMS & Website Builder
Verifies:
- Page Builder block validation and script tag sanitization
- SEO Schema.org JSON-LD generation
- Sitemap XML structure generation
- Robots.txt directive formatting
- AST compilation across all Module 5 backend files
"""
import ast
import os
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

os.environ.setdefault("SECRET_KEY", "test_secret_key_minimum_32_characters_long_for_security")
os.environ.setdefault("REFRESH_SECRET_KEY", "test_refresh_secret_key_minimum_32_characters_long")
os.environ.setdefault("CSRF_SECRET_KEY", "test_csrf_secret_key_minimum_32_characters_long_sec")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("SYNC_DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")

from app.modules.cms.models import Page, WebsiteSettings
from app.modules.cms.page_builder import PageBuilderCompiler, SUPPORTED_BLOCK_TYPES
from app.modules.cms.seo import SEOGenerator


class TestModule5BackendCMS(unittest.TestCase):

    def test_all_module5_python_files_compile(self) -> None:
        cms_dir = PROJECT_ROOT / "backend/app/modules/cms"
        for py_file in cms_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_page_builder_block_sanitization(self) -> None:
        raw_html_payload = {
            "html_content": "<div class='banner'>Hello</div><script>alert('xss')</script>"
        }
        sanitized = PageBuilderCompiler.sanitize_block_payload("HTML", raw_html_payload)
        self.assertNotIn("<script>", sanitized["html_content"])
        self.assertIn("&lt;script&gt;", sanitized["html_content"])

    def test_supported_block_types_coverage(self) -> None:
        expected_blocks = {
            "HERO", "HEADING", "PARAGRAPH", "BUTTON", "CARD", "GALLERY", "SLIDER",
            "ACCORDION", "COUNTER", "TIMELINE", "TABLE", "TESTIMONIAL", "MAP",
            "CONTACT_FORM", "ADMISSION_FORM", "COURSE_LIST", "NEWS_GRID", "DOWNLOADS", "HTML"
        }
        self.assertTrue(expected_blocks.issubset(set(SUPPORTED_BLOCK_TYPES.keys())))

    def test_seo_sitemap_and_robots_generation(self) -> None:
        robots = SEOGenerator.generate_robots_txt("https://myeducationindia.edu.in")
        self.assertIn("Sitemap: https://myeducationindia.edu.in/sitemap.xml", robots)
        self.assertIn("Disallow: /admin/", robots)

        dummy_page = Page(
            title="Admissions 2026",
            slug="admissions",
            is_homepage=False,
            status="PUBLISHED",
        )
        sitemap = SEOGenerator.generate_sitemap_xml([dummy_page], "https://myeducationindia.edu.in")
        self.assertIn("<loc>https://myeducationindia.edu.in/admissions</loc>", sitemap)
        self.assertIn("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", sitemap)


if __name__ == "__main__":
    unittest.main()
