import mimetypes
import uuid
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logging_config import get_logger
from app.models.entities import StoredFile

logger = get_logger(__name__)


def _build_s3_client():
    import boto3
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION_NAME,
    )


def _build_external_s3_url(key: str) -> str:
    if settings.S3_PUBLIC_URL:
        return f"{settings.S3_PUBLIC_URL.rstrip('/')}/{key}"
    if settings.S3_ENDPOINT_URL:
        return f"{settings.S3_ENDPOINT_URL.rstrip('/')}/{settings.S3_BUCKET}/{key}"
    return f"https://{settings.S3_BUCKET}.s3.{settings.S3_REGION_NAME}.amazonaws.com/{key}"


def store_file_binary(
    db: Session,
    file_bytes: bytes,
    filename: str,
    content_type: Optional[str] = None,
    category: str = "general",
) -> StoredFile:
    """
    Stores file binaries persistently:
    1. If S3 / Cloudflare R2 / Backblaze B2 Object Storage is configured, uploads to bucket.
    2. Otherwise stores binary directly in Render PostgreSQL BYTEA column (100% persistent across restarts).
    Never writes uploads to Render's ephemeral local filesystem.
    """
    file_id = f"f_{uuid.uuid4().hex[:16]}"
    safe_filename = (filename or "upload.bin").replace("/", "_").replace("\\", "_")
    if not content_type:
        content_type = mimetypes.guess_type(safe_filename)[0] or "application/octet-stream"

    if settings.S3_BUCKET and settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        try:
            s3_client = _build_s3_client()
            key = f"uploads/{category}/{file_id}_{safe_filename}"
            s3_client.put_object(
                Bucket=settings.S3_BUCKET,
                Key=key,
                Body=file_bytes,
                ContentType=content_type,
            )
            external_url = _build_external_s3_url(key)
            stored = StoredFile(
                id=file_id,
                filename=safe_filename,
                content_type=content_type,
                file_size=len(file_bytes),
                storage_backend="s3",
                external_url=external_url,
                category=category,
            )
            db.add(stored)
            db.flush()
            logger.info("Stored file %s (%d bytes) in S3 bucket %s", file_id, len(file_bytes), settings.S3_BUCKET)
            return stored
        except Exception as exc:
            logger.warning("S3 upload failed (%s); falling back to PostgreSQL BYTEA storage.", exc)

    stored = StoredFile(
        id=file_id,
        filename=safe_filename,
        content_type=content_type,
        file_size=len(file_bytes),
        storage_backend="postgres_bytea",
        file_data=file_bytes,
        external_url=f"/api/v1/storage/file/{file_id}",
        category=category,
    )
    db.add(stored)
    db.flush()
    logger.info("Stored file %s (%d bytes) in PostgreSQL BYTEA storage", file_id, len(file_bytes))
    return stored


def retrieve_file_binary(db: Session, file_id: str) -> Optional[Tuple[bytes, str, str]]:
    """
    Retrieves file binary and metadata: (bytes, filename, content_type).
    """
    file_rec = db.query(StoredFile).filter(StoredFile.id == file_id).first()
    if not file_rec:
        return None

    if file_rec.storage_backend == "postgres_bytea" and file_rec.file_data:
        return (file_rec.file_data, file_rec.filename, file_rec.content_type)

    if file_rec.storage_backend == "s3" and settings.S3_BUCKET:
        try:
            s3_client = _build_s3_client()
            key = f"uploads/{file_rec.category}/{file_rec.id}_{file_rec.filename}"
            obj = s3_client.get_object(Bucket=settings.S3_BUCKET, Key=key)
            data = obj["Body"].read()
            return (data, file_rec.filename, file_rec.content_type)
        except Exception as exc:
            logger.error("Failed to retrieve S3 object for file_id %s: %s", file_id, exc)
            if file_rec.file_data:
                return (file_rec.file_data, file_rec.filename, file_rec.content_type)
            return None

    return None
