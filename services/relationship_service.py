from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.relationship_repository import RelationshipRepository
from schemas.relationship import RelationshipCreate, RelationshipBase
from services.base_service import BaseService

class RelationshipService(BaseService):
    def __init__(self):
        super().__init__(RelationshipRepository)

    def validate_fields(self, relationship: RelationshipCreate):
        required_fields = {
            "type": "Tipo é obrigatório",
            "parent": "Parent é obrigatório",
            "child": "Child é obrigatório",
            "description": "Descrição é obrigatório",
            "database_id": "Banco de dados é obrigatório"
        }

        for field, message in required_fields.items():
            value = getattr(relationship, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
            
        allowed_types = ['ONE_TO_MANY', 'MANY_TO_MANY']
        if relationship.type.upper() not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo inválido")
        
        return relationship

    def get_by_database_id(self, db: Session, database_id: int, skip: int = 0, limit: int = 100):
        return self.repository(db).get_by_database_id(database_id, skip, limit)

relationship_service = RelationshipService()
