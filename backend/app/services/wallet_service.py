from app.utils.btc_client import BlockCypherClient


class WalletService:
    """
    Kapselt die Logik zum Aktualisieren von Wallet-Daten mit externen API-Aufrufen.
    """

    @staticmethod
    def update_balance(wallet_address: str) -> float | None:

        client = BlockCypherClient()

        try:
            wallet_info = client.get_wallet_balance(wallet_address)
        except Exception as e:
            # Option: Logging oder spezifischere Fehlermeldungen
            print(f"BlockCypher API error: {e}")
            return None

        return wallet_info.balance_btc      
