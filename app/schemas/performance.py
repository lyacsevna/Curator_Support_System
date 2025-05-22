from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from .base import BaseSchema

class PerformanceBase(BaseModel):
    student_id: int
    subject: str = Field(..., max_length=100)
    teacher: Optional[str] = Field(None, max_length=100)
    grade: Optional[int] = Field(None, ge=1, le=10)
    exam_date: date
    notes: Optional[str] = None

class PerformanceCreate(PerformanceBase):
    pass

class PerformanceUpdate(BaseModel):
    subject: Optional[str] = Field(None, max_length=100)
    teacher: Optional[str] = Field(None, max_length=100)
    grade: Optional[int] = Field(None, ge=1, le=10)
    exam_date: Optional[date] = None
    notes: Optional[str] = None

class Performance(PerformanceBase, BaseSchema):
    id: int