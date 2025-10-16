from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: Optional[str] = None
    database_id: Optional[int] = None
    ai_model_id: Optional[int] = None
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    message: str
