from sqlalchemy import Column, String, Integer, Date, Boolean, Text, ForeignKey
from .base import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # спортивное, научное, культурное, общественное
    name = Column(String(100), nullable=False)
    event_date = Column(Date, nullable=False)
    is_completed = Column(Boolean, default=False)
    results = Column(Text)
