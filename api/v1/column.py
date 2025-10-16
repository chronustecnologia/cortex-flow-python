from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.column import Column, ColumnCreate
from services.column_service import column_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/column", response_model=Column, status_code=status.HTTP_201_CREATED, tags=["Column"])
def create_column(column: ColumnCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    column_service.validate_fields(column)
    return column_service.create(db, column)

@router.get("/column", response_model=List[Column], tags=["Column"])
def read_columns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    columns = column_service.get_all(db, skip=skip, limit=limit)
    return columns

@router.get("/column/{id}", response_model=Column, tags=["Column"])
def read_column(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    column = column_service.get(db, id)
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return column

@router.put("/column/{id}", response_model=Column, tags=["Column"])
def update_column(id: int, column: ColumnCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    column_service.validate_fields(column)
    db_column = column_service.update(db, id, column)
    if db_column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return db_column

@router.delete("/column/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Column"])
def delete_column(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    column = column_service.delete(db, id)
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return

@router.get("/column/{id}/exists", tags=["Column"])
def exists_column(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if column_service.exists(db, id) else Response(status_code=404)

@router.get("/column/{id}/table", response_model=List[Column], tags=["Column"])
def read_columns_by_table(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    columns = column_service.get_by_table_id(db, id, skip=skip, limit=limit)
    return columns
