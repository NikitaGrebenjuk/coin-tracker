import os
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt, JWTError

# Einstellungen, aus ENV laden (Default-Werte für lokale Entwicklung)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "please_change_me_in_production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

# Passlib Kontext für bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Passwort-Utilities ---------------------------------------------------
def get_password_hash(password: str) -> str:
    """
    Erzeugt einen bcrypt Hash für das gegebene Passwort.
    Stellt sicher, dass das Passwort nicht länger als 72 Bytes ist.
    """

    print("DEBUG - Raw password input:", password)
    print("DEBUG - Type:", type(password))
    try:
        password_bytes = password.encode("utf-8")
        print("DEBUG - Encoded bytes length:", len(password_bytes))
    except Exception as e:
        print("DEBUG - Encoding error:", e)
        raise

    if len(password_bytes) > 72:
        raise ValueError("Password too long for bcrypt (max 72 bytes allowed)")

    return pwd_context.hash(password)   


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Prüft ein Klartext-Passwort gegen den gespeicherten Hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT Utilities -------------------------------------------------------
def create_access_token(data: dict) -> str:
    """
    Erzeugt ein JWT mit den Claims aus `data`. Fügt automatisch das Expiry-Claim hinzu.
    `data` sollte z.B. {"sub": "user_id", "role": "user"} sein.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    """
    Decodiert und validiert ein JWT. Wirft JWTError, wenn ungültig/abgelaufen.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        raise