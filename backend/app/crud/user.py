from sqlalchemy.orm import Session
from app import models
from app.schemas.user import UserCreate, UserRead
from datetime import datetime
from app.core.security import get_password_hash


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> UserRead:
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
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

def update_user(
        db: Session,
        db_user: models.User,
        new_data: dict
        ) -> UserRead:
    for key, value in new_data.items():
        if hasattr(db_user, key) and value is not None:
            setattr(db_user, key, value)
    if "password" in new_data and new_data["password"] is not None:
        db_user.hashed_password = get_password_hash(new_data["password"])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()