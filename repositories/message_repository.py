from sqlalchemy.orm import Session
from models.message import Message
from repositories.base_repository import BaseRepository

class MessageRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Message, db)

    def get_by_conversation_id(self, db: Session, conversation_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).filter(self.model.conversation_id == conversation_id).offset(skip).limit(limit).all()
