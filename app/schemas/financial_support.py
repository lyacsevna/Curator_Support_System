from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal
from .base import BaseSchema


class FinancialSupportBase(BaseModel):
    student_id: int
    support_type: str = Field(..., pattern="^(стипендия|грант|материальная помощь|социальная поддержка)$")
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    period: str = Field(..., max_length=20)
    reason: Optional[str] = None
    payment_date: date


class FinancialSupportCreate(FinancialSupportBase):
    pass


class FinancialSupport(FinancialSupportBase, BaseSchema):
    id: int
