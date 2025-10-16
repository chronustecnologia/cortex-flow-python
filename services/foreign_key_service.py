from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.foreign_key_repository import ForeignKeyRepository
from schemas.foreign_key import ForeignKeyCreate, ForeignKeyBase
from services.base_service import BaseService

class ForeignKeyService(BaseService):
    def __init__(self):
        super().__init__(ForeignKeyRepository)

    def validate_fields(self, foreignKey: ForeignKeyCreate):
        required_fields = {
            "references_table": "Tabela de referência é obrigatório",
            "references_column": "Coluna de referência é obrigatório",
            "column_id": "Coluna é obrigatório"
        }

        for field, message in required_fields.items():
            value = getattr(foreignKey, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
            
        allowed_types = ['RESTRICT', 'CASCADE']
        if foreignKey.on_update and foreignKey.on_update.upper() not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="On update inválido")
        if foreignKey.on_delete and foreignKey.on_delete.upper() not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="On delete inválido")
        
        return foreignKey
    
    def get_by_column_id(self, db: Session, column_id: int, skip: int = 0, limit: int = 100):
        return self.repository(db).get_by_column_id(column_id, skip, limit)

foreign_key_service = ForeignKeyService()
