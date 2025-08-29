from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database
DATABASE_URL = "sqlite:///codetrack.db"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows SQL logs
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

