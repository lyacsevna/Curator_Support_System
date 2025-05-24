from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)  # Добавляем первичный ключ
    entity_type = Column(String(20), nullable=False)  # student, activity, support, reward, performance
    entity_id = Column(Integer, nullable=False)
    file_path = Column(String(255), nullable=False)
    upload_date = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP')  # Исправлено на CURRENT_TIMESTAMP
    document_type = Column(String(100), nullable=False)
    description = Column(Text)



