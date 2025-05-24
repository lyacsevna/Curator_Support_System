from sqlalchemy import Column, String, Boolean, Integer
from .base import Base


class Curator(Base):
    __tablename__ = "curators"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    phone = Column(String(20))
