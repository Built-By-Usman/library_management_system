import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = os.getenv("DATABASE_URL")  # Read from environment variable
DATABASE_URL = "postgresql://library_management_system_e80l_user:zGH8TC4AsfrPJEX6kO66m9CT3Zr92SzI@dpg-d5l8vmqli9vc73cku880-a/library_management_system_e80l" 

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def getDb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
