from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WalletBase(BaseModel):
    address: str
    user_id: int

class WalletCreate(WalletBase):
    user_id: int

class WalletRead(WalletBase):
    id: int
    label: Optional[str] = None
    balance_btc: float
    last_checked: Optional[datetime] = None
    user_id: int

    class Config:
        orm_mode = True