from sqlalchemy.orm import Session
from app import models
from app.schemas.user import UserCreate
from datetime import datetime
from hashlib import sha256


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    hashed_pw = sha256(user.password.encode("utf-8")).hexdigest()
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
