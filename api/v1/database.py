from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.database import Database, DatabaseCreate
from schemas.database_schema import DatabaseSchemaExport
from services.database_service import database_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/database", response_model=Database, status_code=status.HTTP_201_CREATED, tags=["Database"])
def create_database(database: DatabaseCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    database_service.validate_fields(database)
    return database_service.create(db, database)

@router.get("/database", response_model=List[Database], tags=["Database"])
def read_databases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    databases = database_service.get_all(db, skip=skip, limit=limit)
    return databases

@router.get("/database/{id}", response_model=Database, tags=["Database"])
def read_database(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    database = database_service.get(db, id)
    if database is None:
        raise HTTPException(status_code=404, detail="Database not found")
    return database

@router.put("/database/{id}", response_model=Database, tags=["Database"])
def update_database(id: int, database: DatabaseCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    database_service.validate_fields(database)
    db_database = database_service.update(db, id, database)
    if db_database is None:
        raise HTTPException(status_code=404, detail="Database not found")
    return db_database

@router.delete("/database/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Database"])
def delete_database(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    database = database_service.delete(db, id)
    if database is None:
        raise HTTPException(status_code=404, detail="Database not found")
    return

@router.get("/database/{id}/exists", tags=["Database"])
def exists_database(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if database_service.exists(db, id) else Response(status_code=404)

@router.get("/database/{database_id}/schema", response_model=DatabaseSchemaExport, tags=["Database"])
def get_database_schema(database_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return database_service.get_database_schema_json(db, database_id)
