from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.ai_model_repository import AI_ModelRepository
from schemas.ai_model import AI_ModelCreate, AI_ModelBase
from services.base_service import BaseService

class AI_ModelService(BaseService):
    def __init__(self):
        super().__init__(AI_ModelRepository)

    def validate_fields(self, ai_model: AI_ModelCreate):
        required_fields = {
            "name": "Nome é obrigatório",
            "type": "Tipo é obrigatório",
        }

        for field, message in required_fields.items():
            value = getattr(ai_model, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
            
        allowed_types = ['CHATGPT', 'GEMINI', 'CLAUDE', 'DEEPSEEK']
        if ai_model.type.upper() not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo inválido")
        
        return ai_model

ai_model_service = AI_ModelService()
