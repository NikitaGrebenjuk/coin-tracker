from app.database import Base, engine, SessionLocal
from app.models import User, Wallet

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

def test_insert():
    session = SessionLocal()
    try:
        # Create a user
        user = User(
            username="alice12",
            email="alice12@example.com",
            hashed_password="hashed_dummy_pw"
        )


        # Add two wallets for Alice
        wallet1 = Wallet(address="1A1zP1...", label="Main Wallet")
        wallet2 = Wallet(address="3FZbgi...", label="Savings Wallet")
        user.wallets = [wallet1, wallet2]

        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"Inserted user: {user.name}, ID: {user.id}")
        print(f"Inserted wallet1: {wallet1.label}, ID: {wallet1.id}")
        print(f"Inserted wallet2: {wallet2.label}, ID: {wallet2.id}")
        print(f"User's wallets: {user.wallets}")

    except Exception as e:
        print("Error:", e)
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    test_insert()
