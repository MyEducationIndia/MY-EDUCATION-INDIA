import json
import time
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.core.security import get_current_user_optional
from app.models.entities import (
    Advertisement,
    AuditLog,
    BlogPost,
    CMSContent,
    CustomSection,
    Enquiry,
    FAQ,
    GalleryItem,
    NewsletterSubscriber,
    PublicDocument,
    SharedInstitutionalState,
    Testimonial,
    WebsiteSection,
)
from app.models.schemas import (
    AdvertisementCreate,
    AdvertisementUpdate,
    BlogCreate,
    BlogUpdate,
    CmsUpdate,
    CustomSectionCreate,
    CustomSectionUpdate,
    EnquiryCreate,
    EnquiryUpdate,
    FaqCreate,
    FaqUpdate,
    GalleryCreate,
    GalleryUpdate,
    NewsletterSubscribe,
    PublicDocumentCreate,
    PublicDocumentUpdate,
    SectionOrderUpdate,
    TestimonialCreate,
    TestimonialUpdate,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/cms", tags=["Website CMS & Dynamic Content"])


@router.get("/config")
def get_cms_config(db: Session = Depends(get_db)):
    try:
        rows = db.query(CMSContent).all()
        config_map = {r.key: r.value for r in rows}
        shared_row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if shared_row and shared_row.state_json:
            try:
                parsed = json.loads(shared_row.state_json)
                if isinstance(parsed.get("cms"), dict):
                    for k, v in parsed["cms"].items():
                        if k not in config_map and isinstance(v, (str, int, float, bool)):
                            config_map[k] = str(v)
            except Exception:
                pass
        return config_map
    except Exception as exc:
        logger.error("Failed to retrieve CMS config: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve CMS configuration.")


@router.put("/config")
def update_cms_config(
    cfg: CmsUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    if not cfg.settings or not isinstance(cfg.settings, dict):
        raise HTTPException(status_code=400, detail="CMS settings payload cannot be empty.")
    try:
        actor = str(current_user.get("sub", "admin")) if current_user else "admin"
        updated_items = []
        for k, v in cfg.settings.items():
            item = db.query(CMSContent).filter(CMSContent.key == str(k)).first()
            if item:
                item.value = str(v)
                db.add(item)
                updated_items.append(item)
            else:
                new_item = CMSContent(key=str(k), value=str(v))
                db.add(new_item)
                updated_items.append(new_item)

        # Synchronize with SharedInstitutionalState so all devices and reloads see the exact same CMS data
        shared_row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if shared_row and shared_row.state_json:
            try:
                state_obj = json.loads(shared_row.state_json)
                if not isinstance(state_obj.get("cms"), dict):
                    state_obj["cms"] = {}
                for k, v in cfg.settings.items():
                    if v == "true":
                        state_obj["cms"][k] = True
                    elif v == "false":
                        state_obj["cms"][k] = False
                    else:
                        state_obj["cms"][k] = v
                shared_row.state_json = json.dumps(state_obj, default=str)
                db.add(shared_row)
            except Exception as sync_exc:
                logger.warning("Could not sync CMS config into shared state: %s", sync_exc)

        db.add(AuditLog(actor=actor, action="Updated Master Website CMS Configuration", module="CMS"))
        db.commit()
        for item in updated_items:
            db.refresh(item)
        if shared_row:
            db.refresh(shared_row)

        fresh_rows = db.query(CMSContent).all()
        fresh_config = {r.key: r.value for r in fresh_rows}
        return {
            "status": "success",
            "message": "CMS configuration updated and committed to PostgreSQL.",
            "config": fresh_config,
        }
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update CMS config: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to update CMS config: {str(exc)}")


@router.patch("/config")
def patch_cms_config(
    cfg: CmsUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    return update_cms_config(cfg, db, current_user)


@router.get("/seo")
def get_seo_settings(db: Session = Depends(get_db)):
    seo_keys = ["seoMetaTitle", "seoMetaDescription", "seoKeywords", "ogImageUrl", "googleSiteVerification"]
    rows = db.query(CMSContent).filter(CMSContent.key.in_(seo_keys)).all()
    return {r.key: r.value for r in rows}


@router.put("/seo")
def update_seo_settings(cfg: Dict[str, str], db: Session = Depends(get_db)):
    try:
        items = []
        for k, v in cfg.items():
            item = db.query(CMSContent).filter(CMSContent.key == str(k)).first()
            if item:
                item.value = str(v)
                db.add(item)
                items.append(item)
            else:
                new_item = CMSContent(key=str(k), value=str(v))
                db.add(new_item)
                items.append(new_item)
        db.add(AuditLog(actor="admin", action="Updated Website SEO Metadata", module="SEO"))
        db.commit()
        for it in items:
            db.refresh(it)
        return {"status": "success", "message": "SEO metadata updated.", "seo": {it.key: it.value for it in items}}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update SEO: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to update SEO: {str(exc)}")


@router.get("/sections")
def get_website_sections(db: Session = Depends(get_db)):
    try:
        secs = db.query(WebsiteSection).order_by(WebsiteSection.display_order.asc(), WebsiteSection.id.asc()).all()
        return [
            {
                "id": s.id,
                "label": s.label,
                "icon": s.icon,
                "visible": bool(s.visible),
                "display_order": s.display_order,
            }
            for s in secs
        ]
    except Exception as exc:
        logger.error("Failed to get website sections: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve website sections.")


@router.put("/sections")
def update_website_sections(order_data: SectionOrderUpdate, db: Session = Depends(get_db)):
    try:
        updated_secs = []
        for item in order_data.sections:
            sec = db.query(WebsiteSection).filter(WebsiteSection.id == item.id).first()
            if sec:
                if item.label:
                    sec.label = item.label
                if item.icon:
                    sec.icon = item.icon
                sec.visible = 1 if item.visible else 0
                sec.display_order = item.display_order
                db.add(sec)
                updated_secs.append(sec)
            else:
                new_sec = WebsiteSection(
                    id=item.id,
                    label=item.label or item.id,
                    icon=item.icon or "fa-puzzle-piece",
                    visible=1 if item.visible else 0,
                    display_order=item.display_order,
                )
                db.add(new_sec)
                updated_secs.append(new_sec)
        db.add(AuditLog(actor="admin", action="Rearranged Public Website Sections", module="CMS"))
        db.commit()
        for s in updated_secs:
            db.refresh(s)
        return {"status": "success", "message": "Website sections arrangement saved to PostgreSQL."}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update website sections: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to save section order: {str(exc)}")


@router.get("/custom-sections")
def list_custom_sections(db: Session = Depends(get_db)):
    try:
        secs = db.query(CustomSection).order_by(CustomSection.display_order.asc(), CustomSection.id.asc()).all()
        return [
            {
                "id": s.id,
                "badge": s.badge,
                "title": s.title,
                "subtitle": s.subtitle,
                "content": s.content,
                "cta_text": s.cta_text,
                "cta_action": s.cta_action,
                "theme": s.theme,
                "image_url": s.image_url,
                "visible": bool(s.visible),
                "display_order": s.display_order,
            }
            for s in secs
        ]
    except Exception as exc:
        logger.error("Failed to list custom sections: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve custom sections.")


@router.post("/custom-sections", status_code=201)
def add_custom_section(c: CustomSectionCreate, db: Session = Depends(get_db)):
    try:
        sec_id = c.id or f"CUST-SEC-{int(time.time() * 1000) % 100000}"
        new_sec = CustomSection(
            id=sec_id,
            badge=c.badge or "",
            title=c.title,
            subtitle=c.subtitle or "",
            content=c.content or "",
            cta_text=c.cta_text or "",
            cta_action=c.cta_action or "",
            theme=c.theme or "gradient-indigo",
            image_url=c.image_url or "",
            visible=1 if c.visible else 0,
            display_order=c.display_order or 0,
        )
        db.add(new_sec)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Created custom section [{sec_id}] {c.title}", module="CMS"))
        db.commit()
        db.refresh(new_sec)
        return {"status": "success", "id": new_sec.id, "title": new_sec.title}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create custom section: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create custom section: {str(exc)}")


@router.put("/custom-sections/{section_id}")
def update_custom_section(section_id: str, c: CustomSectionUpdate, db: Session = Depends(get_db)):
    try:
        sec = db.query(CustomSection).filter(CustomSection.id == section_id).first()
        if not sec:
            raise HTTPException(status_code=404, detail="Custom section not found.")
        for field, val in c.model_dump(exclude_unset=True).items():
            if val is not None:
                if field == "visible":
                    sec.visible = 1 if val else 0
                else:
                    setattr(sec, field, val)
        db.add(sec)
        db.commit()
        db.refresh(sec)
        return {"status": "success", "message": "Custom section updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update custom section %s: %s", section_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update custom section: {str(exc)}")


@router.delete("/custom-sections/{section_id}")
def delete_custom_section(section_id: str, db: Session = Depends(get_db)):
    try:
        sec = db.query(CustomSection).filter(CustomSection.id == section_id).first()
        if not sec:
            raise HTTPException(status_code=404, detail="Custom section not found.")
        db.delete(sec)
        db.add(AuditLog(actor="admin", action=f"Deleted custom section [{section_id}]", module="CMS"))
        db.commit()
        return {"status": "success", "message": "Custom section removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete custom section %s: %s", section_id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete custom section: {str(exc)}")


@router.get("/testimonials")
def list_testimonials(db: Session = Depends(get_db)):
    try:
        items = db.query(Testimonial).order_by(Testimonial.id.desc()).all()
        return [
            {
                "id": t.id,
                "name": t.name,
                "course": t.course,
                "quote": t.quote,
                "rating": t.rating,
                "is_featured": t.is_featured,
                "created_at": (t.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(t.created_at, "strftime") else str(t.created_at)) if t.created_at else None,
            }
            for t in items
        ]
    except Exception as exc:
        logger.error("Failed to list testimonials: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve testimonials.")


@router.post("/testimonials", status_code=201)
def add_testimonial(t: TestimonialCreate, db: Session = Depends(get_db)):
    try:
        new_t = Testimonial(name=t.name, course=t.course, quote=t.quote, rating=t.rating or 5)
        db.add(new_t)
        db.flush()
        db.commit()
        db.refresh(new_t)
        return {"status": "success", "id": new_t.id}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to add testimonial: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to add testimonial: {str(exc)}")


@router.put("/testimonials/{id}")
def update_testimonial(id: int, t: TestimonialUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(Testimonial).filter(Testimonial.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Testimonial not found.")
        for field, val in t.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(item, field, val)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"status": "success", "message": "Testimonial updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update testimonial %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update testimonial: {str(exc)}")


@router.delete("/testimonials/{id}")
def delete_testimonial(id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(Testimonial).filter(Testimonial.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Testimonial not found.")
        db.delete(item)
        db.commit()
        return {"status": "success", "message": "Testimonial removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete testimonial %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete testimonial: {str(exc)}")


@router.get("/faqs")
def list_faqs(db: Session = Depends(get_db)):
    try:
        items = db.query(FAQ).order_by(FAQ.display_order.asc(), FAQ.id.asc()).all()
        return [
            {
                "id": f.id,
                "question": f.question,
                "answer": f.answer,
                "category": f.category,
                "display_order": f.display_order,
                "created_at": (f.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(f.created_at, "strftime") else str(f.created_at)) if f.created_at else None,
            }
            for f in items
        ]
    except Exception as exc:
        logger.error("Failed to list FAQs: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve FAQs.")


@router.post("/faqs", status_code=201)
def add_faq(f: FaqCreate, db: Session = Depends(get_db)):
    try:
        new_f = FAQ(
            question=f.question,
            answer=f.answer,
            category=f.category or "General",
            display_order=f.display_order or 0,
        )
        db.add(new_f)
        db.flush()
        db.commit()
        db.refresh(new_f)
        return {"status": "success", "id": new_f.id}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to add FAQ: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to add FAQ: {str(exc)}")


@router.put("/faqs/{id}")
def update_faq(id: int, f: FaqUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(FAQ).filter(FAQ.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="FAQ not found.")
        for field, val in f.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(item, field, val)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"status": "success", "message": "FAQ updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update FAQ %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update FAQ: {str(exc)}")


@router.delete("/faqs/{id}")
def delete_faq(id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(FAQ).filter(FAQ.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="FAQ not found.")
        db.delete(item)
        db.commit()
        return {"status": "success", "message": "FAQ removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete FAQ %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete FAQ: {str(exc)}")


@router.get("/gallery")
def list_gallery(db: Session = Depends(get_db)):
    try:
        items = db.query(GalleryItem).order_by(GalleryItem.id.asc()).all()
        return [
            {
                "id": g.id,
                "title": g.title,
                "category": g.category,
                "image_url": g.image_url,
                "created_at": (g.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(g.created_at, "strftime") else str(g.created_at)) if g.created_at else None,
            }
            for g in items
        ]
    except Exception as exc:
        logger.error("Failed to list gallery: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve gallery.")


@router.post("/gallery", status_code=201)
def add_gallery(g: GalleryCreate, db: Session = Depends(get_db)):
    try:
        new_g = GalleryItem(title=g.title, category=g.category, image_url=g.image_url)
        db.add(new_g)
        db.flush()
        db.commit()
        db.refresh(new_g)
        return {"status": "success", "id": new_g.id}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to add gallery item: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to add gallery item: {str(exc)}")


@router.put("/gallery/{id}")
def update_gallery(id: int, g: GalleryUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(GalleryItem).filter(GalleryItem.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Gallery item not found.")
        for field, val in g.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(item, field, val)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"status": "success", "message": "Gallery item updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update gallery item %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update gallery item: {str(exc)}")


@router.delete("/gallery/{id}")
def delete_gallery(id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(GalleryItem).filter(GalleryItem.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Gallery item not found.")
        db.delete(item)
        db.commit()
        return {"status": "success", "message": "Gallery item removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete gallery item %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete gallery item: {str(exc)}")


@router.get("/blogs")
def list_blogs(db: Session = Depends(get_db)):
    try:
        items = db.query(BlogPost).order_by(BlogPost.id.desc()).all()
        return [
            {
                "id": b.id,
                "title": b.title,
                "slug": b.slug,
                "author": b.author,
                "category": b.category,
                "summary": b.summary,
                "content": b.content,
                "read_time": b.read_time,
                "published_at": (b.published_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(b.published_at, "strftime") else str(b.published_at)) if b.published_at else None,
            }
            for b in items
        ]
    except Exception as exc:
        logger.error("Failed to list blogs: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve news articles.")


@router.post("/blogs", status_code=201)
def add_blog(b: BlogCreate, db: Session = Depends(get_db)):
    try:
        new_b = BlogPost(
            title=b.title,
            slug=b.slug,
            author=b.author,
            category=b.category,
            summary=b.summary,
            content=b.content,
            read_time=b.read_time or "5 min read",
        )
        db.add(new_b)
        db.flush()
        db.commit()
        db.refresh(new_b)
        return {"status": "success", "id": new_b.id, "title": b.title}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to add blog: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create blog post: {str(exc)}")


@router.put("/blogs/{id}")
def update_blog(id: int, b: BlogUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(BlogPost).filter(BlogPost.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Blog post not found.")
        for field, val in b.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(item, field, val)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"status": "success", "message": "Blog post updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update blog %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update blog post: {str(exc)}")


@router.delete("/blogs/{id}")
def delete_blog(id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(BlogPost).filter(BlogPost.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Blog post not found.")
        db.delete(item)
        db.commit()
        return {"status": "success", "message": "Blog post removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete blog %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete blog post: {str(exc)}")


@router.post("/enquiries", status_code=201)
def submit_enquiry(e: EnquiryCreate, db: Session = Depends(get_db)):
    try:
        new_e = Enquiry(
            name=e.name,
            phone=e.phone,
            email=e.email,
            course_interest=e.course_interest,
            message=e.message,
            status="New",
        )
        db.add(new_e)
        db.flush()
        db.commit()
        db.refresh(new_e)
        return {"status": "success", "id": new_e.id, "message": "Inquiry recorded. Counselor will call back shortly."}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to submit enquiry: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to record enquiry: {str(exc)}")


@router.get("/enquiries")
def list_enquiries(db: Session = Depends(get_db)):
    try:
        items = db.query(Enquiry).order_by(Enquiry.id.desc()).all()
        return [
            {
                "id": enq.id,
                "name": enq.name,
                "phone": enq.phone,
                "email": enq.email,
                "course_interest": enq.course_interest,
                "message": enq.message,
                "status": enq.status,
                "created_at": (enq.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(enq.created_at, "strftime") else str(enq.created_at)) if enq.created_at else None,
            }
            for enq in items
        ]
    except Exception as exc:
        logger.error("Failed to list enquiries: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve enquiries.")


@router.put("/enquiries/{id}")
def update_enquiry(id: int, e: EnquiryUpdate, db: Session = Depends(get_db)):
    try:
        enq = db.query(Enquiry).filter(Enquiry.id == id).first()
        if not enq:
            raise HTTPException(status_code=404, detail="Enquiry not found.")
        for field, val in e.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(enq, field, val)
        db.add(enq)
        db.commit()
        db.refresh(enq)
        return {"status": "success", "message": "Enquiry updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update enquiry %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update enquiry: {str(exc)}")


@router.delete("/enquiries/{id}")
def delete_enquiry(id: int, db: Session = Depends(get_db)):
    try:
        enq = db.query(Enquiry).filter(Enquiry.id == id).first()
        if not enq:
            raise HTTPException(status_code=404, detail="Enquiry not found.")
        db.delete(enq)
        db.commit()
        return {"status": "success", "message": "Enquiry deleted."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete enquiry %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete enquiry: {str(exc)}")


@router.post("/newsletter", status_code=201)
def subscribe_newsletter(n: NewsletterSubscribe, db: Session = Depends(get_db)):
    try:
        existing = db.query(NewsletterSubscriber).filter(NewsletterSubscriber.email == n.email).first()
        if not existing:
            sub = NewsletterSubscriber(email=n.email)
            db.add(sub)
            db.commit()
            db.refresh(sub)
        else:
            db.commit()
        return {"status": "success", "message": "Subscribed to academic alerts!"}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to subscribe newsletter: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to subscribe: {str(exc)}")


@router.get("/newsletter")
def list_newsletter_subscribers(db: Session = Depends(get_db)):
    subs = db.query(NewsletterSubscriber).order_by(NewsletterSubscriber.id.desc()).all()
    return [
        {
            "id": s.id,
            "email": s.email,
            "subscribed_at": (s.subscribed_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(s.subscribed_at, "strftime") else str(s.subscribed_at)) if s.subscribed_at else None,
        }
        for s in subs
    ]


@router.get("/documents")
def list_public_documents(db: Session = Depends(get_db)):
    try:
        docs = db.query(PublicDocument).filter(PublicDocument.is_active == 1).order_by(PublicDocument.id.desc()).all()
        return [
            {
                "id": d.id,
                "title": d.title,
                "category": d.category,
                "file_type": d.file_type,
                "file_size": d.file_size,
                "description": d.description,
                "content": d.content,
                "download_url": d.download_url,
            }
            for d in docs
        ]
    except Exception as exc:
        logger.error("Failed to list public documents: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve public documents.")


@router.post("/documents", status_code=201)
def create_public_document(d: PublicDocumentCreate, db: Session = Depends(get_db)):
    try:
        new_d = PublicDocument(
            title=d.title,
            category=d.category,
            file_type=d.file_type or "PDF",
            file_size=d.file_size or "1.5 MB",
            description=d.description or "",
            content=d.content or "",
            download_url=d.download_url or "",
            is_active=1,
        )
        db.add(new_d)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Uploaded public document [{new_d.title}]", module="Downloads"))
        db.commit()
        db.refresh(new_d)
        return {"status": "success", "id": new_d.id, "title": new_d.title}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create public document: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to upload document: {str(exc)}")


@router.put("/documents/{id}")
def update_public_document(id: int, d: PublicDocumentUpdate, db: Session = Depends(get_db)):
    try:
        doc = db.query(PublicDocument).filter(PublicDocument.id == id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found.")
        for field, val in d.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(doc, field, val)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return {"status": "success", "message": "Public document updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update public document %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update document: {str(exc)}")


@router.delete("/documents/{id}")
def delete_public_document(id: int, db: Session = Depends(get_db)):
    try:
        doc = db.query(PublicDocument).filter(PublicDocument.id == id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found.")
        db.delete(doc)
        db.add(AuditLog(actor="admin", action=f"Deleted public document [{id}]", module="Downloads"))
        db.commit()
        return {"status": "success", "message": "Document removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete public document %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete document: {str(exc)}")


@router.get("/advertisements")
def list_advertisements(db: Session = Depends(get_db)):
    try:
        ads = db.query(Advertisement).filter(Advertisement.is_active == 1).order_by(Advertisement.id.desc()).all()
        return [
            {
                "id": a.id,
                "title": a.title,
                "placement": a.placement,
                "image_url": a.image_url,
                "target_url": a.target_url,
                "is_active": a.is_active,
                "impressions": a.impressions,
                "clicks": a.clicks,
            }
            for a in ads
        ]
    except Exception as exc:
        logger.error("Failed to list advertisements: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve advertisements.")


@router.post("/advertisements", status_code=201)
def create_advertisement(ad: AdvertisementCreate, db: Session = Depends(get_db)):
    try:
        new_ad = Advertisement(
            title=ad.title,
            placement=ad.placement or "sidebar",
            image_url=ad.image_url,
            target_url=ad.target_url or "",
            is_active=1,
        )
        db.add(new_ad)
        db.flush()
        db.add(AuditLog(actor="admin", action=f"Created advertisement campaign [{new_ad.title}]", module="Advertisements"))
        db.commit()
        db.refresh(new_ad)
        return {"status": "success", "id": new_ad.id, "title": new_ad.title}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create advertisement: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create advertisement: {str(exc)}")


@router.put("/advertisements/{id}")
def update_advertisement(id: int, ad: AdvertisementUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(Advertisement).filter(Advertisement.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Advertisement not found.")
        for field, val in ad.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(item, field, val)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"status": "success", "message": "Advertisement updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update advertisement %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to update advertisement: {str(exc)}")


@router.delete("/advertisements/{id}")
def delete_advertisement(id: int, db: Session = Depends(get_db)):
    try:
        ad = db.query(Advertisement).filter(Advertisement.id == id).first()
        if not ad:
            raise HTTPException(status_code=404, detail="Advertisement not found.")
        db.delete(ad)
        db.commit()
        return {"status": "success", "message": "Advertisement removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("Failed to delete advertisement %s: %s", id, exc)
        raise HTTPException(status_code=400, detail=f"Failed to delete advertisement: {str(exc)}")
