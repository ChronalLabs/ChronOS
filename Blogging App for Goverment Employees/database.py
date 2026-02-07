from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a SQLite database file named blog.db
DATABASE_URL = "sqlite:///./blog.db"

# This connects Python to the database
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# This is used to talk to the database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# This will be used to create database tables later
Base = declarative_base()
