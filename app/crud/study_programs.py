from sqlalchemy.orm import Session
from ..models.study_programs import StudyProgram
from ..schemas.study_programs import StudyProgramCreate, StudyProgramUpdate

def get_program(db: Session, program_id: int):
    return db.query(StudyProgram).filter(StudyProgram.id == program_id).first()

def get_programs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(StudyProgram).offset(skip).limit(limit).all()

def create_program(db: Session, program: StudyProgramCreate):
    db_program = StudyProgram(**program.model_dump())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

def update_program(db: Session, program_id: int, program: StudyProgramUpdate):
    db_program = get_program(db, program_id)
    if not db_program:
        return None
    update_data = program.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_program, key, value)
    db.commit()
    db.refresh(db_program)
    return db_program

def delete_program(db: Session, program_id: int):
    db_program = get_program(db, program_id)
    if not db_program:
        return None
    db.delete(db_program)
    db.commit()
    return db_program