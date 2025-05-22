from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas.students import Student, StudentCreate, StudentUpdate
from ...crud.students import (
    get_student, get_students, get_students_by_group,
    create_student, update_student, delete_student
)
from ...database import get_db

router = APIRouter()

@router.post("/", response_model=Student)
def create_new_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db=db, student=student)

@router.get("/", response_model=List[Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = get_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=Student)
def update_existing_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = update_student(db, student_id=student_id, student=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/{student_id}")
def delete_existing_student(student_id: int, db: Session = Depends(get_db)):
    db_student = delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
