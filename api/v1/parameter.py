from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.parameter import Parameter, ParameterCreate
from services.parameter_service import parameter_service
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/parameter", response_model=Parameter, status_code=status.HTTP_201_CREATED, tags=["Parameter"])
def create_parameter(parameter: ParameterCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    parameter_service.validate_fields(parameter)
    return parameter_service.create(db, parameter)

@router.get("/parameter", response_model=List[Parameter], tags=["Parameter"])
def read_parameters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    parameters = parameter_service.get_all(db, skip=skip, limit=limit)
    return parameters

@router.get("/parameter/{id}", response_model=Parameter, tags=["Parameter"])
def read_parameter(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    parameter = parameter_service.get(db, id)
    if parameter is None:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return parameter

@router.put("/parameter/{id}", response_model=Parameter, tags=["Parameter"])
def update_parameter(id: int, parameter: ParameterCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    parameter_service.validate_fields(parameter)
    db_parameter = parameter_service.update(db, id, parameter)
    if db_parameter is None:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return db_parameter

@router.delete("/parameter/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Parameter"])
def delete_parameter(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    parameter = parameter_service.delete(db, id)
    if parameter is None:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return

@router.get("/parameter/{id}/exists", tags=["Table"])
def exists_parameter(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return Response(status_code=200) if parameter_service.exists(db, id) else Response(status_code=404)

@router.get("/parameter/{code}/code", response_model=Parameter, tags=["Parameter"])
def read_parameter_by_code(code: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    parameter = parameter_service.get_by_code(db, code)
    if parameter is None:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return parameter
