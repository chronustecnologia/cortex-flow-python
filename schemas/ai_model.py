from pydantic import BaseModel, Field
from typing import Optional

class AI_ModelBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    is_active: bool = False
    configs: Optional[str] = None

class AI_ModelCreate(AI_ModelBase):
    pass

class AI_Model(AI_ModelBase):
    id: int

    class Config:
        from_attributes = True
