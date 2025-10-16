from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.conversation import Conversation, ConversationCreate
from services.conversation_service import conversation_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/conversation", response_model=Conversation, status_code=status.HTTP_201_CREATED, tags=["Conversation"])
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    conversation_service.validate_fields(conversation)
    return conversation_service.create(db, conversation)

@router.get("/conversation", response_model=List[Conversation], tags=["Conversation"])
def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    conversations = conversation_service.get_all(db, skip=skip, limit=limit)
    return conversations

@router.get("/conversation/{id}", response_model=Conversation, tags=["Conversation"])
def read_conversation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    conversation = conversation_service.get(db, id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.put("/conversation/{id}", response_model=Conversation, tags=["Conversation"])
def update_conversation(id: int, conversation: ConversationCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    conversation_service.validate_fields(conversation)
    db_conversation = conversation_service.update(db, id, conversation)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@router.delete("/conversation/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Conversation"])
def delete_conversation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    conversation = conversation_service.delete(db, id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return

@router.get("/conversation/{id}/exists", tags=["Table"])
def exists_conversation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if conversation_service.exists(db, id) else Response(status_code=404)
