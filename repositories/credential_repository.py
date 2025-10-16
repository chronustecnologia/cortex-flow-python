from sqlalchemy.orm import Session
from models.credential import Credential
from schemas.credential import CredentialCreate, CredentialBase
from repositories.base_repository import BaseRepository

class CredentialRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Credential, db)

    def get_by_client_id(self, client_id: str) -> Credential | None:
        return self.db.query(self.model).filter(self.model.client_id == client_id).first()


