from sqlalchemy import Column, Integer, String, Text
from db.base import Base

class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    value = Column(Text, nullable=False)
