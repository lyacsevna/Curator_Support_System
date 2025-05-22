from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import BaseSchema


class CuratorPlanBase(BaseModel):
    group_id: int
    name: str = Field(..., max_length=100)
    event_datetime: datetime
    location: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_completed: bool = False


class CuratorPlanCreate(CuratorPlanBase):
    pass


class CuratorPlanUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    event_datetime: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    completion_notes: Optional[str] = None


class CuratorPlan(CuratorPlanBase, BaseSchema):
    id: int
    completion_notes: Optional[str] = None

