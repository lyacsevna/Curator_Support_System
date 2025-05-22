from sqlalchemy.orm import Session
from ..models.documents import Document
from ..schemas.documents import DocumentCreate

def get_document(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Document).offset(skip).limit(limit).all()

def get_entity_documents(db: Session, entity_type: str, entity_id: int, skip: int = 0, limit: int = 100):
    return db.query(Document).filter(
        Document.entity_type == entity_type,
        Document.entity_id == entity_id
    ).offset(skip).limit(limit).all()

def create_document_record(db: Session, document: DocumentCreate):
    db_document = Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_document_record(db: Session, document_id: int):
    db_document = get_document(db, document_id)
    if not db_document:
        return None
    db.delete(db_document)
    db.commit()
    return db_document