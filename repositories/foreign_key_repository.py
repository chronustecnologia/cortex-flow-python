from sqlalchemy.orm import Session
from models.foreign_key import ForeignKey
from schemas.foreign_key import ForeignKeyCreate, ForeignKeyBase
from repositories.base_repository import BaseRepository

class ForeignKeyRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(ForeignKey, db)

    def get_by_column_id(self, column_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).filter(self.model.column_id == column_id).offset(skip).limit(limit).all()
