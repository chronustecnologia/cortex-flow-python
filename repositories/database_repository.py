from sqlalchemy.orm import Session
from models.database import Database
from schemas.database import DatabaseCreate, DatabaseBase
from repositories.base_repository import BaseRepository

class DatabaseRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Database, db)
