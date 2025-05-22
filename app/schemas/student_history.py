from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from .base import BaseSchema


class StudentHistoryBase(BaseModel):
    student_id: int
    action: str = Field(..., pattern="^(зачислен|переведен|отчислен|восстановлен|академический отпуск)$")
    action_date: date
    group_id: Optional[int] = None
    notes: Optional[str] = None


class StudentHistoryCreate(StudentHistoryBase):
    pass


class StudentHistory(StudentHistoryBase, BaseSchema):
    id: int
