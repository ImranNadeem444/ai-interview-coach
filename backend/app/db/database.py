from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# ============================================================
# 1. Create SQLAlchemy Engine
# ============================================================

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


# ============================================================
# 2. Create Database Session Factory
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# ============================================================
# 3. Base Class for Database Models
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# 4. FastAPI Database Dependency
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()