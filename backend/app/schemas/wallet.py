from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WalletBase(BaseModel):
    address: str
    user_id: int

class WalletCreate(WalletBase):
    label: str| None = None

class WalletRead(WalletBase):
    id: int
    user_id: int
    label: str | None = None
    balance_btc: float
    last_checked: datetime | None = None
    created_at : datetime | None = None

    model_config = {  # Pydantic v2
        "from_attributes": True  # vorher: orm_mode = True
    }