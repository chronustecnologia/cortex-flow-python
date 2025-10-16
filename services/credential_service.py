from sqlalchemy.orm import Session
from repositories.credential_repository import CredentialRepository
from schemas.credential import CredentialCreate, CredentialBase
from services.base_service import BaseService

class CredentialService(BaseService):
    def __init__(self):
        super().__init__(CredentialRepository)

    def get_by_client_id(self, db: Session, client_id: str):
        return self.repository(db).get_by_client_id(client_id)

credential_service = CredentialService()


