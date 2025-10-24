from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user as user_crud,wallet as wallet_crud
from app.schemas import user as schemas
from app.database import get_db
from app.models import User
from app.schemas.wallet import WalletRead
from app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Create a new user TODO: by authenticated ADMIN only
@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

# List all users TODO: by authenticated ADMIN only
@router.get("/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    users = user_crud.get_users(db)
    return users

# Get user by ID or email TODO: by authenticated ADMIN only
@router.get("/by_id", response_model=schemas.UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get user by ID or email TODO: by authenticated ADMIN only
@router.get("/by_email", response_model=schemas.UserRead)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get wallets of the current authenticated user
@router.get("/my_wallets", response_model=list[WalletRead])
def read_my_wallets(
    current_user : User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="not authenticated"
            )    
    return wallet_crud.get_wallets_by_user_id(db, current_user.id)

@router.delete("/{user_id}/", response_model=dict)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
    ):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user(db, db_user)
    return {"detail": "User deleted"}

@router.put("/{user_id}/", response_model=schemas.UserRead)
def update_user(
    user_id: int,
    new_data: dict,
    db: Session = Depends(get_db)
    ):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = user_crud.update_user(db, db_user, new_data)
    return updated_user