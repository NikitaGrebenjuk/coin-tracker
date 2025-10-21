from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WalletBase(BaseModel):
    address: str
    user_id: int

class WalletCreate(WalletBase):
    user_id: int

class WalletRead(BaseModel):
    id: int
    address: str
    label: Optional[str] = None
    balance_btc: Optional[float] = None
    last_checked: Optional[datetime] = None

    class Config:
        orm_mode = True