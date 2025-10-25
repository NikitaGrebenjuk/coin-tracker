from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth import  Token
from app.services.auth_service import authenticate_user, login_get_token
from app.crud import user as user_crud
from app.schemas import user as schemas
from app.database import get_db

router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
    )

# Login endpoint
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    user = authenticate_user(
        user_email=form_data.username,
        password=form_data.password,
        db=db
        )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
            )
    token = login_get_token(user)
    return {
        "access_token": token,
        "token_type": "bearer"
        }

# List all users TODO: by authenticated ADMIN only
@router.get("/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    users = user_crud.get_users(db)
    return users