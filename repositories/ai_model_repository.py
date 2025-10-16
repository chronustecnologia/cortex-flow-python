from sqlalchemy.orm import Session
from models.ai_model import AI_Model
from repositories.base_repository import BaseRepository

class AI_ModelRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(AI_Model, db)
