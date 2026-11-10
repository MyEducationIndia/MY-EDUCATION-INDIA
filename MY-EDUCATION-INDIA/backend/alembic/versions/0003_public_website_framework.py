"""Alembic migration for Phase 1 Module 1: Public Website Foundation
Adds:
- website_settings
- website_themes
- website_ticker_items
- website_navigation_menus
- website_social_links
- website_search_index

Revision ID: 0003_public_website_framework
Revises: 0002_module2_enterprise_auth
Create Date: 2026-11-07 10:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0003_public_website_framework"
down_revision: Union[str, None] = "0002_module2_enterprise_auth"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. website_settings
    op.create_table(
        "website_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("site_title", sa.String(length=255), nullable=False, server_default="MY EDUCATION INDIA"),
        sa.Column("tagline", sa.String(length=500), nullable=False, server_default="National Flagship Higher Education Institution"),
        sa.Column("header_logo_url", sa.Text(), nullable=True),
        sa.Column("footer_logo_url", sa.Text(), nullable=True),
        sa.Column("favicon_url", sa.Text(), nullable=True),
        sa.Column("header_is_sticky", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("header_show_search", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("header_show_login", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("header_login_button_text", sa.String(length=64), nullable=False, server_default="Login"),
        sa.Column("header_login_route", sa.String(length=128), nullable=False, server_default="/login"),
        sa.Column("contact_phone", sa.String(length=64), nullable=False, server_default="+91 731 245 6789"),
        sa.Column("contact_email", sa.String(length=255), nullable=False, server_default="info@myeducation.in"),
        sa.Column("contact_address", sa.String(length=500), nullable=False, server_default="Campus Square, Institutional Sector, Indore, MP 452001"),
        sa.Column("meta_description", sa.Text(), nullable=False, server_default="Official Portal of MY EDUCATION INDIA. Autonomous Higher Education & Research Campus."),
        sa.Column("meta_keywords", sa.Text(), nullable=False, server_default="education, university, indore, degrees, cbt, admissions"),
        sa.Column("og_image_url", sa.Text(), nullable=True),
        sa.Column("google_analytics_id", sa.String(length=64), nullable=True),
        sa.Column("is_maintenance_mode", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("maintenance_message", sa.Text(), nullable=True),
        sa.Column("custom_css", sa.Text(), nullable=True),
        sa.Column("custom_head_scripts", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_website_settings_institute_id"), "website_settings", ["institute_id"], unique=True)

    # 2. website_themes
    op.create_table(
        "website_themes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("primary_color", sa.String(length=32), nullable=False, server_default="#1E40AF"),
        sa.Column("secondary_color", sa.String(length=32), nullable=False, server_default="#0D9488"),
        sa.Column("accent_color", sa.String(length=32), nullable=False, server_default="#F59E0B"),
        sa.Column("background_color", sa.String(length=32), nullable=False, server_default="#F8FAFC"),
        sa.Column("surface_color", sa.String(length=32), nullable=False, server_default="#FFFFFF"),
        sa.Column("text_primary_color", sa.String(length=32), nullable=False, server_default="#0F172A"),
        sa.Column("text_secondary_color", sa.String(length=32), nullable=False, server_default="#475569"),
        sa.Column("font_family", sa.String(length=64), nullable=False, server_default="Inter, system-ui, sans-serif"),
        sa.Column("heading_font_family", sa.String(length=64), nullable=False, server_default="Inter, system-ui, sans-serif"),
        sa.Column("border_radius", sa.String(length=32), nullable=False, server_default="0.75rem"),
        sa.Column("button_style", sa.String(length=32), nullable=False, server_default="rounded"),
        sa.Column("shadow_style", sa.String(length=32), nullable=False, server_default="soft"),
        sa.Column("animation_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_website_themes_institute_id"), "website_themes", ["institute_id"], unique=True)

    # 3. website_ticker_items
    op.create_table(
        "website_ticker_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="Important Notice"),
        sa.Column("link_url", sa.String(length=500), nullable=True),
        sa.Column("is_external", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("open_new_tab", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_emergency", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("priority_level", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("publish_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expire_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_website_ticker_items_institute_id"), "website_ticker_items", ["institute_id"], unique=False)

    # 4. website_navigation_menus
    op.create_table(
        "website_navigation_menus",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("menu_location", sa.String(length=64), nullable=False, server_default="HEADER_MAIN"),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("path", sa.String(length=255), nullable=False),
        sa.Column("icon_name", sa.String(length=64), nullable=True),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("website_navigation_menus.id", ondelete="CASCADE"), nullable=True),
        sa.Column("is_external", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("open_new_tab", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_mega_menu", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_website_navigation_menus_institute_id"), "website_navigation_menus", ["institute_id"], unique=False)
    op.create_index(op.f("ix_website_navigation_menus_parent_id"), "website_navigation_menus", ["parent_id"], unique=False)
    op.create_index(op.f("ix_website_navigation_menus_menu_location"), "website_navigation_menus", ["menu_location"], unique=False)

    # 5. website_social_links
    op.create_table(
        "website_social_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_website_social_links_institute_id"), "website_social_links", ["institute_id"], unique=False)

    # 6. website_search_index
    op.create_table(
        "website_search_index",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("keywords", sa.Text(), nullable=True),
        sa.Column("target_url", sa.String(length=500), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_website_search_index_institute_id"), "website_search_index", ["institute_id"], unique=False)
    op.create_index(op.f("ix_website_search_index_entity_type"), "website_search_index", ["entity_type"], unique=False)
    op.create_index(op.f("ix_website_search_index_title"), "website_search_index", ["title"], unique=False)


def downgrade() -> None:
    op.drop_table("website_search_index")
    op.drop_table("website_social_links")
    op.drop_table("website_navigation_menus")
    op.drop_table("website_ticker_items")
    op.drop_table("website_themes")
    op.drop_table("website_settings")
