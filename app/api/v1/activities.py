from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas.activities import Activity, ActivityCreate, ActivityUpdate
from ...crud.activities import (
    get_activity, get_activities, get_student_activities,
    create_activity, update_activity, delete_activity
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

@router.post("/", response_model=Activity)
def create_new_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    return create_activity(db=db, activity=activity)

@router.get("/", response_model=List[Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    activities = get_activities(db, skip=skip, limit=limit)
    return activities

@router.get("/student/{student_id}", response_model=List[Activity])
def read_student_activities(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    activities = get_student_activities(db, student_id=student_id, skip=skip, limit=limit)
    if activities is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return activities

@router.get("/{activity_id}", response_model=Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = get_activity(db, activity_id=activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.put("/{activity_id}", response_model=Activity)
def update_existing_activity(
    activity_id: int,
    activity: ActivityUpdate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_activity = update_activity(db, activity_id=activity_id, activity=activity)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@router.delete("/{activity_id}")
def delete_existing_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_activity = delete_activity(db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"}