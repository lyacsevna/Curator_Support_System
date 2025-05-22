from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from .base import Base

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    reward_type = Column(String(20), nullable=False)  # поощрение, взыскание
    reward_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    order_number = Column(String(50))
