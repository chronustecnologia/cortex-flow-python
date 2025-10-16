from typing import Optional
from pydantic import BaseModel

class IndexBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    columns: Optional[str] = None
    table_id: Optional[int] = None

class IndexCreate(IndexBase):
    pass

class Index(IndexBase):
    id: int

    class Config:
        from_attributes = True


