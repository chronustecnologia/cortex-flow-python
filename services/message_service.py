from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.message_repository import MessageRepository
from schemas.message import MessageCreate, MessageBase
from services.base_service import BaseService

class MessageService(BaseService):
    def __init__(self):
        super().__init__(MessageRepository)

    def validate_fields(self, message: MessageCreate):
        required_fields = {
            "text": "Texto é obrigatório",
            "agent": "Agenda é obrigatório",
            "conversation_id": "Conversa é obrigatório",
        }

        for field, message_text in required_fields.items():
            value = getattr(message, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message_text)
            
        allowed_types = ['USER', 'SYSTEM', 'ASSISTANT']
        if message.agent.upper() not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agente inválido")
        
        return message

    def get_by_conversation_id(self, db: Session, conversation_id: int, skip: int = 0, limit: int = 100):
        return self.repository(db).get_by_conversation_id(db, conversation_id, skip, limit)

message_service = MessageService()


