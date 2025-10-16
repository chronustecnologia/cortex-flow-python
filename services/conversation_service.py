from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.conversation_repository import ConversationRepository
from schemas.conversation import ConversationCreate, ConversationBase
from services.base_service import BaseService

class ConversationService(BaseService):
    def __init__(self):
        super().__init__(ConversationRepository)

    def validate_fields(self, conversation: ConversationCreate):
        required_fields = {
            "title": "Título é obrigatório",
            "created_at": "Data e hora é obrigatório"
        }

        for field, message in required_fields.items():
            value = getattr(conversation, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        return conversation

conversation_service = ConversationService()
