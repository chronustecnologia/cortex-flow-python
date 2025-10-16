from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(60), nullable=False)
    parent = Column(String(60), nullable=False)
    child = Column(String(60), nullable=False)
    description = Column(Text, nullable=False)
    database_id = Column(Integer, ForeignKey("databases.id"), nullable=False)

    database = relationship("Database", backref="relationships")
