from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:8983@localhost:5432/product_info"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db = session()

    try:
        yield db

    finally:
        db.close()