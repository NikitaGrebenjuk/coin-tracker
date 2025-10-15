from fastapi import FastAPI
from .database import engine, Base
from .routers import user, wallet


# Datenbanktabellen anlegen (automatisch)
Base.metadata.create_all(bind=engine)

# FastAPI-Instanz erstellen
app = FastAPI(title="CoinTracker API")

# Router einbinden
app.include_router(user.router)
app.include_router(wallet.router)

# Einfache Root-Route
@app.get("/")
def read_root():
    return {"message": "Coin Tracker API läuft erfolgreich 🚀"}
