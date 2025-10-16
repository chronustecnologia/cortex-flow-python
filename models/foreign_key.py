from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class ForeignKey(Base):
    __tablename__ = "foreign_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    references_table = Column(String(60), nullable=False)
    references_column = Column(String(60), nullable=False)
    on_delete = Column(String(60), nullable=False)
    on_update = Column(String(60), nullable=False)
    column_id = Column(Integer, ForeignKey("columns.id"), nullable=False)

    table = relationship("Column", backref="foreign_keys")
