from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseSchema


class StudyProgramBase(BaseModel):
    code: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class StudyProgramCreate(StudyProgramBase):
    pass


class StudyProgramUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class StudyProgram(StudyProgramBase, BaseSchema):
    id: int
