from typing import Optional
from pydantic import BaseModel

class ColumnBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    size: Optional[int] = None
    nullable: bool = False
    auto_increment: bool = False
    primary_key: bool = False
    unique: bool = False
    description: Optional[str] = None
    table_id: Optional[int] = None

class ColumnCreate(ColumnBase):
    pass

class Column(ColumnBase):
    id: int

    class Config:
        from_attributes = True


