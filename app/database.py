import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL connection string.
# Format: postgresql+psycopg2://<user>:<password>@<host>:<port>/<database>
#
# Reads from the DATABASE_URL environment variable if set, so you can point
# this at a different host/user/password without editing code (handy for
# Docker, CI, or deploying later). Falls back to the local dev defaults
# used in the setup guide.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:Smile321@localhost:5432/Tracker",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
