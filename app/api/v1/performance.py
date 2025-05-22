from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas.performance import Performance, PerformanceCreate, PerformanceUpdate
from ...crud.performance import (
    get_performance_record, get_performance_records,
    get_student_performance, create_performance_record,
    update_performance_record, delete_performance_record
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

@router.post("/", response_model=Performance)
def create_performance_record_endpoint(
    performance: PerformanceCreate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    return create_performance_record(db=db, performance=performance)

@router.get("/", response_model=List[Performance])
def read_performance_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    performance = get_performance_records(db, skip=skip, limit=limit)
    return performance

@router.get("/student/{student_id}", response_model=List[Performance])
def read_student_performance(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    performance = get_student_performance(db, student_id=student_id, skip=skip, limit=limit)
    if performance is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return performance

@router.get("/{record_id}", response_model=Performance)
def read_performance_record(record_id: int, db: Session = Depends(get_db)):
    performance = get_performance_record(db, record_id=record_id)
    if performance is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return performance

@router.put("/{record_id}", response_model=Performance)
def update_performance_record_endpoint(
    record_id: int,
    performance: PerformanceUpdate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_performance = update_performance_record(db, record_id=record_id, performance=performance)
    if db_performance is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_performance

@router.delete("/{record_id}")
def delete_performance_record_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_performance = delete_performance_record(db, record_id=record_id)
    if db_performance is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}