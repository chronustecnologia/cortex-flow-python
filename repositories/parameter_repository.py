from sqlalchemy.orm import Session
from models.parameter import Parameter
from repositories.base_repository import BaseRepository

class ParameterRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Parameter, db)

    def get_by_code(self, code: str) -> Parameter | None:
        return self.db.query(self.model).filter(self.model.code == code).first()
