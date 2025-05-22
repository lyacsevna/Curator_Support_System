from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import BaseSchema


class DocumentBase(BaseModel):
    entity_type: str = Field(..., pattern="^(student|activity|support|reward|performance)$")
    entity_id: int
    file_path: str = Field(..., max_length=255)
    document_type: str = Field(..., max_length=100)
    description: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase, BaseSchema):
    id: int
    upload_date: datetime
