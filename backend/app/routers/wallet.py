from app.services.auth_service import get_current_user
from app.models import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import wallet as wallet_crud
from app.schemas import wallet as schemas
from app.services import wallet_service
from app.database import get_db

router = APIRouter(
    prefix="/wallets"
    , tags=["wallets"]
    , dependencies=[Depends(get_current_user)]
    )

# Create a new wallet for the current authenticated user
@router.post("/", response_model=schemas.WalletRead)
def create_wallet(
    wallet: schemas.WalletBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    if wallet_crud.get_wallet_by_address(db, address=wallet.address):
        raise HTTPException(status_code=400, detail="Wallet address already exists")
    return wallet_crud.create_wallet(db=db, wallet=wallet, current_user=current_user)

# List all wallets (ADMIN only - ToDo)
@router.get("/", response_model=list[schemas.WalletRead])
def list_wallets(db: Session = Depends(get_db)):
    return wallet_crud.get_wallets(db=db)

# ToDo: change to Authenticated ADMIN only
@router.get("/by_user_id/{user_id}/", response_model=list[schemas.WalletRead])
def get_wallets_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return wallet_crud.get_wallets_by_user_id(db, user_id=user_id) 


# ToDo: change to Authenticated CURRENTUSER only
@router.get("/by_address/{address}/update", response_model=schemas.WalletRead)
def update_wallet_balance(address: str, db: Session = Depends(get_db)):
    db_wallet = wallet_crud.get_wallet_by_address(db, address=address)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    new_balance = wallet_service.WalletService.update_balance(address)
    return wallet_crud.update_wallet_balance(db, new_balance, db_wallet)