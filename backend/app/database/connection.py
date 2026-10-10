import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import BASE_DIR, DATABASE_URL

if DATABASE_URL.startswith("sqlite"):
    # keep the sqlite file inside backend/data regardless of working directory
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
