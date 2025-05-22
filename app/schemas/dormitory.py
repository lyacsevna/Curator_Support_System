from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
from .base import BaseSchema


class DormitoryBase(BaseModel):
    student_id: int
    dorm_number: str = Field(..., max_length=10)
    room: str = Field(..., max_length=10)
    check_in_date: date
    check_out_date: Optional[date] = None

    @validator('check_out_date')
    def validate_dates(cls, v, values):
        if v and 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError("Check-out date must be after check-in date")
        return v


class DormitoryCreate(DormitoryBase):
    pass


class DormitoryUpdate(BaseModel):
    dorm_number: Optional[str] = Field(None, max_length=10)
    room: Optional[str] = Field(None, max_length=10)
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None

    @validator('check_out_date')
    def validate_dates(cls, v, values):
        if v and 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError("Check-out date must be after check-in date")
        return v


class Dormitory(DormitoryBase, BaseSchema):
    id: int
