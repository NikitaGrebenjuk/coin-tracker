from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import user as user_crud
from app.schemas import user as schemas
from app.schemas.wallet import WalletRead
from app.models import User
from app.services.auth_service import get_current_user
from app.crud import wallet as wallet_crud
from app.schemas.auth import Token

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    users = user_crud.get_users(db)
    return users

@router.get("/by_id", response_model=schemas.UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/by_email", response_model=schemas.UserRead)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# @router.get("/my_wallets", response_model=list[WalletRead])
# def read_my_wallets(current_user : User = Depends(get_current_user), db: Session = Depends(get_db)):
#     print(f"DEBUG Current user: {current_user}")
#     if not current_user:
#         raise HTTPException(status_code=404, detail="not authenticated")    
#     return wallet_crud.get_wallets_by_user_id(db, current_user.id)