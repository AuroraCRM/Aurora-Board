import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker # Updated import
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # This will be set by tests to a dummy value if not present
    pass # Allow it to be None if not set, tests will override/mock

engine = create_engine(DATABASE_URL if DATABASE_URL else "sqlite:///:memory:_fallback_for_module_load")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() # Correct usage

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
