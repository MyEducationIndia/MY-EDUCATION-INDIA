from fastapi import APIRouter, HTTPException, Request, Body
from app.core.database import get_db
from typing import Dict, Any
import json, time, os

router = APIRouter(prefix="/sync", tags=["Cloud State Synchronization"])

def ensure_sync_table():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS shared_institutional_state (
                id INTEGER PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@router.get("/state")
def get_shared_state():
    ensure_sync_table()
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT state_json, updated_at FROM shared_institutional_state WHERE id = 1")
        row = cur.fetchone()
        if row and row["state_json"]:
            try:
                state_data = json.loads(row["state_json"])
                return {
                    "status": "success",
                    "has_state": True,
                    "updated_at": row["updated_at"],
                    "state": state_data
                }
            except Exception as e:
                return {"status": "error", "has_state": False, "message": str(e)}
        
        # If not in table, check if disk backup exists
        backup_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "my_education_live_backup.json")
        if os.path.exists(backup_path):
            try:
                with open(backup_path, "r", encoding="utf-8") as bf:
                    state_data = json.load(bf)
                return {
                    "status": "success",
                    "has_state": True,
                    "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "state": state_data
                }
            except Exception:
                pass

        return {"status": "success", "has_state": False}

@router.post("/state")
def save_shared_state(payload: Dict[str, Any] = Body(...)):
    ensure_sync_table()
    state_obj = payload.get("state")
    if not state_obj or not isinstance(state_obj, dict):
        raise HTTPException(status_code=400, detail="Missing or invalid state object in request body.")

    state_json = json.dumps(state_obj, default=str)
    
    # 1. Save to SQLite database table on Render server
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO shared_institutional_state (id, state_json, updated_at)
            VALUES (1, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                state_json = excluded.state_json,
                updated_at = CURRENT_TIMESTAMP
        ''', (state_json,))
        
        # 2. Update relational CMS table
        if "cms" in state_obj and isinstance(state_obj["cms"], dict):
            for k, v in state_obj["cms"].items():
                if isinstance(v, (str, int, float, bool)):
                    cur.execute("INSERT OR REPLACE INTO cms_content (key, value) VALUES (?, ?)", (str(k), str(v)))

        # 3. Log to audit_logs table on Render server
        cur.execute(
            "INSERT INTO audit_logs (actor, action, module) VALUES (?, ?, ?)",
            ("CloudSync", "Synchronized institutional state from all portals to Render server database", "RenderServer")
        )
        conn.commit()

    # 4. Save to persistent file backup on Render server disk
    try:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        os.makedirs(data_dir, exist_ok=True)
        backup_path = os.path.join(data_dir, "my_education_live_backup.json")
        with open(backup_path, "w", encoding="utf-8") as bf:
            bf.write(state_json)
    except Exception as e:
        print("[Sync] Warning: could not write disk backup file:", e)

    return {
        "status": "success",
        "message": "All data and changes from all sources successfully saved to Render server database.",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.post("/reset")
def reset_shared_state():
    ensure_sync_table()
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM shared_institutional_state WHERE id = 1")
        conn.commit()
    backup_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "my_education_live_backup.json")
    if os.path.exists(backup_path):
        try:
            os.remove(backup_path)
        except Exception:
            pass
    return {"status": "success", "message": "Shared cloud state cleared on Render server."}
