from sqlalchemy.orm import Session
from ..models.activities import Activity
from ..schemas.activities import ActivityCreate, ActivityUpdate

def get_activity(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()

def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Activity).offset(skip).limit(limit).all()

def get_student_activities(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(Activity).filter(Activity.student_id == student_id).offset(skip).limit(limit).all()

def create_activity(db: Session, activity: ActivityCreate):
    db_activity = Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def update_activity(db: Session, activity_id: int, activity: ActivityUpdate):
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return None
    update_data = activity.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_activity, key, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int):
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return None
    db.delete(db_activity)
    db.commit()
    return db_activity