from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection string
DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/crimereports"

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

# Base class for ORM models
Base = declarative_base()