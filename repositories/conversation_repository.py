from sqlalchemy.orm import Session
from models.conversation import Conversation
from repositories.base_repository import BaseRepository

class ConversationRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Conversation, db)
