from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.table_repository import TableRepository
from schemas.table import TableCreate
from services.base_service import BaseService

class TableService(BaseService):
    def __init__(self):
        super().__init__(TableRepository)

    def get_by_database_id(self, db: Session, database_id: int, skip: int = 0, limit: int = 100):
        return self.repository(db).get_by_database_id(database_id, skip, limit)

    def validate_fields(self, table: TableCreate):
        required_fields = {
            "name": "Nome é obrigatório",
            "description": "Descrição é obrigatório",
            "database_id": "Banco de dados é obrigatório"
        }

        for field, message in required_fields.items():
            value = getattr(table, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        return table
    
table_service = TableService()


