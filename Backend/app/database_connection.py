from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine (no check_same_thread needed)
engine = create_engine(
    DATABASE_URL,
    echo=True # log sql statements and their parameters
)

# Creates a new session per request
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base class for ORM models
Base = declarative_base()