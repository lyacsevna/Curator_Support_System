from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas.rewards import Reward, RewardCreate
from ...crud.rewards import (
    get_reward_records, get_student_rewards,
    create_reward_record
)
from ...database import get_db
from ...models.curators import Curator
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_curator(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    curator = db.query(Curator).filter(Curator.email == email).first()
    if curator is None:
        raise credentials_exception
    return curator

@router.post("/", response_model=Reward)
def create_reward(
    reward: RewardCreate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    return create_reward_record(db=db, reward=reward)

@router.get("/", response_model=List[Reward])
def read_reward_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = get_reward_records(db, skip=skip, limit=limit)
    return records

@router.get("/student/{student_id}", response_model=List[Reward])
def read_student_rewards(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    records = get_student_rewards(db, student_id=student_id, skip=skip, limit=limit)
    if records is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return records