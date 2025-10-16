from sqlalchemy import Column, Integer, String
from db.base import Base

class Database(Base):
    __tablename__ = "databases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    engine = Column(String(60), nullable=False)
    version = Column(String(60), nullable=False)
    hostname = Column(String(100), nullable=False)
    port = Column(Integer, nullable=True)
    database = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    charset = Column(String(100), nullable=True)
