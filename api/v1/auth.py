from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from db.session import get_db
from core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from services.credential_service import credential_service

router = APIRouter()

@router.post("/auth", tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    credential = credential_service.get_by_client_id(db, client_id=form_data.username)
    if not credential or credential.client_secret != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client_id or client_secret",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=credential.client_id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


