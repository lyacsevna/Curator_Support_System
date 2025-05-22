from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    birth_date = Column(Date)
    group_id = Column(Integer, ForeignKey("groups.id"))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    address = Column(String)
    is_active = Column(Boolean, default=True)
    education_type = Column(String(10), nullable=False)
    gender = Column(String(10))
    is_from_rural_area = Column(Boolean, default=False)
    is_from_other_region = Column(Boolean, default=False)
    is_orphan = Column(Boolean, default=False)
    previous_education = Column(String(20))

    group = relationship("Group", back_populates="students")
    history = relationship("StudentHistory", back_populates="student")
    performance = relationship("Performance", back_populates="student")
    activities = relationship("Activity", back_populates="student")
    financial_support = relationship("FinancialSupport", back_populates="student")
    dormitory = relationship("Dormitory", back_populates="student")
    rewards = relationship("Reward", back_populates="student")

