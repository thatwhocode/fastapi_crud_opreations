import os 
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator
engine = None
SessionLocal = None
Base = declarative_base()
def get_database_url():
    """
    Reads credential from Docker secrets and creates connection
    """
    try:
        with open('/run/secrets/postgres', 'r') as f:
            postgres_password = f.read().strip()
        with open('/run/secrets/postgres_user', 'r') as f:
            postgres_user = f.read().strip()
        with open('/run/secrets/postgres_db_name', 'r') as f:
            postgres_db_name = f.read().strip()
        postgres_host = 'db'
        postgres_port = '5432'
        database_url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_name}"
        return database_url
    except FileNotFoundError as e: 
        print("CRITICAL! Key file was not founded", e)
        raise RuntimeError(...)from e
    except Exception as  e:
        print("Undefined error", e)
        raise RuntimeError(...) from e

async def init_db_resources():
    global engine, SessionLocal
    DATABASE_URL =  get_database_url()
    engine = create_async_engine(DATABASE_URL)
    SessionLocal = async_sessionmaker( bind=engine)
    Base =  await declarative_base()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all())


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try: 
        async with SessionLocal as session:
            yield session
    finally:
        pass