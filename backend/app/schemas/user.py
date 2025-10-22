from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from app.schemas.wallet import WalletRead


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None
    wallets: List[WalletRead] = []

    model_config = {  # Pydantic v2
        "from_attributes": True  # vorher: orm_mode = True
    }
