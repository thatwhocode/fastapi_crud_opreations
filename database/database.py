import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
load_dotenv()
def get_database_url():
    """
    Reads credential from Docker secrets and creates connection
    """
    try:
        postgres_user  = os.environ.get("POSTGRES_USER")
        postgres_db = os.environ.get("POSTGRES_DB")
        postgres_password  = os.environ.get("POSTGRES_PASSWORD")
        postgres_host = os.environ.get("POSTGRES_HOST")
        postgres_port = os.environ.get("POSTGRES_PORT")
        database_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
        return database_url
    except FileNotFoundError as e: 
        print("CRITICAL! Key file was not founded", e)
        raise RuntimeError(...)from e
    except Exception as  e:
        print("Undefined error", e)
        raise RuntimeError(...) from e



DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()


