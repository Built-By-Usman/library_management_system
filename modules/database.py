from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://library_management_system_o52u_user:2wPPHn1MKfrkProks9SOJwVTyfPN7HBG@dpg-d4o6qihr0fns73e47n8g-a.oregon-postgres.render.com/library_management_system_o52u"

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDb():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()