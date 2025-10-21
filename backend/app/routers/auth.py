from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import authenticate_user, login_get_token

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(user_email=form_data.useremail, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = login_get_token(user)
    return {"access_token": token, "token_type": "bearer"}