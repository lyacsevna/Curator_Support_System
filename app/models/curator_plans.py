from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from .base import Base


class CuratorPlan(Base):
    __tablename__ = "curator_plans"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    name = Column(String(100), nullable=False)
    event_datetime = Column(DateTime, nullable=False)
    location = Column(String(100))
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    completion_notes = Column(Text)

