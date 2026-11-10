"""Alembic migration for Module 5: Enterprise Website CMS & Website Builder
Creates:
- cms_pages
- cms_page_sections
- cms_menus
- cms_menu_items
- cms_media
- cms_banners
- cms_categories
- cms_tags
- cms_news
- cms_blogs
- cms_albums
- cms_gallery
- cms_downloads
- cms_testimonials
- cms_events
- cms_enquiries
- cms_website_settings

Revision ID: 0005_module5_cms_engine
Revises: 0004_module4_dashboard_control_center
Create Date: 2026-11-06 12:55:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0005_module5_cms_engine"
down_revision: Union[str, None] = "0004_module4_dashboard_control_center"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. cms_pages table
    op.create_table(
        "cms_pages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        sa.Column("featured_image_url", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="DRAFT"),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduled_publish_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_homepage", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("template_type", sa.String(length=64), nullable=False, server_default="DEFAULT"),
        sa.Column("custom_css", sa.Text(), nullable=True),
        sa.Column("custom_js", sa.Text(), nullable=True),
        sa.Column("meta_title", sa.String(length=200), nullable=True),
        sa.Column("meta_description", sa.String(length=500), nullable=True),
        sa.Column("meta_keywords", sa.String(length=500), nullable=True),
        sa.Column("canonical_url", sa.String(length=255), nullable=True),
        sa.Column("og_image_url", sa.Text(), nullable=True),
        sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("slug", "institute_id", name="uq_pages_slug_institute"),
    )
    op.create_index(op.f("ix_cms_pages_slug"), "cms_pages", ["slug"])
    op.create_index(op.f("ix_cms_pages_institute_id"), "cms_pages", ["institute_id"])

    # 2. cms_page_sections table
    op.create_table(
        "cms_page_sections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("page_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cms_pages.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_key", sa.String(length=80), nullable=False),
        sa.Column("block_type", sa.String(length=64), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_visible", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("container_width", sa.String(length=32), nullable=False, server_default="BOXED"),
        sa.Column("background_color", sa.String(length=32), nullable=True),
        sa.Column("background_image_url", sa.Text(), nullable=True),
        sa.Column("padding_top", sa.Integer(), nullable=False, server_default="40"),
        sa.Column("padding_bottom", sa.Integer(), nullable=False, server_default="40"),
        sa.Column("content_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cms_page_sections_page_id"), "cms_page_sections", ["page_id"])

    # 3. cms_menus table
    op.create_table(
        "cms_menus",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("location", sa.String(length=64), nullable=False, server_default="HEADER"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code", "institute_id", name="uq_menus_code_institute"),
    )

    # 4. cms_menu_items table
    op.create_table(
        "cms_menu_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("menu_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cms_menus.id", ondelete="CASCADE"), nullable=False),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cms_menu_items.id", ondelete="CASCADE"), nullable=True),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("url", sa.String(length=255), nullable=False),
        sa.Column("target", sa.String(length=16), nullable=False, server_default="_self"),
        sa.Column("icon_name", sa.String(length=64), nullable=True),
        sa.Column("badge_label", sa.String(length=32), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. cms_media table
    op.create_table(
        "cms_media",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("folder_path", sa.String(length=255), nullable=False, server_default="/"),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("file_type", sa.String(length=32), nullable=False),
        sa.Column("mime_type", sa.String(length=100), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("thumbnail_url", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.String(length=255), nullable=True),
        sa.Column("caption", sa.String(length=500), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. cms_banners table
    op.create_table(
        "cms_banners",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("subtitle", sa.String(length=500), nullable=True),
        sa.Column("banner_type", sa.String(length=64), nullable=False, server_default="DESKTOP"),
        sa.Column("image_url", sa.Text(), nullable=False),
        sa.Column("mobile_image_url", sa.Text(), nullable=True),
        sa.Column("cta_text", sa.String(length=64), nullable=True),
        sa.Column("cta_url", sa.String(length=255), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. cms_categories table
    op.create_table(
        "cms_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category_type", sa.String(length=64), nullable=False, server_default="NEWS"),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("slug", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("slug", "category_type", "institute_id", name="uq_categories_slug_type_inst"),
    )

    # 8. cms_news table
    op.create_table(
        "cms_news",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("excerpt", sa.String(length=500), nullable=True),
        sa.Column("author_name", sa.String(length=120), nullable=False, server_default="Editorial Team"),
        sa.Column("featured_image_url", sa.Text(), nullable=True),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cms_categories.id", ondelete="SET NULL"), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_trending", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PUBLISHED"),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("meta_title", sa.String(length=200), nullable=True),
        sa.Column("meta_description", sa.String(length=500), nullable=True),
        sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("slug", "institute_id", name="uq_news_slug_inst"),
    )

    # 9. cms_downloads table
    op.create_table(
        "cms_downloads",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=False),
        sa.Column("file_url", sa.Text(), nullable=False),
        sa.Column("file_size_formatted", sa.String(length=32), nullable=False, server_default="1.2 MB"),
        sa.Column("download_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    
    # 11. cms_enquiries table
    op.create_table(
        "cms_enquiries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id", ondelete="SET NULL"), nullable=True),
        sa.Column("enquiry_type", sa.String(length=64), nullable=False, server_default="GENERAL"),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.Column("course_interested", sa.String(length=150), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="NEW"),
        sa.Column("source_channel", sa.String(length=64), nullable=False, server_default="WEBSITE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. cms_website_settings table
    op.create_table(
        "cms_website_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("website_title", sa.String(length=200), nullable=False, server_default="MY EDUCATION INDIA"),
        sa.Column("tagline", sa.String(length=300), nullable=False, server_default="Premier Educational Institute & Assessment Center"),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.Column("favicon_url", sa.Text(), nullable=True),
        sa.Column("primary_color", sa.String(length=7), nullable=False, server_default="#1D4ED8"),
        sa.Column("secondary_color", sa.String(length=7), nullable=False, server_default="#0D9488"),
        sa.Column("contact_phone", sa.String(length=32), nullable=False, server_default="+91 755 2400000"),
        sa.Column("contact_email", sa.String(length=255), nullable=False, server_default="contact@myeducationindia.edu.in"),
        sa.Column("whatsapp_number", sa.String(length=32), nullable=True, server_default="+919999999999"),
        sa.Column("address_display", sa.String(length=300), nullable=False, server_default="Main Institutional Area, Bhopal, MP 462011"),
        sa.Column("social_links", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("footer_text", sa.String(length=500), nullable=False, server_default="© 2026 MY EDUCATION INDIA. All rights reserved."),
        sa.Column("analytics_tracking_code", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("institute_id", name="uq_website_settings_inst"),
    )


def downgrade() -> None:
    op.drop_table("cms_website_settings")
    op.drop_table("cms_enquiries")
    op.drop_table("cms_downloads")
    op.drop_table("cms_news")
    op.drop_table("cms_categories")
    op.drop_table("cms_banners")
    op.drop_table("cms_media")
    op.drop_table("cms_menu_items")
    op.drop_table("cms_menus")
    op.drop_table("cms_page_sections")
    op.drop_table("cms_pages")
