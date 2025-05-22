from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from .base import BaseSchema


class ActivityBase(BaseModel):
    student_id: int
    activity_type: str = Field(..., pattern="^(спортивное|научное|культурное|общественное)$")
    name: str = Field(..., max_length=100)
    event_date: date
    is_completed: bool = False
    results: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    activity_type: Optional[str] = Field(None, pattern="^(спортивное|научное|культурное|общественное)$")
    name: Optional[str] = Field(None, max_length=100)
    event_date: Optional[date] = None
    is_completed: Optional[bool] = None
    results: Optional[str] = None


class Activity(ActivityBase, BaseSchema):
    id: int
