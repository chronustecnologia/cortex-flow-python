from sqlalchemy import Boolean, Column, Integer, String, Text
from db.base import Base

class AI_Model(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(20), nullable=False)
    configs = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
