from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from ...main import create_access_token
from ...schemas.curators import Curator, CuratorCreate, Token
from ...crud.curators import (
    get_curator, get_curators, create_curator,
    get_curator_by_email, authenticate_curator
)
from ...database import get_db
from datetime import timedelta
from jose import jwt
import os

router = APIRouter()

@router.post("/", response_model=Curator)
def create_new_curator(curator: CuratorCreate, db: Session = Depends(get_db)):
    db_curator = get_curator_by_email(db, email=curator.email)
    if db_curator:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_curator(db=db, curator=curator)

@router.get("/", response_model=List[Curator])
def read_curators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    curators = get_curators(db, skip=skip, limit=limit)
    return curators

@router.get("/{curator_id}", response_model=Curator)
def read_curator(curator_id: int, db: Session = Depends(get_db)):
    db_curator = get_curator(db, curator_id=curator_id)
    if db_curator is None:
        raise HTTPException(status_code=404, detail="Curator not found")
    return db_curator

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    curator = authenticate_curator(db, form_data.username, form_data.password)
    if not curator:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": curator.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}