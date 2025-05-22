from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from .base import Base


class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    teacher = Column(String(100))
    grade = Column(Integer)  # 1-10
    exam_date = Column(Date, nullable=False)
    notes = Column(Text)
