from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
from .base import BaseSchema


class StudentBase(BaseModel):
    last_name: str = Field(..., max_length=50)
    first_name: str = Field(..., max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = None
    group_id: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    is_active: bool = True
    education_type: str = Field(..., pattern="^(бюджет|контракт|целевое)$")
    gender: Optional[str] = Field(None, pattern="^(мужской|женский)$")
    is_from_rural_area: bool = False
    is_from_other_region: bool = False
    is_orphan: bool = False
    previous_education: Optional[str] = Field(
        None, pattern="^(высшее|общее среднее|специальное среднее)$"
    )


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    last_name: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = None
    group_id: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    is_active: Optional[bool] = None
    education_type: Optional[str] = Field(None, pattern="^(бюджет|контракт|целевое)$")
    gender: Optional[str] = Field(None, pattern="^(мужской|женский)$")
    is_from_rural_area: Optional[bool] = None
    is_from_other_region: Optional[bool] = None
    is_orphan: Optional[bool] = None
    previous_education: Optional[str] = Field(
        None, pattern="^(высшее|общее среднее|специальное среднее)$"
    )


class Student(StudentBase, BaseSchema):
    id: int
