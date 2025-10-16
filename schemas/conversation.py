from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ConversationBase(BaseModel):
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    is_favorite: bool = False

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int

    class Config:
        from_attributes = True
