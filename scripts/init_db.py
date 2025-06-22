import os
from sqlalchemy import create_engine
from src.core.models import Base, User
from src.utils.security import get_password_hash

def init_db():
    # Create tables
    engine = create_engine(os.getenv("DATABASE_URL"))
    Base.metadata.create_all(bind=engine)
    
    # Create session
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Create initial admin user
        if not db.query(User).filter(User.email == "admin@example.com").first():
            admin = User(
                email="admin@example.com",
                hashed_password=get_password_hash("SecurePassword123!"),
                api_key="admin_key_12345",
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("Admin user created")
            
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()