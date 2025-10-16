from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.ai_model import AI_Model, AI_ModelCreate
from services.ai_model_service import ai_model_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/ai_model", response_model=AI_Model, status_code=status.HTTP_201_CREATED, tags=["AI Model"])
def create_ai_model(ai_model: AI_ModelCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ai_model_service.validate_fields(ai_model)
    return ai_model_service.create(db, ai_model)

@router.get("/ai_model", response_model=List[AI_Model], tags=["AI Model"])
def read_ai_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ai_models = ai_model_service.get_all(db, skip=skip, limit=limit)
    return ai_models

@router.get("/ai_model/{id}", response_model=AI_Model, tags=["AI Model"])
def read_ai_model(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ai_model = ai_model_service.get(db, id)
    if ai_model is None:
        raise HTTPException(status_code=404, detail="AI Model not found")
    return ai_model

@router.put("/ai_model/{id}", response_model=AI_Model, tags=["AI Model"])
def update_ai_model(id: int, ai_model: AI_ModelCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ai_model_service.validate_fields(ai_model)
    db_ai_model = ai_model_service.update(db, id, ai_model)
    if db_ai_model is None:
        raise HTTPException(status_code=404, detail="AI Model not found")
    return db_ai_model

@router.delete("/ai_model/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["AI Model"])
def delete_ai_model(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ai_model = ai_model_service.delete(db, id)
    if ai_model is None:
        raise HTTPException(status_code=404, detail="AI Model not found")
    return

@router.get("/column/{id}/exists", tags=["Column"])
def exists_column(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if ai_model_service.exists(db, id) else Response(status_code=404)
