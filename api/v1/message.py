from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.message import Message, MessageCreate
from services.message_service import message_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/message", response_model=Message, status_code=status.HTTP_201_CREATED, tags=["Message"])
def create_message(message: MessageCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    message_service.validate_fields(message)
    return message_service.create(db, message)

@router.get("/message", response_model=List[Message], tags=["Message"])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    messages = message_service.get_all(db, skip=skip, limit=limit)
    return messages

@router.get("/message/{id}", response_model=Message, tags=["Message"])
def read_message(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    message = message_service.get(db, id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.put("/message/{id}", response_model=Message, tags=["Message"])
def update_message(id: int, message: MessageCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    message_service.validate_fields(message)
    db_message = message_service.update(db, id, message)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@router.delete("/message/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Message"])
def delete_message(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    message = message_service.delete(db, id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return

@router.get("/message/{conversation_id}/conversation", response_model=List[Message], tags=["Message"])
def read_messages_by_conversation(conversation_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    messages = message_service.get_by_conversation_id(db, conversation_id, skip, limit)
    return messages

@router.get("/message/{id}/exists", tags=["Table"])
def exists_message(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if message_service.exists(db, id) else Response(status_code=404)
