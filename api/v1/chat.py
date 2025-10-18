from fastapi import APIRouter, Depends, status
from requests import Session

from db.session import get_db
from core.dependencies import get_current_user
from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import chat_service

router = APIRouter()

@router.post("/chat/send", response_model=ChatResponse, status_code=status.HTTP_200_OK, tags=["Chat"])
async def send(chat: ChatRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await chat_service.send(db, chat)
