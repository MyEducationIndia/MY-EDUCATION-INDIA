from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.models.schemas import (
    CmsUpdate, TestimonialCreate, FaqCreate, BlogCreate, EnquiryCreate, NewsletterSubscribe
)
from typing import Dict

router = APIRouter(prefix="/cms", tags=["Website CMS & Dynamic Content"])

@router.get("/config")
def get_cms_config():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT key, value FROM cms_content")
        rows = cur.fetchall()
        return {r["key"]: r["value"] for r in rows}

@router.put("/config")
def update_cms_config(cfg: CmsUpdate):
    with get_db() as conn:
        cur = conn.cursor()
        for k, v in cfg.settings.items():
            cur.execute("INSERT OR REPLACE INTO cms_content (key, value) VALUES (?, ?)", (k, v))
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', 'Updated Master Website CMS Configuration', 'CMS')")
        return {"status": "success", "message": "CMS configuration updated live."}

# Testimonials
@router.get("/testimonials")
def list_testimonials():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM testimonials ORDER BY id DESC")
        return [dict(r) for r in cur.fetchall()]

@router.post("/testimonials", status_code=201)
def add_testimonial(t: TestimonialCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO testimonials (name, course, quote, rating) VALUES (?, ?, ?, ?)", (t.name, t.course, t.quote, t.rating))
        return {"status": "success", "id": cur.lastrowid}

@router.delete("/testimonials/{id}")
def delete_testimonial(id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM testimonials WHERE id = ?", (id,))
        return {"status": "success"}

# FAQs
@router.get("/faqs")
def list_faqs():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM faqs ORDER BY id ASC")
        return [dict(r) for r in cur.fetchall()]

@router.post("/faqs", status_code=201)
def add_faq(f: FaqCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO faqs (question, answer, category) VALUES (?, ?, ?)", (f.question, f.answer, f.category))
        return {"status": "success", "id": cur.lastrowid}

@router.delete("/faqs/{id}")
def delete_faq(id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM faqs WHERE id = ?", (id,))
        return {"status": "success"}

# Gallery
@router.get("/gallery")
def list_gallery():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM gallery ORDER BY id ASC")
        return [dict(r) for r in cur.fetchall()]

# Blogs
@router.get("/blogs")
def list_blogs():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM blogs ORDER BY id DESC")
        return [dict(r) for r in cur.fetchall()]

@router.post("/blogs", status_code=201)
def add_blog(b: BlogCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO blogs (title, slug, author, category, summary, content, read_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (b.title, b.slug, b.author, b.category, b.summary, b.content, b.read_time))
        return {"status": "success", "id": cur.lastrowid}

# Enquiries
@router.post("/enquiries", status_code=201)
def submit_enquiry(e: EnquiryCreate):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO enquiries (name, phone, email, course_interest, message)
            VALUES (?, ?, ?, ?, ?)
        """, (e.name, e.phone, e.email, e.course_interest, e.message))
        return {"status": "success", "message": "Inquiry recorded. Counselor will call back shortly."}

@router.get("/enquiries")
def list_enquiries():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM enquiries ORDER BY id DESC")
        return [dict(r) for r in cur.fetchall()]

# Newsletter
@router.post("/newsletter", status_code=201)
def subscribe_newsletter(n: NewsletterSubscribe):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO newsletter_subscribers (email) VALUES (?)", (n.email,))
        return {"status": "success", "message": "Subscribed to academic alerts!"}
