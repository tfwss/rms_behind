"""Database engine, session factory, and dependency helpers."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


# SQLAlchemy engine used by the application.
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
# Session factory for request-scoped database interactions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for ORM models.
Base = declarative_base()


def get_db():
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
