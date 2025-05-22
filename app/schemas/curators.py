from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from .base import BaseSchema


class CuratorBase(BaseModel):
    email: EmailStr
    last_name: str = Field(..., max_length=50)
    first_name: str = Field(..., max_length=50)


class CuratorCreate(CuratorBase):
    password: str = Field(..., min_length=8)
    middle_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)


class CuratorUpdate(BaseModel):
    email: Optional[EmailStr] = None
    last_name: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)

    is_active: Optional[bool] = None


class Curator(CuratorBase, BaseSchema):
    id: int
    middle_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
