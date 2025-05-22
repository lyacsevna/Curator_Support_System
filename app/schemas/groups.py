from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseSchema


class GroupBase(BaseModel):
    name: str = Field(..., max_length=20)
    study_program_id: int
    study_form: str = Field(..., pattern="^(очная|заочная|очно-заочная)$")
    curator_id: int
    creation_year: int = Field(..., ge=2000, le=2100)
    current_course: int = Field(..., ge=1, le=6)


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=20)
    study_program_id: Optional[int] = None
    study_form: Optional[str] = Field(None, pattern="^(очная|заочная|очно-заочная)$")
    curator_id: Optional[int] = None
    creation_year: Optional[int] = Field(None, ge=2000, le=2100)
    current_course: Optional[int] = Field(None, ge=1, le=6)


class Group(GroupBase, BaseSchema):
    id: int
