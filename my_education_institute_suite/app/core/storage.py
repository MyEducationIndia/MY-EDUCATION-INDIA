import uuid, mimetypes, os
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.entities import StoredFile

def store_file_binary(
    db: Session,
    file_bytes: bytes,
    filename: str,
    content_type: Optional[str] = None,
    category: str = "general"
) -> StoredFile:
    """
    Stores file binaries persistently:
    1. If S3 / R2 / Object Storage is configured in environment, uploads to S3 bucket.
    2. Otherwise, stores binary directly in Render PostgreSQL BYTEA column (100% persistent across container restarts).
    Never relies on Render's ephemeral filesystem.
    """
    file_id = f"f_{uuid.uuid4().hex[:16]}"
    if not content_type:
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    # Attempt S3 Object Storage if configured
    if settings.S3_BUCKET and settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        try:
            import boto3
            s3_client = boto3.client(
                "s3",
                endpoint_url=settings.S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.S3_REGION_NAME,
            )
            key = f"uploads/{category}/{file_id}_{filename}"
            s3_client.put_object(
                Bucket=settings.S3_BUCKET,
                Key=key,
                Body=file_bytes,
                ContentType=content_type
            )
            external_url = f"https://{settings.S3_BUCKET}.s3.amazonaws.com/{key}"
            stored = StoredFile(
                id=file_id,
                filename=filename,
                content_type=content_type,
                file_size=len(file_bytes),
                storage_backend="s3",
                external_url=external_url,
                category=category
            )
            db.add(stored)
            db.flush()
            return stored
        except Exception as e:
            # Fall back to PostgreSQL BYTEA storage
            pass

    # Standard Render Enterprise Storage: Store binary directly in PostgreSQL BYTEA column
    stored = StoredFile(
        id=file_id,
        filename=filename,
        content_type=content_type,
        file_size=len(file_bytes),
        storage_backend="postgres_bytea",
        file_data=file_bytes,
        external_url=f"/api/v1/storage/file/{file_id}",
        category=category
    )
    db.add(stored)
    db.flush()
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
            import boto3
            s3_client = boto3.client(
                "s3",
                endpoint_url=settings.S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.S3_REGION_NAME,
            )
            key = f"uploads/{file_rec.category}/{file_rec.id}_{file_rec.filename}"
            obj = s3_client.get_object(Bucket=settings.S3_BUCKET, Key=key)
            data = obj["Body"].read()
            return (data, file_rec.filename, file_rec.content_type)
        except Exception:
            return None

    return None
