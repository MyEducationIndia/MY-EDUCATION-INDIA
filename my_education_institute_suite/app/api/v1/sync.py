import json
import time
from typing import Any, Dict, Optional
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.core.security import get_current_user_optional
from app.models.entities import AuditLog, CMSContent, SharedInstitutionalState

logger = get_logger(__name__)
router = APIRouter(prefix="/sync", tags=["Cloud State Synchronization"])


@router.get("/state")
def get_shared_state(db: Session = Depends(get_db)):
    try:
        cms_rows = db.query(CMSContent).all()
        cms_table_map = {r.key: r.value for r in cms_rows}

        row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if row and row.state_json:
            try:
                state_data = json.loads(row.state_json)
                if not isinstance(state_data.get("cms"), dict):
                    state_data["cms"] = {}
                # Merge authoritative CMSContent rows into state_data["cms"]
                for k, v in cms_table_map.items():
                    if v == "true":
                        state_data["cms"][k] = True
                    elif v == "false":
                        state_data["cms"][k] = False
                    else:
                        state_data["cms"][k] = v

                # Never expose plaintext passwords in state_data["users"]
                if isinstance(state_data.get("users"), list):
                    for u in state_data["users"]:
                        if isinstance(u, dict):
                            u.pop("password", None)

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
                logger.warning("Corrupt shared state JSON: %s", exc)
                return {"status": "error", "has_state": False, "message": str(exc)}

        if cms_table_map:
            return {
                "status": "success",
                "has_state": True,
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "state": {"cms": cms_table_map},
            }

        return {"status": "success", "has_state": False}
    except Exception as exc:
        logger.error("Failed to fetch cloud state: %s", exc)
        raise HTTPException(status_code=500, detail=f"Failed to fetch cloud state: {str(exc)}")


@router.post("/state")
def save_shared_state(
    payload: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    state_obj = payload.get("state")
    if not state_obj or not isinstance(state_obj, dict):
        raise HTTPException(status_code=400, detail="Missing or invalid state object in request body.")

    # Strip any plaintext passwords from users array before storing
    if isinstance(state_obj.get("users"), list):
        for u in state_obj["users"]:
            if isinstance(u, dict):
                u.pop("password", None)

    state_json = json.dumps(state_obj, default=str)

    try:
        actor = str(current_user.get("sub", "CloudSync")) if current_user else "CloudSync"
        row = db.query(SharedInstitutionalState).filter(SharedInstitutionalState.id == 1).first()
        if row:
            row.state_json = state_json
            db.add(row)
        else:
            row = SharedInstitutionalState(id=1, state_json=state_json)
            db.add(row)

        if "cms" in state_obj and isinstance(state_obj["cms"], dict):
            for k, v in state_obj["cms"].items():
                if isinstance(v, (str, int, float, bool)):
                    val_str = "true" if v is True else ("false" if v is False else str(v))
                    cms_item = db.query(CMSContent).filter(CMSContent.key == str(k)).first()
                    if cms_item:
                        cms_item.value = val_str
                        db.add(cms_item)
                    else:
                        db.add(CMSContent(key=str(k), value=val_str))

        db.add(
            AuditLog(
                actor=actor,
                action="Synchronized institutional state to PostgreSQL database",
                module="CloudSync",
            )
        )

        db.commit()
        db.refresh(row)
        return {
            "status": "success",
            "message": "All institutional state changes successfully saved to PostgreSQL database.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "state": json.loads(row.state_json),
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
