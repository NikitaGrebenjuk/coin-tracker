from app.utils.btc_client import BlockCypherClient

if __name__ == "__main__":
    client = BlockCypherClient()
    wallet_info = client.get_wallet_balance("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")  # Satoshi's Adresse
    print(wallet_info)