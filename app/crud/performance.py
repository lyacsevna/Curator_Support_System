from sqlalchemy.orm import Session
from ..models.performance import Performance
from ..schemas.performance import PerformanceCreate, PerformanceUpdate

def get_performance_record(db: Session, record_id: int):
    return db.query(Performance).filter(Performance.id == record_id).first()

def get_performance_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Performance).offset(skip).limit(limit).all()

def get_student_performance(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(Performance).filter(Performance.student_id == student_id).offset(skip).limit(limit).all()

def create_performance_record(db: Session, performance: PerformanceCreate):
    db_performance = Performance(**performance.model_dump())
    db.add(db_performance)
    db.commit()
    db.refresh(db_performance)
    return db_performance

def update_performance_record(db: Session, record_id: int, performance: PerformanceUpdate):
    db_performance = get_performance_record(db, record_id)
    if not db_performance:
        return None
    update_data = performance.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_performance, key, value)
    db.commit()
    db.refresh(db_performance)
    return db_performance

def delete_performance_record(db: Session, record_id: int):
    db_performance = get_performance_record(db, record_id)
    if not db_performance:
        return None
    db.delete(db_performance)
    db.commit()
    return db_performance