from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# 1. Create the SQLAlchemy connection engine
engine = create_engine(settings.DATABASE_URL)

# 2. Create a SessionLocal factory (each request will open a database session from this)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base class that our models will inherit from
Base = declarative_base()

# 4. FastAPI Dependency: Opens a session for a request and closes it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()