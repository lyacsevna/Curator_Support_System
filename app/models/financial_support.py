from sqlalchemy import Column, String, Integer, Date, Numeric, Text, ForeignKey
from .base import Base


class FinancialSupport(Base):
    __tablename__ = "financial_support"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    support_type = Column(String(50), nullable=False)  # стипендия, грант, материальная помощь, социальная поддержка
    amount = Column(Numeric(10, 2), nullable=False)
    period = Column(String(20), nullable=False)
    reason = Column(Text)
    payment_date = Column(Date, nullable=False)
