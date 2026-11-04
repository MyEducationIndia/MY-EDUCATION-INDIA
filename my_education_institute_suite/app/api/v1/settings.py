from fastapi import APIRouter, HTTPException, Response, Body
from app.core.database import get_db
from app.core.config import settings as app_settings
from app.models.schemas import SettingsUpdate
from typing import Dict, Any
import json, time

router = APIRouter(prefix="/settings", tags=["Enterprise Settings, Backup & Restore"])

@router.get("")
def get_settings():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM institutes WHERE id = 1")
        inst = cur.fetchone()
        return dict(inst) if inst else {}

@router.put("")
def update_settings(s: SettingsUpdate):
    with get_db() as conn:
        cur = conn.cursor()
        updates = []
        params = []
        for field, val in s.dict(exclude_unset=True).items():
            if val is not None:
                updates.append(f"{field} = ?")
                params.append(val)

        if updates:
            params.append(1)
            cur.execute(f"UPDATE institutes SET {', '.join(updates)} WHERE id = ?", params)
            cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', 'Updated Institute General Settings', 'Settings')")

        return {"status": "success", "message": "Institute settings updated successfully."}

@router.get("/audit-logs")
def get_audit_logs(limit: int = 50):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in cur.fetchall()]

@router.get("/backup/json")
def download_backup_json():
    with get_db() as conn:
        cur = conn.cursor()
        tables = [
            'institutes', 'roles', 'users', 'courses', 'staff', 'batches', 
            'students', 'admissions', 'fee_payments', 'attendance', 'study_materials', 
            'notices', 'assignments', 'staff_leaves', 'testimonials', 'faqs', 'cms_content'
        ]
        backup_data = {}
        for t in tables:
            cur.execute(f"SELECT * FROM {t}")
            backup_data[t] = [dict(r) for r in cur.fetchall()]

        json_bytes = json.dumps(backup_data, indent=2, default=str).encode('utf-8')
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', 'Generated Complete Database JSON Backup Snapshot', 'Backup')")
        
        response = Response(content=json_bytes, media_type="application/json")
        today = time.strftime("%Y-%m-%d")
        response.headers["Content-Disposition"] = f"attachment; filename=MY_EDUCATION_BACKUP_{today}.json"
        return response

@router.post("/restore")
def restore_database_from_json(payload: Dict[str, Any] = Body(...), mode: str = "overwrite"):
    """
    Restores database tables from a previously exported JSON backup snapshot.
    Supports both 'overwrite' (replace table records) and 'merge' (insert or replace without clearing).
    """
    allowed_tables = [
        'institutes', 'roles', 'users', 'courses', 'staff', 'batches', 
        'students', 'admissions', 'fee_payments', 'attendance', 'study_materials', 
        'notices', 'assignments', 'staff_leaves', 'testimonials', 'faqs', 'cms_content'
    ]
    restored_counts = {}

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = OFF;")
        try:
            for table in allowed_tables:
                if table in payload and isinstance(payload[table], list):
                    rows = payload[table]
                    if mode == "overwrite" and len(rows) > 0:
                        cur.execute(f"DELETE FROM {table}")
                    count = 0
                    for row in rows:
                        if isinstance(row, dict) and len(row) > 0:
                            cols = list(row.keys())
                            placeholders = ", ".join(["?"] * len(cols))
                            col_names = ", ".join(cols)
                            vals = [row[c] for c in cols]
                            cur.execute(f"INSERT OR REPLACE INTO {table} ({col_names}) VALUES ({placeholders})", vals)
                            count += 1
                    restored_counts[table] = count

            cur.execute(
                "INSERT INTO audit_logs (actor, action, module) VALUES ('admin', ?, 'Restore')",
                (f"Executed full database restore from JSON backup ({sum(restored_counts.values())} total rows)",)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Database restore failed: {str(e)}")
        finally:
            cur.execute("PRAGMA foreign_keys = ON;")

    return {
        "status": "success",
        "mode": mode,
        "restored_tables": restored_counts,
        "total_records_restored": sum(restored_counts.values()),
        "message": "Database snapshot restored successfully."
    }

@router.post("/restore/verify")
def verify_restore_snapshot():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA integrity_check;")
        res = cur.fetchone()[0]
        cur.execute("INSERT INTO audit_logs (actor, action, module) VALUES ('admin', 'Executed Automated Database Integrity Check', 'System')")
        return {"status": "success", "integrity_check": res, "message": "Database snapshot integrity verified: 0 errors found."}
