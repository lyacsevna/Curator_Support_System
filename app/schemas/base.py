from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.strftime("%Y-%m-%d") if v else None,
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }