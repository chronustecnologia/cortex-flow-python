from typing import Optional
from pydantic import BaseModel

class TableBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    database_id: Optional[int] = None

class TableCreate(TableBase):
    pass

class Table(TableBase):
    id: int

    class Config:
        from_attributes = True


