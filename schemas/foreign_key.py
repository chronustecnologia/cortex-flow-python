from typing import Optional
from pydantic import BaseModel

class ForeignKeyBase(BaseModel):
    references_table: Optional[str] = None
    references_column: Optional[str] = None
    on_delete: Optional[str] = None
    on_update: Optional[str] = None
    column_id: Optional[int] = None

class ForeignKeyCreate(ForeignKeyBase):
    pass

class ForeignKey(ForeignKeyBase):
    id: int

    class Config:
        from_attributes = True
