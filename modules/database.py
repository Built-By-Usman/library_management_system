from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://usman:ShaniMalik321@localhost:5432/fast_api_revision"

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDb():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()