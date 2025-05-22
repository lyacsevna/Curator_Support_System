from sqlalchemy import Column, String, Text, Integer
from .base import Base


class StudyProgram(Base):
    __tablename__ = "study_programs"
    id = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
