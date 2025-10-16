from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.relationship import Relationship, RelationshipCreate
from services.relationship_service import relationship_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/relationship", response_model=Relationship, status_code=status.HTTP_201_CREATED, tags=["Relationship"])
def create_relationship(relationship: RelationshipCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    relationship_service.validate_fields(relationship)
    return relationship_service.create(db, relationship)

@router.get("/relationship", response_model=List[Relationship], tags=["Relationship"])
def read_relationships(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    relationships = relationship_service.get_all(db, skip=skip, limit=limit)
    return relationships

@router.get("/relationship/{id}", response_model=Relationship, tags=["Relationship"])
def read_relationship(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    relationship = relationship_service.get(db, id)
    if relationship is None:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return relationship

@router.put("/relationship/{id}", response_model=Relationship, tags=["Relationship"])
def update_relationship(id: int, relationship: RelationshipCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    relationship_service.validate_fields(relationship)
    db_relationship = relationship_service.update(db, id, relationship)
    if db_relationship is None:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return db_relationship

@router.delete("/relationship/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Relationship"])
def delete_relationship(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    relationship = relationship_service.delete(db, id)
    if relationship is None:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return

@router.get("/relationship/{id}/exists", tags=["Column"])
def exists_relationship(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if relationship_service.exists(db, id) else Response(status_code=404)

@router.get("/relationship/{id}/database", response_model=List[Relationship], tags=["Relationship"])
def read_relationships_by_database(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    relationships = relationship_service.get_by_database_id(db, id, skip=skip, limit=limit)
    return relationships


