#!/usr/bin/env python3
"""
Transaction-Safe PostgreSQL Native Backup (pg_dump custom format) and Restore (pg_restore --single-transaction)
Strictly uses PostgreSQL binary dump format (.dump). Never uses JSON or browser storage.
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def create_backup(database_url: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_file = output_dir / f"mei_postgres_backup_{timestamp}.dump"

    cmd = [
        "pg_dump",
        "--dbname",
        database_url.replace("postgresql+psycopg://", "postgresql://"),
        "--format=custom",
        "--compress=9",
        "--no-owner",
        "--no-privileges",
        "--file",
        str(backup_file),
    ]
    subprocess.run(cmd, check=True)
    return backup_file


def restore_backup_transaction_safe(database_url: str, backup_file: Path) -> None:
    if not backup_file.exists():
        raise FileNotFoundError(f"Backup archive not found: {backup_file}")

    # --single-transaction guarantees atomic execution and automatic rollback on any failure
    cmd = [
        "pg_restore",
        "--dbname",
        database_url.replace("postgresql+psycopg://", "postgresql://"),
        "--single-transaction",
        "--clean",
        "--if-exists",
        "--no-owner",
        "--no-privileges",
        str(backup_file),
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MY EDUCATION INDIA PostgreSQL Backup & Restore Utility")
    parser.add_argument("action", choices=["backup", "restore"])
    parser.add_argument("--file", type=Path, help="Path to .dump file for restore")
    parser.add_argument("--out-dir", type=Path, default=Path("./backups"))
    args = parser.parse_args()

    db_url = os.environ.get("SYNC_DATABASE_URL")
    if not db_url:
        sys.stderr.write("ERROR: SYNC_DATABASE_URL environment variable is required.\n")
        sys.exit(1)

    if args.action == "backup":
        path = create_backup(db_url, args.out_dir)
        print(f"Backup created successfully: {path}")
    else:
        if not args.file:
            sys.stderr.write("ERROR: --file is required for restore.\n")
            sys.exit(1)
        restore_backup_transaction_safe(db_url, args.file)
        print("Database restored atomically inside a single PostgreSQL transaction.")
