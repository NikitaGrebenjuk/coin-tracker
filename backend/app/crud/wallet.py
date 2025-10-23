from sqlalchemy.orm import Session
from app import models
from app.schemas.wallet import WalletCreate,WalletRead
from datetime import datetime

def create_wallet(db: Session, wallet: WalletCreate, current_user: models.User) -> WalletRead:
    db_wallet = models.Wallet(
        address=wallet.address,
        user_id=current_user.id,
        balance_btc=0.0,
        created_at=datetime.utcnow(),
        last_checked=None,
        )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def get_wallets(db: Session) -> list[WalletRead]:
    return db.query(models.Wallet).all()

def get_wallet_by_address(db: Session, address: str) -> WalletRead | None:
    return db.query(models.Wallet).filter(models.Wallet.address == address).first()

def get_wallets_by_user_id(db: Session, user_id: int) -> list[WalletRead]:
    return db.query(models.Wallet).filter(models.Wallet.user_id == user_id).all()

def update_wallet_balance(db: Session, new_balance: float, db_wallet: models.Wallet) -> WalletRead:
    if new_balance is not None:
        db_wallet.balance_btc = new_balance
        db_wallet.last_checked = datetime.utcnow()
        db.add(db_wallet)
        db.commit()
        db.refresh(db_wallet)
    return db_wallet
