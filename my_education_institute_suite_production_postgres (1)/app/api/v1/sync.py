from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import SharedInstitutionalState, CMSContent, AuditLog
from typing import Dict, Any
import json, time

router = APIRouter(prefix="/sync", tags=["Cloud State Synchronization"])

@router.get("/state")
def get_shared_state(db: Session = Depends(get_db)):
    try:
        row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if row and row.state_json:
            try:
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
                    "state": state_data
                }
            except Exception as e:
                return {"status": "error", "has_state": False, "message": str(e)}

        return {"status": "success", "has_state": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cloud state: {str(e)}")

@router.post("/state")
def save_shared_state(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    state_obj = payload.get("state")
    if not state_obj or not isinstance(state_obj, dict):
        raise HTTPException(status_code=400, detail="Missing or invalid state object in request body.")

    state_json = json.dumps(state_obj, default=str)

    try:
        # 1. Save directly into PostgreSQL database table
        row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if row:
            row.state_json = state_json
        else:
            db.add(SharedInstitutionalState(id=1, state_json=state_json))

        # 2. Update relational CMS table in PostgreSQL
        if "cms" in state_obj and isinstance(state_obj["cms"], dict):
            for k, v in state_obj["cms"].items():
                if isinstance(v, (str, int, float, bool)):
                    cms_item = db.query(CMSContent).filter(CMSContent.key == str(k)).first()
                    if cms_item:
                        cms_item.value = str(v)
                    else:
                        db.add(CMSContent(key=str(k), value=str(v)))

        # 3. Log to PostgreSQL audit trail
        db.add(AuditLog(
            actor="CloudSync",
            action="Synchronized institutional state to Render PostgreSQL database",
            module="RenderPostgres"
        ))

        return {
            "status": "success",
            "message": "All institutional state changes successfully saved to Render PostgreSQL database.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save state to PostgreSQL: {str(e)}")

@router.post("/reset")
def reset_shared_state(db: Session = Depends(get_db)):
    try:
        row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if row:
            db.delete(row)
        return {"status": "success", "message": "Shared institutional state cleared from PostgreSQL database."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to reset state: {str(e)}")
