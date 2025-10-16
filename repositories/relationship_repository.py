from sqlalchemy.orm import Session
from models.relationship import Relationship
from schemas.relationship import RelationshipCreate, RelationshipBase
from repositories.base_repository import BaseRepository

class RelationshipRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Relationship, db)

    def get_by_database_id(self, database_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).filter(self.model.database_id == database_id).offset(skip).limit(limit).all()


