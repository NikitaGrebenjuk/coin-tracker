from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    address = Column(String, unique=True, index=True)
    label = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    balance_btc = Column(Numeric(precision=18, scale=8), default=0)
    last_checked = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="wallets")
    
    def __repr__(self):
        return f"<Wallet(address={self.address}, balance_btc={self.balance_btc}, last_checked={self.last_checked}>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan", lazy="joined")
    
    def __repr__(self):
        return f"<User(username={self.username}, email={self.created_at}, wallets={len(self.wallets)})>"