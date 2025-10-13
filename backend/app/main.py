from fastapi import FastAPI
from .database import engine
from . import models

# Datenbanktabellen anlegen (automatisch)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coin Tracker API")

@app.get("/")
def read_root():
    return {"message": "Coin Tracker API läuft erfolgreich 🚀"}
