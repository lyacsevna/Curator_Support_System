from sqlalchemy.orm import Session
from ..models.financial_support import FinancialSupport
from ..schemas.financial_support import FinancialSupportCreate

def get_financial_support_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FinancialSupport).offset(skip).limit(limit).all()

def get_student_financial_support(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(FinancialSupport).filter(FinancialSupport.student_id == student_id).offset(skip).limit(limit).all()

def create_financial_support_record(db: Session, financial_support: FinancialSupportCreate):
    db_support = FinancialSupport(**financial_support.model_dump())
    db.add(db_support)
    db.commit()
    db.refresh(db_support)
    return db_support