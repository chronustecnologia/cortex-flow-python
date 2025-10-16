from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.parameter_repository import ParameterRepository
from schemas.parameter import ParameterCreate, ParameterBase
from services.base_service import BaseService

class ParameterService(BaseService):
    def __init__(self):
        super().__init__(ParameterRepository)

    def validate_fields(self, parameter: ParameterCreate):
        required_fields = {
            "code": "Código é obrigatório",
            "description": "Descrição é obrigatório",
            "value": "Valor é obrigatório",
        }

        for field, message in required_fields.items():
            value = getattr(parameter, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        return parameter

    def get_by_code(self, db: Session, code: str):
        return self.repository(db).get_by_code(code)

parameter_service = ParameterService()
