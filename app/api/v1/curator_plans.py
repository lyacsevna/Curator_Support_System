from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas.curator_plans import CuratorPlan, CuratorPlanCreate, CuratorPlanUpdate
from ...crud.curator_plans import (
    get_curator_plan, get_curator_plans, get_group_plans,
    create_curator_plan, update_curator_plan, delete_curator_plan
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

@router.post("/", response_model=CuratorPlan)
def create_curator_plan(
    plan: CuratorPlanCreate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    return create_curator_plan(db=db, plan=plan)

@router.get("/", response_model=List[CuratorPlan])
def read_curator_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plans = get_curator_plans(db, skip=skip, limit=limit)
    return plans

@router.get("/group/{group_id}", response_model=List[CuratorPlan])
def read_group_plans(
    group_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    plans = get_group_plans(db, group_id=group_id, skip=skip, limit=limit)
    if plans is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return plans

@router.get("/{plan_id}", response_model=CuratorPlan)
def read_curator_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = get_curator_plan(db, plan_id=plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.put("/{plan_id}", response_model=CuratorPlan)
def update_curator_plan(
    plan_id: int,
    plan: CuratorPlanUpdate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_plan = update_curator_plan(db, plan_id=plan_id, plan=plan)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan

@router.delete("/{plan_id}")
def delete_curator_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_plan = delete_curator_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted successfully"}