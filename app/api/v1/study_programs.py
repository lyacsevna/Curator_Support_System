from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas.study_programs import StudyProgram, StudyProgramCreate, StudyProgramUpdate
from ...crud.study_programs import (
    get_program, get_programs, create_program,
    update_program, delete_program
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

@router.post("/", response_model=StudyProgram)
def create_new_program(
    program: StudyProgramCreate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    return create_program(db=db, program=program)

@router.get("/", response_model=List[StudyProgram])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programs = get_programs(db, skip=skip, limit=limit)
    return programs

@router.get("/{program_id}", response_model=StudyProgram)
def read_program(program_id: int, db: Session = Depends(get_db)):
    program = get_program(db, program_id=program_id)
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@router.put("/{program_id}", response_model=StudyProgram)
def update_existing_program(
    program_id: int,
    program: StudyProgramUpdate,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_program = update_program(db, program_id=program_id, program=program)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_program

@router.delete("/{program_id}")
def delete_existing_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_curator: Curator = Depends(get_current_curator)
):
    db_program = delete_program(db, program_id=program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted successfully"}