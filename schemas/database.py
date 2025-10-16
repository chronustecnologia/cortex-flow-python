from typing import Optional
from pydantic import BaseModel

class DatabaseBase(BaseModel):
    engine: Optional[str] = None
    version: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    charset: Optional[str] = None

class DatabaseCreate(DatabaseBase):
    pass

class Database(DatabaseBase):
    id: int

    class Config:
        from_attributes = True


