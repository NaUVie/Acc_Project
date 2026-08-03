from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

# Ensure UTF-8 (utf8mb4) character set for MySQL connection
db_url = DATABASE_URL
if "mysql" in db_url and "charset=" not in db_url:
    separator = "&" if "?" in db_url else "?"
    db_url = f"{db_url}{separator}charset=utf8mb4"

# Create database engine
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get db session in endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
