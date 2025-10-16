from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Index(Base):
    __tablename__ = "indexes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    type = Column(String(60), nullable=False)
    columns = Column(Text, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)

    table = relationship("Table", backref="indexes")
