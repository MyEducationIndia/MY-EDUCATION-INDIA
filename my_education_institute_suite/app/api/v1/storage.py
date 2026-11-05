from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.core.storage import retrieve_file_binary, store_file_binary
from app.models.entities import AuditLog, StoredFile

logger = get_logger(__name__)
router = APIRouter(prefix="/storage", tags=["Persistent File & Object Storage"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    category: Optional[str] = Form("general"),
    db: Session = Depends(get_db),
):
    """
    Persistently uploads a file binary:
    - Stores in S3 / Cloudflare R2 / Backblaze B2 if configured in environment.
    - Otherwise stores binary in Render PostgreSQL BYTEA column (100% persistent across container restarts).
    """
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file upload.")

        stored = store_file_binary(
            db=db,
            file_bytes=content,
            filename=file.filename or "upload.bin",
            content_type=file.content_type,
            category=category or "general",
        )

        db.add(
            AuditLog(
                actor="admin",
                action=f"Uploaded persistent file [{stored.id}] {stored.filename} ({stored.file_size} bytes)",
                module="Storage",
            )
        )
        db.commit()
        db.refresh(stored)

        return {
            "status": "success",
            "file_id": stored.id,
            "filename": stored.filename,
            "file_size": stored.file_size,
            "content_type": stored.content_type,
            "file_url": stored.external_url,
            "storage_backend": stored.storage_backend,
        }
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error("File upload failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(exc)}")


@router.get("/file/{file_id}")
def stream_file(file_id: str, db: Session = Depends(get_db)):
    res = retrieve_file_binary(db, file_id)
    if not res:
        raise HTTPException(status_code=404, detail="File not found in persistent storage.")

    data, filename, content_type = res
    response = Response(content=data, media_type=content_type)
    disp = "inline" if content_type.startswith(("image/", "application/pdf")) else "attachment"
    response.headers["Content-Disposition"] = f'{disp}; filename="{filename}"'
    return response


@router.get("/files")
def list_files(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(StoredFile)
    if category:
        query = query.filter(StoredFile.category == category)
    files = query.order_by(StoredFile.created_at.desc()).all()
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "content_type": f.content_type,
            "file_size": f.file_size,
            "storage_backend": f.storage_backend,
            "external_url": f.external_url,
            "category": f.category,
            "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S") if f.created_at else None,
        }
        for f in files
    ]


@router.delete("/file/{file_id}")
def delete_file(file_id: str, db: Session = Depends(get_db)):
    stored = db.query(StoredFile).filter(StoredFile.id == file_id).first()
    if not stored:
        raise HTTPException(status_code=404, detail="File not found.")
    db.delete(stored)
    db.add(AuditLog(actor="admin", action=f"Deleted persistent file [{file_id}] {stored.filename}", module="Storage"))
    db.commit()
    return {"status": "success", "message": f"File {file_id} removed from persistent storage."}
