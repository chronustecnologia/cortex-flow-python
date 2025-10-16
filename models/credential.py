from sqlalchemy import Column, Integer, String, Boolean, Text
from db.base import Base

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(String(80), unique=True, index=True, nullable=False)
    client_secret = Column(String(80), nullable=False)
    grant_types = Column(Text, nullable=False)
    scopes = Column(Text, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
