from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas.dormitory import Dormitory, DormitoryCreate, DormitoryUpdate
from ...crud.dormitory import (
    get_dormitory_record, get_dormitory_records,
    get_student_dormitory, create_dormitory_record,
    update_dormitory_record, delete_dormitory_record
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

@router.post("/", response_model=Dormitory)
def create_dormitory_record_endpoint(
    dormitory: DormitoryCreate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    return create_dormitory_record(db=db, dormitory=dormitory)

@router.get("/", response_model=List[Dormitory])
def read_dormitory_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = get_dormitory_records(db, skip=skip, limit=limit)
    return records

@router.get("/student/{student_id}", response_model=List[Dormitory])
def read_student_dormitory(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    records = get_student_dormitory(db, student_id=student_id, skip=skip, limit=limit)
    if records is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return records

@router.get("/{record_id}", response_model=Dormitory)
def read_dormitory_record(record_id: int, db: Session = Depends(get_db)):
    record = get_dormitory_record(db, record_id=record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/{record_id}", response_model=Dormitory)
def update_dormitory_record_endpoint(
    record_id: int,
    dormitory: DormitoryUpdate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_record = update_dormitory_record(db, record_id=record_id, dormitory=dormitory)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.delete("/{record_id}")
def delete_dormitory_record_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_record = delete_dormitory_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}