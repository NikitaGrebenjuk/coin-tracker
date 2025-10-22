from app.core.security import verify_password, create_access_token
from app.crud.user import get_user_by_email, get_user_by_id

from fastapi import Depends, HTTPException, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from sqlalchemy.orm import Session

from app.schemas.user import UserRead


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate_user(user_email: str, password: str, db: Session ):
    user = get_user_by_email(db, user_email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def login_get_token(user):
    data = {"sub": str(user.id), "role": user.role if hasattr(user, "role") else "user"}
    access_token = create_access_token(data=data)
    return access_token

def get_current_user( db: Session, token: str = Depends(oauth2_scheme)) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"DEBUG auth_service Current token: {token}")
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    return user