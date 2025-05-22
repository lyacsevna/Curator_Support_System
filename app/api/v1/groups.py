from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas.groups import Group, GroupCreate, GroupUpdate
from ...crud.groups import (
    get_group, get_groups, create_group,
    update_group, delete_group
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

@router.post("/", response_model=Group)
def create_new_group(
    group: GroupCreate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    return create_group(db=db, group=group)

@router.get("/", response_model=List[Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = get_groups(db, skip=skip, limit=limit)
    return groups

@router.get("/{group_id}", response_model=Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = get_group(db, group_id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.put("/{group_id}", response_model=Group)
def update_existing_group(
    group_id: int,
    group: GroupUpdate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_group = update_group(db, group_id=group_id, group=group)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.delete("/{group_id}")
def delete_existing_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_group = delete_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"message": "Group deleted successfully"}