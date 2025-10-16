from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.column_repository import ColumnRepository
from schemas.column import ColumnCreate, ColumnBase
from services.base_service import BaseService

class ColumnService(BaseService):
    def __init__(self):
        super().__init__(ColumnRepository)

    def validate_fields(self, column: ColumnCreate):
        required_fields = {
            "name": "Nome é obrigatório",
            "type": "Tipo é obrigatório",
            "description": "Descrição é obrigatório",
            "table_id": "Tabela obrigatório"
        }

        for field, message in required_fields.items():
            value = getattr(column, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
            
        allowed_types = ['INT', 'VARCHAR', 'DOUBLE', 'BOOLEAN', 'DATE', 'TIMESPAN']
        if column.type.upper() not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo inválido")
        
        return column

    def get_by_table_id(self, db: Session, table_id: int, skip: int = 0, limit: int = 100):
        return self.repository(db).get_by_table_id(table_id, skip, limit)

column_service = ColumnService()


