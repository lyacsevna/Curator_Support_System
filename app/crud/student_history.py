from sqlalchemy.orm import Session
from ..models.student_history import StudentHistory
from ..schemas.student_history import StudentHistoryCreate

def get_history_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(StudentHistory).offset(skip).limit(limit).all()

def get_history_for_student(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(StudentHistory).filter(StudentHistory.student_id == student_id).offset(skip).limit(limit).all()

def create_history_record(db: Session, history: StudentHistoryCreate):
    db_history = StudentHistory(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history