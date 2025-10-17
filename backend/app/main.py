from datetime import datetime
from fastapi import FastAPI
from .database import engine, Base
from .routers import user, wallet
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.wallet_service import WalletService
from app.crud import wallet as wallet_crud
from app.database import SessionLocal


# Datenbanktabellen anlegen (automatisch)
Base.metadata.create_all(bind=engine)

# FastAPI-Instanz erstellen
app = FastAPI(title="CoinTracker API")

# Scheduler für Hintergrund-Update-Aufgaben
scheduler = BackgroundScheduler()

# Router einbinden
app.include_router(user.router)
app.include_router(wallet.router)

# Einfache Root-Route
@app.get("/")
def read_root():
    return {"message": "Coin Tracker API läuft erfolgreich 🚀"}


# Hintergrund-Update-Job für Wallet-Salden
def update_all_wallets():
    print(f"✅ started updating wallets at {datetime.utcnow()}")
    db = SessionLocal()
    wallets = wallet_crud.get_wallets(db)
    for wallet in wallets:
        new_balance = WalletService.update_balance(wallet.address)
        if new_balance is not None:
            wallet_crud.update_wallet_balance(db, new_balance, wallet)
            print(f"✅ Wallet updated: {wallet.address}")
        else:
            print(f"⚠️ Failed to update wallet: {wallet.address}")
    db.close()

@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(update_all_wallets, "interval", minutes=300)
    scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()