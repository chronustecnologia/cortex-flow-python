from sqlalchemy.orm import Session
from db.base import Base
from db.session import engine
from models.credential import Credential

def init_db(db: Session):
    Base.metadata.create_all(bind=engine)

    # Inserir registro inicial na tabela credentials
    initial_credential = db.query(Credential).filter(Credential.id == 1).first()
    if not initial_credential:
        db_credential = Credential(
            client_id="da64a1d1-3ed3-4085-a002-9ab301f224ad",
            client_secret="dabaa1c3748a3110e3c1f481516130d6e756eb06d34ebbce6623f2cea92a96f6",
            grant_types="client_credentials",
            scopes="",
            active=True
        )
        db.add(db_credential)
        db.commit()
        db.refresh(db_credential)
        print("Registro inicial de credencial inserido.")
    else:
        print("Registro inicial de credencial já existe.")

