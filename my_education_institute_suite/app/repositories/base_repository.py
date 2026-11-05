from typing import Any, Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic Clean Architecture Repository enforcing strict SQLAlchemy 2.x transaction rules:
    - Every create executes db.add(), db.commit(), db.refresh()
    - Every update executes db.add(), db.commit(), db.refresh()
    - Every delete executes db.delete(), db.commit()
    - Automatic rollback on failure
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, record_id: Any) -> Optional[ModelType]:
        pk_col = list(self.model.__table__.primary_key.columns)[0]
        return self.db.query(self.model).filter(pk_col == record_id).first()

    def list_all(self, skip: int = 0, limit: int = 500) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: ModelType) -> ModelType:
        try:
            self.db.add(obj_in)
            self.db.commit()
            self.db.refresh(obj_in)
            return obj_in
        except Exception:
            self.db.rollback()
            raise

    def update(self, db_obj: ModelType, update_data: dict) -> ModelType:
        try:
            for field, value in update_data.items():
                if value is not None and hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except Exception:
            self.db.rollback()
            raise

    def delete(self, db_obj: ModelType) -> bool:
        try:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise
