from sqlalchemy import Column, Integer, String
from .database import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, )
    address = Column(String, unique=True, index=True)
    label = Column(String, nullable=True)