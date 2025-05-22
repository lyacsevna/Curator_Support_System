from sqlalchemy import Column, String, Integer, Date, ForeignKey, CheckConstraint
from .base import Base


class Dormitory(Base):
    __tablename__ = "dormitory"
    __table_args__ = (
        CheckConstraint('check_out_date IS NULL OR check_out_date > check_in_date', name='valid_dates'),
    )

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    dorm_number = Column(String(10), nullable=False)
    room = Column(String(10), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date)
