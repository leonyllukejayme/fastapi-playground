from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# SQL_ALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
# SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/blogs"
SQL_ALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine.
# This is the core interface to the database; it manages connections
# and translates SQLAlchemy commands into actual SQL queries.
# echo=True enables logging of all generated SQL statements (useful for debugging).
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, echo=True)


# Create a configured "Session" class.
# sessionmaker is a factory that will create new Session objects when called.
# autocommit=False means changes must be explicitly committed.
# autoflush=False prevents SQLAlchemy from automatically pushing changes to the DB
# before certain queries (you control when flushing happens).
# bind=engine attaches this session factory to the database engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a base class for all ORM models.
# All SQLAlchemy models should inherit from this Base class
# so SQLAlchemy can keep track of tables and mappings.
Base = declarative_base()


def get_db():
    # Create a new database session for a single request/operation.
    db = SessionLocal()
    try:
        # Yield the session to the caller (commonly used as a FastAPI dependency).
        # The session stays open while the request is being processed.
        yield db
    finally:
        # Always close the session after use to release the database connection
        # back to the connection pool and avoid leaks.
        db.close()

