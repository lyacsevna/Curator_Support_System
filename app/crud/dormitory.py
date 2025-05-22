from sqlalchemy.orm import Session
from ..models.dormitory import Dormitory
from ..schemas.dormitory import DormitoryCreate, DormitoryUpdate

def get_dormitory_record(db: Session, record_id: int):
    return db.query(Dormitory).filter(Dormitory.id == record_id).first()

def get_dormitory_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dormitory).offset(skip).limit(limit).all()

def get_student_dormitory(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(Dormitory).filter(Dormitory.student_id == student_id).offset(skip).limit(limit).all()

def create_dormitory_record(db: Session, dormitory: DormitoryCreate):
    db_dormitory = Dormitory(**dormitory.model_dump())
    db.add(db_dormitory)
    db.commit()
    db.refresh(db_dormitory)
    return db_dormitory

def update_dormitory_record(db: Session, record_id: int, dormitory: DormitoryUpdate):
    db_dormitory = get_dormitory_record(db, record_id)
    if not db_dormitory:
        return None
    update_data = dormitory.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dormitory, key, value)
    db.commit()
    db.refresh(db_dormitory)
    return db_dormitory

def delete_dormitory_record(db: Session, record_id: int):
    db_dormitory = get_dormitory_record(db, record_id)
    if not db_dormitory:
        return None
    db.delete(db_dormitory)
    db.commit()
    return db_dormitory