from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from ...schemas.documents import Document, DocumentCreate
from ...crud.documents import (
    get_document, get_documents, get_entity_documents,
    create_document_record, delete_document_record
)
from ...database import get_db
from ...models.curators import Curator
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from datetime import datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_curator(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    curator = db.query(Curator).filter(Curator.email == email).first()
    if curator is None:
        raise credentials_exception
    return curator


@router.post("/upload", response_model=Document)
async def upload_document(
        entity_type: str,
        entity_id: int,
        document_type: str,
        description: str,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_curator: Curator = Depends(get_current_curator)
):
    # Create uploads directory if not exists
    os.makedirs("uploads", exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{timestamp}_{entity_type}_{entity_id}{file_extension}"
    file_path = os.path.join("uploads", filename)

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Create document record
    document_data = DocumentCreate(
        entity_type=entity_type,
        entity_id=entity_id,
        file_path=file_path,
        document_type=document_type,
        description=description
    )

    return create_document_record(db=db, document=document_data)


@router.get("/", response_model=List[Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = get_documents(db, skip=skip, limit=limit)
    return documents


@router.get("/entity/{entity_type}/{entity_id}", response_model=List[Document])
def read_entity_documents(
        entity_type: str,
        entity_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    documents = get_entity_documents(db, entity_type=entity_type, entity_id=entity_id, skip=skip, limit=limit)
    return documents


@router.get("/{document_id}", response_model=Document)
def read_document(document_id: int, db: Session = Depends(get_db)):
    document = get_document(db, document_id=document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}")
def delete_document(
        document_id: int,
        db: Session = Depends(get_db),
        current_curator: Curator = Depends(get_current_curator)
):
    document = delete_document_record(db, document_id=document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete physical file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    return {"message": "Document deleted successfully"}