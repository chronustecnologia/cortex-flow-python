from typing import Optional
from pydantic import BaseModel

class RelationshipBase(BaseModel):
    type: Optional[str] = None
    parent: Optional[str] = None
    child: Optional[str] = None
    description: Optional[str] = None
    database_id: Optional[int] = None

class RelationshipCreate(RelationshipBase):
    pass

class Relationship(RelationshipBase):
    id: int

    class Config:
        from_attributes = True
