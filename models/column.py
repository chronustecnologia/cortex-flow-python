from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Column(Base):
    __tablename__ = "columns"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    type = Column(String(60), nullable=False)
    size = Column(Integer, nullable=True)
    nullable = Column(Boolean, nullable=False)
    auto_increment = Column(Boolean, nullable=False)
    primary_key = Column(Boolean, nullable=False)
    unique = Column(Boolean, nullable=False)
    description = Column(Text, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)

    table = relationship("Table", backref="columns")
