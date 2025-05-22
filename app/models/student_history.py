from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from .base import Base


class StudentHistory(Base):
    __tablename__ = "student_history"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    action = Column(String(20), nullable=False)  # зачислен, переведен, отчислен, восстановлен, академический отпуск
    action_date = Column(Date, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    notes = Column(Text)
