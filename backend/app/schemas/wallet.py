from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Optional

class WalletBase(BaseModel):
    address: str


class WalletCreate(WalletBase):
    user_id: int
    label: Optional[str] = None

class WalletRead(BaseModel):
    id: int
    address: str
    label: Optional[str] = None
    balance_btc: Decimal
    last_checked: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # <- wichtig in v2
    