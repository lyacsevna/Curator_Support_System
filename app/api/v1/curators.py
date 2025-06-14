from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from typing import List
from ...schemas.curators import Curator, CuratorCreate, Token
from ...crud.curators import (
    get_curator, get_curators, create_curator,
    get_curator_by_email
)
from ...database import get_db
from datetime import timedelta, datetime
import os

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta = None, SECRET_KEY=None, ALGORITHM=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
    # Получаем куратора по email
    curator = get_curator_by_email(db, form_data.username)
    # Проверяем, существует ли куратор и совпадает ли пароль (без хеширования)
    if not curator or curator.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    access_token = create_access_token(
        data={"sub": curator.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
