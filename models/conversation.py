from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    is_favorite = Column(Boolean, nullable=False, default=False)

    messages = relationship("Message", back_populates="conversation")
