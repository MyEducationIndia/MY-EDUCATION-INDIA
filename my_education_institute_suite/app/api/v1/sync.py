from datetime import datetime
import json
import time
from typing import Any, Dict
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import AuditLog, CMSContent, SharedInstitutionalState

logger = get_logger(__name__)
router = APIRouter(prefix="/sync", tags=["Cloud State Synchronization"])


def _build_fallback_clean_state() -> Dict[str, Any]:
    return {
        "theme": "light",
        "currentView": "website",
        "currentAdminTab": "dashboard",
        "currentStaffTab": "overview",
        "loginRole": "student",
        "cms": {
            "instituteName": "MY EDUCATION INSTITUTE",
            "instituteSlogan": "Premier Institute of Computer & IT Studies",
            "regNo": "REG-MP-2008-84920",
            "isoCertification": "ISO 9001:2015 Certified",
            "heroBadge": "Govt. Recognized & ISO 9001:2015 Certified Center of Excellence",
            "heroTitle": "Shaping Digital Leaders in Computer Technology",
            "heroSubtitle": "Empowering students with industry-standard IT diplomas, government-recognized teaching certifications (TCCP), data analysis, accounting, and professional software skills with 100% placement support.",
            "announcementTicker": "ADMISSIONS OPEN 2026-27: DCA, PGDCA, TCCP, CCA & Tally Prime Batches Commencing 1st & 15th of Every Month • Call: +91 98765 43210",
            "statAlumni": "15,200+",
            "statPlacement": "98.4%",
            "statCourses": "25+",
            "statYears": "18+",
            "contactPhone": "+91 98765 43210",
            "contactEmail": "admission@myeducation.edu.in",
            "contactAddress": "Tech Innovation Park, Sector 4, Central IT Corridor, Indore, MP - 452001",
            "whatsApp": "919876543210",
            "hidePublicCourseFees": "true",
            "theme": "light",
        },
        "courses": [],
        "batches": [],
        "users": [
            {
                "id": "USR-ADMIN-1",
                "name": "Administrator (Super Admin)",
                "role": "admin",
                "username": "admin",
                "email": "admin@myeducation.edu.in",
                "password": "Admin@1234",
                "linkedId": "ADM-1",
                "status": "Active",
            },
            {
                "id": "USR-ACC-101",
                "name": "Chief Accounts Officer",
                "role": "accounts",
                "username": "accounts",
                "email": "accounts@myeducation.edu.in",
                "password": "Accounts@1234",
                "linkedId": "ACC-1",
                "status": "Active",
            },
        ],
        "students": [],
        "staff": [],
        "admissions": [],
        "fees": [],
        "materials": [],
        "notices": [],
        "testimonials": [],
        "faqs": [],
        "gallery": [],
        "blogs": [],
        "auditLogs": [],
        "enquiries": [],
        "examForms": [],
        "submissions": [],
        "assignments": [],
        "expenses": [],
        "customSections": [],
        "feeHeads": [],
        "websiteSectionsList": [],
    }


@router.get("/state")
def get_shared_state(db: Session = Depends(get_db)):
    try:
        row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if not row or not row.state_json:
            # Self-healing: Automatically initialize row 1 in PostgreSQL if absent
            initial_state = _build_fallback_clean_state()
            state_json = json.dumps(initial_state, default=str)
            row = SharedInstitutionalState(id=1, state_json=state_json, updated_at=datetime.utcnow())
            db.add(row)
            db.commit()
            db.refresh(row)
            logger.info("Initialized clean shared institutional state row 1 in PostgreSQL.")

        state_data = json.loads(row.state_json)
        updated_str = (
            row.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if hasattr(row.updated_at, "strftime")
            else time.strftime("%Y-%m-%d %H:%M:%S")
        )
        return {
            "status": "success",
            "has_state": True,
            "updated_at": updated_str,
            "state": state_data,
        }
    except Exception as exc:
        db.rollback()
        logger.error("Failed to fetch cloud state: %s", exc)
        raise HTTPException(status_code=500, detail=f"Failed to fetch cloud state: {str(exc)}")


@router.post("/state")
def save_shared_state(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    state_obj = payload.get("state")
    if not state_obj or not isinstance(state_obj, dict):
        raise HTTPException(status_code=400, detail="Missing or invalid state object in request body.")

    state_json = json.dumps(state_obj, default=str)

    try:
        row = (
            db.query(SharedInstitutionalState)
            .filter(SharedInstitutionalState.id == 1)
            .with_for_update()
            .first()
        )
        if row:
            row.state_json = state_json
            row.updated_at = datetime.utcnow()
        else:
            row = SharedInstitutionalState(id=1, state_json=state_json, updated_at=datetime.utcnow())
            db.add(row)

        if "cms" in state_obj and isinstance(state_obj["cms"], dict):
            for k, v in state_obj["cms"].items():
                if isinstance(v, (str, int, float, bool)):
                    cms_item = db.query(CMSContent).filter(CMSContent.key == str(k)).first()
                    if cms_item:
                        cms_item.value = str(v)
                    else:
                        db.add(CMSContent(key=str(k), value=str(v)))

        db.add(
            AuditLog(
                actor="CloudSync",
                action="Synchronized institutional state to Render PostgreSQL database",
                module="RenderPostgres",
            )
        )

        # Enforce PostgreSQL immediate transaction commit & refresh
        db.commit()
        db.refresh(row)

        updated_str = (
            row.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if hasattr(row.updated_at, "strftime")
            else time.strftime("%Y-%m-%d %H:%M:%S")
        )

        return {
            "status": "success",
            "message": "All institutional state changes successfully saved to Render PostgreSQL database.",
            "updated_at": updated_str,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as exc:
        db.rollback()
        logger.error("Failed to save state to PostgreSQL: %s", exc)
        raise HTTPException(status_code=500, detail=f"Failed to save state to PostgreSQL: {str(exc)}")


@router.post("/reset")
def reset_shared_state(db: Session = Depends(get_db)):
    try:
        row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if row:
            db.delete(row)
        db.commit()
        return {"status": "success", "message": "Shared institutional state cleared from PostgreSQL database."}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to reset shared state: %s", exc)
        raise HTTPException(status_code=500, detail=f"Failed to reset state: {str(exc)}")
