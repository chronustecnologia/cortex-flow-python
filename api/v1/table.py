from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.table import Table, TableCreate
from services.table_service import table_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/table", response_model=Table, status_code=status.HTTP_201_CREATED, tags=["Table"])
def create_table(table: TableCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    table_service.validate_fields(table)
    return table_service.create(db, table)

@router.get("/table", response_model=List[Table], tags=["Table"])
def read_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tables = table_service.get_all(db, skip=skip, limit=limit)
    return tables

@router.get("/table/{id}", response_model=Table, tags=["Table"])
def read_table(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    table = table_service.get(db, id)
    if table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.put("/table/{id}", response_model=Table, tags=["Table"])
def update_table(id: int, table: TableCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    table_service.validate_fields(table)
    db_table = table_service.update(db, id, table)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return db_table

@router.delete("/table/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Table"])
def delete_table(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    table = table_service.delete(db, id)
    if table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return

@router.get("/table/{id}/exists", tags=["Table"])
def exists_table(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if table_service.exists(db, id) else Response(status_code=404)

@router.get("/table/{id}/database", response_model=List[Table], tags=["Table"])
def read_tables_by_database(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tables = table_service.get_by_database_id(db, id, skip=skip, limit=limit)
    return tables
