from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class WalletRead(BaseModel):
    id: int
    address: str
    label: Optional[str] = None
    balance_btc: float
    last_checked: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None
    wallets: List[WalletRead] = []

    class Config:
        orm_mode = True
