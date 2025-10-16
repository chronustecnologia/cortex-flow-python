from sqlalchemy.orm import Session
from models.index import Index
from repositories.base_repository import BaseRepository

class IndexRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Index, db)

    def get_by_table_id(self, table_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).filter(self.model.table_id == table_id).offset(skip).limit(limit).all()


