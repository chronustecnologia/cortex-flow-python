from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.index_repository import IndexRepository
from schemas.index import IndexCreate, IndexBase
from services.base_service import BaseService

class IndexService(BaseService):
    def __init__(self):
        super().__init__(IndexRepository)

    def validate_fields(self, index: IndexCreate):
        required_fields = {
            "name": "Nome é obrigatório",
            "type": "Tipo é obrigatório",
            "columns": "Colunas é obrigatório",
            "table_id": "Tabela obrigatório"
        }

        for field, message in required_fields.items():
            value = getattr(index, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
            
        allowed_types = ['INDEX', 'UNIQUE']
        if index.type.upper() not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo inválido")
        
        return index

    def get_by_table_id(self, db: Session, table_id: int, skip: int = 0, limit: int = 100):
        return self.repository(db).get_by_table_id(table_id, skip, limit)

index_service = IndexService()


