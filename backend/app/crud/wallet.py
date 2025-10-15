from sqlalchemy.orm import Session
from app import models
from app.schemas.wallet import WalletCreate
from datetime import datetime
from app.utils import btc_client

def create_wallet(db: Session, wallet: WalletCreate) -> models.Wallet:
    db_wallet = models.Wallet(
        address=wallet.address,
        user_id=wallet.user_id,
        balance_btc=0.0,
        created_at=datetime.utcnow(),
        last_checked=None,
        )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def get_wallets(db: Session) -> list[models.Wallet]:
    return db.query(models.Wallet).all()

def get_wallet_by_address(db: Session, address: str) -> models.Wallet | None:
    return db.query(models.Wallet).filter(models.Wallet.address == address).first()

def get_wallets_by_user_id(db: Session, user_id: int) -> list[models.Wallet]:
    return db.query(models.Wallet).filter(models.Wallet.user_id == user_id).all()

def update_wallet_balance(db: Session, new_balance: float, address: str) -> models.Wallet:
    wallet=db.query(models.Wallet).filter(models.Wallet.address == address).first()
    wallet.balance_btc = new_balance
    wallet.last_checked = datetime.utcnow()
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet
