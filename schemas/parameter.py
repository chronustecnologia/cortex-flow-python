from pydantic import BaseModel, Field
from typing import Optional

class ParameterBase(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    value: Optional[str] = None

class ParameterCreate(ParameterBase):
    pass

class Parameter(ParameterBase):
    id: int

    class Config:
        from_attributes = True
