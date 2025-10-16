from pydantic import BaseModel

class CredentialBase(BaseModel):
    client_id: str
    client_secret: str
    grant_types: str
    scopes: str
    active: bool = True

class CredentialCreate(CredentialBase):
    pass

class Credential(CredentialBase):
    id: int

    class Config:
        from_attributes = True
