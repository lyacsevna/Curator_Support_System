from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .study_programs import StudyProgram
from .curators import Curator
from .students import Student

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    study_program_id = Column(Integer, ForeignKey("study_programs.id"))
    study_form = Column(String(15), nullable=False)  # очная, заочная, очно-заочная
    curator_id = Column(Integer, ForeignKey("curators.id"))
    creation_year = Column(Integer, nullable=False)
    current_course = Column(Integer, nullable=False)  # 1-6
