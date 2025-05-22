from sqlalchemy.orm import Session
from ..models.curator_plans import CuratorPlan
from ..schemas.curator_plans import CuratorPlanCreate, CuratorPlanUpdate

def get_curator_plan(db: Session, plan_id: int):
    return db.query(CuratorPlan).filter(CuratorPlan.id == plan_id).first()

def get_curator_plans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CuratorPlan).offset(skip).limit(limit).all()

def get_group_plans(db: Session, group_id: int, skip: int = 0, limit: int = 100):
    return db.query(CuratorPlan).filter(CuratorPlan.group_id == group_id).offset(skip).limit(limit).all()

def create_curator_plan(db: Session, plan: CuratorPlanCreate):
    db_plan = CuratorPlan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def update_curator_plan(db: Session, plan_id: int, plan: CuratorPlanUpdate):
    db_plan = get_curator_plan(db, plan_id)
    if not db_plan:
        return None
    update_data = plan.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plan, key, value)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def delete_curator_plan(db: Session, plan_id: int):
    db_plan = get_curator_plan(db, plan_id)
    if not db_plan:
        return None
    db.delete(db_plan)
    db.commit()
    return db_plan