from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from .base import BaseSchema


class RewardBase(BaseModel):
    student_id: int
    reward_type: str = Field(..., pattern="^(поощрение|взыскание)$")
    reward_date: date
    reason: str
    order_number: Optional[str] = Field(None, max_length=50)


class RewardCreate(RewardBase):
    pass


class Reward(RewardBase, BaseSchema):
    id: int
