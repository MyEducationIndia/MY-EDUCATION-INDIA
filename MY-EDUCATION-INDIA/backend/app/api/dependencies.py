"""Shared API Dependencies for Database & Security"""
from app.db.session import get_db_session

__all__ = ["get_db_session"]
