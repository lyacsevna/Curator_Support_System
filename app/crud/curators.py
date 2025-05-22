from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.curators import Curator
from ..schemas.curators import CuratorCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_curator(db: Session, curator_id: int):
    return db.query(Curator).filter(Curator.id == curator_id).first()

def get_curators(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Curator).offset(skip).limit(limit).all()

def get_curator_by_email(db: Session, email: str):
    return db.query(Curator).filter(Curator.email == email).first()

def create_curator(db: Session, curator: CuratorCreate):
    hashed_password = pwd_context.hash(curator.password)
    db_curator = Curator(
        email=curator.email,
        last_name=curator.last_name,
        first_name=curator.first_name,
        middle_name=curator.middle_name,
        phone=curator.phone,
        password_hash=hashed_password
    )
    db.add(db_curator)
    db.commit()
    db.refresh(db_curator)
    return db_curator

def authenticate_curator(db: Session, email: str, password: str):
    curator = get_curator_by_email(db, email)
    if not curator:
        return False
    if not pwd_context.verify(password, curator.password_hash):
        return False
    return curator