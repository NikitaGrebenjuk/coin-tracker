from pydantic import BaseModel, EmailStr, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)  # <- wichtig in v2