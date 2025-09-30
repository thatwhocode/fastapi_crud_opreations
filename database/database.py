import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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
        database_url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
        return database_url
    except FileNotFoundError as e: 
        print("CRITICAL! Key file was not founded", e)
        raise RuntimeError(...)from e
    except Exception as  e:
        print("Undefined error", e)
        raise RuntimeError(...) from e



DATABASE_URL = get_database_url()

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker( bind=engine)
Base = declarative_base()

async def get_db():
    try: 
        async with SessionLocal() as session:
            yield session
    finally:
        pass

async def init_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
