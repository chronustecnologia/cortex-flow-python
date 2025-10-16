from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.foreign_key import ForeignKey, ForeignKeyCreate
from services.foreign_key_service import foreign_key_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/foreign_key", response_model=ForeignKey, status_code=status.HTTP_201_CREATED, tags=["Foreign Key"])
def create_foreign_key(foreign_key: ForeignKeyCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    foreign_key_service.validate_fields(foreign_key)
    return foreign_key_service.create(db, foreign_key)

@router.get("/foreign_key", response_model=List[ForeignKey], tags=["Foreign Key"])
def read_foreign_keys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    foreign_keys = foreign_key_service.get_all(db, skip=skip, limit=limit)
    return foreign_keys

@router.get("/foreign_key/{id}", response_model=ForeignKey, tags=["Foreign Key"])
def read_foreign_key(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    foreign_key = foreign_key_service.get(db, id)
    if foreign_key is None:
        raise HTTPException(status_code=404, detail="Foreign Key not found")
    return foreign_key

@router.put("/foreign_key/{id}", response_model=ForeignKey, tags=["Foreign Key"])
def update_foreign_key(id: int, foreign_key: ForeignKeyCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    foreign_key_service.validate_fields(foreign_key)
    db_foreign_key = foreign_key_service.update(db, id, foreign_key)
    if db_foreign_key is None:
        raise HTTPException(status_code=404, detail="Foreign Key not found")
    return db_foreign_key

@router.delete("/foreign_key/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Foreign Key"])
def delete_foreign_key(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    foreign_key = foreign_key_service.delete(db, id)
    if foreign_key is None:
        raise HTTPException(status_code=404, detail="Foreign Key not found")
    return

@router.get("/foreign_key/{id}/exists", tags=["Foreign Key"])
def exists_foreign_key(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if foreign_key_service.exists(db, id) else Response(status_code=404)

@router.get("/foreign_key/{id}/column", response_model=List[ForeignKey], tags=["Foreign Key"])
def read_foreign_keys_by_column(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    foreign_keys = foreign_key_service.get_by_column_id(db, id, skip=skip, limit=limit)
    return foreign_keys
