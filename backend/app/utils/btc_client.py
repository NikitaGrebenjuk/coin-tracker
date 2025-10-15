import os
import httpx
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel
from dotenv import load_dotenv

# Environment Variablen laden (.env)
load_dotenv()


class WalletBalance(BaseModel):
    address: str
    balance_btc: Decimal
    total_received_btc: Decimal
    unconfirmed_balance_btc: Decimal


class BlockCypherClient:
    """
    Ein Client zum Abfragen von Bitcoin-Adressdaten über die BlockCypher API.
    """

    BASE_URL = "https://api.blockcypher.com/v1/btc/main"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("BLOCKCYPHER_API_KEY")

    def get_wallet_balance(self, address: str) -> WalletBalance:
        """
        Fragt den Kontostand einer BTC-Adresse ab.
        """
        url = f"{self.BASE_URL}/addrs/{address}/balance"
        params = {"token": self.api_key} if self.api_key else {}

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"BlockCypher API error: {response.status_code} {response.text}")

        data = response.json()

        # Werte in BTC (nicht Satoshis) umrechnen
        return WalletBalance(
            address=address,
            balance_btc=Decimal(data["balance"]) / Decimal(1e8),
            total_received_btc=Decimal(data["total_received"]) / Decimal(1e8),
            unconfirmed_balance_btc=Decimal(data["unconfirmed_balance"]) / Decimal(1e8),
        )
