from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.index import Index, IndexCreate
from services.index_service import index_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/index", response_model=Index, status_code=status.HTTP_201_CREATED, tags=["Index"])
def create_index(index: IndexCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    index_service.validate_fields(index)
    return index_service.create(db, index)

@router.get("/index", response_model=List[Index], tags=["Index"])
def read_indexes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    indexes = index_service.get_all(db, skip=skip, limit=limit)
    return indexes

@router.get("/index/{id}", response_model=Index, tags=["Index"])
def read_index(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    index = index_service.get(db, id)
    if index is None:
        raise HTTPException(status_code=404, detail="Index not found")
    return index

@router.put("/index/{id}", response_model=Index, tags=["Index"])
def update_index(id: int, index: IndexCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    index_service.validate_fields(index)
    db_index = index_service.update(db, id, index)
    if db_index is None:
        raise HTTPException(status_code=404, detail="Index not found")
    return db_index

@router.delete("/index/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Index"])
def delete_index(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    index = index_service.delete(db, id)
    if index is None:
        raise HTTPException(status_code=404, detail="Index not found")
    return

@router.get("/index/{id}/exists", tags=["Column"])
def exists_index(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if index_service.exists(db, id) else Response(status_code=404)

@router.get("/index/{id}/table", response_model=List[Index], tags=["Index"])
def read_indexes_by_table(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    indexes = index_service.get_by_table_id(db, id, skip=skip, limit=limit)
    return indexes
